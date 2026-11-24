from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from support_agent.api.orders import router as orders_router

app = FastAPI(
    title="AI Customer Support Agent API",
    description="API for an e-commerce support agent",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(orders_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "customer-support-api"}
