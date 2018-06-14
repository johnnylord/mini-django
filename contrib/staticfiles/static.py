from urls.resolver import RegexPattern

def static(static_url, view):
    """Generate a RegexPattern and link to view of static app

    [Keyword arguments]:
    static_url --- STATIC_URL in settings
    view --- function in contrib.staticfiles.views to process static request 

    [Return]:
    RegexPattern object
    """
    static_rex = r"^%s" %static_url
    return RegexPattern(static_rex, view)