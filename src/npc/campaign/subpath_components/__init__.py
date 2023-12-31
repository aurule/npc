from .first_value_component import FirstValueComponent
from .static_value_component import StaticValueComponent
from .conditional_value_component import ConditionalValueComponent

__all__ = [
    "FirstValueComponent",
    "StaticValueComponent",
    "ConditionalValueComponent",
]

all_components = [
    FirstValueComponent,
    StaticValueComponent,
    ConditionalValueComponent,
]

def get_component(component_key: str):
    """Get the subpath component class with the given SELECTOR

    This gets the class directly. It still must be instantiated. If no class is
    defined with a SELECTOR that matches component_key, no class will be
    returned.

    Args:
        component_key (str): Unique key for the component class, defined in
            each class' SELECTOR property

    Returns:
        BaseComponent: A subpath component class, or None if no class matches
    """
    for component_class in all_components:
        if component_key == component_class.SELECTOR:
            return component_class

    return None
