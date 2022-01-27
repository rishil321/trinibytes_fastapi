# Pull base image from dockerhub
FROM python:3.10
# create the directory to store our project files
RUN mkdir /code
# Set the working directory inside the container 
WORKDIR /code
COPY ./config/nginx/certs /etc/certs
# Update the index of packages available to apk
#RUN apt -qq update --yes
# install some package dependencies that we need
#RUN apt install apache2 apache2-dev unixodbc-dev --yes
#RUN apt install unixodbc-dev --yes
# Copy the poetry.lock and pyproject.toml files to setup poetry
COPY poetry.lock pyproject.toml /code/
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi
# Copy project files into container
COPY . /code/