from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/')
def index():
    return render_template('index.html')


@frontend_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@frontend_bp.route('/profile')
def profile():
    return render_template('profile.html')


@frontend_bp.route('/permissions')
def permissions():
    return render_template('permissions.html')
