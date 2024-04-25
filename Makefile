# Makefile for installing the dependencies, running the linter and running the tests.

# Target: install
# Description: Sets up Python virtual environment and installs requirements
install:
	python -m venv .venv                 # Create a virtual environment
	. .venv/bin/activate;                # Activate the virtual environment
	pip install -r requirements.txt      # Install requirements

# Target: lint
# Description: Runs the linter over the codebase excluding the tests
lint:
	pylint server/database.py server/errors.py server/handlers.py client_library/translate_video/*      # Running the linter over the codebase excluding the tests


# Target: run_integration_test
# Description: Run the end to end test test which spins up the server
# locally, and tests the client library's functions.
run_integration_test:
	./run_integration_test.sh

# Target: test
# Description: Execute tests using pytest
test:
	pytest -v server/tests               # Execute server tests
	pytest -v client_library/tests       # Execute client library tests
