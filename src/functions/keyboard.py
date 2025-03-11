named_keys = {"ESC": 27, "SINGLE_QUOTES": ord("'"), "DOUBLE_QUOTES": ord('"')}


def get_named_key(key: str) -> int:
    """
    Get a key code by its name
    """
    return named_keys.get(key.upper(), -1)


def get_char_key(key_char: str) -> int:
    """
    Get a key code by char
    """
    return ord(key_char)
