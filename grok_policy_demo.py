import requests, uuid, os

API_KEY = os.getenv("GROK_API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

cases = [
    ("₹5,000 domestic transfer"),
    ("₹45,000 transfer to new beneficiary"),
    ("₹9,00,000 transfer to offshore account")
]

for case in cases:
    trace_id = str(uuid.uuid4())

    prompt = f"""
Classify the financial risk of this transaction and respond with one word:
ALLOW, FLAG, or BLOCK.

Transaction: {case}
"""

    payload = {
        "model": "grok-4",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }

    r = requests.post(
        "https://api.x.ai/v1/chat/completions",
        headers=headers,
        json=payload,
    )

    ai_decision = r.json()["choices"][0]["message"]["content"].strip()

    print("\n======================")
    print("TRANSACTION:", case)
    print("AI RISK CLASSIFICATION:", ai_decision)
    print("TRACE ID:", trace_id)

    gov = requests.post(
        "http://localhost:8000/evaluate",
        headers={
            "Content-Type": "application/json",
            "Idempotency-Key": trace_id
        },
        json={
            "trace_id": trace_id,
            "transaction": case,
            "ai_decision": ai_decision
        }
    )

    print("GOVERNANCE ENFORCEMENT:", gov.text)
