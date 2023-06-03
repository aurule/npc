from . import ValidationError

class TagValidationError(ValidationError):
    def __init__(self, message: str, name):
        super().__init__(f"Error in tag @{name}: {message}")

class TagDeprecatedError(TagValidationError):
    def __init__(self, name: str, replacement: str):
        super().__init__(f"deprecated. Use {replacement} instead.", name)

class TagEmptyError(TagValidationError):
    def __init__(self, name: str):
        super().__init__("missing value", name)

class TagMaxError(TagValidationError):
    def __init__(self, name: str, cap: int, count: int):
        super().__init__(f"too many. {cap} allowed, found {count}", name)

class TagMinError(TagValidationError):
    def __init__(self, name: str, floor: int, count: int):
        super().__init__(f"too few. {floor} required, found {count}", name)

class TagNoValueAllowedError(TagValidationError):
    def __init__(self, name: str, value: str):
        super().__init__(f"no value allowed, but has '{value}'", name)

class TagReplacedError(TagValidationError):
    def __init__(self, name: str, replacement: str):
        super().__init__(f"replaced. Use {replacement} instead.", name)

class TagRequiredError(TagValidationError):
    def __init__(self, name: str):
        super().__init__("required, but not present", name)

class TagValueError(TagValidationError):
    def __init__(self, name: str, badvalue: str):
        super().__init__(f"unrecognized value '{badvalue}'", name)
