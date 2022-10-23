from app.api.rest.context import RequestContext
from app.api.rest.gateway import authenticate
from app.api.rest.gateway import forward_request
from app.api.rest.responses import Success
from app.models.clans import Clan
from app.models.clans import CreateClan
from app.models.clans import UpdateClan
from app.models.sessions import Session
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials as HTTPCredentials
from fastapi.security import HTTPBearer

router = APIRouter()

SERVICE_URL = "http://clans-service"


oauth2_scheme = HTTPBearer()


# https://osuakatsuki.atlassian.net/browse/V2-20
@router.post("/v1/clans", response_model=Success[Clan])
async def create_clan(args: CreateClan,
                      token: HTTPCredentials = Depends(oauth2_scheme),
                      ctx: RequestContext = Depends()):
    session = await authenticate(ctx, token.credentials)

    response = await forward_request(ctx,
                                     method="POST",
                                     url=f"{SERVICE_URL}/v1/clans",
                                     json=args.dict())
    return response


# https://osuakatsuki.atlassian.net/browse/V2-21
@router.get("/v1/clans/{clan_id}", response_model=Success[Clan])
async def get_clan(clan_id: int,
                   token: HTTPCredentials = Depends(oauth2_scheme),
                   ctx: RequestContext = Depends()):
    session = await authenticate(ctx, token.credentials)

    response = await forward_request(ctx,
                                     method="GET",
                                     url=f"{SERVICE_URL}/v1/clans/{clan_id}")
    return response


# https://osuakatsuki.atlassian.net/browse/V2-113
@router.get("/v1/clans", response_model=Success[list[Clan]])
async def get_all_clans(ctx: RequestContext = Depends()):
    response = await forward_request(ctx,
                                     method="GET",
                                     url=f"{SERVICE_URL}/v1/clans")
    return response


# https://osuakatsuki.atlassian.net/browse/V2-64
@router.patch("/v1/clans/{clan_id}", response_model=Success[Clan])
async def partial_update_clan(clan_id: int, args: UpdateClan,
                              token: HTTPCredentials = Depends(oauth2_scheme),
                              ctx: RequestContext = Depends()):
    session = await authenticate(ctx, token.credentials)

    response = await forward_request(ctx,
                                     method="PATCH",
                                     url=f"{SERVICE_URL}/v1/clans/{clan_id}",
                                     json=args.dict())
    return response


# https://osuakatsuki.atlassian.net/browse/V2-23
@router.delete("/v1/clans/{clan_id}", response_model=Success[Clan])
async def disband_clan(clan_id: int,
                       token: HTTPCredentials = Depends(oauth2_scheme),
                       ctx: RequestContext = Depends()):
    session = await authenticate(ctx, token.credentials)

    response = await forward_request(ctx,
                                     method="DELETE",
                                     url=f"{SERVICE_URL}/v1/clans/{clan_id}")
    return response
