import json
def chunk_transcript(video_id):
    buckets = {}
    chunks =[]
    with open(f"data/{video_id}.json",'r') as f:
        data = json.load(f)

    for line in data:
        time = line['time'].split(":")
        minutes = int(time[0])
        seconds = int(time[1])
        total_seconds = minutes * 60 + seconds
        
        bucket = total_seconds // 60

        if bucket not in buckets:
            buckets[bucket] = []
        buckets[bucket].append(line)
        
    for bucket_num, snippets in buckets.items():        
        start_time = snippets[0]['time']
        end_time = snippets[-1]['time']
        text = " ".join([s['text'] for s in snippets])
        chunk = {
        "video_id": video_id,
        "start_time": start_time,
        "end_time": end_time,
        "text": text,
        "timestamp_link": f"https://youtube.com/watch?v={video_id}&t={bucket_num * 60}"
    }
        chunks.append(chunk)
    
    with open(f'data/'+video_id+'_chunks.json','w') as f:
        json.dump(chunks, f, indent=4, ensure_ascii=False)     
        
    return chunks
