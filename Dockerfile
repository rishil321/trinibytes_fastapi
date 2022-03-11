# Pull base image from dockerhub
FROM python:3.10
# create the directory to store our project files
RUN mkdir /code
# Set the working directory inside the container 
WORKDIR /code
#COPY ./config/nginx/certs /etc/certs
# install crontab
RUN apt-get update && apt-get -y install cron
# Copy hello-cron file to the cron.d directory
COPY crontab /etc/cron.d/crontab

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/crontab

# Apply cron job
RUN crontab /etc/cron.d/crontab

# Create the log file to be able to run tail
RUN touch /var/log/cron.log
# Copy the poetry.lock and pyproject.toml files to setup poetry
COPY poetry.lock pyproject.toml /code/
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi
# Copy project files into container
COPY . /code/