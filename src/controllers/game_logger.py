Colors = {
    "RESET"           : 0,
    "BOLD"            : 1,
    
    "BLACK"           : 30,
    "RED"             : 31,
    "GREEN"           : 32,
    "YELLOW"          : 33,
    "BLUE"            : 34,
    "MAGENTA"         : 35,
    "CYAN"            : 36,
    "WHITE"           : 37,

    "BG_BLACK"        : 40,
    "BG_RED"          : 41,
    "BG_GREEN"        : 42,
    "BG_YELLOW"       : 43,
    "BG_BLUE"         : 44,
    "BG_MAGENTA"      : 45,
    "BG_CYAN"         : 46,
    "BG_WHITE"        : 47,

    "LIGHTBLACK_EX"   : 90,
    "LIGHTRED_EX"     : 91,
    "LIGHTGREEN_EX"   : 92,
    "LIGHTYELLOW_EX"  : 93,
    "LIGHTBLUE_EX"    : 94,
    "LIGHTMAGENTA_EX" : 95,
    "LIGHTCYAN_EX"    : 96,
    "LIGHTWHITE_EX"   : 97
}

def replaceColors(string: str):
    newString = string

    for key, value in Colors.items():
        newString = newString.replace(f'&{key.lower()}', f'\033[{value}m')
    
    return newString

class GameLogger:
    '''
        Send messages to console with some colors.
    '''

    @staticmethod
    def input(string: str) -> str:
        result = input(f'{replaceColors(string)}')
        print(f'\033[{Colors.get('RESET')}m', end='')
        return result

    @staticmethod
    def print(string: str) -> None:
        print(f'{replaceColors(string)}\033[{Colors.get('RESET')}m')

    @staticmethod
    def loading(string: str) -> None:
        print(f'\033[{Colors.get('WHITE')}m{string}\033[{Colors.get('RESET')}m')

    @staticmethod
    def success(string: str) -> None:
        print(f'\033[{Colors.get('GREEN')}m{string}\033[{Colors.get('RESET')}m')

    @staticmethod
    def warn(string: str) -> None:
        print(f'\033[{Colors.get('YELLOW')}m{string}\033[{Colors.get('RESET')}m')

    @staticmethod
    def error(string: str) -> None:
        print(f'\033[{Colors.get('RED')}m{string}\033[{Colors.get('RESET')}m')
