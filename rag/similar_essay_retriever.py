from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import pandas as pd
from argument_mining_persuade import config
import os


CHROMA_PATH = os.path.join(config.DATA_DIR, "essay_chroma_data")
COLLECTION_NAME = "essay_embeddings"
EMBEDDINGS = OpenAIEmbeddings(model="text-embedding-3-small")

df_dus = pd.read_csv(config.PERSUADE_2_CLEANED_PATH, index_col=0,
                     low_memory=False)


def retrieve_similar_essays(text, numOfEssays):
    db = Chroma(persist_directory=CHROMA_PATH,
                collection_name=COLLECTION_NAME,
                embedding_function=EMBEDDINGS)
    similar_essays = db.similarity_search(query=text, k=numOfEssays)
    # Get essay_ids of similar essays
    essay_id_list = [sim_essay.metadata["essay_id"]
                     for sim_essay in similar_essays]
    # Get data frame lines of those essays
    df = df_dus[df_dus["essay_id"].isin(essay_id_list)]
    # Replace "{" and "}" because they are interpreted as template placeholders
    df["full_text_clean"] = df["full_text_clean"].apply(
        lambda t: t.replace("{", "(").replace("}", ")"))
    return df
