import pytest
from app import app
from config import db
from models import User, Task

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def test_signup(client):
    response = client.post('/signup', json={'username': 'alice', 'password': 'pass123'})
    assert response.status_code == 201
    assert 'access_token' in response.json


def test_signup_duplicate_username(client):
    client.post('/signup', json={'username': 'alice', 'password': 'pass123'})
    response = client.post('/signup', json={'username': 'alice', 'password': 'pass456'})
    assert response.status_code == 422


def test_login_success(client):
    client.post('/signup', json={'username': 'bob', 'password': 'pass123'})
    response = client.post('/login', json={'username': 'bob', 'password': 'pass123'})
    assert response.status_code == 200
    assert 'access_token' in response.json


def test_login_wrong_password(client):
    client.post('/signup', json={'username': 'bob', 'password': 'pass123'})
    response = client.post('/login', json={'username': 'bob', 'password': 'wrongpass'})
    assert response.status_code == 401


def test_me_requires_auth(client):
    response = client.get('/me')
    assert response.status_code == 401


def test_task_requires_auth(client):
    response = client.get('/tasks')
    assert response.status_code == 401


def test_create_and_get_task(client):
    signup = client.post('/signup', json={'username': 'carol', 'password': 'pass123'})
    token = signup.json['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    create_response = client.post('/tasks', json={'title': 'Test task'}, headers=headers)
    assert create_response.status_code == 201

    get_response = client.get('/tasks', headers=headers)
    assert get_response.status_code == 200
    assert get_response.json['total'] == 1


def test_user_cannot_access_others_task(client):
    signup1 = client.post('/signup', json={'username': 'dave', 'password': 'pass123'})
    token1 = signup1.json['access_token']
    headers1 = {'Authorization': f'Bearer {token1}'}
    create_response = client.post('/tasks', json={'title': 'Daves task'}, headers=headers1)
    task_id = create_response.json['id']

    signup2 = client.post('/signup', json={'username': 'erin', 'password': 'pass123'})
    token2 = signup2.json['access_token']
    headers2 = {'Authorization': f'Bearer {token2}'}
    response = client.get(f'/tasks/{task_id}', headers=headers2)
    assert response.status_code == 404
