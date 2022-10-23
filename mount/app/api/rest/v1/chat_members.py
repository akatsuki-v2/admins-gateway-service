from app.api.rest.context import RequestContext
from app.api.rest.gateway import authenticate
from app.api.rest.gateway import forward_request
from app.api.rest.responses import Success
from app.models.chat_members import Member
from app.models.chat_members import MemberInput
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials as HTTPCredentials
from fastapi.security import HTTPBearer

router = APIRouter()

SERVICE_URL = "http://chat-service"

oauth2_scheme = HTTPBearer()


# https://osuakatsuki.atlassian.net/browse/V2-86
@router.post("/v1/chats/{chat_id}/members", response_model=Success[Member])
async def join_chat(chat_id: int, args: MemberInput,
                    token: HTTPCredentials = Depends(oauth2_scheme),
                    ctx: RequestContext = Depends()):
    session = await authenticate(ctx, token.credentials)

    response = await forward_request(ctx,
                                     method="POST",
                                     url=f"{SERVICE_URL}/v1/chats/{chat_id}/members",
                                     json=args.dict())
    return response


# https://osuakatsuki.atlassian.net/browse/V2-87
@router.delete("/v1/chats/{chat_id}/members", response_model=Success[Member])
async def leave_chat(chat_id: int,
                     token: HTTPCredentials = Depends(oauth2_scheme),
                     ctx: RequestContext = Depends()):
    session = await authenticate(ctx, token.credentials)

    response = await forward_request(ctx,
                                     method="DELETE",
                                     url=f"{SERVICE_URL}/v1/chats/{chat_id}/members")
    return response


# https://osuakatsuki.atlassian.net/browse/V2-88
@router.get("/v1/chats/{chat_id}/members", response_model=Success[list[Member]])
async def get_chat_members(chat_id: int,
                           token: HTTPCredentials = Depends(oauth2_scheme),
                           ctx: RequestContext = Depends()):
    # TODO: should this not be authenticated?
    session = await authenticate(ctx, token.credentials)

    response = await forward_request(ctx,
                                     method="GET",
                                     url=f"{SERVICE_URL}/v1/chats/{chat_id}/members")
    return response
