from uuid import UUID

from app.api.rest.context import RequestContext
from app.api.rest.gateway import authenticate
from app.api.rest.gateway import forward_request
from app.api.rest.responses import Success
from app.models.sessions import LoginForm
from app.models.sessions import Session
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials as HTTPCredentials
from fastapi.security import HTTPBearer

router = APIRouter()

SERVICE_URL = "http://users-service"

oauth2_scheme = HTTPBearer()


# https://osuakatsuki.atlassian.net/browse/V2-11
@router.post("/v1/sessions", response_model=Success[Session])
async def log_in(args: LoginForm, ctx: RequestContext = Depends()):
    response = await forward_request(ctx,
                                     method="POST",
                                     url=f"{SERVICE_URL}/v1/sessions",
                                     json=args.dict())
    return response


# https://osuakatsuki.atlassian.net/browse/V2-12
@router.patch("/v1/sessions/{session_id}")
async def partial_update_session(session_id: UUID,
                                 token: HTTPCredentials = Depends(
                                     oauth2_scheme),
                                 ctx: RequestContext = Depends()):
    session = await authenticate(ctx, token.credentials)

    response = await forward_request(ctx,
                                     method="PATCH",
                                     url=f"{SERVICE_URL}/v1/sessions/{session_id}")
    return response


# https://osuakatsuki.atlassian.net/browse/V2-13
@router.delete("/v1/sessions/{session_id}")
async def log_out(session_id: UUID,
                  token: HTTPCredentials = Depends(oauth2_scheme),
                  ctx: RequestContext = Depends()):
    session = await authenticate(ctx, token.credentials)

    response = await forward_request(ctx,
                                     method="DELETE",
                                     url=f"{SERVICE_URL}/v1/sessions/{session_id}")
    return response
