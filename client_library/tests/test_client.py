"""Testing the client library"""

import pytest
from client_library.translate_video.translate_video import TranslateVideo


@pytest.fixture
def mock_status_api_response(mocker):
    """Patches the response from the GET /status API calls"""

    def _mock_status_api_response(status_code, job_status):
        mock_response = mocker.Mock()
        mock_response.status_code = status_code
        if job_status:
            mock_response.json.return_value = {"result": job_status}
        return mocker.patch("requests.get", return_value=mock_response)

    return _mock_status_api_response


@pytest.fixture
def mock_submit_api_response(mocker):
    """Patches the response from the POST /submit API calls"""

    def _mock_submit_api_response(status_code):
        mock_response = mocker.Mock()
        mock_response.status_code = status_code
        return mocker.patch("requests.post", return_value=mock_response)

    return _mock_submit_api_response


def test_get_status_completed_job(
    mock_status_api_response, mock_submit_api_response
) -> None:
    """Fetching the status of a job that has been completed
    by the first call to the GET /status API
    """
    job = TranslateVideo("JOB_000")
    mock_submit_api_response(201)
    mock_status_api_response(200, "completed")
    status = job.get_status()
    assert status["result"] == "completed"


def test_get_status_pending_job(
    mock_status_api_response, mock_submit_api_response
) -> None:
    """Fetching the status of a job that will remain "pending"
    until the timeout_seconds have elapsed
    """
    mock_submit_api_response(201)
    job = TranslateVideo("JOB_000", polling_interval_seconds=1, timeout_seconds=3)
    mock_status_api_response(200, "pending")
    status = job.get_status()
    assert status["result"] == "pending"


def test_object_instantiation(mock_submit_api_response) -> None:
    """Tests the object instantiation"""
    mock_submit_api_response(201)

    # Testing instantiation with default values
    job = TranslateVideo("JOB_000")

    assert job.job_id == "JOB_000"
    assert job.delay_seconds == 20
    assert job.polling_interval_seconds == 5
    assert job.timeout_seconds == 3600

    # Testing instantiation with user defined values
    job = TranslateVideo(
        "JOB_001", delay_seconds=5, polling_interval_seconds=1, timeout_seconds=3
    )

    assert job.job_id == "JOB_001"
    assert job.delay_seconds == 5
    assert job.polling_interval_seconds == 1
    assert job.timeout_seconds == 3
