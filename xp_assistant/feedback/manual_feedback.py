from __future__ import annotations

from xp_assistant.feedback.feedback import FeedbackMechanism, Ok, NotOk


class ManualFeedback(FeedbackMechanism):
    def get_description(self) -> str:
        return 'Manual approval'

    def get_constraint(self) -> str:
        return ''

    def get_feedback(self) -> Ok | NotOk:
        approve = input("\nDo you approve these changes? (y/n): ").strip().lower()
        if approve == "y":
            return Ok('Manually approved')

        why = input("\nWhy is it not ok? (y/n): ").strip().lower()

        return NotOk(why)
