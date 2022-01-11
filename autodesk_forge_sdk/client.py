from typing import List
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
        headers = kwargs.setdefault("headers", {})
        if "region" in kwargs:
            headers["x-ads-region"] = kwargs["region"]
            del kwargs["region"]
        return await super()._fix_kwargs_for_headers(kwargs)

    async def _get_paginated(self, url: str, **kwargs) -> List:
        items = []
        should_stop = False
        while not should_stop:
            json = await self._req_json(self._get, url, **kwargs)
            new_items = json.get("data")
            if new_items is None:
                should_stop = True
                continue
            items.extend(new_items)
            links = json["links"]
            next = links.get("next")
            if next is None:
                should_stop = True
                continue
            url = next.get("href")
            if url is None:
                should_stop = True
                continue
        return items
