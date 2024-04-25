"""Defining custom exceptions that get raised"""


class GetJobInfoError(Exception):
    """Raised when getting the job info fails"""


class SubmitJobError(Exception):
    """Raised when submitting a job fails"""


class UpdateJobStatusError(Exception):
    """Raised when updating a job's status fails"""
