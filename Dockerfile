FROM python:3.9.4-alpine

WORKDIR /api
COPY . /api/

RUN pip install -U -r requirements.txt

WORKDIR /api/src
EXPOSE 5000

CMD [ "flask", "run" ]