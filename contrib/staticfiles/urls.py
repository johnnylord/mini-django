from urls.resolver import url
from . import views

urlpatterns = [
    url(r"^(?P<staticfile>.+)/$", views.serve_static),
]


