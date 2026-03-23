import json
import ollama
import os
from dotenv import load_dotenv
load_dotenv()
model = os.getenv("OLLAMA_MODEL")

def take_notes(video_id):
    with open (f'data/'+video_id+'_chunks.json','r') as f:
        chunks = json.load(f)
    text = "\n\n".join([chunk['text'] for chunk in chunks])
    prompt = f"""You are a helpful assistant. You take notes in the most efficient and structured way, Structured as bullet points by topic.
            More detailed than summary and easy to reference later

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

    
