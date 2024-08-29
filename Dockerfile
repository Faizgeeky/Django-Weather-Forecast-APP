FROM python:3.11.4-slim-bullseye
WORKDIR /app

ENV WEATHER_API e5a76d950c834ddba56100009242808
# install system dependencies
RUN apt-get update

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "gunicorn", "wforecast.wsgi", "-b", "0.0.0.0:8000"]