import pandas as pd
import chromadb
import os
from openai import OpenAI
from tqdm import tqdm
from argument_mining_persuade import config

client = OpenAI()


def get_embedding(text, model="text-embedding-3-small"):
    return client.embeddings.create(
        input=[text], model=model).data[0].embedding


essay_csv_path = config.EMBEDDING_ESSAYS
chroma_path = os.path.join(config.DATA_DIR, "essay_chroma_data")

df = pd.read_csv(essay_csv_path, index_col=0)

db_client = chromadb.PersistentClient(path=chroma_path)
collection = db_client.get_or_create_collection(name="essay_embeddings")

# Generate embeddings and add to Chroma store
for i, essay_row in tqdm(df.iterrows(), total=df.shape[0]):
    collection.add(
        ids=[f"{i}"],
        documents=[essay_row.essay_id],
        embeddings=[get_embedding(essay_row.full_text_clean)],
        metadatas=[essay_row.to_dict()])
