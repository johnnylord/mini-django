class Color:
    """Color inforamtion

    [Description]:
        Change the color of the displayed information by
    adding the color attribute before or after the displayed
    information.(e.g: Color.ERROR + message + Color.ENDC)
    """
    PURPLE = '\033[95m'     # Light Purple
    BLUE = '\033[94m'       # Light Blue
    GREEN = '\033[92m'      # Light Green
    YELLOW = '\033[93m'     # Light Yellow
    WARNING = '\033[93m'    # Light Yellow
    RED = '\033[91m'        # RED
    ERROR = '\033[91m'      # RED
    FAIL = '\033[91m'       # RED
    ENDC = '\033[0m'        # White
    BOLD = '\033[1m'        # Bold White
    UNDERLINE = '\033[4m'   # UNDERLINE

