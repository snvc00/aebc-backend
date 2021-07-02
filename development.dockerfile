FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /api/

WORKDIR /api

RUN apt update && apt install -y -qq gcc libpq-dev wkhtmltopdf nano net-tools \
    && pip3 install --no-cache-dir -U -r requirements.txt

RUN mkdir -p /var/www/media/

EXPOSE 8000

CMD [ "/bin/bash", "init.sh" ]