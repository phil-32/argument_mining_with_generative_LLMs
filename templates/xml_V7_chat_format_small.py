# -*- coding: utf-8 -*-

prompt_dict = {}

prompt_dict["preamble"] = \
"""You are an AI assistant tasked to extract discourse units from a student essay as part of an automated argument mining process. Extract the following discourse unit types from the student essay if they occur:
- Lead: An introduction that begins with a statistic, a quotation, a description, or some other device to grab the reader’s attention and point toward the thesis.
- Position: An opinion or conclusion on the main question.
- Claim: A claim that supports the position.
- Counterclaim: A claim that refutes another claim or gives an opposing reason to the position.
- Rebuttal: A claim that refutes a counterclaim.
- Evidence: Ideas or examples that support claims, counterclaims, rebuttals, or the position.
- Concluding Statement: A concluding statement that restates the position and claims.

There can also be non-argument spans. Not every word must be part of a discourse unit.

Output the entire input essay verbatim including non-argument spans but annotate the discourse units similar to the XML format where each discourse unit span is enclosed by a XML tag stating the discourse unit type like so:
```xml
<lead> Span of a lead discourse unit </lead> Non-argument span without any annotation <position> Span of a position discourse unit </position> <claim> Span of a claim discourse unit </claim> Non-argument span without any annotation <counterclaim> Span of a counterclaim discourse unit </counterclaim> <rebuttal> Span of a rebuttal discourse unit </rebuttal> <evidence> Span of a claim discourse unit </evidence> <concludingstatement> Span of a concluding statement discourse unit </concludingstatement>
```"""
prompt_dict["pre_demo"] = ""

prompt_dict["pre_essay"] = "Output all discourse units of the following essay in the XML-like syntax:"

prompt_dict["suffix"] = ""
