
from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


from app.auth.router import router as auth_router
from app.category.router import router as category_router

from app.core.exceptions import Unauthorized, Forbidden, NotFound, Conflict, BadRequest

app = FastAPI()

@app.exception_handler(Unauthorized)
async def unauthorized_exception_handler(request: Request, exc: Unauthorized):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=
        {
            "detail": str(exc),
        },
    )


@app.exception_handler(Forbidden)
async def forbidden_exception_handler(request: Request, exc: Forbidden):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=
        {
            "detail": str(exc),
        },
    )

@app.exception_handler(NotFound)
async def not_found_exception_handler(request: Request, exc: NotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=
        {
            "detail": str(exc),
        },
    )


@app.exception_handler(Conflict)
async def conflict_exception_handler(request: Request, exc: Conflict):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=
        {
            "detail": str(exc),
        },
    )

@app.exception_handler(BadRequest)
async def bad_request_exception_handler(request: Request, exc: BadRequest):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=
        {
            "detail": str(exc),
        },
    )



app.include_router(auth_router)
app.include_router(category_router)
