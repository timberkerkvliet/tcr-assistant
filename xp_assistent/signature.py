import dspy


class RefactorSignature(dspy.Signature):
    test_code = dspy.InputField(
        desc="A set of unit tests that describe the behaviour of the production code. The refactored code should still pass these test."
    )
    prod_code = dspy.InputField(
        desc="The production code that needs refactoring"
    )
    refactor_hint = dspy.InputField(
        desc="Refactor hint"
    )

    # OutputField defines what we expect the model to generate.
    python_code = dspy.OutputField(
        desc="The refactored production code",
        prefix="```python\n", # A prefix helps guide the model's output format.
        suffix="\n```"
    )

