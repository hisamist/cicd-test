import pytest
from app import app


@pytest.fixture
def client():
    # preparation test client
    with app.test_client() as client:
        yield client


def test_hello_and_send_200(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello World"}


def test_health_and_send_200(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
