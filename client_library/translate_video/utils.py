"""Module exposing various utility methods for displaying helpful information
regarding the progress of the video translation job on the console,
handling errors when the API calls aren't successful, parsing the response to
retrieve the job's status and calculating the elapsed time.
"""

from dataclasses import dataclass
from logging import Logger
from typing import Dict, Literal

import time

from colorama import Fore, init
from requests import Response

init(autoreset=True)


@dataclass
class JobResultAndElapsedTime:
    """DTO with attributes holding the current status of the job along with the elapsed time"""

    result: Literal["completed", "error", "pending"]
    elapsed_time: float


def _display_elapsed_time(elapsed_time: float) -> None:
    """Displays the elapsed time since initially checking the status of the job"""
    print(
        Fore.WHITE
        + "Elapsed time: "
        + Fore.LIGHTCYAN_EX
        + str(round(elapsed_time, 2))
        + " seconds"
        + "\n"
    )


def _display_job_status(
    job_id: str, job_status: Literal["completed", "error", "pending"]
) -> None:
    """Displays the status of the given job_id"""
    if job_status == "completed":
        color = Fore.GREEN
    elif job_status == "pending":
        color = Fore.LIGHTYELLOW_EX
    else:
        color = Fore.RED

    print(
        "\n"
        + Fore.WHITE
        + "Status of "
        + Fore.LIGHTCYAN_EX
        + job_id
        + Fore.WHITE
        + " : "
        + color
        + f" {job_status}"
    )


def _display_job_status_and_elapsed_time(
    job_id: str,
    job_status: Literal["completed", "error", "pending"],
    elapsed_time: float,
) -> None:
    """Invokes the 'private' functions that display the job status and the elapsed time"""
    _display_job_status(job_id, job_status)
    _display_elapsed_time(elapsed_time)


def _get_status_and_elapsed_time(
    response: Response, start_time: float
) -> JobResultAndElapsedTime:
    """Returns the job status and the elapsed time"""
    status = _jsonify_response(response)
    elapsed_time = time.time() - start_time

    return JobResultAndElapsedTime(result=status["result"], elapsed_time=elapsed_time)


def _jsonify_response(response: Response) -> Dict[str, str]:
    """Converts the HTTP Response to JSON"""
    return response.json()


def check_status_and_display(
    job_id: str,
    response: Response,
    start_time: float,
) -> JobResultAndElapsedTime:
    """Gets the job's status and the elapsed time. Displays the job info"""
    job_info = _get_status_and_elapsed_time(response, start_time)
    _display_job_status_and_elapsed_time(
        job_id=job_id, job_status=job_info.result, elapsed_time=job_info.elapsed_time
    )

    return job_info


def display_object_attributes(job) -> None:
    """Displays the object's attributes and its values"""
    print(
        "\n"
        + Fore.GREEN
        + "Instantiated a client instance with the following attributes:"
    )
    print(Fore.LIGHTYELLOW_EX + "job_id: " + Fore.LIGHTCYAN_EX + job.job_id)
    print(
        Fore.LIGHTYELLOW_EX
        + "delay_seconds: "
        + Fore.LIGHTCYAN_EX
        + str(job.delay_seconds)
    )
    print(
        Fore.LIGHTYELLOW_EX
        + "polling_interval_seconds: "
        + Fore.LIGHTCYAN_EX
        + str(job.polling_interval_seconds)
    )
    print(
        Fore.LIGHTYELLOW_EX
        + "timeout_seconds: "
        + Fore.LIGHTCYAN_EX
        + str(job.timeout_seconds)
        + "\n"
    )


def handle_status_api_errors(response: Response, job_id: str, logger: Logger) -> None:
    """In case of an unsuccessful request to the
    /status API, this method handles the errors
    """
    if response.status_code == 404:
        logger.error(
            f"{job_id} could not be found.\nPlease ensure the job has been submitted "
            "by calling cls_obj.submit()"
        )
    elif response.status_code != 200:
        logger.error(f"Failed to get the status of the job {job_id}. Try again later")
