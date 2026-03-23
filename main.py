from rag import ask
from embedder import embed_and_store
from chunker import chunk_transcript
from transcript_fetcher import get_video_id, get_transcript, format_transcript
from summarizer import summarize
from note_taking import take_notes

url = input("Enter YouTube URL: ")
video_id = get_video_id(url)
transcript = get_transcript(video_id)
format_transcript(transcript, video_id)
chunk_transcript(video_id)
embed_and_store(video_id)

while True:

    qns = input("""
What do you want to do?
                
    1. Ask questions
    2. Summarize video
    3. Take notes
    4. Exit
                
    --> """)
    
    match qns.lower():
        case "1":
            question = input("Ask a qns -> ")
            mode = input("Mode (strict/extended): ").strip().lower()

            ask(question,mode)
        case "2":
            summarize(video_id)

        case "3":
            take_notes(video_id)
        case "exit":
            break
        case _:
            print("Invalid option. Please choose 1, 2, 3 or exit.")


   
        
    