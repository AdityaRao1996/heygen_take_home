"""Module that's executed as part of the end-to-end test
after spinning up the FastAPI server and by making use of
the installed 'translate_video' client library.
"""

from translate_video.translate_video import TranslateVideo

job = TranslateVideo(
    job_id="TEST_JOB",
    delay_seconds=15,
    polling_interval_seconds=3,
    timeout_seconds=60,
)
job.display_attributes()

job.submit()
status = job.get_status()

assert status == {"result": "completed"} or status == {"result": "error"}
