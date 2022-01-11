"""
Helper classes used by other API clients.
"""

from typing import Coroutine
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

    async def _req_content(
        self, req: Coroutine, *args, **kwargs
    ) -> aiohttp.ClientResponse:
        response = await req(*args, **kwargs)
        return response._body

    async def _req_json(
        self, req: Coroutine, *args, **kwargs
    ) -> aiohttp.ClientResponse:
        response = await req(*args, **kwargs)
        return await response.json()

    async def _req_text(
        self, req: Coroutine, *args, **kwargs
    ) -> aiohttp.ClientResponse:
        response = await req(*args, **kwargs)
        return await response.text()

    async def _request(self, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
        params = kwargs.get("params")
        if params is not None:
            kwargs["params"] = _fix_params(params)
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, self._resolve_url(url), **kwargs
            ) as response:
                response.raise_for_status()
                await response.read()
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


def _fix_params(params):
    for k, v in {**params}.items():
        if isinstance(v, bool):
            params[k] = "true" if v else "false"
    return params
