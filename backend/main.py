from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.routes import messages, threads, users

app = FastAPI(debug=True)

version_prefix = "/api/v1"

app.include_router(messages.router, prefix=version_prefix)

app.include_router(users.router, prefix=version_prefix)

app.include_router(threads.router, prefix=version_prefix)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
