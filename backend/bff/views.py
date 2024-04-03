from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import LoginSerializer
from .services import PatientService


class LoginView(ModelViewSet):
    permission_classes = [AllowAny]

    # Nome da funcao pode mudar, so precisa alterar no arquivo urls.py
    def post(self, request):
        serialized_data = LoginSerializer(data=request.data)

        if not serialized_data.is_valid():
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

        # Colocar aqui processamento especifico da View

        return Response(data=None, status=status.HTTP_200_OK)


class PatientView(ModelViewSet):
    patient_service: PatientService = None

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
