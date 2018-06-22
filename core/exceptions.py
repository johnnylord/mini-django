

class Error(Exception):
    pass

class DisallowedRedirect(Error):

    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message

class Http404(Error):
    
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message