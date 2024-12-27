def equalize_string(string: str, length: int):
    spaces = length - len(string)

    if spaces <= 0:
        return string
    
    spaces_before = spaces // 2
    spaces_after = spaces - spaces_before

    equalized_string = (" " * spaces_before) + string + (" " * spaces_after)

    return equalized_string

def space_string(string: str, length: int):
    spaces = length - len(string)

    if spaces <= 0:
        return string

    spaced_string = string + (" " * spaces)

    return spaced_string

def insert_string(original_string: str, string_to_insert: str, position: int):
    return original_string[:position] +\
        string_to_insert +\
        original_string[position:]

def create_bar(current: float | int, total: float | int, size: int = 20):
    bar_size = int(
        (current / total) * size
    )

    bar = equalize_string(
            f'{current}/{total}',
            size
        )

    return bar