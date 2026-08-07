import pytest
from app import create_app
from app.services.tts_service import TTSService

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        yield app

def test_tts_synthesis(app):
    res = TTSService.synthesize_speech("Welcome to AI Career Connect testing environment.")
    assert 'status' in res
    assert res['status'] in ['success', 'fallback']
