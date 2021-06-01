from utils.exceptions import ApiException
from utils.responses import error_response, ok_response
from utils.auth import Auth
from werkzeug.local import LocalProxy

def verify_token(request: LocalProxy):
    try:
        token = request.headers.get("Token", None)
        is_valid_token = Auth.is_valid_token(token)

        return ok_response(200, {"is_valid_token": is_valid_token})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))
