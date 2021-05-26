from utils.exceptions import ApiException
from utils.exceptions import ApiException
from utils.responses import error_response, ok_response
from utils.database import CreditCardDB
from datetime import datetime
from werkzeug.local import LocalProxy

def fetch_credit_cards():
    try:
        credit_cards = CreditCardDB.fetch_all()

        return ok_response(200, {"credit_cards": credit_cards})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))


def insert_credit_card(request: LocalProxy):
    try:
        if not request.is_json:
            raise ApiException("Request is not JSON", 400)
        
        CreditCardDB.insert(request.json)

        return ok_response(200, {"inserted_at": datetime.today().isoformat()})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))
    


def fetch_credit_card(id: str):
    try:
        credit_card = CreditCardDB.fetch_by_id(id)

        return ok_response(200, {"credit_card": credit_card})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))


def update_credit_card(id: str, request: LocalProxy):
    try:
        if not request.is_json:
            raise ApiException("Request is not JSON", 400)

        CreditCardDB.update_by_id(id, request.json)

        return ok_response(200, {"updated_at": datetime.today().isoformat()})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))


def delete_credit_card(id: str):
    try:
        CreditCardDB.delete_by_id(id)

        return ok_response(200, {"deleted_at": datetime.today().isoformat()})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))
