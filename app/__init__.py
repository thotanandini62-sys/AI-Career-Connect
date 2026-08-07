import os
from flask import Flask
from app.config import config
from app.extensions import db, migrate, login_manager

def create_app(config_name='default'):
    """Application Factory function for initializing Flask app instances."""
    app = Flask(__name__)
    
    # Load configuration settings
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize Flask extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Configure user loader function for Flask-Login
    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    # Register application blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.dashboard import dashboard_bp
    from app.blueprints.ai_coaching import ai_coaching_bp
    from app.blueprints.voice import voice_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(ai_coaching_bp, url_prefix='/ai-coaching')
    app.register_blueprint(voice_bp, url_prefix='/api/voice')
    
    # Root route redirecting to dashboard
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('dashboard.index'))
    
    # Context processor for shell / template variables
    @app.context_processor
    def inject_global_vars():
        return {
            'app_name': 'AI Career Connect',
            'mistral_enabled': bool(app.config.get('MISTRAL_API_KEY'))
        }
        
    # Auto-create SQLite database tables if development
    with app.app_context():
        db.create_all()
        _seed_demo_data()
        
    return app

def _seed_demo_data():
    """Seed initial demo user & metrics if database is fresh."""
    from app.models.user import User
    from app.models.career import ResumeAnalysis, MockInterview, CareerGoal
    from app.models.voice_session import VoiceSession
    
    if User.query.first() is None:
        demo_user = User(
            username='johndoe',
            email='john@example.com',
            full_name='John Doe',
            target_role='Senior AI Engineer',
            skills='Python, Flask, PyTorch, SQL, Mistral AI, Speech Synthesis',
            experience_level='Mid-Level (3+ years)'
        )
        demo_user.set_password('password123')
        db.session.add(demo_user)
        db.session.commit()
        
        # Add sample resume analysis
        sample_analysis = ResumeAnalysis(
            user_id=demo_user.id,
            resume_title='AI Developer Resume 2026',
            overall_score=84,
            key_strengths='Strong Python backend experience, Flask architecture, clean module design.',
            improvement_areas='Highlight quantified achievements (e.g. reduced latency by 35%), add PyTest coverage details.',
            recommended_skills='LangChain, Vector DBs (Chroma/FAISS), FastAPI integration'
        )
        db.session.add(sample_analysis)
        
        # Add sample mock interview
        sample_interview = MockInterview(
            user_id=demo_user.id,
            target_role='Senior AI Engineer',
            question='Can you explain how you design a scalable Flask backend service with third-party LLM integrations?',
            user_answer='I use the Application Factory pattern, separate service modules for LLMs, and handle async calls with background tasks.',
            feedback_score=88,
            feedback_text='Great structure! Mentioning Application Factory shows Flask expertise. Consider adding error handling for LLM timeouts.',
            suggested_improvements='Discuss retry logic and rate limit handling explicitly.'
        )
        db.session.add(sample_interview)
        
        # Add sample career goal
        sample_goal = CareerGoal(
            user_id=demo_user.id,
            title='Master Mistral AI & Speech Services',
            target_date='2026-10-01',
            status='In Progress',
            progress_pct=65
        )
        db.session.add(sample_goal)
        
        # Add sample voice session
        sample_voice = VoiceSession(
            user_id=demo_user.id,
            session_type='STT',
            input_text='Tell me about your experience with AI career coaching platforms.',
            transcription='Tell me about your experience with AI career coaching platforms.',
            audio_url='/static/uploads/sample_demo.mp3'
        )
        db.session.add(sample_voice)
        
        db.session.commit()
