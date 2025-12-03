from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_via_url_returns_job_and_finishes():
    response = client.post(
        "/api/v1/upload",
        data={"title": "Test Lecture", "video_url": "https://example.com/video.mp4"},
    )
    assert response.status_code == 202
    payload = response.json()
    assert payload["status"] == "queued"

    status_resp = client.get(f"/api/v1/jobs/{payload['job_id']}")
    assert status_resp.status_code == 200
    status_data = status_resp.json()
    assert status_data["status"] in {"running", "finished"}
    assert "progress" in status_data["meta"]
