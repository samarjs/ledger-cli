from colorama import init, Fore, Style

# Initialize colorama (makes colors work on Windows)
init(autoreset=True)

class Colors:
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    MAGENTA = Fore.MAGENTA
    WHITE = Fore.WHITE
    BRIGHT = Style.BRIGHT
    RESET = Style.RESET_ALL

def success(text):
    return f"{Colors.GREEN}{Colors.BRIGHT}{text}{Colors.RESET}"

def error(text):
    return f"{Colors.RED}{Colors.BRIGHT}{text}{Colors.RESET}"

def warning(text):
    return f"{Colors.YELLOW}{text}{Colors.RESET}"

def info(text):
    return f"{Colors.CYAN}{text}{Colors.RESET}"

def header(text):
    return f"{Colors.BLUE}{Colors.BRIGHT}{text}{Colors.RESET}"

def bold(text):
    return f"{Colors.BRIGHT}{text}{Colors.RESET}"