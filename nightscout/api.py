import asyncio

import socket
from typing import Any, Mapping, Optional

import aiohttp
import async_timeout
from yarl import URL

from .models import GlucoseMonitor


class NS:
    def __init__(
        self,
        host: str,
        base_path: str = "/api/v1/entries/sgv",
        loop: asyncio.events.AbstractEventLoop = None,
        request_timeout: int = 3,
        session: aiohttp.client.ClientSession = None,
        query: str = "count=1",
        https: bool = True,
    ) -> None:
        """Init the connection."""
        self._loop = loop
        self._session = session
        self._close_session = False

        self.base_path = base_path
        self.host = host
        self.query = query
        self.request_timeout = request_timeout
        self.https = https

        if self.base_path[-1] != "/":
            self.base_path += "/"

    async def _request(
        self,
        uri: str = "",
        method: str = "GET",
        data: Optional[Any] = None,
        json_data: Optional[dict] = None,
        params: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """Handle a request."""
        scheme = "https" if self.https else "http"
        url = URL.build(
            scheme=scheme, host=self.host, path=self.base_path, query=self.query
        ).join(URL(uri))
        headers = {"content-type": "application/json", "accept": "application/json"}

        if self._loop is None:
            self._loop = asyncio.get_event_loop()

        if self._session is None:
            self._session = aiohttp.ClientSession(loop=self._loop)
            self._close_session = True

        try:
            with async_timeout.timeout(self.request_timeout):
                response = await self._session.request(
                    method,
                    url,
                    data=data,
                    json=json_data,
                    params=params,
                    headers=headers,
                )
        except asyncio.TimeoutError:
            print("Timeout occurred.")
        except (aiohttp.ClientError, socket.gaierror):
            print("Error occurred while communicating.")
        content_type = response.headers.get("Content-Type", "")

        if "application/json" in content_type:
            return await response.json()

        return await response.text()

    async def update(self) -> Optional[GlucoseMonitor]:
        """Get all information in a single call."""

        data = await self._request()
        self.glucose_info = GlucoseMonitor.from_dict(data)

        return self.glucose_info

    async def close(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> "NS":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()
