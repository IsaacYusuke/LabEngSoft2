import datetime as dt
import json

import requests
from django.conf import settings
from django.utils.module_loading import import_string


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
    
    def _put_response(self, url, data=None, files=None, headers=None):
        response = requests.put(url, data=data, files=files, headers=headers)

        return response.json()

    def _delete_response(self, url, data=None, headers=None):
        response = requests.delete(url, json=data, headers=headers)

        return response.json()


class AuthenticatedService(BaseService):
    def get_auth_header(self, request=None, auth_token=None):
        if request and request.auth:
            return {"Authorization": f"Bearer {request.auth.token}"}
        if auth_token:
            return {"Authorization": f"Bearer {auth_token}"}
        return {"Authorization": ""}


class AuthenticationService(AuthenticatedService):
    def _import_settings(self):
        self.url = settings.AUTHENTICATION_SERVICE_URL
        custom_auth_settings = settings.CUSTOM_AUTHENTICATION_SETTINGS
        self.token_classes = {
            "access": import_string(custom_auth_settings.get("AUTH_TOKEN_CLASS")),
            "refresh": import_string(custom_auth_settings.get("REFRESH_TOKEN_CLASS")),
        }

    def __init__(self):
        self._import_settings()
        self.token_url = self.url + "/token/"
        self.refresh_token_url = self.url + "/token/refresh/"
        self.register_url = self.url + "/register/"
        self.user_url = self.url + "/user/"
        self.user_self_url = self.url + "/user/self/"

    def _get_from_raw_token(self, raw_token, token_type):
        Token = self.token_classes[token_type]
        return Token(raw_token)

    def _get_from_json(self, json_value, token_type):
        raw_token = json_value.get(token_type)
        return self._get_from_raw_token(raw_token, token_type)

    def access(self, data):
        response = self._get_valid_post_response(self.token_url, data)

        access_token = self._get_from_json(response, self.access_typename)
        refresh_token = self._get_from_json(response, self.refresh_typename)

        tokens = {self.access_typename: access_token, self.refresh_typename: refresh_token}

        return tokens

    def refresh(self, refresh_token):
        data = {"refresh": refresh_token}

        response = self._get_valid_post_response(self.refresh_url, data)
        access_token = self._get_from_json(response, self.access_typename)

        return access_token

    def get_token_utc_expiration(self, token):
        return dt.datetime.utcfromtimestamp(token["exp"])

    def register(self, data):
        response = self._post_response(self.register_url, data)

        return response

    def list(self, request, params=None):
        response = self._get_response(self.user_url, params=params, headers=self.get_auth_header(request=request))

        return response

    def retrieve_self(self, request):
        response = self._get_response(self.user_self_url, headers=self.get_auth_header(request=request))

        return response

    def retrieve_basic_info_by_id(self, request, pk):
        response = self._get_response(f"{self.user_url}{pk}/", headers=self.get_auth_header(request=request))

        return response

    def set_authentication_cookies(self, response, auth):
        access = auth.get("access")
        access_expiration = self.get_token_utc_expiration(access)
        refresh = auth.get("refresh")
        refresh_expiration = self.get_token_utc_expiration(refresh)

        response.set_cookie(
            "access_token",
            access.token,
            expires=access_expiration,
            httponly=True,
        )
        response.set_cookie(
            "refresh_token",
            refresh.token,
            expires=refresh_expiration,
            httponly=True,
        )
        return response


class DoctorService(BaseService):
    def _import_settings(self):
        self.url = settings.DOCTOR_SERVICE_URL

    def __init__(self):
        self._import_settings()

    def list_doctors(self, request, params=None):
        response = self._get_response(self.url, params=params)

        return response


class PatientService(AuthenticatedService):
    def _import_settings(self):
        self.url = settings.PATIENT_SERVICE_URL

    def __init__(self):
        self._import_settings()
        self.patient_url = self.url + "/patient/"
        self.patient_from_logged_user = self.url + "/patient_from_logged_user/"
        self.appointment_url = self.url + "/appointment/"
        self.appointment_from_professional_id = self.url + "/appointment_from_professional_id/"

    def list_patients(self, request, params=None):
        response = self._get_response(self.patient_url, params=params, headers=self.get_auth_header(request=request))

        return response

    def get_patient_from_logged_user(self, request):
        response = self._get_response(self.patient_from_logged_user, headers=self.get_auth_header(request=request))

        return response

    def get_patient_by_user_id(self, request, pk):
        response = self._get_response(f"{self.patient_url}{pk}", headers=self.get_auth_header(request=request))

        return response

    def create_patient(self, request, data):
        response = self._post_response(self.patient_url, data, headers=self.get_auth_header(request=request))

        return response

    def list_appointments_from_user(self, request):
        response = self._get_response(self.appointment_url, headers=self.get_auth_header(request=request))

        return response

    def get_appointment_from_id(self, request, pk):
        response = self._get_response(f"{self.appointment_url}{pk}", headers=self.get_auth_header(request=request))

        return response

    def create_appointment(self, request, data):
        response = self._post_response(self.appointment_url, data, headers=self.get_auth_header(request=request))

        return response

    def cancel_appointment(self, request, pk):
        response = self._patch_response(
            f"{self.appointment_url}{pk}/cancel/", headers=self.get_auth_header(request=request)
        )

        return response

    def list_appointments_from_professional_id(self, request, id_user_professional):
        response = self._get_response(
            f"{self.appointment_from_professional_id}{id_user_professional}/",
            headers=self.get_auth_header(request=request),
        )

        return response

