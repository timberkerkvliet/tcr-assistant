import dspy



class ChangeExistingCode(dspy.Signature):
    current_code = dspy.InputField(
        desc="The code that need to be changed"
    )

    main_goal = dspy.InputField(desc="The main goal of the change")

    constraints = dspy.InputField(desc="Everything the output code needs to satisfy")

    python_code = dspy.OutputField(
        desc="The output code",
        prefix="```python\n", # A prefix helps guide the model's output format.
        suffix="\n```"
    )


class CreateNewCode(dspy.Signature):
    main_goal = dspy.InputField(desc="The main goal of the code")

    constraints = dspy.InputField(desc="Everything the output code needs to satisfy")

    python_code = dspy.OutputField(
        desc="The output code",
        prefix="```python\n", # A prefix helps guide the model's output format.
        suffix="\n```"
    )
