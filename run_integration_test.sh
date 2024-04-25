#!/bin/bash

# Start the FastAPI server
echo "Starting FastAPI server..."
uvicorn server.handlers:app --host 127.0.0.1 --port 8000 &

# Waiting for the server to start
sleep 3

echo "Creating a virtual environment and installing the dependencies..."
make install

echo "Creating an installable python library inside client_library/"
cd client_library
python3 setup.py bdist_wheel
pip3 install dist/translate_video-0.1.0-py3-none-any.whl --force-reinstall
cd .. && clear

# Run the Python script in a new terminal
echo "Running the integration test..."
python3 test_end_to_end.py

# Spin down the FastAPI server
echo "Stopping FastAPI server..."
PID="$(pgrep -f server.handlers:app)"
if [[ -n "$PID" ]]
then
    kill -SIGINT $PID
fi

# Wait for server to be shut down
sleep 3

echo "Server has been shut down"
