from fastapi import FastAPI
from app.routers import transactions, watchlist

app = FastAPI(title="FraudMesh")
app.include_router(transactions.router)
app.include_router(watchlist.router)


@app.get("/health")
def health():
    return {"status": "ok"}