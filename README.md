# Altpronote — base project

Minimal Flask + SQLite starter for Altpronote.

Quick start

1. Create a virtualenv and install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2. Create the database:

```powershell
python create_db.py
```

3. (Optional) Assign IDs to users without them:

```powershell
python migrate_ids.py
```

4. Run the dev server:

```powershell
python run.py
```

API endpoints

- `POST /register` — register a new user (JSON)
- `POST /login` — login with username & password (JSON)

Notes

- Database is `sqlite:///altpronote.db` by default.
- Passwords are stored hashed (Werkzeug).
- The `User` model includes `id`, `username`, `password_hash`, `age`, `email`, `phone`, `address`, `role`.
