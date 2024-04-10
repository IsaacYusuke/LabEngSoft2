from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Roles
from .serializers import LoginSerializer
from .services import AuthenticationService, PatientService


class TokenRefreshView(ModelViewSet):
    permission_classes = [AllowAny]
    authentication_service: AuthenticationService = None

    def get(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        access = self.authentication_service.refresh(refresh_token)
        access_expiration = self.authentication_service.get_token_utc_expiration(access)
        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(
            "access_token",
            access.token,
            expires=access_expiration,
            httponly=True,
        )
        return response


class LoginView(ModelViewSet):
    permission_classes = [AllowAny]
    authentication_service: AuthenticationService = None

    def post(self, request):
        serialized_data = LoginSerializer(data=request.data)
        if not serialized_data.is_valid():
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

        auth_response = self.authentication_service.access(serialized_data.validated_data)

        response = self.authentication_service.set_authentication_cookies(
            Response(status=status.HTTP_200_OK), auth_response
        )

        return response


class LogoutView(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserView(ModelViewSet):
    authentication_service: AuthenticationService = None
    patient_service: PatientService = None

    def _register_in_authentication_service(self, request_data):
        data = {
            "email": request_data.get("email"),
            "first_name": request_data.get("first_name"),
            "last_name": request_data.get("last_name"),
            "role": request_data.get("role"),
        }

        response = self.authentication_service.register(data)

        return response

    def register(self, request):
        authentication_service_response = self._register_in_authentication_service(request.data)
        if not status.is_success(authentication_service_response.status_code):
            return authentication_service_response

        user_role = request.data.get("role")

        if user_role == Roles.PATIENT:
            user = authentication_service_response.data
            data = {
                "id_user": user.id,
                "first_name": request.data.get("first_name"),
                "last_name": request.data.get("last_name"),
                "birth_date": request.data.get("birth_date"),
                "email": request.data.get("email"),
                "phone_number": request.data.get("phone_number"),
                "cpf": request.data.get("cpf"),
                "address": request.data.get("address"),
                "gender": request.data.get("gender"),
            }

            response = self.patient_service.create_patient(request, data)

            return Response(response.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        response = self.authentication_service.list(request, params=request.query_params)

        return Response(response.data, status=status.HTTP_200_OK)

    def retrieve_self(self, request):
        response = self.authentication_service.retrieve_self(request)

        return Response(response.data, status=status.HTTP_200_OK)

    def retrieve_basic_info_by_id(self, request, pk):
        response = self.authentication_service.retrieve_basic_info_by_id(request, pk)

        return Response(response.data, status=status.HTTP_200_OK)


class PatientView(ModelViewSet):
    patient_service: PatientService = None
    permission_classes = [IsAuthenticated]

    def list(self, request):
        response = self.patient_service.list_patients(request, request.query_params)

        return Response(response.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        response = self.patient_service.get_patient(request, pk)

        return Response(response.data, status=status.HTTP_200_OK)

    def get_from_logged_user(self, request):
        response = self.patient_service.get_patient_from_logged_user(request)

        return Response(response.data, status=status.HTTP_200_OK)

    def create(self, request):
        response = self.patient_service.create_patient(request, request.data)

        return Response(response.data, status=status.HTTP_201_CREATED)


class AppointmentView(ModelViewSet):
    patient_service: PatientService = None
    doctor_service = None
    personal_trainer_service = None
    psychologist_service = None
    nutritionist_service = None

    permission_classes = [IsAuthenticated]

    def retrieve_patient_appointment(self, request, pk):
        patient_service_response = self.patient_service.get_appointment_from_id(request, pk)
        if patient_service_response.status != status.HTTP_200_OK:
            return Response(patient_service_response.errors, status=patient_service_response.status)

        # TODO: identificar serviço do profissional pelo ID do user
        professional_service_response = None
        if professional_service_response.status != status.HTTP_200_OK:
            return Response(professional_service_response.errors, status=professional_service_response.status)

        data = {
            "professional": {
                "type": professional_service_response.data.type,
                "address": professional_service_response.data.address,
                "first_name": professional_service_response.data.first_name,
                "last_name": professional_service_response.data.last_name,
            },
            "scheduled_date": patient_service_response.data.datetime,
            "is_online": patient_service_response.data.is_online,
        }

        return Response(data, status=status.HTTP_200_OK)

    def list_patient_appointments(self, request):
        response = self.patient_service.list_appointments_from_user(request)

        return Response(response.data, status=status.HTTP_200_OK)

    def create(self, request):
        # TODO: criar instância da consulta no serviço do profissional

        patient_service_data = {
            "id_user_professional": request.data.id_user_professional,
            "datetime": request.data.datetime,
            "is_online": request.data.is_online,
        }

        patient_service_response = self.patient_service.create_appointment(request, patient_service_data)
        if patient_service_response.status != status.HTTP_201_CREATED:
            return Response(patient_service_response.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_201_CREATED)

    def list_appointments_from_professional_id(self, request, id_user_professional):
        response = self.patient_service.list_appointments_from_professional_id(request, id_user_professional)

        return Response(response.data, status=status.HTTP_200_OK)
