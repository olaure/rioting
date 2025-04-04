from typing import (
    Annotated,
    Any,
)
from fastapi import (
    APIRouter,
    Depends,
)

from app.services.cypher import CypherService
from .utils import check_json_body

router = APIRouter()

@router.post("/encrypt")
async def encrypt(body: Annotated[Any, Depends(check_json_body)]):
    return CypherService.encrypt_message(body)

@router.post("/decrypt")
async def decrypt(body: Annotated[Any, Depends(check_json_body)]):
    return CypherService.decrypt_message(body)
