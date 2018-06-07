from urls.resolver import url
from template.shortcuts import render

def index(request):
	return render(request,"./test.html",{'name':'eric','numbers':[1,2]})


urlpatterns = [
    url(r"/index/$", index),
]
