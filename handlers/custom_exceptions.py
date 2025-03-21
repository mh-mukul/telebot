class APIKeyException(Exception):
    def __init__(self, status: int, message: str, data: dict = None):
        self.status = status
        self.message = message
        self.data = data or {}
