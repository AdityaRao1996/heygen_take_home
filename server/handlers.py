# pylint: skip-file
"""Entry point to the GET /status API and the POST /submit API"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Annotated, Literal

from fastapi import FastAPI, Path, Query, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from . import database, errors


@dataclass
class GetStatusResponse:
    """DTO for the /status API's response object"""

    result: Literal["completed", "error", "pending"]


app = FastAPI()


@app.get("/status/{job_id}")
async def get_job_status(
    job_id: Annotated[str, Path(description="ID of the job whose status to check for")],
) -> JSONResponse:
    """Returns the status of the given job_id

    Args:
        job_id: str: ID of the job whose status to check for

    Returns:
        The status of the given job_id ["completed" OR "error" OR "pending"]
    """
    try:
        job_info = database.fake_get_job_info(job_id)
    except errors.GetJobInfoError as e:
        raise HTTPException(status_code=503, detail=str(e))

    if not job_info:
        raise HTTPException(
            status_code=404, detail=f"Job ID {job_id} could not be found"
        )

    if job_info.random_num <= 0.2:  # Want to return "error" 20% of the times
        try:
            database.fake_update_job_status(job_id, "error")
        except errors.UpdateJobStatusError as e:
            raise HTTPException(status_code=503, detail=str(e))

        response = GetStatusResponse(result="error")
        json_compatible_response = jsonable_encoder(response)

        return JSONResponse(content=json_compatible_response)

    current_time = datetime.now()
    job_completes_at = job_info.started_at + timedelta(seconds=job_info.delay)

    if current_time >= job_completes_at:
        try:
            database.fake_update_job_status(job_id, "completed")
        except errors.UpdateJobStatusError as e:
            raise HTTPException(status_code=503, detail=str(e))

        response = GetStatusResponse(result="completed")
        json_compatible_response = jsonable_encoder(response)

        return JSONResponse(content=json_compatible_response)

    response = GetStatusResponse(result="pending")
    json_compatible_response = jsonable_encoder(response)

    return JSONResponse(content=json_compatible_response)


@app.post("/submit/{job_id}")
async def submit_job(
    job_id: Annotated[str, Path(description="ID of the job to create")],
    delay_seconds: Annotated[
        int, Query(description="Time in seconds for the job to complete")
    ] = 20,
) -> Response:
    """Returns the job_id after submitting it successfully

    Args:
        job_id: str: ID of the job to submit
        delay_seconds: int: Proxy for indicating the time (in seconds) it
        takes for the given job_id to complete successfully. (default 20)

    Returns: A string indicating successful submission of the job, with its ID
    """
    try:
        database.fake_submit_job(job_id, delay_seconds)
        return Response(
            content=f"Successfully submitted the job: {job_id}", status_code=201
        )
    except errors.SubmitJobError as e:
        raise HTTPException(status_code=503, detail=str(e))
