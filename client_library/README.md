# Python library: translate_video

Easily submit jobs for translating videos and monitor their statuses.

## Creating the installable library

From the root of this project's directory, run:

```bash
make install
```

This ^ installs the dependencies required for being able to create a python library.
Now, switch to the `client_library/` directory [`cd client_library`] and run:

```bash
python setup.py bdist_wheel
```

## Installation

```bash
pip install dist/translate_video-0.1.0-py3-none-any.whl --force-reinstall
```

## Quick Start

Here's a quick example of how to import this library:

```python
from translate_video.translate_video import TranslateVideo

# Implementation...
```

## Features

1. Submitting a video translation job: This library exposes a `submit()` method which calls the `/submit` API for submitting a job with its configured attributes.
2. Fetching the status of a job: This library exposes a `get_status()` method which calls the `/status` API for checking the status of the job, and will continue to do so until either the job is completed (successfully or not) or the elapsed time becomes greater than the timeout seconds that was set when creating the instance of the `TranslateVideo` class.

## Usage

To create an instance of the `TranslateVideo` class, the `job_id` must be passed. Along with the `job_id`, optional parameters such as `delay_seconds`, `polling_interval_seconds` and `timeout_seconds` can be passed. These optional attributes all have a default value they are set to, if not passed when creating an instance of the class.

```python
from translate_video import TranslateVideo

# Creating an instance of the TranslateVideo class
video_translation_job = TranslateVideo(
    job_id="TEST_JOB", # ID of the job
    delay_seconds=15, # Attribute indicating the time (seconds) it takes to process the job
    polling_interval_seconds=3, # Seconds between successive calls to the GET /status API
    timeout_seconds=60, # Seconds to wait for the job to process before returning the status of the job
)

# Submitting the job
video_translation_job.submit()

# Fetch the status of the above job
status = video_translation_job.get_status() # Will run until the job is completed or the timeout seconds has elapsed
print(status) # {"result": "completed"}
```
