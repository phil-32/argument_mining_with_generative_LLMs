# -*- coding: utf-8 -*-

prompt_dict = {}

prompt_dict["preamble"] = \
"""Extract discourse units from a student essay as part of an automated argument mining process. Identify and annotate the following discourse unit types within the essay:

- **Lead**: An introduction designed to grab the reader’s attention, often starting with a statistic, quotation, or description, and pointing toward the thesis.
- **Position**: An opinion or conclusion on the main question.
- **Claim**: A statement that supports the position.
- **Counterclaim**: A statement that refutes another claim or presents an opposing reason to the position.
- **Rebuttal**: A statement that refutes a counterclaim.
- **Evidence**: Ideas or examples that support claims, counterclaims, rebuttals, or the position.
- **Concluding Statement**: A final statement that restates the position and claims.

Note that there can be non-argument spans in the essay, and not every word needs to be part of a discourse unit.

Output the entire input essay verbatim, including non-argument spans, but annotate the discourse units using XML-like tags. Each discourse unit span should be enclosed by a tag that indicates the discourse unit type. For example:

```xml
<Lead> Introduction with an attention-grabbing element </Lead> non-argument text <Position> Main opinion or conclusion </Position>
```

Ensure that the annotations are clearly marked and preserve the original text of the essay."""
prompt_dict["pre_demo"] = "Example output:"

prompt_dict["pre_essay"] = "Output all discourse units of the following essay in the XML-like syntax:"

prompt_dict["suffix"] = ""
