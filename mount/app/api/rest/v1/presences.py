from uuid import UUID

from app.api.rest.context import RequestContext
from app.api.rest.gateway import authenticate
from app.api.rest.gateway import forward_request
from app.api.rest.responses import Success
from app.models.presences import Presence
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials as HTTPCredentials
from fastapi.security import HTTPBearer

router = APIRouter()

SERVICE_URL = "http://users-service"

oauth2_scheme = HTTPBearer()


# https://osuakatsuki.atlassian.net/browse/V2-116
@router.get("/v1/presences/{session_id}", response_model=Success[Presence])
async def get_presence(session_id: UUID, token: HTTPCredentials = Depends(oauth2_scheme),
                       ctx: RequestContext = Depends()):
    session = await authenticate(ctx, token.credentials)

    response = await forward_request(ctx,
                                     method="GET",
                                     url=f"{SERVICE_URL}/v1/presences/{session_id}")
    return response


# https://osuakatsuki.atlassian.net/browse/V2-116
@router.get("/v1/presences", response_model=Success[list[Presence]])
async def get_presences(token: HTTPCredentials = Depends(oauth2_scheme),
                        ctx: RequestContext = Depends()):
    session = await authenticate(ctx, token.credentials)

    response = await forward_request(ctx,
                                     method="GET",
                                     url=f"{SERVICE_URL}/v1/presences")
    return response
