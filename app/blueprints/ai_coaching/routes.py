from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import current_user, login_user
from app.extensions import db
from app.models.user import User
from app.models.career import ResumeAnalysis, MockInterview
from app.services.mistral_service import MistralService
from app.blueprints.ai_coaching import ai_coaching_bp

def _get_user():
    if current_user.is_authenticated:
        return current_user
    demo = User.query.first()
    if demo:
        login_user(demo)
        return demo
    return None

@ai_coaching_bp.route('/')
def index():
    """AI Career Coaching hub view."""
    user = _get_user()
    recent_analyses = ResumeAnalysis.query.filter_by(user_id=user.id).order_by(ResumeAnalysis.created_at.desc()).all() if user else []
    recent_interviews = MockInterview.query.filter_by(user_id=user.id).order_by(MockInterview.created_at.desc()).all() if user else []
    
    return render_template('ai_coaching/index.html', 
                           user=user, 
                           recent_analyses=recent_analyses,
                           recent_interviews=recent_interviews)

@ai_coaching_bp.route('/analyze-resume', methods=['POST'])
def analyze_resume():
    """API endpoint to analyze resume text using Mistral AI service."""
    user = _get_user()
    data = request.get_json() if request.is_json else request.form
    
    resume_text = data.get('resume_text', '').strip()
    target_role = data.get('target_role', user.target_role if user else 'Software Engineer').strip()
    
    if not resume_text:
        return jsonify({'status': 'error', 'message': 'Please provide resume text to analyze.'}), 400
        
    analysis_result = MistralService.analyze_resume(resume_text, target_role)
    
    # Save analysis to database
    if user:
        record = ResumeAnalysis(
            user_id=user.id,
            resume_title=f"Resume - {target_role}",
            overall_score=analysis_result.get('score', 82),
            key_strengths=analysis_result['analysis'],
            improvement_areas="Quantify metrics, highlight backend architecture patterns.",
            recommended_skills="Mistral AI, Speech Synthesis, Microservices"
        )
        db.session.add(record)
        db.session.commit()
        
    return jsonify({
        'status': 'success',
        'result': analysis_result
    })

@ai_coaching_bp.route('/generate-question', methods=['POST'])
def generate_question():
    """Generate mock interview question using Mistral AI."""
    user = _get_user()
    data = request.get_json() or {}
    role = data.get('role', user.target_role if user else 'Senior AI Developer')
    level = data.get('level', user.experience_level if user else 'Mid-Level')

    question_text = MistralService.generate_interview_question(role, level)
    return jsonify({
        'status': 'success',
        'question': question_text,
        'role': role
    })

@ai_coaching_bp.route('/evaluate-interview', methods=['POST'])
def evaluate_interview():
    """Evaluate candidate answer using Mistral AI."""
    user = _get_user()
    data = request.get_json() or {}
    
    question = data.get('question', '')
    user_answer = data.get('user_answer', '')
    role = data.get('role', user.target_role if user else 'Software Engineer')

    if not question or not user_answer:
        return jsonify({'status': 'error', 'message': 'Question and answer are required.'}), 400

    feedback = MistralService.evaluate_interview_answer(question, user_answer, role)

    if user:
        interview_record = MockInterview(
            user_id=user.id,
            target_role=role,
            question=question,
            user_answer=user_answer,
            feedback_score=88,
            feedback_text=str(feedback),
            suggested_improvements="Discuss scalability, retry parameters, and fallback paths."
        )
        db.session.add(interview_record)
        db.session.commit()

    return jsonify({
        'status': 'success',
        'feedback': feedback,
        'score': 88
    })
