from sentence_transformers import SentenceTransformer
import chromadb
import json


st = SentenceTransformer('BAAI/bge-small-en')
cd = chromadb.PersistentClient(path="./chroma_db")

def load_data(video_id):
    with open(video_id+'_chunks.json','r') as f:
        chunks = json.load(f)
        return chunks
    

def embed_and_store(video_id):


    try:
        cd.delete_collection("kt_videos")
    except:
        pass
    collection = cd.create_collection("kt_videos")
    chunks = load_data(video_id)
    for index, chunk in enumerate(chunks):
        embedding = st.encode(chunk['text'])
        collection.add(
            ids=[f"{video_id}_chunk_{index}"],
            documents=[chunk['text']],
            embeddings=[embedding.tolist()],
            metadatas=[{
                "video_id": chunk['video_id'],
                "start_time": chunk['start_time'],
                "end_time": chunk['end_time'],
                "timestamp_link": chunk['timestamp_link']
            }]
        )

        print(f"Stored chunk {index}")


#embed_and_store('some_other_video')