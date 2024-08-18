# -*- coding: utf-8 -*-

import pandas as pd
from nltk.tokenize import word_tokenize
from argument_mining_persuade import config
from tqdm import tqdm

# %% Load Datasets

# Persuade 1.0 (one row per discourse unit)
df = pd.read_csv(config.PERSUADE_2_RAW_PATH, low_memory=False)

df.drop("essay_id", axis=1, inplace=True)
df.rename(columns={"essay_id_comp": "essay_id"}, inplace=True)

df_essays = df.drop_duplicates("essay_id", keep="first")
df_essays.reset_index(drop=True, inplace=True)
df_essays.drop(["discourse_id", "discourse_start", "discourse_end",
                "discourse_text", "discourse_type", "discourse_type_num",
                "hierarchical_id", "hierarchical_text", "hierarchical_label",
                "provider", "discourse_effectiveness", "competition_set"],
                axis=1, inplace=True)

# %% Delete discourse units of type "Unanotated" and two essays with discourse
# unit annotaton problems

df = df[df["discourse_type"] != "Unannotated"]
df = df[df["essay_id"] != "B7E1A842F675"]
df = df[df["essay_id"] != "CC149CD4B584"]

df_du = df
# %% Word counts

# Do word and token counts with essay level dataframe
df = df_essays

def removePunctuationFromList(str_list):
    """
    Removes single punctuation strings from list.
    """
    l_local = list(str_list)  # avoid side effects by copying
    import string
    for p in string.punctuation:
        l_local = list(filter(lambda a: a != p, l_local))
    return l_local


# Count words for each essay in dataset and calculate difference to
# offical word count
df.insert(len(df.columns), "word_count_clean", None)
df.insert(len(df.columns), "word_count_diff", None)
df.insert(len(df.columns), "word_count_diff_ratio", None)

for i, row_dict in df.iterrows():
    essay_tokenized = word_tokenize(row_dict["full_text"])
    word_count_clean = len(removePunctuationFromList(essay_tokenized))
    # word_count_clean = len(list(
    #     filter(lambda s: s.isalpha(), essay_tokenized)))
    df.at[i, "word_count_clean"] = word_count_clean
    df.at[i, "word_count_diff"] = word_count_clean - row_dict[
        "essay_word_count"]
    df.at[i, "word_count_diff_ratio"] = \
        (word_count_clean - row_dict["essay_word_count"]) / row_dict[
            "essay_word_count"]
    print(i, row_dict["essay_id"],
          word_count_clean,
          row_dict["essay_word_count"],
          word_count_clean - row_dict["essay_word_count"])

print(df.loc[df['word_count_diff'].idxmax()])
print()
print(df.loc[df['word_count_diff'].idxmin()])

sorted_df = df.sort_values("word_count_diff_ratio",
                           ascending=True,
                           ignore_index=True)
sorted_df_min = sorted_df[["essay_id", "essay_word_count", "word_count_clean",
                           "word_count_diff", "word_count_diff_ratio",
                           "holistic_essay_score"]].head(60)

# %% Tokenization for whole df
# Add colums of normalized text to df as well as columns for token count and
# token/word ratio
import tiktoken
encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')

df.insert(len(df.columns), "full_text_clean", None)
df.insert(len(df.columns), "token_count_cleaned_text", None)
df.insert(len(df.columns), "ratio_token_to_words", None)

for i, row_dict in df.iterrows():
    essay_text = row_dict["full_text"]
    df.at[i, "full_text_clean"] = essay_text.replace(
        "\xa0 ", " ").replace(" \xa0", " ").replace("\xa0", " ")\
        .replace("\'", "'").strip()
    df.at[i, "token_count_cleaned_text"] = len(encoding.encode
                                               (df.at[i, "full_text_clean"]))
    df.at[i, "ratio_token_to_words"] = \
        df.at[i, "token_count_cleaned_text"] / df.at[i, "word_count_clean"]
    print(i, df.at[i, "essay_id"], df.at[i, "word_count_clean"],
          df.at[i, "token_count_cleaned_text"],
          df.at[i, "ratio_token_to_words"])

print(df[["token_count_cleaned_text",
          "word_count_clean",
          "word_count_diff_ratio"]].convert_dtypes().describe())

# %% Merge the essay level information with the 

df = df_du.merge(df)

print("Number of essays:", len(df.essay_id.unique()))
print("Number of discourse units:", len(df))


# %% Check if discourse units are contained in full texts verbatim


def countContainedDiscourseUnitsInFullText(df):
    error_count = 0
    success_count = 0
    for i, row in df.iterrows():
        if row.discourse_text in row.full_text:
            success_count += 1
        else:
            error_count += 1
    print(f"error_count: {error_count}")
    print(f"success_count: {success_count}")


def printFirstDiscourseTextWithError(df):
    # Print the first discourse_text and the corresponding full_text with an
    # error
    for i, row in df.iterrows():
        if row.discourse_text in row.full_text:
            pass
        else:
            print(row.discourse_id)
            print(repr(row.discourse_text))
            print("-----------")
            print(repr(row.full_text))
            break  # print only the first discourse_text

# The full text contains "/'" and the discourse unit only "'"
# Additionally the full text might contain \n\n at the end and the discourse
# unit a space
# --> Delete trailing spaces and make "'" in discourse units to "\'"

df["discourse_text"] = df[
   "discourse_text"].apply(lambda s: s.replace("'", "\'"))
df["discourse_text"] = df[
   "discourse_text"].apply(lambda s: s.strip())

# countContainedDiscourseUnitsInFullText(df)
# printFirstDiscourseTextWithError(df)

