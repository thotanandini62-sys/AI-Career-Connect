from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(UserMixin, db.Model):
    """User database model storing authentication details and career profiles."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100))
    target_role = db.Column(db.String(100), default='Software Engineer')
    skills = db.Column(db.Text, default='Python, SQL, HTML/CSS')
    experience_level = db.Column(db.String(50), default='Mid-Level')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    resumes = db.relationship('ResumeAnalysis', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    interviews = db.relationship('MockInterview', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    goals = db.relationship('CareerGoal', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    voice_sessions = db.relationship('VoiceSession', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify user password against hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Serialize user instance to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'target_role': self.target_role,
            'skills': [s.strip() for s in self.skills.split(',')] if self.skills else [],
            'experience_level': self.experience_level,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<User {self.username} ({self.target_role})>'
