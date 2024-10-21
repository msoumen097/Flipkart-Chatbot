from langchain_astradb import AstraDBVectorStore
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
import os
from FlipkartBot.data_converter import dataconverter
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY="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"
ASTRA_DB_API_ENDPOINT="https://3f641552-16c4-4e5f-ac2a-fcdf4796424c-us-east-2.apps.astra.datastax.com"
ASTRA_DB_APPLICATION_TOKEN="AstraCS:KxEsGEjpYWIaZZrwwXlQKmrM:99e9e853a63217157cf55410c3e7235b3a9ce608ae14a1f61e5cab121862fcf4"
ASTRA_DB_KEYSPACE="default_keyspace"
HF_TOKEN = "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"

embedding = HuggingFaceInferenceAPIEmbeddings(api_key= HF_TOKEN, model_name="BAAI/bge-base-en-v1.5")

def data_ingestion(status):

    vstore = AstraDBVectorStore(
        embedding=embedding,
        collection_name = "flipkart",
        api_endpoint = ASTRA_DB_API_ENDPOINT,
        token = ASTRA_DB_APPLICATION_TOKEN,
        namespace = ASTRA_DB_KEYSPACE 
    )
    storage = status

    if storage == None:
        docs = dataconverter()
        insert_ids = vstore.add_documents(docs)
    
    else:
        return vstore
    return vstore, insert_ids

if __name__ == "__main__":

    vstore, insert_ids = data_ingestion(None)
    print(f"\n Inserted {len(insert_ids)} documents.")
    results = vstore.similarity_search("Can you tell me the low budget sound basshead?")
    for res in results:
        print(f"\n {res.page_content} [{res.metadata}]")