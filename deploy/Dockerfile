FROM python:3.6-alpine

RUN adduser -D app
WORKDIR /home/app

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]

COPY deploy/requirements.txt ./
RUN apk add --update mariadb-dev gcc musl-dev \
 && python -m venv venv \
 && venv/bin/pip install -r requirements.txt \
 && venv/bin/pip install gunicorn mysqlclient \
 && chown -R app:app ./ \
 && apk del gcc musl-dev \
 && rm -fr /var/cache/apk/*

COPY deploy/boot.sh deploy/update.sh ./
RUN chmod +x boot.sh update.sh

USER app
ENV FLASK_APP abituz.py
ENV PYTHONUNBUFFERED 1

COPY abituz.py ./
COPY app app
COPY migrations migrations
