import json

import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response


class BaseService:
    def _get_response(self, url, headers=None, params=None):
        response = requests.get(url, headers=headers, params=params)

        return response.json()

    def _post_response(self, url, data, headers=None):
        response = requests.post(url, json=data, headers=headers)

        return response.json()

    def _patch_response(self, url, data=None, files=None, headers=None):
        response = requests.patch(url, data=data, files=files, headers=headers)

        return response.json()

    def _delete_response(self, url, data=None, headers=None):
        response = requests.delete(url, json=data, headers=headers)

        return response.json()


class DoctorService(BaseService):
    def _import_settings(self):
        self.url = settings.DOCTOR_SERVICE_URL

    def __init__(self):
        self._import_settings()

    def list_doctors(self, request, params=None):
        response = self._get_response(self.url, params=params)

        return response


class PatientService(BaseService):
    def _import_settings(self):
        self.url = settings.PATIENT_SERVICE_URL

    def __init__(self):
        self._import_settings()
        self.patient_url = self.url + "/patient/"
        self.patient_from_logged_user = self.url + "/patient_from_logged_user/"
        self.appointment_url = self.url + "/appointment/"

    def list_patients(self, request, params=None):
        response = self._get_response(self.patient_url, params=params)

        return response

    def get_patient_from_logged_user(self, request):
        response = self._get_response(self.patient_from_logged_user)

        return response

    def get_patient_by_user_id(self, request, pk):
        response = self._get_response(
            f"{self.patient_url}{pk}",
        )

        return response

    def create_patient(self, request):
        response = self._post_response(
            self.url,
            request.data,
        )

        return response
