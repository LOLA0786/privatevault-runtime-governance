from sqlalchemy.orm import Session
from runtime_governance.ledger.models import LedgerEvent
from runtime_governance.utils.hash import sha256_str
from runtime_governance.ledger.merkle import compute_merkle_root
from runtime_governance.ledger.signature import sign_data
import json

class LedgerRepository:

    def __init__(self, db_session: Session):
        self.db = db_session

    def get_last_hash(self):
        last = self.db.query(LedgerEvent).order_by(LedgerEvent.id.desc()).first()
        return last.event_hash if last else "0" * 64

    def append(self, payload: dict):

        payload_str = json.dumps(payload, sort_keys=True)
        payload_hash = sha256_str(payload_str)

        previous_hash = self.get_last_hash()
        merkle_root = compute_merkle_root(previous_hash, payload_hash)

        event_hash = sha256_str(merkle_root)
        signature = sign_data(event_hash)

        event = LedgerEvent(
            event_hash=event_hash,
            previous_hash=previous_hash,
            merkle_root=merkle_root,
            signature=signature,
            payload=payload
        )

        self.db.add(event)
        self.db.commit()
