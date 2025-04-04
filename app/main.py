from fastapi import FastAPI

from fastapi.responses import Response
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api import cypher_router
from app.api import signing_router


def import_routes(app: FastAPI):
    app.include_router(cypher_router)
    app.include_router(signing_router)


app = FastAPI(debug=True, title="take-home", openapi_url="/openapi.json")

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    """This handler ensures that exception are kept minimal to the status code.
    """
    return Response(None, status_code=exc.status_code)

import_routes(app)
