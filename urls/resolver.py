import sys
import re
from importlib import import_module

class UrlResolver(object):
    """Help resolve the url routing task
    
    [Public methods]:
    resolve_url --- resolve the url routing task

    [Description]:
        help user resolve the url routing task. Find the associated
    view handler for sepcific url.
    """

    def __init__(self, url_config_path):
        """Construct a urlResolver with a specific urlpatterns list

        [Keyword argument]:
        url_config_path --- the path to the module containing 'urlpatterns'
                            list, which store the essential information of
                            url routing task.
        [Attributes]:
        urlpatterns --- a list containing the information of url routing.
                        e.g: regex --> view
        """
        try:
            # Dynamically import the module based on the path
            url_config = import_module(url_config_path)

            # load the urlpatterns from the url_config module
            self.urlpatterns = getattr(url_config, 'urlpatterns')
        except:
            raise

    def resolve_url(self, path):
        """Resolve the url and return the view handler

        [Keyword arguments]:
        path --- the url path to resolve.

        [Return]:
        args --- the arguments which will pass to view later
        kwargs --- the keyword argument which will pass to view later
        view --- the handler to process the request

        [Description]:
            Based on the 'path', find the associated view handler.
        """
        urlpatterns = self.urlpatterns
        
        # args and kwargs which will pass to view handler later
        view_args = []
        view_kwargs = {}

        # Iterate through the regex pattern object in the urlpatterns
        for regex_pattern in urlpatterns:
            (args, kwargs, sub_path, view) = regex_pattern.resolve_path(path)

            # Update the args and kwargs
            if args:
                view_args = view_args + args
            if kwargs:
                view_kwargs.update(kwargs)

            if view and sub_path:
                # If sub_path is not empty, then the view must be another
                # UrlResolver object, which will process the sub_path further
                another_resolver = view
                (args, kwargs, view) = another_resolver.resolve_url(sub_path)

                # update the args and kwargs from another urlresolver
                if args:
                    view_args = view_args + args
                if kwargs:
                    view_kwargs.update(kwargs)

                # return (args, kwargs, view) from another urlresolver
                return view_args, view_kwargs, view
            elif view and not sub_path:
                # If sub_path is empty, then the view function is found
                return view_args, view_kwargs, view
            else:
                # Keep finding matching regex pattern
                pass
        
        # There is no matching.
        return (None, None, None)


class RegexPattern(object):
    """A one-to-one mapping between a url regex and a view handler

    [Public methods]:
    resolve_path --- try to match the url path, and return
                    the registered view handler.

    [Description]:
        Keep the relationship between a url regex and a view handler,
    which will be refered by urlresolver later.
    """

    def __init__(self, regex, view):
        """Construct the mapping of url regex and view handler

        [Keyword arguments]:
        regex --- the regular expression for a specific url pattern
        view --- the view handler

        [Attributes]:
        regex --- compiled regular expression object
        view --- the view handler
        """
        self.regex = re.compile(regex)
        self.view = view

    def resolve_path(self, path):
        """Resolve the url path

        [Keyword arguments]:
        path --- the url path inforamtion

        [Return]:
        args --- the arguments matched in regex
        kwargs --- the keyword arguments matched in regex
        sub_path --- the remaining path
        view --- the object registered on the regex

        [Description]:
            Try to match the path with the regex. If matched, return 
        the view handler and some accompany information, otherwise return
        the original information.
        """
        match = self.regex.search(path)
 
        if match:
            kwargs = match.groupdict()
            args = [] if kwargs else match.groups()
            return args, kwargs, path[match.end():], self.view
        return (None, None, path, None)
            

def url(regex, view):
    """Helper function to construct a RegexPattern object
    
    [Keyword arguments]:
    regex --- the regular expression specification
    view --- the handler object

    [Return]
    a RegexPattern object
    """
    return RegexPattern(regex, view)

def include(url_config_path):
    """Helper function to construct a UrlResolver object
    
    [Keyword arguments]:
    url_config_path --- the path to the module containg urlpatterns
                        variable.

    [Return]
    a UrlResolver object
    """
    return UrlResolver(url_config_path)


if __name__ == '__main__':

    resolver = UrlResolver('root')

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
