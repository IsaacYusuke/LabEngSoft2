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
