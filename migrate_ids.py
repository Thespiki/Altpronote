from app import create_app, db
from app.models import User, generate_hex_id


def assign_missing_ids():
    """Assign hexadecimal IDs to users who don't have one, keeping existing IDs unchanged."""
    app = create_app()
    with app.app_context():
        # Find users without IDs (id is NULL or empty)
        users_without_id = User.query.filter((User.id.is_(None)) | (User.id == '')).all()

        if not users_without_id:
            print('✔ All users already have IDs.')
            return

        print(f'Found {len(users_without_id)} user(s) without ID.')
        for user in users_without_id:
            user.id = generate_hex_id()
            print(f'  → Assigned ID {user.id} to user "{user.username}"')

        db.session.commit()
        print(f'✔ Migration complete. {len(users_without_id)} user(s) updated.')


if __name__ == '__main__':
    assign_missing_ids()
