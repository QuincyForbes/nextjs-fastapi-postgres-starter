from fastapi import FastAPI
from api.v1.views import messages, threads, users
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(messages.router, prefix="/api/v1")

app.include_router(users.router, prefix="/api/v1")

app.include_router(threads.router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
