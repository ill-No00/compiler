


class RuntimeError(Exception):
    def __init__(self, message, token):
        self.message = message
        self.token = token

    def __str__(self):
        print(f"Token: {self.token}")
        return f"Runtime Error: {self.message} at line {self.token.line}"