from rag import ask
from embedder import embed_and_store
from chunker import chunk_transcript
from transcript_fetcher import get_video_id, get_transcript, format_transcript

url = input("Enter YouTube URL: ")
video_id = get_video_id(url)
transcript = get_transcript(video_id)
format_transcript(transcript, video_id)
chunk_transcript(video_id)
embed_and_store(video_id)

while True:
    qns = input("Ask a question: ")
    if qns.lower() == "exit":
        break
    ask(qns)