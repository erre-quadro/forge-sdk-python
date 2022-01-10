import pytest

from autodesk_forge_sdk import AuthenticationClient, Scope, get_authorization_url


def test_authorization_url(client_id: str):
    assert get_authorization_url(
        client_id,
        "code",
        "http://foo.bar",
        [Scope.VIEWABLES_READ, Scope.USER_READ],
        "random state",
    )


@pytest.mark.anyio
async def test_authenticate(client_id: str, client_secret: str):
    client = AuthenticationClient()
    token = await client.authenticate(
        client_id,
        client_secret,
        [Scope.VIEWABLES_READ, Scope.USER_READ],
    )
    assert token["access_token"]
