from sentence_transformers import SentenceTransformer

from ingest import load_documents
from ingest import create_chunks

import faiss
import numpy as np

import pickle
import os

from config import model

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def create_embeddings(chunks):

    texts = [chunk["text"] for chunk in chunks]

    embeddings = embedding_model.encode(
        texts,
        convert_to_numpy = True
    )

    return embeddings


# embeddings = create_embeddings(chunks)

# if __name__ == "__main__":
#     docs = load_documents("data")

#     chunks = create_chunks(docs)

#     embeddings = create_embeddings(chunks)

#     print("number of chunks:" , len(chunks))

#     print("Embeddings Shape : " , embeddings.shape)


def build_faiss_index(embeddings):
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(
        np.array(embeddings).astype("float32")
    )

    return index


def search_index(query_embedding , index , k=3):
    distances , indices = index.search(
        query_embedding.astype("float32"),
        k
    )

    return distances , indices


def embed_query(query):

    embedding = embedding_model.encode(
        [query] ,  # square bracket - because the model expects a list of sentences.
        convert_to_numpy = True
    )

    return embedding


def retrieve_chunks(indices , chunks):
    retrieved = []

    for idx in indices[0]:

        retrieved.append(chunks[idx])

    return retrieved




# if __name__ == "__main__":
#     docs = load_documents("data")

#     chunks = create_chunks(docs)

#     embeddings = create_embeddings(chunks)

#     index = build_faiss_index(embeddings)

#     question = "What is Artificial Intelligence ?"

#     query_embedding = embed_query(question)

#     distance , indices = search_index(query_embedding , index , 3)

#     print(indices)

#     retrieve_chunks = retrieve_chunks(indices , chunks)

#     for chunk in retrieve_chunks:
#         print("=" * 50)

#         print(chunk["text"])



def save_index(index):

    os.makedirs("vector_store" , exist_ok = True)

    faiss.write_index(
        index,
        "vector_store/faiss.index"
    )


def save_chunks(chunks):

    with open(
        "vector_store/chunks.pk1",
        "wb"
    ) as f:
        
        pickle.dump(chunks,f)



def load_index():

    return faiss.read_index(
        "vector_store/faiss.index"
    )


def load_chunks():

    with open(
        "vector_store/chunks.pk1",
        "rb"
    ) as f:
        
        return pickle.load(f)
    


def create_context(retrieved_chunks):

    context = ""

    for chunk in retrieved_chunks:

        context += chunk["text"]

        context += "\n\n"

    return context
    

def ask_gemini(question,context):

    prompt = f"""
        
        You are an AI assistant.

        Answer ONLY using context below.
        If the answer is not present 
        reply with:
        "I couldn't find the answer in the uploaded documents."

        then give the answer u know as :

        "On searching the web i got" :
        then your answer

        Context : 
        {context}

        Question : 
        {question}

    """
    
    response = model.generate_content(prompt)

    return response.text


if __name__ == "__main__":

    index = load_index()

    chunks = load_chunks()

    question = input("Ask: ")

    query_embedding = embed_query(question)

    distances, indices = search_index(
        query_embedding,
        index
    )

    retrieved = retrieve_chunks(
        indices,
        chunks
    )

    context = create_context(
        retrieved
    )

    answer = ask_gemini(
        question,
        context
    )

    print()

    print(answer)


