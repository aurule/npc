class ValidationError():
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message

class SettingsValidationError(ValidationError):
    def __init__(self, message: str, file: str, lineno: int = -1, colno: int = -1):
        linepart = ""
        colpart = ""
        if lineno >= 0:
            linepart = f" line {lineno}"
        if colno >= 0:
            colpart = f" column {colpart}"

        super().__init__(f"Error in settings file {file}{linepart}{colpart}: {message}")
