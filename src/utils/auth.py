from utils.database import AdminTokenTable
from utils.exceptions import ApiException

class Auth():
    """
    """


    def is_valid_token(token: str) -> bool:
        try:
            token = AdminTokenTable.fetch(token)
            
            return token.get("is_active", False)
            
        except ApiException as e:
            print(e, e.message)
            raise ApiException("Invalid Token", 400)
        except Exception as e:
            print(e.__class__.__name__, str(e))
            raise ApiException("Invalid Token", 400)

