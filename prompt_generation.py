# -*- coding: utf-8 -*-
import pandas as pd
from langchain_core.prompts import (PromptTemplate, ChatPromptTemplate)
from argument_mining_persuade.rag import similar_essay_retriever as retriever


def assembleChatPrompt(preamble, essay_text, example_df_file="",
                       pre_essay="Essay:", pre_demo="Output:", suffix="",
                       example_format_function=None):
    messages = []
    # System prompt with basic instructions
    messages.append(("system", preamble))
    # Append 'fake' conversation showing examples
    if example_df_file:
        if type(example_df_file) is str:
            df = pd.read_csv(example_df_file, index_col=0)
        elif type(example_df_file) is int:
            df = retriever.retrieve_similar_essays(essay_text, example_df_file)
        for essay_id in df.essay_id.unique():
            # example essay text
            text = df[df["essay_id"] == essay_id].iloc[0].full_text_clean
            # Fill in any placeholder if there are any
            temp_pre_essay = formatPreEssayString(df, essay_id, pre_essay)
            messages.append(
                ("human", f"{temp_pre_essay}\n\"\"\"\n{text}\n\"\"\""))
            # 'fake' AI answer with formated essay only
            du = df[df["essay_id"] == essay_id]
            messages.append(("ai", example_format_function(du, "", "")))
    # Actual essay to classify
    messages.append(("human", pre_essay + "\n\"\"\"\n{essay}\n\"\"\""))

    prompt = ChatPromptTemplate.from_messages(messages)
    return prompt


def assembleSimplePrompt(preamble, essay_text, example_df_file="",
                         pre_essay="Essay:", pre_demo="Output:", suffix="",
                         example_format_function=None):
    prompt = PromptTemplate.from_template(preamble)
    prompt += "\n\n"
    # Format and add example
    if example_df_file:
        if type(example_df_file) is str:
            example_df = pd.read_csv(example_df_file, index_col=0)
        elif type(example_df_file) is int:
            example_df = retriever.retrieve_similar_essays(essay_text,
                                                           example_df_file)
        for essay_id in example_df.essay_id.unique():
            # Fill in any placeholder if there are any
            temp_pre_essay = formatPreEssayString(example_df, essay_id,
                                                  pre_essay)
            prompt += example_format_function(
                example_df[example_df["essay_id"] == essay_id],
                pre_essay=temp_pre_essay, pre_demo=pre_demo)
            prompt += "\n\n"
    prompt += pre_essay
    prompt = prompt + "\n"
    prompt += "\"\"\"\n{essay}\n\"\"\""
    if suffix:
        prompt += "\n\n"
        prompt += suffix

    return prompt


def assembleCoTPrompt(preamble, essay_text, example_df_file="",
                      pre_essay="Essay:", pre_demo="Output:", suffix="",
                      example_format_function=None):
    messages = []
    # System prompt with basic instructions
    messages.append(("system", preamble))
    if example_df_file:
        if type(example_df_file) is str:
            df = pd.read_csv(example_df_file, index_col=0)
        for essay_id in df.essay_id.unique():
            # example essay text
            text = df[df["essay_id"] == essay_id].iloc[0].full_text_clean
            # Fill in any placeholder if there are any
            temp_pre_essay = formatPreEssayString(df, essay_id, pre_essay)
            messages.append(
                ("human", f"{temp_pre_essay}\n\"\"\"\n{text}\n\"\"\""))
    # Take pre_demo as demonstration in this experiment (the prompt template
    # must contain the reasoning and example essay)
    messages.append(("ai", pre_demo))
    # Actual essay to classify
    messages.append(("human", pre_essay + "\n\"\"\"\n{essay}\n\"\"\""))

    prompt = ChatPromptTemplate.from_messages(messages)
    return prompt


def formatExampleEssayPythonDict(df, pre_essay, pre_demo):
    """
    Returns the discourse units of the df formated as a Python dictionary.
    """
    # out = pre_essay
    # out += "\n\n"
    # # Append full essay first (because non-argument text would not appear)
    # full_essay = df.iloc[0].full_text_clean.replace('"', "'")
    # out += f"\"\"\"{full_essay}\"\"\"\n\n"
    if pre_demo:
        out = pre_demo
        out += "\n"
    else:
        out = ""
    out += "{{\n"
    for i, du_row in df.sort_values("discourse_start").iterrows():
        discourse_unit_text = du_row.discourse_text_clean.replace('"', "'")
        out += f'\"{discourse_unit_text}\": '\
            f'\"{du_row.discourse_type}\",\n'
    out += r"}}"
    return out


def formatExampleEssayXML(df, pre_essay, pre_demo):
    """
    Returns the discourse units of the df formated with the XML-like syntax.
    """
    if pre_demo:
        out = pre_demo
        out += "\n"
    else:
        out = ""
    out += "```xml\n"
    # out += "<essay>"
    cursor = 0
    sorted_df = df.sort_values("discourse_start", ignore_index=True)
    for i, du_row in sorted_df.iterrows():
        discourse_start = du_row.discourse_start_clean
        discourse_end = du_row.discourse_end_clean
        # If no non-argument sections are between two discourse units
        if cursor != discourse_start:
            out += du_row.full_text_clean[cursor:discourse_start]
        # Add next discourse unit
        du_type = du_row.discourse_type  # .lower().replace(" ", "")
        out += f"<{du_type}>"\
            f"{du_row.full_text_clean[discourse_start:discourse_end]}"\
            f"</{du_type}>"
        cursor = discourse_end
    # Add non-argument spans from the end of the essay
    if cursor != len(du_row.full_text_clean):
        out += du_row.full_text_clean[cursor:len(du_row.full_text_clean)]
    # out += "</essay>"
    out += "```"
    return out


def formatExampleEssayTANL(df, pre_essay, pre_demo):
    """
    Returns the discourse units of the df formated with the TANL syntax.
    """
    cursor = 0
    if pre_demo:
        out = pre_demo
        out += "\n"
    else:
        out = ""
    sorted_df = df.sort_values("discourse_start", ignore_index=True)
    for i, du_row in sorted_df.iterrows():
        discourse_start = du_row.discourse_start_clean
        discourse_end = du_row.discourse_end_clean
        # If no non-argument sections are between two discourse units
        if cursor != discourse_start:
            out += du_row.full_text_clean[cursor:discourse_start]
        # Add next discourse unit
        du_type = du_row.discourse_type
        out += \
            f"[{du_row.full_text_clean[discourse_start:discourse_end]}"\
            f"|{du_type}]"
        cursor = discourse_end
    # Add non-argument spans from the end of the essay
    if cursor != len(du_row.full_text_clean):
        out += du_row.full_text_clean[cursor:len(du_row.full_text_clean)]
    return out


def formatPreEssayString(df, essay_id, pre_essay):
    """
    Fill in any placeholder if there are any.
    """
    assignment = df[df["essay_id"] == essay_id].iloc[0].assignment
    task = df[df["essay_id"] == essay_id].iloc[0].task
    prompt_name = df[df["essay_id"] == essay_id].iloc[0].prompt_name
    return pre_essay.format(assignment=assignment, prompt_name=prompt_name,
                            task=task)


if __name__ == "__main__":
    prompt = assembleSimplePrompt(
        "", "essay_text",
        example_df_file=r"D:\PERSUADE\example_essay_2_shot.csv",
        example_format_function=formatExampleEssayTANL)
    print(prompt.template)
    # from argument_mining_persuade import utils
    # m = utils.parser_XML(prompt.template)
    # print(m)
