# Altpronote — base project

Minimal Flask + SQLite starter for Altpronote with permission system and JWT authentication.

Quick start

1. Create a virtualenv and install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2. Create the database:

```powershell
python create_db.py
```

3. Seed the database with principal user and default permissions:

```powershell
python seed_db.py
```

4. (Optional) Assign IDs to users without them:

```powershell
python migrate_ids.py
```

5. Run the dev server:

```powershell
python run.py
```

6. Open http://127.0.0.1:5000 in your browser.

Principal credentials

- **Username:** `principal`
- **Password:** `Principal123!`

Features

- **User Registration & Login** — JWT-based authentication with encrypted hex IDs (32 chars)
- **Role System** — principal, professeur, élève, personnel d'administration
- **Permission Management** — Principal can grant/revoke permissions to other users
- **Protected Routes** — Token-based access control
- **Multi-page UI** — Dashboard, Profile, Permissions pages with theme switcher

API endpoints

- `POST /register` — register a new user (JSON)
- `POST /login` — login with username & password, returns JWT token
- `GET /me` — get current authenticated user info (requires token)
- `GET /permissions/` — list all permissions
- `POST /permissions/user/<user_id>/grant` — grant permission to user (principal only)
- `POST /permissions/user/<user_id>/revoke` — revoke permission from user (principal only)

Frontend

- `/` — login/register page
- `/dashboard` — user dashboard (requires authentication)
- `/profile` — user profile page (requires authentication)
- `/permissions` — permissions management (principal) or view permissions (others)

Notes

- Database is `sqlite:///altpronote.db` by default.
- Passwords are hashed using Werkzeug.
- User IDs are 32-character hexadecimal, cryptographically random.
- JWT tokens expire in 1 hour by default.
- Principal's permissions cannot be modified by anyone.
- Tokens are stored in browser localStorage as `alt-token`.

