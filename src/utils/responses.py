from flask import make_response
from flask.globals import request

def error_response(code: int, type: str, message: str):
    return make_response({
        "error": {
            "type": type,
            "message": message
        }},
        code
    )

def ok_response(code: int, body: dict):
    return make_response(body, code)