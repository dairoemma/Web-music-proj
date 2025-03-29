import json
import pytest
from app import app  

# seting up a test client that we can use to simulate requests to our app
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# ------------------- USER -------------------

# Test for adding a new user
def test_add_user(client):
    payload = {
        "username": "testuser",  # dummy username
        "password": "testpass",  # dummy password
        "email": "testuser@example.com",  # dummy email
        "name": "test name",  #dummy name
        "task_id": "test-task-id"  # assuming payment was done
    }
    res = client.post("/user/add_user", json=payload)
    assert res.status_code in (200, 201)  # should return either success or created
    assert "success" in res.get_json()["status"].lower()  # checking response status

# Test for authenticating a user we just added
def test_authenticate_user(client):
    payload = {
        "username": "testuser",
        "password": "testpass"
    }
    res = client.post("/user/authenticate_user", json=payload)
    assert res.status_code == 200  # should be allowed
    assert res.get_json()["status"] == "success"  # must be success if credentials are right

# ------------------- MUSICIAN -------------------

# Test for adding a musician account
def test_add_musician(client):
    payload = {
        "username": "testmusician",
        "password": "testpass",
        "email": "testmusician@example.com",
        "music_genre": "jazz",
        "task_id": "test-task-id"
    }
    res = client.post("/musician/add_musician", json=payload)
    assert res.status_code in (200, 201)  # 200 for OK, 201 for created
    assert "success" in res.get_json()["status"].lower()

# Test for logging in with the musician account
def test_authenticate_musician(client):
    payload = {
        "music_name": "testmusician",  # different from user, we use 'music_name'
        "password": "testpass"
    }
    res = client.post("/musician/authenticate_musician", json=payload)
    assert res.status_code == 200
    assert res.get_json()["status"] == "success"

# ------------------- ADMIN -------------------

# Test for adding an admin
def test_add_admin(client):
    payload = {
        "username": "testadmin",
        "password": "testpass",
        "email": "admin@example.com"
    }
    res = client.post("/admin/add_admin", json=payload)
    assert res.status_code in (200, 201)
    assert "success" in res.get_json()["status"].lower()

# Test for authenticating admin
def test_authenticate_admin(client):
    payload = {
        "username": "testadmin",
        "password": "testpass"
    }
    res = client.post("/admin/authenticate_admin", json=payload)
    assert res.status_code == 200
    assert res.get_json()["status"] == "success"
