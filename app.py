from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from controller import get_home_page, router

app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/templates", StaticFiles(directory="templates"), name="static")