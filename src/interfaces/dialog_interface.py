from abc import ABC

from .layer_interface import LayerInterface


class DialogInterface(ABC):
    """
    A dialog is a group of layers with more priority and can be placed on windows

    The layers priority is based on Dialog, not on Window, example:
    - Window has a layer with priority 5
    - But the Dialog has a layer with priority 6
    - So, the Dialog layer has priority than Window
    """

    name: str
    priority: int
    layers: list[LayerInterface] = list()
