def check_size(n: int, min_n: int, max_n: int) -> int:
    return max(min_n, min(n, max_n))


def in_size(n: int, min_n: int, max_n: int) -> bool:
    return n >= min_n and n <= max_n
