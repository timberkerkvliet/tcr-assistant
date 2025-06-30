import dspy

from xp_assistant.feedback.feedback import FeedbackMechanism
from xp_assistant.signature import ChangeExistingCode


class ChangeCodeIterator:
    def __init__(self, feedback: FeedbackMechanism, target_path: str, main_goal: str):
        self._feedback = feedback
        self._target_path = target_path
        self._main_goal = main_goal

    def run(self) -> bool:
        extra_constraints = []

        while True:
            with open(self._target_path) as f:
                prod_code = f.read()

            code_generator = dspy.Predict(ChangeExistingCode)

            res = code_generator(
                current_code=prod_code,
                main_goal=self._main_goal,
                constraints=self._feedback.get_constraint() + '\n'.join(extra_constraints)
            )

            with open(self._target_path, 'wb') as f:
                f.write(res.python_code.encode())

            res = self._feedback.get_feedback()

            if res.is_ok():
                return True

            extra_constraints.append(res.why)
