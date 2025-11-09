from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import CORS_ORIGINS
from .routers import public
app = FastAPI(title="Smart City NGSI-LD API")
app.add_middleware(CORSMiddleware, allow_origins=["*"] if "*" in CORS_ORIGINS else CORS_ORIGINS,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(public.router)
@app.get("/") async def root(): return {"service":"smartcity-ngsild-api","docs":"/docs"}
