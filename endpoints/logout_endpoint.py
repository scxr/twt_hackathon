from fastapi import APIRouter, Request, Depends
from fastapi_jwt_auth import AuthJWT

router = APIRouter()

@router.get('/logout')
async def logout(Authorise: AuthJWT = Depends()):
    Authorise.jwt_required()
    Authorise.unset_jwt_cookies()
    return 'ok'
