# -*- coding: utf-8 -*-

prompt_dict = {}

prompt_dict["preamble"] = \
"""Extract discourse units from a student essay as part of an automated argument mining process. Extract the following discourse unit types from the student essay if they occur:
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
<Lead> Span of a lead discourse unit </Lead> Non-argument span without any annotation <Position> Span of a position discourse unit </Position> <Claim> Span of a claim discourse unit </Claim> Non-argument span without any annotation <Counterclaim> Span of a counterclaim discourse unit </Counterclaim> <Rebuttal> Span of a rebuttal discourse unit </Rebuttal> <Evidence> Span of a claim discourse unit </Evidence> <Concluding Statement> Span of a concluding statement discourse unit </Concluding Statement>
```"""
prompt_dict["pre_demo"] = "Example output:"

prompt_dict["pre_essay"] = "Output all discourse units of the following essay in the XML-like syntax:"

prompt_dict["suffix"] = ""
