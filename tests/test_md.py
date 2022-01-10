import pytest

from autodesk_forge_sdk import ModelDerivativeClient, urnify


@pytest.fixture()
def client(token_provider):
    return ModelDerivativeClient(token_provider)


def test_urnify():
    urn = urnify("test")
    assert urn == "dGVzdA"


@pytest.mark.anyio
async def test_get_formats(client: ModelDerivativeClient):
    assert await client.get_formats()
