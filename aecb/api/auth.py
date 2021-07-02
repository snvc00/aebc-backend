from google.oauth2 import id_token
from google.auth.transport import requests
from .models import Account


class AuthException(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return super().__str__()


class AuthResult():
    def __init__(self, account: Account, email: str, detail: str) -> None:
        self.account = account
        self.email_from_token = email
        self.detail = detail
    
    def __str__(self) -> str:
        return self.detail


class GoogleTokenAuth():
    def authenticate(token: str) -> AuthResult:
        try:
            email = None
            user = id_token.verify_firebase_token(token, requests.Request())
            email = user.get("email", None)

            if email is None:
                raise AuthException("Invalid token")

            account = Account.objects.filter(user_email=email).first()

            if account is None:
                raise AuthException("No account with the given email")

            return AuthResult(account, email, "Auth as: {role}".format(role=account.role))
        except AuthException as e:
            return AuthResult(None, email, "Authentication Error: {message}".format(message=str(e)))
        except Exception as e:
            return AuthResult(None, None, "Authentication Error: Invalid token")
