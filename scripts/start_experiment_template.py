# -*- coding: utf-8 -*-
import importlib
import pkgutil

import argument_mining_persuade as am
from argument_mining_persuade.models import lm_studio
from argument_mining_persuade.models import ollama_phi3_4k
from argument_mining_persuade.models import ollama_phi3_128k
from argument_mining_persuade.models import ollama_llama3_8B
from argument_mining_persuade.models import ollama_mistral_7B
from argument_mining_persuade.models import mistral_7B
from argument_mining_persuade.models import gpt_4o
from argument_mining_persuade.models import gpt_3_5_turbo
from argument_mining_persuade import utils
from argument_mining_persuade import experiments
from argument_mining_persuade import prompt_generation
from argument_mining_persuade import config


# %% Import all template modules
package_name = "argument_mining_persuade.templates"
package = importlib.import_module(package_name)
for _, module_name, _ in pkgutil.iter_modules(package.__path__):
    importlib.import_module(f"{package_name}.{module_name}")

# %% Template dictionary

template_param_dict = {
    "model_abbrev": "",
    "output_dir": config.OUTPUT_DIR,
    "df_file": config.TEST_DATASET_PATH,
    "model_module": None,
    "prompt_module": None,
    "parser": utils.parser_XML,
    "example_format_function": prompt_generation.formatExampleEssayXML,
    "fuzzysearch_factor": 7,
    "slice_start": None,
    "slice_end": None,
    "temperature": 0,
    "max_tokens": 3000,
    "create_batch_only": False,
    # "batch_result_file": r""
    "prompt_format": "",
    }

exp_params = []

# %% Configure experiments to run here

for example_df_file, experiment_abbrev in [
        (config.EXAMPLE_ESSAYS_1_SHOT, "1shot_"),
        # (config.EXAMPLE_ESSAYS_5_SHOT, "5shot_"),
        # (config.EXAMPLE_ESSAYS_10_SHOT, "10shot_"),
        # (config.EXAMPLE_ESSAYS_15_SHOT, "15shot_"),
        # (1, "1shot_RAG_"),
        # (5, "5shot_RAG_"),
        # (10, "10shot_RAG_"),
        # (15, "15shot_RAG_"),
        ]:
    for model_module, model_abbrev in [
            (ollama_phi3_4k, "ollama_phi3_4k_"),
            # (ollama_llama3_8B, "llama3_8B_"),
            # (ollama_mistral_7B, "mistral_7B_"),
            # (mistral_7B, "mistral_7B_api_"),
            # (gpt_4o, "gpt_4o_"),
            # (gpt_3_5_turbo, "gpt_3_5_turbo_"),
            ]:
        for prompt_module in [
                am.templates.xml_V1_with_format,
                # am.templates.xml_V1_with_format_assignment,
                # am.templates.xml_V1_with_format_assignment_CoT,
                ]:
            for prompt_format in [
                    "chat",
                    # "simple",
                    # "CoT", # always with 1-shot
                    ]:
                temp_dict = template_param_dict.copy()
                temp_dict["model_module"] = model_module
                temp_dict["prompt_module"] = prompt_module
                temp_dict["model_abbrev"] = experiment_abbrev + model_abbrev
                temp_dict["example_df_file"] = example_df_file
                temp_dict["prompt_format"] = prompt_format
                exp_params.append(temp_dict)

# %% Run experiment
i = 0
for param_dict in exp_params:
    i += 1
    print(f"\nRunning experiment {i} of {len(exp_params)}")
    experiments.run_simple_argument_mining_experiment(**param_dict)
