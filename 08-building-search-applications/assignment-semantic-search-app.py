import os
import pandas as pd
import numpy as np
from openai import AzureOpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = AzureOpenAI(
  api_key=os.environ['AZURE_OPENAI_API_KEY'],  # this is also the default, it can be omitted
  api_version = "2023-05-15"
)

model = os.environ['AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT']

SIMILARITIES_RESULTS_THRESHOLD = 0.75
DATASET_NAME = "../embedding_index_3m.json"

model = os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT", "").strip()
assert model, "AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT environment variable must be set and non-empty"

# load data 
def load_data():
    with open('embedding_index_3m.json', 'r') as file:
        data_set = json.load(file)
    print(f"loaded data set size: {len(data_set)}.\n")
    return data_set

data_set = load_data()

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_input_embedding(text):
    embedding_text = client.embeddings.create(input = [text], model=model).data[0].embedding
    print ("Embedding text succeeded!\n")
    return embedding_text

# Informat: Video name, url, timestamp, content
def return_top_result(data_set, embedding_text):
    top_entry = data_set[0]
    top_entry_diff = cosine_similarity(top_entry['ada_v2'], embedding_text)
    for entry in data_set:
        diff = cosine_similarity(entry['ada_v2'], embedding_text)
        if diff > top_entry_diff:
            top_entry = entry
    if top_entry_diff > 0.75:
        return (top_entry, top_entry_diff)
    else:
        raise Exception(f"Not able to find similar text. Closes one is {top_entry_diff}")

# take input
text = input("Enter the sentence you want to search: ")

# calculate embedding value
embedding_text = get_input_embedding(text)

# compare with data set and return top result
(result, score) = return_top_result(data_set, embedding_text)
print(f"Score: {score}\nSpeaker: {result['speaker']}\nTitle: {result['title']}\nStart: {result['start']}\nSeconds: {result['seconds']}\nSummary: {result['summary']}\n")