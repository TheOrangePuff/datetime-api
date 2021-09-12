FROM python:buster

WORKDIR /app

ENV FLASK_APP=datetime_api
ENV FLASK_RUN_HOST=0.0.0.0:80
ENV PYTHONPATH=/app

ADD requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 80
COPY tests tests
COPY datetime_api datetime_api

CMD ["gunicorn", "-b", "0.0.0.0:80", "datetime_api:create_app()"]
