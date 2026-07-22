from fastapi import FastAPI
from app.routers import transactions

app = FastAPI(title="FraudMesh")
app.include_router(transactions.router)


@app.get("/health")
def health():
    return {"status": "ok"}