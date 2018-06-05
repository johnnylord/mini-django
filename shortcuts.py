from template.html import HtmlTemplite
from mini_http.response import HttpResponse
import os.path

def render(request , template_name , context = None , context_type = None ,status = None):
    """
    Return a HttpResponse whose content is filled with html file content that is compiled by template engine
    """
    if os.path.isfile(template_name) is False:
        pass
    else:
        if context_type is None:
            context_type = "text/html"

        content = HtmlTemplite(template_name).render(context)
        return HttpResponse(content,context_type,status)
