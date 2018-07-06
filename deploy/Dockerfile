FROM python:3.6-alpine

RUN adduser -D app
WORKDIR /home/app

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]

COPY abituz.py deploy/requirements.txt deploy/boot.sh ./
RUN apk add --update mariadb-dev gcc musl-dev \
 && python -m venv venv \
 && venv/bin/pip install -r requirements.txt \
 && venv/bin/pip install gunicorn \
 && chmod +x boot.sh \
 && chown -R app:app ./ \
 && apk del gcc musl-dev \
 && rm -fr /var/cache/apk/*

USER app
ENV FLASK_APP abituz.py

COPY app app
COPY migrations migrations