# -*- coding: utf-8 -*-

prompt_dict = {}

prompt_dict["preamble"] = \
"""You need to extract specific types of discourse units from a student essay for an automated argument mining process. Identify and extract the following discourse unit types if they are present:

- **Lead**: An introduction that grabs the reader's attention with a statistic, quotation, description, or other device and points toward the thesis.
- **Position**: An opinion or conclusion on the main question.
- **Claim**: A statement that supports the position.
- **Counterclaim**: A statement that refutes another claim or opposes the position.
- **Rebuttal**: A statement that refutes a counterclaim.
- **Evidence**: Ideas or examples that support claims, counterclaims, rebuttals, or the position.
- **Concluding Statement**: A concluding statement that restates the position and claims.

Ignore non-argument spans; not every word must be part of a discourse unit.

Output your results as a Python dictionary, where each key is the verbatim span from the student essay, and the value is the corresponding discourse unit type (Lead, Position, Claim, Counterclaim, Rebuttal, Evidence, or Concluding Statement).

Output format example:
```python
{{
    "<verbatim span of 1st discourse unit>": "<discourse unit type of the 1st discourse unit>",
    "<verbatim span of 2nd discourse unit>": "<discourse unit type of the 2nd discourse unit>",
}}
```

Do not provide any additional explanations or remarks."""

prompt_dict["pre_demo"] = "Example output:"

prompt_dict["pre_essay"] = "Output all discourse units of the following essay in the python dictionary syntax:"

prompt_dict["suffix"] = "Output:"
