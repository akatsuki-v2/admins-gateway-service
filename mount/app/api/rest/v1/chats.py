from app.api.rest.context import RequestContext
from app.api.rest.gateway import forward_request
from app.api.rest.responses import Success
from app.models.chats import Chat
from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()

SERVICE_URL = "http://chat-service"


@router.get("/v1/chats/{chat_id}", response_model=Success[Chat])
async def get_chat(chat_id: int, ctx: RequestContext = Depends()):
    response = await forward_request(ctx,
                                     method="GET",
                                     url=f"{SERVICE_URL}/v1/chats/{chat_id}")
    return response


@router.get("/v1/chats", response_model=Success[Chat])
async def get_all_chats(ctx: RequestContext = Depends()):
    response = await forward_request(ctx,
                                     method="GET",
                                     url=f"{SERVICE_URL}/v1/chats")
    return response
