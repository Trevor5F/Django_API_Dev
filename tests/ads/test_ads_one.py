import pytest

from ads.serializers.ad import AdDetailSerializer


@pytest.mark.django_db
def test_ads_detail(client, ad, user_token):
    resp = client.get(f"/ad/{ad.id}/", content_type="application/json", HTTP_AUTHORIZATION="Bearer " + user_token)
    assert resp.status_code == 200
    assert resp.data == AdDetailSerializer(ad).data