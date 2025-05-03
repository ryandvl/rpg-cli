from src.globals import Callable


class SelectionInterface:
    id: str
    num: int
    text: str
    render: Callable
