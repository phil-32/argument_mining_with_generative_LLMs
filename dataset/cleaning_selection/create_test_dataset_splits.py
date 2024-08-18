import pandas as pd
import os
import argument_mining_persuade
from argument_mining_persuade import config

# Read full cleaned Dataset
df = pd.read_csv(config.PERSUADE_2_CLEANED_PATH, index_col=0, low_memory=False)

# Get path to csv with essay IDs
module_path = os.path.dirname(argument_mining_persuade.__file__)
dataset_path = os.path.join(module_path, "dataset")

essay_id_output_path_list = [
    ("example_essay_1_shot_essay_ids.csv", config.EXAMPLE_ESSAYS_1_SHOT),
    ("example_essay_5_shot_essay_ids.csv", config.EXAMPLE_ESSAYS_5_SHOT),
    ("example_essay_10_shot_essay_ids.csv", config.EXAMPLE_ESSAYS_10_SHOT),
    ("example_essay_15_shot_essay_ids.csv", config.EXAMPLE_ESSAYS_15_SHOT),
    ("test_dataset_200_essay_ids.csv", config.TEST_DATASET_PATH),
    ("test_dataset_1000_essay_ids.csv", config.TEST_DATASET_1000_PATH),
    ("essays_for_embeddings_ids.csv", config.EMBEDDING_ESSAYS),]

for source_file_name, res_path in essay_id_output_path_list:
    essay_ids_path = os.path.join(dataset_path, source_file_name)
    essay_ids = pd.read_csv(essay_ids_path, index_col=0)

    # Create dataframe with essays of test dataset
    df_sliced = df[df["essay_id"].isin(essay_ids["essay_id"])]

    # Save dataframe
    df_sliced.to_csv(res_path)
