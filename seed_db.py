from app import create_app, db
from app.models import User, Permission, Role


def seed_database():
    """Seed the database with initial data."""
    app = create_app()
    with app.app_context():
        # Check if principal already exists
        principal = User.query.filter_by(username='principal').first()
        if principal:
            print('✔ Principal user already exists.')
        else:
            principal = User(
                username='principal',
                email='principal@altpronote.local',
                role=Role.PRINCIPAL.value,
            )
            principal.set_password('Principal123!')
            db.session.add(principal)
            db.session.commit()
            print(f'✔ Principal user created.')
            print(f'  → Username: principal')
            print(f'  → Password: Principal123!')
            print(f'  → ID: {principal.id}')

        # Create default permissions
        default_perms = [
            ('manage_users', 'Can create, edit, and delete users'),
            ('view_permissions', 'Can view user permissions'),
            ('manage_permissions', 'Can grant and revoke permissions'),
            ('manage_grades', 'Can manage student grades'),
            ('view_grades', 'Can view student grades'),
        ]

        for name, desc in default_perms:
            perm = Permission.query.filter_by(name=name).first()
            if not perm:
                perm = Permission(name=name, description=desc)
                db.session.add(perm)
                print(f'✔ Created permission: {name}')
            else:
                print(f'✔ Permission already exists: {name}')

        db.session.commit()
        print('✔ Seed complete.')


if __name__ == '__main__':
    seed_database()
