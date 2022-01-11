import pytest

from autodesk_forge_sdk import OSSClient
from autodesk_forge_sdk.auth import OAuthTokenProvider
from autodesk_forge_sdk.dm import DataManagementClient, ProjectManagementClient


@pytest.fixture()
def oss_client(token_provider: OAuthTokenProvider):
    return OSSClient(token_provider)


@pytest.fixture()
def pm_client(token_provider: OAuthTokenProvider):
    return ProjectManagementClient(token_provider)


@pytest.fixture()
def dm_client(token_provider: OAuthTokenProvider):
    return DataManagementClient(token_provider)


@pytest.mark.anyio
async def test_get_buckets(oss_client: OSSClient):
    page = await oss_client.get_buckets(limit=2)
    assert "items" in page
    assert len(page["items"]) <= 2


@pytest.mark.anyio
async def test_get_all_buckets(oss_client: OSSClient):
    assert await oss_client.get_all_buckets() is not None


@pytest.mark.anyio
async def test_get_bucket_details(oss_client: OSSClient, forge_bucket: str):
    details = oss_client.get_bucket_details(forge_bucket)
    assert "bucketKey" in details


@pytest.mark.anyio
async def test_get_objects(oss_client: OSSClient, forge_bucket: str):
    page = await oss_client.get_objects(forge_bucket, limit=2)
    assert "items" in page
    assert len(page["items"]) <= 2


@pytest.mark.anyio
async def test_get_all_objects(oss_client: OSSClient, forge_bucket: str):
    assert await oss_client.get_all_objects(forge_bucket)


@pytest.mark.anyio
async def test_upload_object_buff(oss_client: OSSClient, forge_bucket: str):
    buff = bytes("This is a test...", "utf-8")
    assert await oss_client.upload_object(forge_bucket, "unittest.txt", buff)


@pytest.mark.anyio
async def test_upload_object_file(oss_client: OSSClient, forge_bucket: str):
    with open(__file__, "rb") as file:
        assert await oss_client.upload_object(forge_bucket, "unittest.py", file)


@pytest.mark.anyio
async def test_get_all_hubs(pm_client: ProjectManagementClient):
    assert await pm_client.get_all_hubs() is not None