# Only two essay with missmatches remain (in full text "florida" is replaced by
# "LOCATION_NAME")
index = df.loc[df[
    "discourse_id"] == 1623258656795].index[0]

text = df.at[index, "discourse_text"].replace(
    "florida", "LOCATION_NAME")
df.at[index, "discourse_text"] = text

# countContainedDiscourseUnitsInFullText(df)
# printFirstDiscourseTextWithError(df)

# --> returns 0 errors

# %% Check discourse start and end labels
import difflib
sm = difflib.SequenceMatcher()


def findCorrectStartIndex(full_text, snippet, start_index_in_df, tolerance):
    """
    Finds the correct start index of the snippet in full_text based on the
    supposed often inaccurate start index given in the dataset
    """
    start_index = full_text.find(snippet)
    # If the difference between the start indices is too large look for a later
    # occurence in full_text.
    if abs(start_index - start_index_in_df) > tolerance:
        num_iterations = 0
        while abs(start_index_in_df - start_index) > tolerance:
            old_start_index = start_index
            start_index = full_text[start_index + len(snippet):]\
                .find(snippet)
            # Error (snippet was not found in full_text)
            if start_index == -1:
                return (full_text.find(snippet), -1)
            start_index = start_index + old_start_index + len(snippet)
            num_iterations += 1

        return (start_index, num_iterations)

    # Real start is within margin of error:
    else:
        return (start_index, 0)


# Find correct start and end indices for the original discourse unit
for i, row in df.iterrows():
    start_index, iteration_count = findCorrectStartIndex(
        row.full_text, row.discourse_text, row.discourse_start, 25)
    if iteration_count == -1:
        print("ERROR:")
        print(i, " | ", row.discourse_start, start_index, iteration_count)
    if iteration_count > 0:
        print(i, " | ", row.discourse_start, start_index, iteration_count)
    df.at[i, "discourse_start"] = start_index
    df.at[i, "discourse_end"] = \
        start_index + len(row.discourse_text)

print("Checking similarity scores of discourse units:")
ratios = []
for i, row in tqdm(df.iterrows(), total=df.shape[0]):
    full_text_slice = row.full_text[row.discourse_start:row.discourse_end]
    sm = difflib.SequenceMatcher(None, a=full_text_slice, b=row.discourse_text)
    df.at[i, "similarity_ratio"] = sm.ratio()

print("Number of discourse units with similarity score 1:",
      len(df[df.similarity_ratio == 1]))


# %% Create a new column with cleaned discourse_text and full essay text

df["full_text_clean"] = df[
    "full_text"].apply(lambda s: s.replace("\xa0 ", " ")
                       .replace(" \xa0", " ").replace("\xa0", " ")
                       .replace("\'", "'").strip())

# Add cleaned version of discourse_units
df["discourse_text_clean"] = df[
    "discourse_text"].apply(lambda s: s.replace("\xa0 ", " ")
                            .replace(" \xa0", " ").replace("\xa0", " ")
                            .replace("\'", "'").strip())

# %% Check discourse start and end labels for cleaned texts and discourse units
print("--------- Run with cleaned data ------------")

df.insert(len(df.columns), "discourse_start_clean", None)
df.insert(len(df.columns), "discourse_end_clean", None)
df.insert(len(df.columns), "similarity_ratio_clean", None)


essays_to_check = []
# Find correct start and end indices for the cleaned discourse unit
for i, row in df.iterrows():
    tolerance = 25
    start_index, iteration_count = findCorrectStartIndex(
        row.full_text_clean, row.discourse_text_clean, row.discourse_start,
        tolerance)

    while iteration_count == -1:
        print("ERROR:")
        print(i, " | ", row.discourse_start, start_index, iteration_count)
        # print("--------- Slice of clean text with original start index")
        # print(row.full_text_clean[row.discourse_start: row.discourse_start +
        #                           len(row.discourse_text_clean)])
        # print("--------- Slice of clean text with new start index "
        #       "(might be the first)")
        # print(row.full_text_clean[start_index: start_index +
        #                           len(row.discourse_text_clean)])
        # print("--------- Cleaned discourse unit text")
        # print(row.discourse_text_clean)
        # print("---------")
        tolerance += 10
        print("trying again with tolerance of", tolerance)
        # incease tolerance value
        start_index, iteration_count = findCorrectStartIndex(
            row.full_text_clean, row.discourse_text_clean, row.discourse_start,
            tolerance)
        essays_to_check.append(row.essay_id)
    if iteration_count > 0:
        print(i, " | ", row.discourse_start, start_index, iteration_count)
    df.at[i, "discourse_start_clean"] = start_index
    df.at[i, "discourse_end_clean"] = \
        int(start_index + len(row.discourse_text_clean))
df.discourse_start_clean = \
    df.discourse_start_clean.astype(int)
df.discourse_end_clean = \
    df.discourse_end_clean.astype(int)

print("Checking similarity scores of discourse units:")
ratios = []
for i, row in tqdm(df.iterrows(),  total=df.shape[0]):
    full_text_slice = row.full_text_clean[
        row.discourse_start_clean:row.discourse_end_clean]
    sm = difflib.SequenceMatcher(None, a=full_text_slice,
                                 b=row.discourse_text_clean)
    df.at[i, "similarity_ratio_clean"] = sm.ratio()


print("Number of cleaned discourse units with similarity score 1:",
      len(df[df.similarity_ratio_clean == 1]))

# %% Save dataframe with additional columns
print("Writing cleaned dataframe to file.")
df.to_csv(config.PERSUADE_2_CLEANED_PATH)
print("Done.")
