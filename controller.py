from fastapi import APIRouter
from service import AppService

router = APIRouter()
appService = AppService()


@router.get('/query')
def get_transaction_with_query(q: str = "", page: str = "1"):
    search_term = q
    search_page = int(page)
    return appService.get_transaction_with_query(search_term, search_page)