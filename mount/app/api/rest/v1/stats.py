from app.api.rest.context import RequestContext
from app.api.rest.gateway import authenticate
from app.api.rest.gateway import forward_request
from app.api.rest.responses import Success
from app.models.stats import Stats
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPBearer

router = APIRouter()

SERVICE_URL = "http://users-service"

oauth2_scheme = HTTPBearer()


# https://osuakatsuki.atlassian.net/browse/V2-78
@router.get("/v1/accounts/{account_id}/stats", response_model=Success[list[Stats]])
async def get_stats(account_id: int,
                    ctx: RequestContext = Depends()):
    response = await forward_request(ctx,
                                     method="GET",
                                     url=f"{SERVICE_URL}/v1/accounts/{account_id}/stats")
    return response
