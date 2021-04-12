FROM python:3.9-slim-buster

ADD requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
# packages required for setting up WSGI
RUN apt-get update \
&& apt-get install -y --no-install-recommends gcc libc-dev libpq-dev python3-dev \
&& pip install -r /app/requirements.txt

ADD src /app
WORKDIR /app

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "estimer.wsgi:application"]



