from __future__ import annotations

from tcr_assistant.feedback.feedback import FeedbackMechanism, Accepted, NotAccepted


class FeedbackChain(FeedbackMechanism):
    def __init__(self, mechanisms: list[FeedbackMechanism]):
        self._mechanisms = mechanisms

    def get_description(self) -> str:
        pass

    def get_constraint(self) -> str:
        return '\n'.join(mechanism.get_constraint() for mechanism in self._mechanisms)

    def get_feedback(self) -> Accepted | NotAccepted:
        for mechanism in self._mechanisms:
            result = mechanism.get_feedback()
            if not result.is_ok():
                return result

        return Accepted('all ok')
