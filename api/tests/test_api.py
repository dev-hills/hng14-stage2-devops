from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_job():
    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()

def test_not_found():
    response = client.get("/jobs/fake-id")
    assert response.status_code == 200

def test_job_status():
    job = client.post("/jobs").json()
    response = client.get(f"/jobs/{job['job_id']}")
    assert response.status_code == 200