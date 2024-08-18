import os

# Directory of the dataset
DATA_DIR = r"D:\temp\PERSUADE"


# PERSUADE_1_RAW_PATH = os.path.join(
#     DATA_DIR, "persuade_corpus_1.0.csv")
# PERSUADE_2_RAW_PATH = os.path.join(
#     DATA_DIR, "persuade_2.0_human_scores_demo_id_github.csv")
PERSUADE_2_RAW_PATH = os.path.join(
    DATA_DIR, "persuade_corpus_2.0.csv")
PERSUADE_2_CLEANED_PATH = os.path.join(
    DATA_DIR, "persuade2_cleaned_discourse_units.csv")
TEST_DATASET_PATH = os.path.join(
    DATA_DIR, "test_dataset_200.csv")
TEST_DATASET_1000_PATH = os.path.join(
    DATA_DIR, "test_dataset_1000.csv")
EMBEDDING_ESSAYS = os.path.join(
    DATA_DIR, "essays_for_embeddings.csv")
OUTPUT_DIR = os.path.join(
    DATA_DIR, "results")
EXAMPLE_ESSAYS_1_SHOT = os.path.join(
    DATA_DIR, "example_essay_1_shot.csv")
EXAMPLE_ESSAYS_5_SHOT = os.path.join(
    DATA_DIR, "example_essay_5_shot.csv")
EXAMPLE_ESSAYS_10_SHOT = os.path.join(
    DATA_DIR, "example_essay_10_shot.csv")
EXAMPLE_ESSAYS_15_SHOT = os.path.join(DATA_DIR, "example_essay_15_shot.csv")
# 