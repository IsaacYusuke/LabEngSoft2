from django.urls import path

from .views import DoctorView, LoginView

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(actions={"post": "post"}),
    ),
    path("doctor/", DoctorView.as_view(actions={"get": "list"})),
]
