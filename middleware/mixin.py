class MiddlewareMixin:
    """The class that every middleware must hierarchy"""
    def __init__(self, get_response=None):
        """Accepts get_response argument and stores

        [Keyword argument]:
        get_response ---  later middleware or the view

        [Attribute]:
        get_response ---  to get the response from later middleware or the view.
        """
        self.get_response = get_response
        super().__init__()

    def __call__(self, request):
        """Call process_request, get_response, process_response user defined

        [Keyword argument]:
        request --- the WSGIRequest object that passed from WSGIHandler

        [Return]:
        response --- the WSGIResponse object
        """
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if response is None:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response
