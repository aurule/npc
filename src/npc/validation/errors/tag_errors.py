from . import ValidationError

class TagValidationError(ValidationError):
    def __init__(self, detail: str, tag_name: str):
        super().__init__(detail)
        self.tag_name: str = tag_name
        self.preamble: str = f"Error in tag @{tag_name}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tag_name={self.tag_name!r})"

class TagDeprecatedError(TagValidationError):
    def __init__(self, tag_name: str, replacement: str):
        super().__init__(f"deprecated. Use {replacement} instead.", tag_name)
        self.replacement: str = replacement

class TagEmptyError(TagValidationError):
    def __init__(self, tag_name: str):
        super().__init__("missing value", tag_name)

class TagMaxError(TagValidationError):
    def __init__(self, tag_name: str, cap: int, count: int):
        super().__init__(f"too many. {cap} allowed, found {count}", tag_name)
        self.cap: int = cap
        self.count: int = count

class TagMinError(TagValidationError):
    def __init__(self, tag_name: str, floor: int, count: int):
        super().__init__(f"too few. {floor} required, found {count}", tag_name)
        self.floor: int = floor
        self.count: int = count

class TagNoValueAllowedError(TagValidationError):
    def __init__(self, tag_name: str, value: str):
        super().__init__(f"no value allowed, but has '{value}'", tag_name)
        self.value: str = value

class TagReplacedError(TagValidationError):
    def __init__(self, tag_name: str, replacement: str):
        super().__init__(f"replaced. Use {replacement} instead.", tag_name)
        self.replacement: str = replacement

class TagRequiredError(TagValidationError):
    def __init__(self, tag_name: str):
        super().__init__("required, but not present", tag_name)

class TagUndefinedError(TagValidationError):
    def __init__(self, tag_name: str):
        super().__init__("no definition found", tag_name)

class TagValueError(TagValidationError):
    def __init__(self, tag_name: str, value: str):
        super().__init__(f"unrecognized value '{value}'", tag_name)
        self.value: str = value
