from resolver import url

def test2():
    pass

urlpatterns = [
   url(r'^name/(?P<name2>\w+)/$', test2),
]
