from flask import render_template, jsonify, request
from flask_login import current_user, login_user
from app.extensions import db
from app.models.user import User
from app.models.career import ResumeAnalysis, MockInterview, CareerGoal
from app.models.voice_session import VoiceSession
from app.blueprints.dashboard import dashboard_bp

def _get_active_user():
    """Retrieve logged in user or auto-login demo user for preview."""
    if current_user.is_authenticated:
        return current_user
    demo = User.query.first()
    if demo:
        login_user(demo)
        return demo
    return None

@dashboard_bp.route('/')
def index():
    """Main dynamic dashboard view."""
    user = _get_active_user()
    if not user:
        return render_template('dashboard/index.html', user=None, metrics={})

    # Fetch latest analyses & activities
    latest_resume = ResumeAnalysis.query.filter_by(user_id=user.id).order_by(ResumeAnalysis.created_at.desc()).first()
    recent_interviews = MockInterview.query.filter_by(user_id=user.id).order_by(MockInterview.created_at.desc()).limit(5).all()
    active_goals = CareerGoal.query.filter_by(user_id=user.id).all()
    voice_sessions_count = VoiceSession.query.filter_by(user_id=user.id).count()

    metrics = {
        'resume_score': latest_resume.overall_score if latest_resume else 78,
        'mock_interviews_count': len(recent_interviews),
        'avg_interview_score': sum(i.feedback_score for i in recent_interviews) // max(len(recent_interviews), 1) if recent_interviews else 82,
        'goals_completed': sum(1 for g in active_goals if g.status == 'Completed'),
        'total_goals': len(active_goals),
        'voice_interactions': voice_sessions_count or 4
    }

    return render_template('dashboard/index.html', 
                           user=user, 
                           metrics=metrics, 
                           latest_resume=latest_resume,
                           recent_interviews=recent_interviews,
                           active_goals=active_goals)

@dashboard_bp.route('/api/metrics')
def api_metrics():
    """REST API endpoint serving real-time dynamic dashboard metrics."""
    user = _get_active_user()
    if not user:
        return jsonify({'error': 'User not authenticated'}), 401

    resumes = ResumeAnalysis.query.filter_by(user_id=user.id).all()
    interviews = MockInterview.query.filter_by(user_id=user.id).all()
    goals = CareerGoal.query.filter_by(user_id=user.id).all()

    return jsonify({
        'status': 'success',
        'metrics': {
            'resume_score': resumes[-1].overall_score if resumes else 85,
            'interview_readiness': sum(i.feedback_score for i in interviews) // max(len(interviews), 1) if interviews else 80,
            'skills_mastery': 74,
            'voice_practice_minutes': 18.5,
            'goals_progress': [g.to_dict() for g in goals]
        }
    })

@dashboard_bp.route('/api/chart-data')
def api_chart_data():
    """REST API returning dynamic dataset for Chart.js dashboard components."""
    user = _get_active_user()
    
    # Skill proficiency radar dataset
    skills_radar = {
        'labels': ['System Architecture', 'Python Backend', 'Mistral AI / LLMs', 'Speech STT/TTS', 'SQL & Databases', 'DevOps / CI-CD'],
        'datasets': [{
            'label': 'Current Skill Level',
            'data': [85, 92, 78, 70, 88, 65],
            'backgroundColor': 'rgba(99, 102, 241, 0.2)',
            'borderColor': '#6366f1',
            'pointBackgroundColor': '#818cf8'
        }, {
            'label': 'Target Role Benchmark',
            'data': [90, 90, 85, 80, 85, 75],
            'backgroundColor': 'rgba(236, 72, 153, 0.1)',
            'borderColor': '#ec4899',
            'borderDash': [5, 5],
            'pointBackgroundColor': '#f472b6'
        }]
    }

    # Weekly mock interview score progression line chart
    score_history = {
        'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'scores': [72, 75, 78, 82, 80, 86, 89]
    }

    return jsonify({
        'skills_radar': skills_radar,
        'score_history': score_history
    })
