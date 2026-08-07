import pytest
from app import create_app
from app.services.mistral_service import MistralService

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        yield app

def test_mistral_resume_analysis(app):
    result = MistralService.analyze_resume("Python Flask developer with SQLite experience", "Senior AI Developer")
    assert 'score' in result
    assert 'analysis' in result
    assert result['score'] >= 80

def test_mistral_interview_question(app):
    question = MistralService.generate_interview_question("Senior AI Engineer")
    assert isinstance(question, str)
    assert len(question) > 10
