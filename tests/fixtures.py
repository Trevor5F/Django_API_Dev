import pytest


@pytest.fixture
@pytest.mark.django_db
def user_token(client, django_user_model):
    username = "test_user"
    password = "testpassword"
    email = "test@testdomen.ru"

    django_user_model.objects.create_user(
        username=username,
        password=password,
        email=email,
        role="admin")

    response = client.post(
        "/user/token/",
        {"username": username, "password": password},
        content_type="application/json")

    return response.data['access']
