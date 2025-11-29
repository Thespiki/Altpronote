import secrets
from datetime import datetime
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class Role(Enum):
    ELEVE = 'élève'
    PROFESSEUR = 'professeur'
    ADMINISTRATION = 'personnel d\'administration'


def generate_hex_id():
    return secrets.token_hex(16)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(32), primary_key=True, default=generate_hex_id)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(50), nullable=False, default=Role.ELEVE.value)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'age': self.age,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