class NutritionistService(AuthenticatedService):
    def _import_settings(self):
        self.url = settings.NUTRITIONIST_SERVICE_URL

    def __init__(self):
        self._import_settings()
        self.nutritionist_url = self.url + "/nutritionist/"
        self.evaluation_url = self.url + "/evaluation/"
        self.evaluation_from_patient = self.url + "/evaluation_from_patient/"
        self.evolution_url = self.url + "/evolution/"
        self.evolution_from_patient = self.url + "/evolution_from_patient/"
        self.diet_url = self.url + "/diet/"
        self.diet_from_patient = self.url + "/diet_from_patient/"

    def create_nutritionist(self, request, data):
        response = self._post_response(self.nutritionist_url, data, headers=self.get_auth_header(request=request))
        
        return response
    
    def retrieve_nutritionist(self, request, pk):
        response = self._get_response(f"{self.nutritionist_url}{pk}/", headers=self.get_auth_header(request=request))

        return response
    
    def list_all_nutritionist (self, request, params=None):
        response = self._get_response(self.nutritionist_url, params=params, headers=self.get_auth_header(request=request))

        return response
    
    def create_evaluation (self, request, data):
        response = self._post_response(self.evaluation_url, data, headers=self.get_auth_header(request=request))

        return response
    
    def retrieve_evaluation  (self, request, pk):
        response = self._get_response(f"{self.evaluation_url}{pk}/", headers=self.get_auth_header(request=request))

        return response
    
    def list_all_evaluation (self, request, params=None):
        response = self._get_response(self.evaluation_url, params=params, headers=self.get_auth_header(request=request))

        return response
    
    def delete_evaluation(self, request, pk):
        response = self._delete_response(f"{self.evaluation_url}{pk}/", headers=self.get_auth_header(request=request))

        return response
    
    def list_evaluation_from_patient_id(self, request, pk):
        response = self._get_response(
            f"{self.evaluation_from_patient}{pk}/",
            headers=self.get_auth_header(request=request),
        )

        return response

    def create_evolution (self, request, data):
        response = self._post_response(self.evolution_url, data, headers=self.get_auth_header(request=request))

        return response
    
    def update_evolution (self, request, pk):
        response = self._put_response(
            f"{self.evolution_url}{pk}", headers=self.get_auth_header(request=request)
        )

        return response
    
    def retrieve_evolution  (self, request, pk):
        response = self._get_response(f"{self.evolution_url}{pk}/", headers=self.get_auth_header(request=request))

        return response
    
    def list_all_evolution (self, request, params=None):
        response = self._get_response(self.evolution_url, params=params, headers=self.get_auth_header(request=request))

        return response
    
    def list_evolution_from_patient_id(self, request, pk):
        response = self._get_response(
            f"{self.evolution_from_patient}{pk}/",
            headers=self.get_auth_header(request=request),
        )

        return response
    
    def create_diet (self, request, data):
        response = self._post_response(self.diet_url, data, headers=self.get_auth_header(request=request))

        return response
    
    def retrieve_diet  (self, request, pk):
        response = self._get_response(f"{self.diet_url}{pk}/", headers=self.get_auth_header(request=request))

        return response
    
    def list_all_diet (self, request, params=None):
        response = self._get_response(self.diet_url, params=params, headers=self.get_auth_header(request=request))

        return response
    
    def delete_diet(self, request, pk):
        response = self._delete_response(f"{self.diet_url}{pk}/", headers=self.get_auth_header(request=request))

        return response
    
    def list_diet_from_patient_id(self, request, pk):
        response = self._get_response(
            f"{self.diet_from_patient}{pk}/",
            headers=self.get_auth_header(request=request),
        )

        return response

    

