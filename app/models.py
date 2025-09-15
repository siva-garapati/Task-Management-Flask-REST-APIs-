import uuid
from datetime import datetime
from .extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    tasks = db.relationship("Task", backref="owner", lazy=True)

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="Pending")  # Pending / Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=True)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)