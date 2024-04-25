"""Methods exposed by the Client Library"""

from typing import Dict

import logging
import time

import requests

from . import api, utils

logger = logging.getLogger(__name__)


class TranslateVideo:
    """A class representing a video translation job.

    This class provides functionality for submitting a video translation
    job, getting the status of a submitted job and prettily displaying
    the attributes of an instantiated instance of the class.

    Attributes:
        job_id: str -> ID of the video translation job to be submitted.

        delay_seconds: int -> Configurable "delay" seconds indicating how long
        the job takes to successfully complete. (default 20).

        polling_interval_seconds: int -> Value indicating the time interval (in seconds)
        between successive calls to the GET /status API when the job's status is "pending".
        (default 5).

        timeout_seconds: int -> Value indicating the amount of time (in seconds) to wait
        before returning the status of the job, when the status is "pending".
        (default 3600).

    Public Methods:
        display_attributes: Prettily displays the attributes of the class object.
        get_status: Returns the status of the job by calling the GET /status API.
        submit: Submits a video translation job by calling the /submit API.


    Usage:
        >>> job = TranslateVideo("JOB_001")
        >>> job.display_attributes() # Prettily prints the attributes of the object with its values.
        >>> job.submit() # Submits the job for processing.
        >>> job.get_status()
        {"result": "pending"} OR {"result": "completed"} OR {"result": "error"}
    """

    def __init__(
        self,
        job_id: str,
        delay_seconds: int = 20,
        polling_interval_seconds: int = 5,
        timeout_seconds: int = 3600,
    ) -> None:

        self.job_id = job_id
        self.delay_seconds = delay_seconds
        self.polling_interval_seconds = polling_interval_seconds
        self.timeout_seconds = timeout_seconds

    def display_attributes(self) -> None:
        """Prettily displays the attributes of the class instance"""
        utils.display_object_attributes(self)

    def get_status(self) -> Dict[str, str]:
        """Gets the job's status by calling the GET /status API repeatedly
        after every `polling_interval_seconds` seconds, as long as the elapsed
        time is within the `timeout_seconds` seconds.
        """
        valid_statuses_to_exit = {"completed", "error"}
        start_time = time.time()
        url = api.STATUS_URL + f"/{self.job_id}"

        response = requests.get(url=url, timeout=10)
        utils.handle_status_api_errors(response, self.job_id, logger)

        job_status = utils.check_status_and_display(
            response=response, start_time=start_time, job_id=self.job_id
        )

        while (
            job_status.result not in valid_statuses_to_exit
            and job_status.elapsed_time < self.timeout_seconds
        ):

            time.sleep(self.polling_interval_seconds)
            response = requests.get(url=url, timeout=10)
            utils.handle_status_api_errors(response, self.job_id, logger)

            job_status = utils.check_status_and_display(
                response=response, start_time=start_time, job_id=self.job_id
            )

        return {"result": job_status.result}

    def submit(self) -> None:
        """Submits the job by calling the POST /submit API"""
        params = {"delay_seconds": self.delay_seconds}
        url = api.SUBMIT_URL + f"/{self.job_id}"

        response = requests.post(url=url, params=params, timeout=10)
        if response.status_code != 201:
            message = response.json()["detail"]
            logger.error(message)
