# route is the path we get from url , view is the function we will return to
# base
class urlResolver:
    def __init__(self, route, view):
        self.route = route
        self.view = view 


def path(route, view):
    return urlResolver(route, view)


def index():
    return "<html><body>Hello</body></html>"


urlPattern = [
    path("/index/",index),
]


#def render():
     


def extractViewFromUrlPattern(urlPattern, route):
    route = parseRoute(route)
    #print("route is ",route)
    for urlresolver in urlPattern:
        if urlresolver.route == route:
            return urlresolver.view

    #print("view Function not found")    
    return False


#because incoming path will include http://localhost
def parseRoute(originalRoute):
    location = "/"
    routeList = []
    if originalRoute is not None :
        routeList = originalRoute.split("/")

    for i in range(1, len(routeList)):
        location = location + routeList[i] + "/"
    return(location)
