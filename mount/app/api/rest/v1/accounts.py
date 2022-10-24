from app.api.rest.context import RequestContext
from app.api.rest.gateway import authenticate
from app.api.rest.gateway import forward_request
from app.api.rest.responses import Success
from app.models import Status
from app.models.accounts import Account
from app.models.accounts import AccountUpdate
from app.models.accounts import SignupForm
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials as HTTPCredentials
from fastapi.security import HTTPBearer

router = APIRouter()

SERVICE_URL = "http://users-service"

oauth2_scheme = HTTPBearer()


@router.post("/v1/accounts", response_model=Success[Account])
async def sign_up(args: SignupForm, ctx: RequestContext = Depends()):
    response = await forward_request(ctx,
                                     method="POST",
                                     url=f"{SERVICE_URL}/v1/accounts",
                                     json=args.dict())
    return response


@router.get("/v1/accounts", response_model=Success[list[Account]])
async def get_accounts(country: str | None = None,
                       status: Status | None = Status.ACTIVE,
                       ctx: RequestContext = Depends()):
    response = await forward_request(ctx,
                                     method="GET",
                                     url=f"{SERVICE_URL}/v1/accounts",
                                     params={"country": country,
                                             "status": status})
    return response


@router.get("/v1/accounts/{account_id}", response_model=Success[Account])
async def get_account(account_id: int, ctx: RequestContext = Depends()):
    response = await forward_request(ctx,
                                     method="GET",
                                     url=f"{SERVICE_URL}/v1/accounts/{account_id}")
    return response


@router.patch("/v1/accounts/{account_id}", response_model=Success[Account])
async def partial_update_account(account_id: int,
                                 args: AccountUpdate,
                                 token: HTTPCredentials = Depends(
                                     oauth2_scheme),
                                 ctx: RequestContext = Depends()):
    session = await authenticate(ctx, token.credentials)

    response = await forward_request(ctx,
                                     method="PATCH",
                                     url=f"{SERVICE_URL}/v1/accounts/{account_id}",
                                     json=args.dict())
    return response


@router.delete("/v1/accounts/{account_id}", response_model=Success[Account])
async def delete_account(account_id: int,
                         token: HTTPCredentials = Depends(oauth2_scheme),
                         ctx: RequestContext = Depends()):
    session = await authenticate(ctx, token.credentials)

    response = await forward_request(ctx,
                                     method="DELETE",
                                     url=f"{SERVICE_URL}/v1/accounts/{account_id}")
    return response
