from datetime import datetime, timezone
from app.extensions import db

class VoiceSession(db.Model):
    """Model tracking Speech-to-Text and Text-to-Speech interactions."""
    __tablename__ = 'voice_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_type = db.Column(db.String(20), nullable=False)  # 'STT' or 'TTS'
    input_text = db.Column(db.Text)
    transcription = db.Column(db.Text)
    audio_url = db.Column(db.String(255))
    duration_seconds = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'session_type': self.session_type,
            'input_text': self.input_text,
            'transcription': self.transcription,
            'audio_url': self.audio_url,
            'duration_seconds': self.duration_seconds,
            'created_at': self.created_at.strftime('%b %d, %Y %H:%M')
        }
