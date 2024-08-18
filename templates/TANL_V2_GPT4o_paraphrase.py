# -*- coding: utf-8 -*-

prompt_dict = {}

prompt_dict["preamble"] = \
"""Your task is to identify and extract specific discourse units from a student essay as part of an automated argument mining process. The types of discourse units you need to identify and extract are:

- **Lead:** An introduction that starts with a statistic, quotation, description, or other device to capture the reader's attention and hint at the thesis.
- **Position:** An opinion or conclusion regarding the main question.
- **Claim:** A statement that supports the position.
- **Counterclaim:** A statement that opposes another claim or provides an opposing reason to the position.
- **Rebuttal:** A statement that refutes a counterclaim.
- **Evidence:** Ideas or examples that back up claims, counterclaims, rebuttals, or the position.
- **Concluding Statement:** A closing statement that reiterates the position and claims.

Note that there may also be non-argument spans in the essay. Not every word needs to be part of a discourse unit.

Your output should include the entire essay verbatim, including non-argument spans, but annotate the discourse units by enclosing each span and its discourse type in square brackets, with the span and type separated by a pipe symbol (|), like this:

```
[<span of 1st discourse type>|<1st discourse type>]<non-argument span without any annotation>[<span of 2nd discourse type>|<2nd discourse type>]
```
"""
prompt_dict["pre_demo"] = "Example output:"

prompt_dict["pre_essay"] = "Output all discourse units of the follwing essay:"

prompt_dict["suffix"] = ""
