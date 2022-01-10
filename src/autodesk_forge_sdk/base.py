"""
Helper classes used by other API clients.
"""

from typing import Callable
import aiohttp


class BaseClient:
    """
    Base client for accessing web-based APIs.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url

    def _resolve_url(self, url: str) -> str:
        if url.startswith("/"):
            url = self.base_url + url
        return url

    async def _exec_and_content(
        self, func: Callable, *args, **kwargs
    ) -> aiohttp.ClientResponse:
        response = await func(*args, **kwargs)
        return await response.read()

    async def _exec_and_json(
        self, func: Callable, *args, **kwargs
    ) -> aiohttp.ClientResponse:
        response = await func(*args, **kwargs)
        return await response.json()

    async def _exec_and_text(
        self, func: Callable, *args, **kwargs
    ) -> aiohttp.ClientResponse:
        response = await func(*args, **kwargs)
        return await response.text()

    async def _request(self, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, self._resolve_url(url), **kwargs
            ) as response:
                response.raise_for_status()
                return response

    async def _head(self, url: str, **kwargs) -> aiohttp.ClientResponse:
        return await self._request("HEAD", url, **kwargs)

    async def _get(self, url: str, **kwargs) -> aiohttp.ClientResponse:
        return await self._request("GET", url, **kwargs)

    async def _post(self, url: str, **kwargs) -> aiohttp.ClientResponse:
        return await self._request("POST", url, **kwargs)

    async def _put(self, url: str, **kwargs) -> aiohttp.ClientResponse:
        return await self._request("PUT", url, **kwargs)

    async def _patch(self, url: str, **kwargs) -> aiohttp.ClientResponse:
        return await self._request("PATCH", url, **kwargs)

    async def _delete(self, url: str, **kwargs) -> aiohttp.ClientResponse:
        return await self._request("DELETE", url, **kwargs)
