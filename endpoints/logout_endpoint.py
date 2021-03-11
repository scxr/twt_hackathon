from fastapi import APIRouter, Request, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import RedirectResponse
router = APIRouter()

@router.get('/logout')
async def logout(Authorise: AuthJWT = Depends()):
    Authorise.jwt_required()
    Authorise.unset_jwt_cookies()
    rr = RedirectResponse('/login')
    rr.set_cookie('access_token_cookie','')
    return rr
