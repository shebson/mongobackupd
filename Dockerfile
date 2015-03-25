#
# Python Dockerfile
#
# https://github.com/dockerfile/python
#

# Pull base image.
FROM dockerfile/ubuntu

# Install Python.
RUN \
  apt-get update && \
  apt-get install -y python python-dev python-pip python-virtualenv && \
  rm -rf /var/lib/apt/lists/*

# Configure cron
ADD crontab /etc/crontab
RUN touch /var/log/cron.log
RUN crontab /etc/crontab

# Define working directory.
WORKDIR /backupd

ADD ./requirements.txt /backupd/requirements.txt
RUN pip install -r /backupd/requirements.txt
ADD ./backup.py /backupd/backup.py
ADD ./settings.py /backupd/settings.py
ADD ./reporting.py /backupd/reporting.py

# Run cron by default
ENTRYPOINT cron -f