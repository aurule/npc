from .validation_error import ValidationError

class SettingsValidationError(ValidationError):
    def __init__(self, detail: str, file: str, lineno: int = -1, colno: int = -1):
        super().__init__(detail)
        self.file = file
        self.lineno = lineno
        self.colno = colno

        linepart = ""
        colpart = ""
        if lineno >= 0:
            linepart = f" line {lineno}"
        if colno >= 0:
            colpart = f" column {colpart}"
        self.preamble = f"Error in settings file {file}{linepart}{colpart}"

class SettingsNoVersionError(SettingsValidationError):
    def __init__(self, file: str):
        super().__init__(f"missing npc.version", file)

class SettingsLockedTagError(SettingsValidationError):
    def __init__(self, tag_name: str, file: str, lineno: int = -1, colno: int = -1):
        super().__init__(f"tag {tag_name} is locked", file, lineno, colno)
        self.tag_name = tag_name
