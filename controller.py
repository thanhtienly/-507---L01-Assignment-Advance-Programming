import json
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request

from modules.redis import RedisService
from service import AppService

router = APIRouter()
templates = Jinja2Templates(directory="templates")
appService = AppService()

# Define the path operation decorator
@router.get("/")
def get_home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    

@router.get('/query')
def get_transaction_with_query(amount: str = "", message : str = "", next_cursor: str = ""):
    return appService.get_transaction_with_query(amount, message, next_cursor)