from typing import (
    Annotated,
    Any,
)
from fastapi import (
    APIRouter,
    Depends,
    Response,
    status
)
from app.services import SigningService

from .utils import check_json_body

router = APIRouter()

@router.post("/sign")
async def sign(body: Annotated[Any, Depends(check_json_body)]):
    return {"signature": SigningService.sign(body)}


@router.post("/verify", response_model=None)
async def verify(body: Annotated[Any, Depends(check_json_body)]):
    if isinstance(body, dict) and "signature" in body and "data" in body:
        if SigningService.verify(body["data"], body["signature"]):
            return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)
    return Response(content=None, status_code=status.HTTP_400_BAD_REQUEST)