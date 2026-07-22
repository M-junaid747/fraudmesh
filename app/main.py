from fastapi import FastAPI

app= FastAPI(name = "FraudMesh")

@app.get("/health")
def health():
    return {'status': 'ok'}