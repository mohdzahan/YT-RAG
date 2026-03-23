from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
import json

def get_video_id(video_url):
    video_id = urlparse(video_url)
    params = parse_qs(video_id.query)
    return params['v'][0]

def get_transcript(video_id):
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    return transcript
     
def format_transcript(transcript,video_id):
    file_name = video_id+'.json'
    data = []
    for snippet in transcript:
        minute = snippet.start//60
        second = snippet.start%60
        time_stamp = f"{int(minute)}:{int(second):02d}"
        json_string = {"time": time_stamp , "text":snippet.text}  
        data.append(json_string)
    with open(file_name,'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)        



#video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=120s"

#video_id = get_video_id(video_url)
#transcript = get_transcript(video_id)
#format_transcript(transcript,video_id)