from typing import Any
from fastapi import(
    HTTPException,
    Request,
    status,
)


async def check_json_body(request: Request) -> Any:
    try:
        return await request.json()
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=None)
