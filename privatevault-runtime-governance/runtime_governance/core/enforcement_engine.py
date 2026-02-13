from runtime_governance.utils.hash import sha256_str

class EnforcementEngine:

    def __init__(self, policy_engine, ledger_repository, drift_service):
        self.policy_engine = policy_engine
        self.ledger_repository = ledger_repository
        self.drift_service = drift_service

    def evaluate(self, prompt, llm_result, principal):

        drift_result = self.drift_service.evaluate(
            prompt,
            llm_result["content"]
        )

        decision = self.policy_engine.evaluate(
            llm_result["content"],
            principal,
            drift_result
        )

        event_payload = {
            "prompt_hash": sha256_str(prompt),
            "response_hash": sha256_str(llm_result["content"]),
            "principal": principal,
            "model": llm_result["model"],
            "drift": drift_result,
            "decision": decision
        }

        self.ledger_repository.append(event_payload)

        return decision
