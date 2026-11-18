from fastapi import FastAPI

app = FastAPI(
    title='AI Customer Support Agent API',
    description='API for an e-commerce support agent',
    version='0.1.0'
)

@app.get('/health')
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "customer-support-api"
    }