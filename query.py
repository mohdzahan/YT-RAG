import chromadb
from sentence_transformers import SentenceTransformer


st = SentenceTransformer('BAAI/bge-small-en')

def query_chunks(question):
    cd = chromadb.PersistentClient(path="./chroma_db")
    collection = cd.get_collection("kt_videos")  
    embedding = st.encode(question)
    result = collection.query(
        query_embeddings=[embedding.tolist()],
        n_results=3
    )
    return result

def format_results(res):
    for index in range(len(res['documents'][0])):
        print(f"Result {index + 1}:")        
        print(f"Link: {res['metadatas'][0][index]['timestamp_link']}")
        print(f"Time: {res['metadatas'][0][index]['start_time']} - {res['metadatas'][0][index]['end_time']}")
        print("----------")


res = query_chunks("Never want to give you up")
format_results(res)