"""Testing the server's functionality"""

from datetime import datetime

from fastapi.testclient import TestClient
import pytest

from server.handlers import app
from server.database import JOB_INFO_BY_ID, Job

client = TestClient(app)

FAKE_COMPLETED_JOB_ID = "JOB_001"
FAKE_COMPLETED_JOB_INFO = Job(
    delay=1, random_num=1.0, started_at=datetime(2000, 1, 1), status="pending"
)

FAKE_ERRONEOUS_JOB_ID = "JOB_002"
FAKE_ERRONEOUS_JOB_INFO = Job(
    delay=1, random_num=0.0, started_at=datetime.now(), status="pending"
)

FAKE_PENDING_JOB_ID = "JOB_003"
FAKE_PENDING_JOB_INFO = Job(
    delay=10, random_num=1.0, started_at=datetime.now(), status="pending"
)


@pytest.fixture
def fake_create_completed_job() -> None:
    """Fixture for writing a job-record in the database"""
    JOB_INFO_BY_ID[FAKE_COMPLETED_JOB_ID] = FAKE_COMPLETED_JOB_INFO


@pytest.fixture
def fake_create_erroneous_job() -> None:
    """Fixture for writing a job-record in the database"""
    JOB_INFO_BY_ID[FAKE_ERRONEOUS_JOB_ID] = FAKE_ERRONEOUS_JOB_INFO


@pytest.fixture
def fake_create_pending_job() -> None:
    """Fixture for writing a job-record in the database"""
    JOB_INFO_BY_ID[FAKE_PENDING_JOB_ID] = FAKE_PENDING_JOB_INFO


def test_get_status_non_existent_job_id() -> None:
    """Fetching the status of a job that hasn't been submitted"""
    response = client.get("/status/non_existent_job_id")
    assert response.status_code == 404

    message = response.json()["detail"]
    assert message == "Job ID non_existent_job_id could not be found"


def test_get_status_completed_job(fake_create_completed_job) -> None:
    """Fetching the status of a completed job"""
    response = client.get(f"/status/{FAKE_COMPLETED_JOB_ID}")
    assert response.status_code == 200

    status = response.json()
    assert status["result"] == "completed"


def test_get_status_erroneous_job(fake_create_erroneous_job) -> None:
    """Fetching the status of an erroneous job"""
    response = client.get(f"/status/{FAKE_ERRONEOUS_JOB_ID}")
    assert response.status_code == 200

    status = response.json()
    assert status["result"] == "error"


def test_get_status_pending_job(fake_create_pending_job) -> None:
    """Fetching the status of an erroneous job"""
    response = client.get(f"/status/{FAKE_PENDING_JOB_ID}")
    assert response.status_code == 200

    status = response.json()
    assert status["result"] == "pending"


def test_submit_job() -> None:
    """Tests the /submit API"""
    response = client.post("/submit/JOB_000")
    assert response.status_code == 201
