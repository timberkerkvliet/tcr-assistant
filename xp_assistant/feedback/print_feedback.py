from __future__ import annotations

from xp_assistant.feedback.feedback import FeedbackMechanism, Ok, NotOk


class PrintFeedback(FeedbackMechanism):
    def __init__(self, feedback_mechanism: FeedbackMechanism):
        self._feedback_mechanism = feedback_mechanism

    def get_description(self) -> str:
        return self._feedback_mechanism.get_description()

    def get_constraint(self) -> str:
        return self._feedback_mechanism.get_constraint()

    def get_feedback(self) -> Ok | NotOk:
        print(self._feedback_mechanism.get_description())

        result = self._feedback_mechanism.get_feedback()

        message = f'✅ {result.description}' if result.is_ok()  else f'❌ {result.why}'

        print(message)

        return result
