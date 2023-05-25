import os
from typing import Optional
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)

from routers import users, images, institutions, logs
from mongoengine import connect, disconnect
from helpers.settings import MONGODB_URI

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "*"
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(exc)
    #print(f"OMG! An HTTP error!: {exc}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(exc)
    #print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)

@app.on_event("startup")
async def create_db_client():
    # start client here and reuse in future requests
    connect(host=MONGODB_URI, retryWrites=False)

@app.on_event("shutdown")
async def shutdown_db_client():
    # stop your client here
    disconnect()


@app.get("/")
def read_root():
    return {"status": "OK"}


app.include_router(institutions.router)
app.include_router(users.router)
app.include_router(images.router)
app.include_router(logs.router)