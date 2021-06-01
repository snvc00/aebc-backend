from utils.exceptions import ApiException
from utils.exceptions import ApiException
from utils.responses import error_response, ok_response
from utils.database import CreditCardTable
from datetime import datetime
from werkzeug.local import LocalProxy
from utils.auth import Auth

def fetch_credit_cards(request: LocalProxy):
    try:
        token = request.headers.get("Token", None)

        if token is None:
            raise ApiException("Token headers is required", 400)

        if not Auth.is_valid_token(token):
            raise ApiException("Invalid Token", 400)

        credit_cards = CreditCardTable.fetch_all()

        return ok_response(200, {"credit_cards": credit_cards})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))


def insert_credit_card(request: LocalProxy):
    try:
        token = request.headers.get("Token", None)

        if token is None:
            raise ApiException("Token headers is required", 400)

        if not Auth.is_valid_token(token):
            raise ApiException("Invalid Token", 400)

        if not request.is_json:
            raise ApiException("Request is not JSON", 400)
        
        CreditCardTable.insert(request.json)

        return ok_response(200, {"inserted_at": datetime.today().isoformat()})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))
    


def fetch_credit_card(id: str, request: LocalProxy):
    try:
        token = request.headers.get("Token", None)

        if token is None:
            raise ApiException("Token headers is required", 400)

        if not Auth.is_valid_token(token):
            raise ApiException("Invalid Token", 400)

        credit_card = CreditCardTable.fetch_by_id(id)

        return ok_response(200, {"credit_card": credit_card})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))


def update_credit_card(id: str, request: LocalProxy):
    try:
        token = request.headers.get("Token", None)

        if token is None:
            raise ApiException("Token headers is required", 400)

        if not Auth.is_valid_token(token):
            raise ApiException("Invalid Token", 400)

        if not request.is_json:
            raise ApiException("Request is not JSON", 400)

        CreditCardTable.update_by_id(id, request.json)

        return ok_response(200, {"updated_at": datetime.today().isoformat()})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))


def delete_credit_card(id: str, request: LocalProxy):
    try:
        token = request.headers.get("Token", None)

        if token is None:
            raise ApiException("Token headers is required", 400)

        if not Auth.is_valid_token(token):
            raise ApiException("Invalid Token", 400)

        CreditCardTable.delete_by_id(id)

        return ok_response(200, {"deleted_at": datetime.today().isoformat()})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))
