# the structure path will return
# route : request url 
# view : function called to handle request
class urlResolver:
    def __init__(self, route, view):
        self.route = route
        self.view = view 


def path(route, view):
    return urlResolver(route, view)


def extractViewFromUrlPattern(urlPattern, route):
    route = parseRoute(route)
    for urlresolver in urlPattern:
        if urlresolver.route == route:
            return urlresolver.view
    return False


def parseRoute(originalRoute):
    location = "/"
    routeList = []
    if originalRoute is not None :
        routeList = originalRoute.split("/")
    for i in range(1, len(routeList)):
        location = location + routeList[i] + "/"
    return(location)
