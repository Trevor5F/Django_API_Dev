import pytest

@pytest.mark.django_db
def test_ad_create(client, user, category):
    data = {
        "name": "Продам что-то",
        "author_id": user.pk,
        "price": 4000,
        "description": "",
        "is_published": False,
        "category_id": category.pk,
        "image": None,
    }
    resp = client.post("/ad/create/", data, content_type="application/json")

    assert resp.status_code == 200
