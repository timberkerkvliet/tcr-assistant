import dspy


class RefactorSignature(dspy.Signature):
    test_code = dspy.InputField(
        desc="A set of unit tests"
    )
    prod_code = dspy.InputField(
        desc="The production component"
    )
    refactor_hint = dspy.InputField(
        desc="Refactor hint"
    )

    # OutputField defines what we expect the model to generate.
    python_code = dspy.OutputField(
        desc="The generated Python code.",
        prefix="```python\n", # A prefix helps guide the model's output format.
        suffix="\n```"
    )

