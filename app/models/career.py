from datetime import datetime, timezone
from app.extensions import db

class ResumeAnalysis(db.Model):
    """Model storing AI-evaluated resume feedback and scores."""
    __tablename__ = 'resume_analyses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resume_title = db.Column(db.String(150), default='Uploaded Resume')
    overall_score = db.Column(db.Integer, default=75)  # Out of 100
    key_strengths = db.Column(db.Text)
    improvement_areas = db.Column(db.Text)
    recommended_skills = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'resume_title': self.resume_title,
            'overall_score': self.overall_score,
            'key_strengths': self.key_strengths,
            'improvement_areas': self.improvement_areas,
            'recommended_skills': self.recommended_skills,
            'created_at': self.created_at.strftime('%b %d, %Y')
        }

class MockInterview(db.Model):
    """Model tracking AI mock interview sessions and responses."""
    __tablename__ = 'mock_interviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_role = db.Column(db.String(100))
    question = db.Column(db.Text, nullable=False)
    user_answer = db.Column(db.Text)
    feedback_score = db.Column(db.Integer, default=80)
    feedback_text = db.Column(db.Text)
    suggested_improvements = db.Column(db.Text)
    audio_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'target_role': self.target_role,
            'question': self.question,
            'user_answer': self.user_answer,
            'feedback_score': self.feedback_score,
            'feedback_text': self.feedback_text,
            'suggested_improvements': self.suggested_improvements,
            'audio_path': self.audio_path,
            'created_at': self.created_at.strftime('%b %d, %Y %H:%M')
        }

class CareerGoal(db.Model):
    """Model tracking user skill progression and career milestones."""
    __tablename__ = 'career_goals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    target_date = db.Column(db.String(50))
    status = db.Column(db.String(50), default='In Progress')  # In Progress, Completed, Paused
    progress_pct = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'target_date': self.target_date,
            'status': self.status,
            'progress_pct': self.progress_pct,
            'created_at': self.created_at.strftime('%b %d, %Y')
        }
