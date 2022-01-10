from autodesk_forge_sdk.auth import BaseOAuthClient, TokenProviderInterface
from enum import Enum


class Region(str, Enum):
    US = "US"
    EMEA = "EMEA"


class ForgeClient(BaseOAuthClient):
    """
    Forge base class for API clients with authentication and headers.
    """

    def __init__(self, token_provider: TokenProviderInterface, base_url: str):
        BaseOAuthClient.__init__(self, token_provider, base_url)

    async def _fix_kwargs_for_headers(self, kwargs):
        if "region" in kwargs:
            if "headers" not in kwargs:
                kwargs["headers"] = {}
            kwargs["x-ads-region"] = kwargs["region"]
            del kwargs["region"]
        return await super()._fix_kwargs_for_headers(kwargs)
