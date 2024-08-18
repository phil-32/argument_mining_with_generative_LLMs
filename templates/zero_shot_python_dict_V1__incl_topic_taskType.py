# -*- coding: utf-8 -*-

prompt_dict = {}

prompt_dict["preamble"] = \
"""You are tasked to extract discourse units from a student essay as part of an automated argument mining process. Extract the following discourse unit types from the student essay:

- Lead: An introduction that begins with a statistic, a quotation, a description, or some other device to grab the reader’s attention and point toward the thesis.
- Position: An opinion or conclusion on the main question.
- Claim: A claim that supports the position.
- Counterclaim: A claim that refutes another claim or gives an opposing reason to the position.
- Rebuttal: A claim that refutes a counterclaim.
- Evidence: Ideas or examples that support claims, counterclaims, rebuttals, or the position.
- Concluding Statement: A concluding statement that restates the position and claims.

There can also be non-argument spans which means that not every word must be part of a discourse unit. Ignore those non-argument spans.

Output your results as Python dictionary, where each key is the verbatim span of the student essay and value the corresponding discourse unit type (Lead, Position, Claim, Counterclaim, Rebuttal and Concluding Statement) and do not give any addional explainations or remaks. The format should look like this:

Output:
{{
	"<verbatim span of 1st discourse unit>": "<discourse unit type of the 1st discourse unit>",
	"<verbatim span of 2nd discourse unit>": "<discourse unit type of the 1nd discourse unit>",
}}
"""
prompt_dict["pre_essay"] = "This is a {task} essay about the topic '{prompt_name}'\n\nEssay:"

prompt_dict["suffix"] = "Output:"
