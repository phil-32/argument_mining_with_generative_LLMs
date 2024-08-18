# -*- coding: utf-8 -*-

prompt_dict = {}

prompt_dict["preamble"] = \
"""Automatically Identify and Annotate Discourse Units in a Student Essay

Objective: Analyze the provided student essay to identify specific types of discourse units commonly found in argumentative writing. The identified discourse units should be annotated using an XML-like format, where each unit is enclosed within tags indicating its type. The following discourse unit types must be extracted if present:

1. Lead: Identify and tag any introductive statements that begin with a statistic, quotation, description, or other attention-grabbing devices leading to the thesis statement. Example format: `<lead> Statement </lead>`
2. Position: Tag opinions or conclusions related to the main question of the essay. Example format: `<position> Opinion/Conclusion </position>`
3. Claim: Highlight and tag claims that support the position within the essay. Example format: `<claim> Supporting claim </claim>`
4. Counterclaim: Identify and tag any statements refuting another claim or presenting opposing reasons to the main argument. Example format: `<counterclaim> Refutation/Opposing reason </counterclaim>`
5. Rebuttal: Tag claims that counteract a previously mentioned counterclaim. Example format: `<rebuttal> Counter-refutation claim </rebuttal>`
6. Evidence: Annotate examples or ideas supporting the claims, counterclaims, rebuttals, and positions in the essay. Example format: `<evidence> Supporting evidence/example </evidence>`
7. Concluding Statement: Tag any concluding statements that restate the position and its associated claims. Example format: `<conclusion> Restating conclusion statement </concluding>`

Note: The output should include all non-argumentative portions of the essay without annotation, while discourse units are annotated as per the specified XML-like format.
"""
prompt_dict["pre_demo"] = "Example output:"

prompt_dict["pre_essay"] = "Output all discourse units of the following essay in the XML-like syntax:"

prompt_dict["suffix"] = ""
