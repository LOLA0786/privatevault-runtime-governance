from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

@app.post("/evaluate")
def evaluate(request: dict, idempotency_key: str = Header(None)):
    if not idempotency_key:
        raise HTTPException(status_code=400, detail="Missing Idempotency-Key")

    return {"status": "runtime governance placeholder"}
