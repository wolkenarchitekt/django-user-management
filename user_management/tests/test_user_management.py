import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture(scope="class")
def user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user = User.objects.create_user(username="testuser", email="testuser@test.com")
        user.save()
        return user


@pytest.fixture(scope="class")
def authenticated_client(django_db_setup, django_db_blocker, request, user):
    with django_db_blocker.unblock():
        client = APIClient()
        client.force_authenticate(user)
        request.cls.client = client


@pytest.mark.usefixtures("authenticated_client")
class TestUserManagement:
    @pytest.mark.django_db
    def test_get_users(self):
        url = reverse(viewname="users")
        response = self.client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "username,email",
        [("testuser1", "testemail1@test.de"), ("testuser2", "testemail2@test.de")],
    )
    def test_add_user(self, username, email):
        url = reverse(viewname="users")
        response = self.client.post(url, data={"username": username, "email": email})
        assert response.status_code == 200
        assert User.objects.exists()
