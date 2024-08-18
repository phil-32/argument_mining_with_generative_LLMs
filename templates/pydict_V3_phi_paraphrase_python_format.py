# -*- coding: utf-8 -*-

prompt_dict = {}

prompt_dict["preamble"] = \
"""Task: Analyze a student's essay and identify specific types of discourse units. Extract these units if they appear in the text, following their descriptions below, while leaving out any non-argument spans. Present your findings as a Python dictionary with each key being an exact excerpt from the essay (verbatim span) paired with its corresponding discourse unit type:

Discourse Unit Types to Look For:
1. Lead: An engaging opening that uses statistics, quotes, or descriptions to draw attention and hint at the thesis.
2. Position: A statement expressing an opinion or conclusion on the main topic of discussion.
3. Claim: A claim that supports the position.
4. Counterclaim: A claim that refutes another claim or gives an opposing reason to the position.
5. Rebuttal: Responds directly to a counterclaim by providing rebuttal evidence.
6. Evidence: Ideas or examples that support claims, counterclaims, rebuttals, or the position.
7. Concluding Statement: A closing remark that restates the position and claims made in the essay.

Ensure your output is formatted as shown below using Python dictionary syntax, without any additional comments or explanations.

Output Format Example:
```python
{{
    "<text_span>": "<type of discourse unit identified>",
}}
```"""

prompt_dict["pre_demo"] = "Example output:"

prompt_dict["pre_essay"] = "Output all discourse units of the following essay in the python dictionary syntax:"

prompt_dict["suffix"] = "Output:"
