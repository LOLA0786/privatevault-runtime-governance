import requests, uuid

cases = [
    ("ALLOW", 5000, "domestic transfer"),
    ("FLAG", 45000, "new beneficiary"),
    ("BLOCK", 900000, "offshore transfer")
]

for expected, amount, reason in cases:
    trace_id = str(uuid.uuid4())

    payload = {
        "trace_id": trace_id,
        "action": "money_transfer",
        "amount": amount,
        "reason": reason
    }

    r = requests.post(
        "http://localhost:8000/evaluate",
        headers={
            "Content-Type": "application/json",
            "Idempotency-Key": trace_id
        },
        json=payload
    )

    print("\n====================")
    print(f"AMOUNT: ₹{amount}")
    print(f"SCENARIO: {reason}")
    print("EXPECTED POLICY:", expected)
    print("TRACE ID:", trace_id)
    print("GOVERNANCE DECISION:", r.text)
