from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import LoginSerializer


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
    patient_service = None

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

        return Response(response, status=status.HTTP_201_CREATED)
