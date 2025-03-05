named_keys = {
    "ESC": 27,
    "SINGLE_QUOTES": ord("'"),
    "DOUBLE_QUOTES": ord('"')
}

def get_named_key(key: str) -> int:
    return named_keys.get(key.upper(), -1)

def get_char_key(key_char: str) -> int:
    return ord(key_char)
