# QUICK START - Follow these steps exactly:

## Step 1: Install Dependencies
Open PowerShell in this directory and run:
```
pip install Flask==2.3.4 Flask-SQLAlchemy==3.0.3 PyJWT==2.8.0
```

## Step 2: Create Database
```
python create_db.py
```
You should see: "Database and tables created (altpronote.db)"

## Step 3: Seed Database (Create Principal User)
```
python seed_db.py
```
You should see:
- "✔ Principal user created."
- Username: principal
- Password: Principal123!

## Step 4: Run the Server
```
python run.py
```
You should see: "Running on http://127.0.0.1:5000"

## Step 5: Open in Browser
Go to http://127.0.0.1:5000

## Login with:
Username: principal
Password: Principal123!

---

If you see errors about missing modules, make sure you ran Step 1.
If you see "database locked" error, make sure the server from a previous run is stopped.

Questions? Check README.md for full documentation.
