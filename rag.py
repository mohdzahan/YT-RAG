from query import query_chunks
import ollama

def ask(question):
    chunk = query_chunks(question)
    text = "\n\n".join(chunk['documents'][0])
    prompt = f"""You are a helpful assistant. Answer the question based only on the context below.
                    If the answer is not in the context, say "I couldn't find this in the videos."

                    Context:
                    {text}

                    Question: {question}"""
    

    response = ollama.chat(
    model='llama3.2',
    messages=[
        {"role": "user", "content": prompt}
    ]
    )
    print(response['message']['content'])
    return response

ask("who will never give you up?")
