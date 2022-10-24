from uuid import UUID

from app.api.rest.context import RequestContext
from app.api.rest.gateway import authenticate
from app.api.rest.gateway import forward_request
from app.api.rest.responses import Success
from app.models.queued_packets import EnqueuePacket
from app.models.queued_packets import QueuedPacket
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials as HTTPCredentials
from fastapi.security import HTTPBearer

router = APIRouter()

SERVICE_URL = "http://users-service"

oauth2_scheme = HTTPBearer()


@router.post("/v1/sessions/{session_id}/queued-packets",
             response_model=Success[QueuedPacket])
async def create_queued_packet(session_id: UUID, args: EnqueuePacket,
                               token: HTTPCredentials = Depends(oauth2_scheme),
                               ctx: RequestContext = Depends()):
    session = await authenticate(ctx, token.credentials)

    response = await forward_request(ctx,
                                     method="POST",
                                     url=f"{SERVICE_URL}/v1/sessions/{session_id}/queued-packets",
                                     json=args.dict())
    return response


@router.get("/v1/sessions/{session_id}/queued-packets",
            response_model=Success[list[QueuedPacket]])
async def get_queued_packets(session_id: UUID,
                             token: HTTPCredentials = Depends(oauth2_scheme),
                             ctx: RequestContext = Depends()):
    session = await authenticate(ctx, token.credentials)

    response = await forward_request(ctx,
                                     method="GET",
                                     url=f"{SERVICE_URL}/v1/sessions/{session_id}/queued-packets")
    return response
