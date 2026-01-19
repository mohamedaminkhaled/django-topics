# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /docker_compose

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /docker_compose/entrypoint.sh
RUN chmod +x /docker_compose/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/docker_compose/entrypoint.sh"]