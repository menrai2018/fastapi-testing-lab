from fastapi import FastAPI
from app.routers import product_router

app = FastAPI(
    title="Product API",
    description="FastAPI service for software testing lab",
    version="1.0.0",
)

app.include_router(product_router.router)

@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok", "version": "1.0.0"}