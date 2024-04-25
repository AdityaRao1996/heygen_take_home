"""Database module mimicking a persistent storage and methods to interact with it"""

from dataclasses import dataclass
from datetime import datetime

import random
from typing import Literal, Optional

from server import errors


@dataclass
class Job:
    """Attributes of every Job object/record"""

    delay: int
    random_num: float
    started_at: datetime
    status: Literal["completed", "error", "pending"]


# Dictionary acting like a database. Gets initialized every session.
JOB_INFO_BY_ID: dict[str, Job] = {}


# This can be implemented if we ever want to delete the job-records from the database
# pylint: disable=unused-argument
def fake_delete_job(job_id: str) -> None:
    """Placeholder method for deleting job-records from the database"""


def fake_get_job_info(job_id: str) -> Optional[Job]:
    """Mimicks fetching a Job record from the database"""

    # Adding a try-except block as I would, if this method
    # was actually interacting with a database.
    try:
        return JOB_INFO_BY_ID.get(job_id)
    except Exception as e:
        raise errors.GetJobInfoError(f"Failed to get {job_id}'s info") from e


def fake_submit_job(job_id: str, delay: int) -> None:
    """Mimicks writing a Job record to the database"""

    # Adding a try-except block as I would, if this method
    # was actually interacting with a database.
    try:
        JOB_INFO_BY_ID[job_id] = Job(
            delay=delay,
            random_num=random.random(),
            started_at=datetime.now(),
            status="pending",
        )
    except Exception as e:
        # rollback any transactions
        raise errors.SubmitJobError(f"Failed to submit the job {job_id}") from e


def fake_update_job_status(job_id: str, status: Literal["completed", "error"]) -> None:
    """Mimicks updating a Job record in the database"""

    # Adding a try-except block as I would, if this method
    # was actually interacting with a database.
    try:
        JOB_INFO_BY_ID[job_id].status = status
    except Exception as e:
        raise errors.UpdateJobStatusError(
            f"Failed to update the status of the job {job_id}"
        ) from e
