FROM python:buster

WORKDIR /app

ENV FLASK_APP=datetime-api.py
ENV FLASK_RUN_HOST=0.0.0.0

ADD requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 80
ADD datetime-api.py .

CMD ["uwsgi"]
