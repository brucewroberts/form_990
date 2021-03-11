FROM ubuntu:20.04

MAINTAINER Bruce Roberts "bruce@roberscave.net"

RUN apt-get update && apt-get install -y \
  python3.9 \
  python3-pip
RUN python3.9 -m pip install pip
RUN apt-get update && apt-get install -y \
  python3-distutils \
  python3-setuptools

# Copy requirements and run pip first to avoid running every code update
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Only copy what we need for the app to run, and nothing else.
RUN mkdir /app
COPY run.py /app
RUN mkdir /app/app
COPY app /app/app/
RUN mkdir /app/instance
COPY instance /app/instance/

WORKDIR /app

EXPOSE 5000

ARG APP_ENV

ENV APP_ENV ${APP_ENV}
ENV DATABASE_ENV production

CMD ["gunicorn", \
     "--capture-output", \
     "--error-logfile", "-", \
     "--access-logfile", "-", \
     "--access-logformat", "%(h)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\" %({x-forwarded-for}i)s", \
     "--log-level", "info", \
     "--certfile=instance/server.crt", \
     "--keyfile=instance/server.key", \
     "--bind",  "0.0.0.0:5000",  \
     "-w", "2", \
     "app:create_app()"]
