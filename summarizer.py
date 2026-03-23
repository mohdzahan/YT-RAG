import json
import ollama
import os
from dotenv import load_dotenv
load_dotenv()
model = os.getenv("OLLAMA_MODEL")

def summarize(video_id):
    with open (f'data/'+video_id+'_chunks.json','r') as f:
        chunks = json.load(f)
    text = "\n\n".join([chunk['text'] for chunk in chunks])
    prompt = f"""You are a helpful assistant. Summarize the text strictly based on the context below.
    keep it concised and structured, cover the main topics

                    Context:
                    {text}

                    """

    response = ollama.chat(
    model=model,
    messages=[
        {"role": "user", "content": prompt}
    ]
    )
    print(response['message']['content'])
    
    return response

    
