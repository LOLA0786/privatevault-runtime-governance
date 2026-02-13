class IdempotencyService:

    def __init__(self, repository):
        self.repository = repository

    def check_and_store(self, key: str):
        if self.repository.exists(key):
            raise Exception("Duplicate idempotency key")

        self.repository.store(key)
