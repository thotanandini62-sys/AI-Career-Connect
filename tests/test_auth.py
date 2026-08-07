import pytest
from app import create_app, db
from app.models.user import User

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_user_creation(app):
    with app.app_context():
        user = User(username='testuser', email='test@example.com', target_role='AI Engineer')
        user.set_password('secret123')
        db.session.add(user)
        db.session.commit()

        fetched = User.query.filter_by(username='testuser').first()
        assert fetched is not None
        assert fetched.check_password('secret123') is True
        assert fetched.check_password('wrong') is False

def test_dashboard_access(client):
    response = client.get('/dashboard/')
    assert response.status_code == 200
    assert b'Dynamic Career Analytics' in response.data
