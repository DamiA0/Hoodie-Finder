from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import analyse, health

app = FastAPI(title="Hoodie Finder")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(analyse.router, prefix="/api")