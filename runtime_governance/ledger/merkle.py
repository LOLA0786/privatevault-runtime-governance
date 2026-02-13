from runtime_governance.utils.hash import sha256_str

def compute_merkle_root(previous_hash: str, payload_hash: str) -> str:
    combined = previous_hash + payload_hash
    return sha256_str(combined)
