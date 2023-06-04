class ValidationError():
    def __init__(self, detail: str):
        self.detail = detail
        self.preamble = "Error"

    def __str__(self) -> str:
        return self.message

    @property
    def message(self) -> str:
        return f"{self.preamble}: {self.detail}"

class SettingsValidationError(ValidationError):
    def __init__(self, message: str, file: str, lineno: int = -1, colno: int = -1):
        linepart = ""
        colpart = ""
        if lineno >= 0:
            linepart = f" line {lineno}"
        if colno >= 0:
            colpart = f" column {colpart}"

        super().__init__(f"Error in settings file {file}{linepart}{colpart}: {message}")
