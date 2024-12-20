class InsufficientError(Exception):
    def __init__(self, message, detail=None):
        self.message = message
        self.details = detail
        self.status_code = 507
