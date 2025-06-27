import os

import dspy

from xp_assistent.signature import RefactorSignature

api_key = os.environ["OPENAI_KEY"]
gemini = dspy.LM(model='openai/gpt-4o-mini', api_key=api_key)
dspy.configure(lm=gemini)

code_generator = dspy.Predict(RefactorSignature)

with open('test_code/test_fibonacci.py') as f:
    test_code = f.read()

with open('test_code/fibo.py') as f:
    prod_code = f.read()

res = code_generator(test_code=test_code, prod_code=prod_code, refactor_hint='Clean up')

with open('test_code/fibo.py', 'wb') as f:
    f.write(res.python_code.encode())

os.system("python -m unittest test_fibo.py || git reset --hard")