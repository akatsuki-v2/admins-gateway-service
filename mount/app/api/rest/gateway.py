from typing import Any
from typing import Literal
from uuid import UUID

from app.common import json as jsonlib
from app.common import settings
from app.common.context import Context
from app.models.sessions import Session
from fastapi import HTTPException
from fastapi import Response
from httpx._types import CookieTypes
from httpx._types import HeaderTypes
from httpx._types import QueryParamTypes
from httpx._types import RequestContent
from httpx._types import RequestData
from httpx._types import RequestFiles
from httpx._types import URLTypes
from shared_modules import logger
MethodTypes = Literal["POST", "PUT", "PATCH",
                      "GET", "HEAD", "DELETE", "OPTIONS"]


# TODO: read & implement things from
# https://www.python-httpx.org/advanced


async def authenticate(ctx: Context, session_id: UUID | str) -> Session:
    response = await ctx.http_client.patch(
        url=f"http://admins-service/v1/sessions/{session_id}",
        json={"ttl": settings.AUTH_SESSION_DURATION},
    )
    response_data = response.json()
    if response.status_code != 200:
        logger.error("Failed to authenticate request",
                     status_code=response.status_code,
                     response_data=response_data)
        raise HTTPException(status_code=response.status_code,
                            detail=response_data)

    return Session(**response_data["data"])


async def forward_request(ctx: Context,
                          method: MethodTypes,
                          url: URLTypes,
                          content: RequestContent | None = None,
                          data: RequestData | None = None,
                          files: RequestFiles | None = None,
                          json: Any | None = None,
                          params: QueryParamTypes | None = None,
                          headers: HeaderTypes | None = None,
                          cookies: CookieTypes | None = None,
                          ) -> Response:
    if json is not None:
        json = jsonlib._default_processor(json)

    logger.info("Forwarding HTTP request", method=method, url=url)

    response = await ctx.http_client.request(method=method,
                                             content=content,
                                             data=data,
                                             url=url,
                                             files=files,
                                             json=json,
                                             params=params,
                                             headers=headers,
                                             cookies=cookies)

    if response.status_code >= 500:
        logger.error("Core service internal server error",
                     method=method,
                     url=url,
                     status_code=response.status_code,
                     response_data=response.json())  # TODO: aread?

    return Response(content=response.content,
                    status_code=response.status_code,
                    headers=response.headers)
