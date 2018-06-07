from urls.resolver import RegexPattern

def static(static_url, view):
    static_rex = r"^%s" %static_url
    
    return RegexPattern(static_rex, view)