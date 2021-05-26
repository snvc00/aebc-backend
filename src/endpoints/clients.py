from utils.exceptions import ApiException
from utils.responses import error_response, ok_response
from utils.database import ClientDB
from datetime import datetime
from werkzeug.local import LocalProxy

def fetch_clients():
    try:
        clients = ClientDB.fetch_all()

        return ok_response(200, {"clients": clients})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))


def insert_client(request: LocalProxy):
    try:
        if not request.is_json:
            raise ApiException("Request is not JSON", 400)
        
        ClientDB.insert(request.json)

        return ok_response(200, {"inserted_at": datetime.today().isoformat()})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))
    


def fetch_client(curp: str):
    try:
        client = ClientDB.fetch_by_curp(curp)

        return ok_response(200, {"client": client})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))


def update_client(curp: str, request: LocalProxy):
    try:
        if not request.is_json:
            raise ApiException("Request is not JSON", 400)

        ClientDB.update_by_curp(curp, request.json)

        return ok_response(200, {"updated_at": datetime.today().isoformat()})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))


def delete_client(curp: str):
    try:
        ClientDB.delete_by_curp(curp)

        return ok_response(200, {"deleted_at": datetime.today().isoformat()})

    except ApiException as e:
        return error_response(e.status_code, "ApiException", e.message)
    except Exception as e:
        return error_response(500, e.__class__.__name__, str(e))
