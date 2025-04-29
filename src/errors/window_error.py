class WindowError(Exception):
    def __init__(self, message: str, type: str = "Unknown") -> None:
        super().__init__(message)
        self.message = message
        self.type = type
        self.name = "Window"
