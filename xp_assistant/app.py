import os

import dspy

from xp_assistant.signature import RefactorSignature

api_key = os.environ["OPENAI_KEY"]
gemini = dspy.LM(model='openai/gpt-4o-mini', api_key=api_key)
dspy.configure(lm=gemini)

code_generator = dspy.Predict(RefactorSignature)

PROJECT_DIR = '/Users/timberkerkvliet/PycharmProjects/fibonacci'
TEST_FILE = 'fibonacci/test_fibonacci.py'
PROD_FILE = 'fibonacci/fibo.py'

while True:
    refactor_hint = input("Refactor hint: ")
    with open(f'{PROJECT_DIR}/{TEST_FILE}') as f:
        test_code = f.read()

    with open(f'{PROJECT_DIR}/{PROD_FILE}') as f:
        prod_code = f.read()

    res = code_generator(test_code=test_code, prod_code=prod_code, refactor_hint=refactor_hint)

    with open(f'{PROJECT_DIR}/{PROD_FILE}', 'wb') as f:
        f.write(res.python_code.encode())

    exit_code = os.system(f"cd {PROJECT_DIR} && python -m unittest {TEST_FILE}")

    if exit_code == 0:
        print("✅ Tests passed.\n")

        # Ask for approval
        approve = input("\nDo you want to commit these changes? (y/n): ").strip().lower()
        if approve == "y":
            os.system(f'cd {PROJECT_DIR} && git commit -am "Passing tests"')
            print("✅ Changes committed.")
        else:
            os.system(f"cd {PROJECT_DIR} && git reset --hard")
            print("❌ Changes reverted.")
    else:
        print("❌ Tests failed. Reverting changes...")
        os.system(f"cd {PROJECT_DIR} && git reset --hard")
