class Color:
    """
    Give output text color.
    ex:
        print(Color.HEADER, "hello world", Color.ENDC)
    """
    PURPLE = '\033[95m'     # Light Purple
    BLUE = '\033[94m'       # Light Blue
    GREEN = '\033[92m'      # Light Green
    YELLOW = '\033[93m'     # Light Yellow
    WARNING = '\033[93m'    # Light Yellow
    RED = '\033[91m'        # RED
    FAIL = '\033[91m'       # RED
    ENDC = '\033[0m'        # White
    BOLD = '\033[1m'        # Bold White
    UNDERLINE = '\033[4m'   # UNDERLINE

