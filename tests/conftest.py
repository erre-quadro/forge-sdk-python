import pytest
import os

from autodesk_forge_sdk.auth import OAuthTokenProvider


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client_id():
    return os.environ["FORGE_CLIENT_ID"]


@pytest.fixture()
def client_secret():
    return os.environ["FORGE_CLIENT_SECRET"]


@pytest.fixture()
def bucket():
    return os.environ["FORGE_BUCKET"]


@pytest.fixture()
def token_provider(client_id: str, client_secret: str):
    return OAuthTokenProvider(client_id, client_secret)
