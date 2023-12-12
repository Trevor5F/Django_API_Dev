import pytest


@pytest.mark.django_db
def test_selection_create(client, user, ad, user_token):
    resp = client.post('/selection/create/',
                       {"name": "test",
                        "owner": user.pk,
                        "items": [ad.pk]},
                       content_type="application/json", HTTP_AUTHORIZATION="Bearer " + user_token)
    assert resp.status_code == 201
    assert resp.data == {"id": 1, "name": "test", "owner": user.pk, "items": [ad.pk]}