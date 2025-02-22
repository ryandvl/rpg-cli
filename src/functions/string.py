def equalize_string(string: str, length: int) -> str:
    spaces = length - len(string)

    if spaces <= 0:
        return string
    
    spaces_before = spaces // 2
    spaces_after = spaces - spaces_before

    equalized_string = (" " * spaces_before) + string + (" " * spaces_after)

    return equalized_string

def space_string(string: str, length: int) -> str:
    spaces = length - len(string)

    if spaces <= 0:
        return string

    spaced_string = string + (" " * spaces)

    return spaced_string

def insert_string(original_string: str, string_to_insert: str, position: int) -> str:
    return original_string[:position] +\
        string_to_insert +\
        original_string[position:]

def create_bar(current: float | int, total: float | int, size: int = 20) -> tuple[str, str]:
    bar_size = int(
        (current / total) * size
    )

    if bar_size <= (total / 10):
        bar_size = 1

    bar = insert_string(
        equalize_string(
            f'{current}/{total}',
            size
        ),
        "|",
        bar_size
    )

    first_part, final_part = bar.split('|')

    return (first_part, final_part)
