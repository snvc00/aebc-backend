import os


VALID_ENVIRONMENTS = [
    "production",
    "development"
]

ENV = os.environ.get("FLASK_ENVIRONMENT", "development")

if not ENV in VALID_ENVIRONMENTS:
    raise Exception("FLASK_ENVIRONMENT environment variables is not defined or not in {}".format(VALID_ENVIRONMENTS))

SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "TheSecretKey")
DEBUG = ENV == "development"
TESTING = os.environ.get("FLASK_TESTING_ENABLED", "0") == "1"
HOST = os.environ.get("FLASK_HOST", "0.0.0.0")
PORT = int(os.environ.get("FLASK_PORT", 5000))

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_NAME = os.environ.get("DB_NAME", "aebc")

if ENV == "production":
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_URI = "mysql://{}:{}@{}:{}/{}".format(
        DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
    )
elif ENV == "development":
    DB_URI = "mysql://{}:{}/{}".format(DB_HOST, DB_PORT, DB_NAME)
    DB_URL = "mysql://api:password@{}:{}/{}".format(
        DB_HOST, DB_PORT, DB_NAME
    )
