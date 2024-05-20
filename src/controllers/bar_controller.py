from src.utils.string_manipulation import equalize_string, insert_string

def createBar(current: float | int, total: float | int, color: str, size: int = 20):
    bar_size = int(
        (current / total) * size
    )

    bar = insert_string(
        equalize_string(
            f'{current}/{total}',
            size
        ),
        "&reset",
        bar_size
    )

    return f'&reset&black[&bg_{color}' +\
        bar +\
        '&reset&black]&reset'