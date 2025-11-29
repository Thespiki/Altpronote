from app import create_app, db


def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        print('Database and tables created (altpronote.db)')


if __name__ == '__main__':
    main()
