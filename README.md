# FraudMesh

Privacy-preserving cross-institution fraud signal network (proof of concept).

## Run locally
    pip install -r requirements.txt
    uvicorn app.main:app --reload

## Run with Docker
    docker build -t fraudmesh .
    docker run -p 8000:8000 fraudmesh

## Seed demo data
    python scripts/seed_data.py

## Key endpoints
- POST /banks/{bank_id}/transactions
- GET  /banks/{bank_id}/watchlist
- GET  /dashboard/alerts
- GET  /health