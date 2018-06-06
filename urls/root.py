from resolver import url, include

def test():
    pass

def test1():
    pass

urlpatterns = [
    url(r'^admin/$', test),
    url(r'^admin/(?P<name>\w+)/$', test1),
    url(r'^homepage/', include('child')),
]
