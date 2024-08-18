# -*- coding: utf-8 -*-
import pandas as pd
import os
import time
from datetime import datetime

from argument_mining_persuade import metrics
from argument_mining_persuade import utils


def run_simple_argument_mining_experiment(
        model_abbrev, output_dir, df_file,
        model_module, prompt_module, parser, create_batch_only=True,
        prompt_format="simple", example_df_file=None, fuzzysearch_factor=7,
        slice_start=None, slice_end=None, temperature=0, max_tokens=3000,
        example_format_function=None, batch_result_file="",
        numOfEssaysPerBatchFile=None):
    """
    Function to run a simple argument mining with a simple chain.

    Parameters
    ----------
    model_abbrev : string
        model name.
    output_dir : string
        Output directory for log and result data frames.
    df_file : string
        Path to data frame csv with all discourse units and essay information.
        This df contains the essays to be classified and the ground truth
        discourse units to calculate the result metrics.
    model_module : module
        Module containing get_llm() method that returns the model.
    prompt_module : module
        Module containing prompt_dict which is used to build the prompt
        template.
    create_batch_only : boolean
        If set to true, the model is not invoked directly but a batch file is
        created and writen to the output directory to be used with the
        OpenAI Batch API
    numOfEssaysPerBatchFile : int
        If a number is given the batch file is parted into multiple files
        with the given amount of essays.
    prompt_fromat : string
        "simple": The whole prompt consists only of one user (human) message
        "chat": the system role is used for the preample, user (human) massages
                for the essays that are to be classifed and assistant (ai)
                messages to show example essays.
    parser : function
        Parser function from utils according to prompt template format.
    example_df_file : string or int
        Path to data frame csv with all discourse units and essay information
        of the essays that are supposed to be given to the model as examples.
        If int then the retriever is used to return the specified number of
        similar essays as examples
    fuzzysearch_factor : int, optional
        Per how many characters one correction operation is allowed
        (fussysearch max_l_dist = character count of discourse unit /
         fuzzysearch_factor).
        The lower the more differences are allowed but runtime longer.
        The default is 7.
    slice_start : int, optional
        Start index of slice of essays for tests with less essays
        (enter None for using entire df). The default is None.
    slice_end : int, optional
        End index of slice of essays for tests with less essays
        (enter None for using entire df). The default is None.
    temperature : int, optional
        Temperature parameter of LLM. The default is 0.
    max_tokens : int, optional
        Max number of tokens the LLM is supposed to generate.
        The default is 3000.

    Returns
    -------
    None.

    """
    # Building string to identify experiment
    start_time_readable = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    module_name = os.path.splitext(os.path.basename(prompt_module.__file__))[0]
    exp_string = \
        f"{start_time_readable}_{model_abbrev}_{module_name}_{prompt_format}"
    full_output_dir = os.path.join(output_dir, exp_string)

    # Logging setup
    log = utils.createLogger(full_output_dir)

    # Print start_time
    start_time = time.time()
    start_time_readable = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log.info(f"\nScript started at: {start_time_readable}")

    # Write parameters to log
    log.debug(f"fuzzysearch_factor: {fuzzysearch_factor}")
    log.debug(f"df_file: {df_file}")
    log.debug(f"slice_start: {slice_start}")
    log.debug(f"slice_end: {slice_end}")
    log.debug(f"model_module: {model_module.__file__}")
    log.debug(f"temperature: {temperature}")
    log.debug(f"prompt_module: {prompt_module.__file__}")
    log.debug(f"parser: {parser.__name__}")

    # LLM-inference
    # Read csv
    df = pd.read_csv(df_file, index_col=0)
    df_essay = df.drop_duplicates("essay_id")

    # Slice of essays for tests with less essays
    df_essay = df_essay[slice_start:slice_end]
    df = df[df["essay_id"].isin(df_essay.essay_id)]

    prompt_var_func_dict = {"essay": lambda df: df.full_text_clean,
                            "task": lambda df: df.task,
                            "prompt_name": lambda df: df.prompt_name,
                            "assignment": lambda df: df.assignment}

    # model = model_module.get_llm(temperature=temperature,
    #                              max_tokens=max_tokens)

    # prompt_dict = prompt_module.prompt_dict
    # if prompt_format == "simple":
    #     prompt = prompt_generation.assembleSimplePrompt(
    #         example_df_file=example_df_file,
    #         example_format_function=example_format_function,
    #         **prompt_dict)
    # elif prompt_format == "chat":
    #     prompt = prompt_generation.assembleChatPrompt(
    #         example_df_file=example_df_file,
    #         example_format_function=example_format_function,
    #         **prompt_dict)

    # chain = prompt | model

    model = model_module.get_llm(temperature=temperature,
                                 max_tokens=max_tokens)

    if create_batch_only and not batch_result_file:
        utils.write_batch_file(
            df_essay=df_essay,
            df_du=df,
            prompt_var_func_dict=prompt_var_func_dict,
            parser_func=parser,
            output_dir=full_output_dir,
            exp_string=exp_string,
            numOfEssaysPerBatchFile=numOfEssaysPerBatchFile,
            prompt_module=prompt_module,
            model=model,
            prompt_format=prompt_format,
            example_df_file=example_df_file,
            example_format_function=example_format_function)
    else:
        result_df, statistics_df = utils.invoke_llm(
            df_essay=df_essay,
            df_du=df,
            prompt_var_func_dict=prompt_var_func_dict,
            parser_func=parser,
            fuzzysearch_factor=fuzzysearch_factor,
            output_dir=full_output_dir,
            batch_result_file=batch_result_file,
            prompt_module=prompt_module,
            model=model,
            prompt_format=prompt_format,
            example_df_file=example_df_file,
            example_format_function=example_format_function)

        # Evaluate results (get metrics)
        metrics_df = metrics.get_span_and_word_metrics(
            gt_df=df, result_df=result_df, output_dir=full_output_dir)
        # Write metrics and statistics to overview excel file
        utils.write_metrics_statistics_to_excel_overview(
            statistics_df, metrics_df, output_dir, "results_overview.xlsx",
            exp_string)

    # End Timing
    end_time = time.time()
    elapsed_time = end_time - start_time
    log.info(f'Total execution time: {elapsed_time:.2f} seconds')
