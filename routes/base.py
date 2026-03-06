from fastapi import FastAPI, APIRouter
import os

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)


@base_router.get("/")
async def welcome_message():
    app_name = os.getenv("APP_NAME")
    return {"message": f"Welcome to the {app_name}!"}
