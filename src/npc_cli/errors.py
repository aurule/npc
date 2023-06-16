from click import ClickException, BadParameter, UsageError

class BadCharacterTypeException(BadParameter):
    def __init__(self, type_key, valid_keys, hint):
        super().__init__(f"'{type_key}' is not one of {valid_keys}", param_hint=hint)

class CampaignNotFoundException(ClickException):
    def __init__(self):
        super().__init__("Not a campaign (or any of the parent directories)")

class CampaignRequiredException(UsageError):
    def __init__(self, hint=("-s", "--system")):
        formatted_hint = "' '".join(hint)
        super().__init__(f"Not a campaign, so the '{formatted_hint}' option must be provided")
