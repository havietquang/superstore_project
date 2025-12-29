FROM apache/airflow:2.9.1-python3.9

# Install Python dependencies as root so packages are placed in system site-packages
USER root

COPY requirements.txt /requirements.txt

# Allow pip to run as root during image build (some base images prevent this)
ENV PIP_REQUIRE_VIRTUALENV=false

RUN pip install --no-cache-dir -r /requirements.txt

# Switch back to non-root `airflow` user for running the container
USER airflow
