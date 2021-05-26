from models.benefit import Benefit
from utils.exceptions import ApiException
from utils.responses import error_response, ok_response
from utils.database import BenefitTable
from datetime import datetime
from werkzeug.local import LocalProxy

def fetch_benefits():
    try:
        benefits = BenefitTable.fetch_all()

        return ok_response(200, {"benefits": benefits})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))


def insert_benefit(request: LocalProxy):
    try:
        if not request.is_json:
            raise ApiException("Request is not JSON", 400)
        
        BenefitTable.insert(request.json)

        return ok_response(200, {"inserted_at": datetime.today().isoformat()})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))
    


def fetch_benefit(id: str):
    try:
        benefit = BenefitTable.fetch_by_id(id)

        return ok_response(200, {"benefit": benefit})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))


def update_benefit(id: str, request: LocalProxy):
    try:
        if not request.is_json:
            raise ApiException("Request is not JSON", 400)

        BenefitTable.update_by_id(id, request.json)

        return ok_response(200, {"updated_at": datetime.today().isoformat()})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))


def delete_benefit(id: str):
    try:
        BenefitTable.delete_by_id(id)

        return ok_response(200, {"deleted_at": datetime.today().isoformat()})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))
