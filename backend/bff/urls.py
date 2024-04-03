from django.urls import path

from .views import AppointmentView, LoginView, PatientView

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(actions={"post": "post"}),
    ),
    path("patient/", PatientView.as_view(actions={"get": "list", "post": "create"})),
    path("patient/<int:pk>/", PatientView.as_view(actions={"get": "retrieve"})),
    path("patient/profile/", PatientView.as_view(actions={"get": "get_from_logged_user"})),
    path("appointment/", AppointmentView.as_view(actions={"post": "create"})),
    path("patient/appointments/", AppointmentView.as_view(actions={"get": "list_patient_appointments"})),
    path("patient/appointments/<int:pk>/", AppointmentView.as_view(actions={"get": "retrieve_patient_appointment"})),
]
