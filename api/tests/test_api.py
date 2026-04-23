from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app

client = TestClient(app)


@patch("main.r")
def test_create_job(mock_redis):
    mock_redis.lpush = MagicMock()
    mock_redis.hset = MagicMock()

    response = client.post("/jobs")

    assert response.status_code == 200
    assert "job_id" in response.json()


@patch("main.r")
def test_not_found(mock_redis):
    mock_redis.hget.return_value = None

    response = client.get("/jobs/fake-id")

    assert response.status_code == 200
    assert "error" in response.json()


@patch("main.r")
def test_job_status(mock_redis):
    mock_redis.lpush = MagicMock()
    mock_redis.hset = MagicMock()
    mock_redis.hget.return_value = "queued"

    job = client.post("/jobs").json()
    response = client.get(f"/jobs/{job['job_id']}")

    assert response.status_code == 200
    assert response.json()["status"] == "queued"
