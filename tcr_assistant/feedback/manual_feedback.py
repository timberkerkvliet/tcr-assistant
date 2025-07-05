from __future__ import annotations

from xp_assistant.feedback.feedback import FeedbackMechanism, Accepted, NotAccepted


class ManualFeedback(FeedbackMechanism):
    def get_feedback(self) -> Accepted | NotAccepted:
        approve = input("\nDo you approve these changes? (y/n): ").strip().lower()
        if approve == "y":
            return Accepted('Manually approved')

        why = input("\nWhy is it not ok?: ").strip().lower()

        return NotAccepted(why)
