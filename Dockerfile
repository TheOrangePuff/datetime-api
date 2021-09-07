FROM python:buster

WORKDIR /app

ENV FLASK_APP=datetime_api
ENV FLASK_RUN_HOST=0.0.0.0

ADD requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 80
ADD datetime_api .

CMD ["uwsgi"]
