import pytest

pytestmark = pytest.mark.django_db


def test_simple(client):
    response = client.get('/')
    assert response.status_code == 200
