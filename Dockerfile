# For more information, please refer to https://aka.ms/vscode-docker-python
# set base image as python
FROM python:3.7

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
RUN pip install gunicorn[gevent]
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# set the working directory for the following instructions
WORKDIR /app

# copying the source code from local system to docker image
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
#RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
#USER root

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# defines the program or command to run when container starts
# it will run sh command and will pass run.sh as argument
CMD ["sh", "run.sh"]