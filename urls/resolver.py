import sys
import re
from importlib import import_module

class UrlResolver(object):
    """
    Based on urlpatterns in the url_config module.
    resolve the url mapping problem.
    """

    def __init__(self, url_config_path):
        """
        'self.urlpatterns':
            a list of url pattern with each entry associated with a handler
        """
        url_config = import_module(url_config_path)

        try:
            # load the urlpatterns from the url_config module
            self.urlpatterns = getattr(url_config, 'urlpatterns')
        except AttributeError as e:
            print(str(e)) 
            sys.exit(1)

    def resolve_url(self, path):
        """
        Based on the parameter 'path', return a specific view function along with
        args, kwargs which would be passed to view function later.
        """
        urlpatterns = self.urlpatterns
        view_args = []
        view_kwargs = {}

        # Iterate through the regex pattern object in the urlpatterns
        for regex_pattern in urlpatterns:
            (args, kwargs, remain_path, view) = regex_pattern.resolve_path(path)

            # Update the args and kwargs
            if args:
                view_args = view_args + args
            if kwargs:
                view_kwargs.update(kwargs)

            if view and remain_path:
                # If remain_path is not empty, then the view must be a UrlResolver object
                # Call another UrlResolver to resolve the remaining_url
                (args, kwargs, view) = view.resolve_url(remain_path)

                # update the args and kwargs from another urlresolver
                if args:
                    view_args = view_args + args
                if kwargs:
                    view_kwargs.update(kwargs)

                # return (args, kwargs, view) from another urlresolver
                return view_args, view_kwargs, view
        
            elif view and not remain_path:
                # If remain_path is empty, then the view function is found
                return view_args, view_kwargs, view
            else:
                # Keep searching matching pattern
                pass
        
        # There is no matching.
        return (None, None, None)


class RegexPattern(object):
    """
    A one-to-one relationship between a url regex and a view handler
    """

    def __init__(self, regex, view):
        """
        'self.regex': the regular expression for a specific url pattern
        'self.view': the view handler
        """
        self.regex = re.compile(regex)
        self.view = view

    def resolve_path(self, path):
        match = self.regex.search(path)
 
        if match:
            kwargs = match.groupdict()
            args = [] if kwargs else match.groups()
            return args, kwargs, path[match.end():], self.view
        return (None, None, path, None)
            

def url(url_pattern, view):
    """
    helper function to construct a RegexPattern object
    """
    return RegexPattern(url_pattern, view)

def include(url_config_path):
    """
    helper function to construct a UrlResolver object
    """
    return UrlResolver(url_config_path)


if __name__ == '__main__':

    resolver = UrlResolver('urls')

    case0 = 'null/'
    case1 = 'admin/'
    case2 = 'admin/johnnylord/'
    case3 = 'homepage/name/johnnylord/'

    print("Case0: %r" % case0)
    print(resolver.resolve_url(case0))
    print("Case1: %r" % case1)
    print(resolver.resolve_url(case1))
    print("Case2: %r" % case2)
    print(resolver.resolve_url(case2))
    print("Case3: %r" % case3)
    print(resolver.resolve_url(case3))
