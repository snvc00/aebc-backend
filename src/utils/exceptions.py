class ApiException(Exception):
    def __init__(self, message, status_code: int) -> None:
        self.message = message
        self.status_code = status_code

    def __str__(self) -> str:
        return "ApiException"