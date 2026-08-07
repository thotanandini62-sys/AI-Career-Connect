import os
from app import create_app, db

# Instantiate the Flask application via factory
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    """Register database models in flask shell for easy debugging."""
    from app.models.user import User
    from app.models.career import ResumeAnalysis, MockInterview, CareerGoal
    from app.models.voice_session import VoiceSession
    return {
        'db': db,
        'User': User,
        'ResumeAnalysis': ResumeAnalysis,
        'MockInterview': MockInterview,
        'CareerGoal': CareerGoal,
        'VoiceSession': VoiceSession
    }

if __name__ == '__main__':
    # Ensure static upload directory exists
    upload_dir = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    
    app.run(host='127.0.0.1', port=5000, debug=True)
