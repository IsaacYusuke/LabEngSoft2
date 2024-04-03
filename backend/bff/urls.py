from django.urls import path

from .services import AuthenticationService, PatientService
from .views import AppointmentView, LoginView, LogoutView, PatientView, TokenRefreshView, UserView

urlpatterns = [
    path(
        "token/refresh",
        TokenRefreshView.as_view(actions={"get": "get"}, authentication_service=AuthenticationService()),
    ),
    path("login/", LoginView.as_view(actions={"post": "post"}, authentication_service=AuthenticationService())),
    path("logout/", LogoutView.as_view(actions={"post": "post"}, authentication_service=AuthenticationService())),
    path(
        "register/",
        UserView.as_view(
            actions={"post": "register"},
            authentication_service=AuthenticationService(),
            patient_service=PatientService(),
        ),
    ),
    path(
        "user/",
        UserView.as_view(
            actions={"get": "list"},
            authentication_service=AuthenticationService(),
        ),
    ),
    path(
        "user/self/",
        UserView.as_view(
            actions={"get": "retrieve_self"},
            authentication_service=AuthenticationService(),
        ),
    ),
    path(
        "user/<int:pk>/",
        UserView.as_view(
            actions={"get": "retrieve_basic_info_by_id"},
            authentication_service=AuthenticationService(),
        ),
    ),
    path("patient/", PatientView.as_view(actions={"get": "list"}, patient_service=PatientService())),
    path("patient/<int:pk>/", PatientView.as_view(actions={"get": "retrieve"}, patient_service=PatientService())),
    path(
        "patient/profile/",
        PatientView.as_view(actions={"get": "get_from_logged_user"}, patient_service=PatientService()),
    ),
    path("appointment/", AppointmentView.as_view(actions={"post": "create"}, patient_service=PatientService())),
    path(
        "patient/appointments/",
        AppointmentView.as_view(actions={"get": "list_patient_appointments"}, patient_service=PatientService()),
    ),
    path(
        "patient/appointments/<int:pk>/",
        AppointmentView.as_view(actions={"get": "retrieve_patient_appointment"}, patient_service=PatientService()),
    ),
]
