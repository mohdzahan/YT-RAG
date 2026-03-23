from query import query_chunks
import ollama

def ask(question, mode = "strict"):
    chunk = query_chunks(question)
    text = "\n\n".join(chunk['documents'][0])
    if mode == "strict":
        prompt = f"""You are a helpful assistant. Answer the question based only on the context below.
                    If the answer is not in the context, say "I couldn't find this in the videos. Try extended mode to nkow further more"

                    Context:
                    {text}

                    Question: {question}"""
    else: 
        prompt = f"""You are a helpful assistant. Answer the question based primarily on the context below.
                    If the answer is not in the context, supplement it with your own knowledge, make sure the answers are valid and 
                    you are are not hallucinating.

                    Do indicate when its going beyond what the video must have talked about.

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

#ask("who will never give you up?")
