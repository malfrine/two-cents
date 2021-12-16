from typing import Dict, Optional

import firebase_admin.auth as firebase_auth
from django.db.models import Model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.viewsets import ModelViewSet

from core.apps.users import utilities as user_utilities
from core.apps.users.models import User
from core.apps.users.serializers import UserWriteSerializer
from core.apps.users.utilities import delete_user


def delete_firebase_user_if_exists(email: str):
    try:
        firebase_user = firebase_auth.get_user_by_email(email=email)
        firebase_auth.delete_user(firebase_user.uid)
    except firebase_auth.UserNotFoundError:
        return


def delete_user_if_exists(email: str):
    try:
        user = User.objects.get(email__iexact=email)
        user.delete()
    except User.DoesNotExist:
        return


def create_user(
    email="test@email.ca", password="random_password", first_name="first name"
):
    # delete firebase user in case it already exists
    delete_user_if_exists(email)
    delete_firebase_user_if_exists(email)
    data = {"email": email, "password": password, "first_name": first_name}
    user = user_utilities.create_user(UserWriteSerializer(data=data))
    return user


class ModelCRUDTestCaseMixin:

    url = None
    model = None
    viewset = None

    PK_FIELD = "id"
    pk = None

    def setUp(self) -> None:
        self.user = create_user()
        self.factory = APIRequestFactory()
        assert isinstance(self.url, str), "URL must be of type string"
        assert issubclass(self.model, Model), "Model must inherit the Model class"
        assert issubclass(
            self.viewset, ModelViewSet
        ), "Viewset must inherit the Viewset class"

    def tearDown(self) -> None:
        delete_user(self.user)

    def get_create_data(self) -> Dict:
        raise NotImplementedError()

    def get_update_data(self) -> Dict:
        raise NotImplementedError()

    def set_pk(self, create_response: Response):
        print(f"setting primary key of {self.__class__}")
        print(create_response.data)
        self.pk = create_response.data[self.PK_FIELD]

    def get_obj(self):
        if self.pk is None:
            return None
        else:
            return self.model.objects.get(pk=self.pk)

    def create(self) -> Response:
        request = self.factory.post(
            self.url, data=self.get_create_data(), format="json"
        )
        force_authenticate(request, user=self.user)
        view = self.viewset.as_view({"post": "create"})
        response = view(request)
        return response

    def read(self) -> Response:
        request = self.factory.get(f"{self.url}{self.pk}", format="json")
        force_authenticate(request, user=self.user)
        view = self.viewset.as_view({"get": "retrieve"})
        response = view(request, pk=self.pk)
        return response

    def update(self) -> Response:
        request = self.factory.put(
            f"{self.url}{self.pk}", data=self.get_update_data(), format="json"
        )
        force_authenticate(request, user=self.user)
        view = self.viewset.as_view({"put": "update"})
        response = view(request, pk=self.pk)
        return response

    def delete(self) -> Response:
        request = self.factory.delete(f"{self.url}{self.pk}", format="json")
        force_authenticate(request, user=self.user)
        view = self.viewset.as_view({"delete": "destroy"})
        response = view(request, pk=self.pk)
        return response

    def run_create_assertions(self, response: Response):
        assert response.status_code == status.HTTP_201_CREATED, response.data
        assert self.PK_FIELD in response.data

    def run_read_assertions(self, response: Response):
        assert isinstance(self.get_obj(), self.model)

    def run_update_assertions(self, response: Response):
        assert response.status_code == status.HTTP_200_OK, response.data

    def run_delete_assertions(self, response: Optional[Response]):
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.data
        try:
            self.get_obj()
            assert False, f"{self.model} should not exist"
        except self.model.DoesNotExist:
            assert True

    def test_crud(self):
        create_response = self.create()
        self.run_create_assertions(create_response)
        self.set_pk(create_response)
        read_response = self.read()
        self.run_read_assertions(read_response)
        update_response = self.update()
        self.run_update_assertions(update_response)
        delete_response = self.delete()
        self.run_delete_assertions(delete_response)
