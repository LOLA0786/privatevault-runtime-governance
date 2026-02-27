import requests
import uuid
import os

GROK_API_KEY = os.getenv("GROK_API_KEY")

prompt = "Explain how AI governance prevents financial fraud in one paragraph."

headers = {
    "Authorization": f"Bearer {GROK_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "grok-4-latest",
    "messages": [
        {"role": "user", "content": prompt}
    ]
}

resp = requests.post(
    "https://api.x.ai/v1/chat/completions",
    headers=headers,
    json=payload,
)

data = resp.json()
response_text = data["choices"][0]["message"]["content"]

trace_id = str(uuid.uuid4())

print("\n=== PROMPT ===\n", prompt)
print("\n=== GROK RESPONSE ===\n", response_text)
print("\n=== TRACE ID ===\n", trace_id)

# send to governance layer
gov = requests.post(
    "http://localhost:8000/evaluate",
    headers={
        "Content-Type": "application/json",
        "Idempotency-Key": trace_id
    },
    json={
        "trace_id": trace_id,
        "model": "grok",
        "response": response_text
    }
)

print("\n=== GOVERNANCE RESPONSE ===\n", gov.text)
