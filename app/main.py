from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import transactions, watchlist, dashboard, banks
from app.bank_registry import seed_default_banks

app = FastAPI(title="FraudMesh")
app.include_router(banks.router)
app.include_router(transactions.router)
app.include_router(watchlist.router)
app.include_router(dashboard.router)


@app.on_event("startup")
def on_startup():
    seed_default_banks()


@app.get("/health")
def health():
    return {"status": "ok"}


# Serves app/static/index.html at "/" (and any other static assets).
# Mounted LAST so it never shadows the API routes registered above.
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")