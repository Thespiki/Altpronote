@echo off
echo Installing dependencies...
python -m pip install Flask==2.3.4 Flask-SQLAlchemy==3.0.3 PyJWT==2.8.0

echo.
echo Creating database...
python create_db.py

echo.
echo Seeding database with principal user...
python seed_db.py

echo.
echo Setup complete! Run: python run.py
pause
