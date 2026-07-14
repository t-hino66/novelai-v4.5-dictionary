import urllib.request
import urllib.parse
import json
import time
import os
import sys

BASE_URL = "https://danbooru.donmai.us"
# Fetch high score and sensitive/explicit works (NSFW included)
DEFAULT_TAGS = "score:>=50" 
OUTPUT_FILE = "danbooru_raw_works.json"
TARGET_COUNT = 1000  # Default count to fetch
PAGE_SIZE = 100
DELAY = 1.0  # Respectful delay between API calls

def http_get(url, params=None):
    import ssl
    if params:
        query_string = urllib.parse.urlencode(params)
        url = f"{url}?{query_string}"
    
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'NovelAIPromptBuilder/1.0 (Mozilla compatible)'}
    )
    
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(req, timeout=15, context=context) as response:
        return json.loads(response.read().decode('utf-8'))

def fetch_posts(tags, target_count):
    posts = []
    page = 1
    
    print(f"Fetching posts from Danbooru for search tags: '{tags}'...")
    while len(posts) < target_count:
        url = f"{BASE_URL}/posts.json"
        params = {
            "tags": tags,
            "page": page,
            "limit": PAGE_SIZE
        }
        try:
            data = http_get(url, params=params)
            if not isinstance(data, list) or not data:
                print("No more posts returned.")
                break
                
            for item in data:
                # Keep only necessary fields to reduce JSON file size
                posts.append({
                    "id": item.get("id"),
                    "score": item.get("score"),
                    "rating": item.get("rating"),
                    "tag_string": item.get("tag_string"),
                    "tag_string_character": item.get("tag_string_character"),
                    "tag_string_artist": item.get("tag_string_artist"),
                    "file_ext": item.get("file_ext"),
                    "width": item.get("image_width"),
                    "height": item.get("image_height")
                })
                if len(posts) >= target_count:
                    break
            
            print(f"Page {page} fetched (Total posts count: {len(posts)})")
            page += 1
            time.sleep(DELAY)
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break
            
    return posts[:target_count]

def main():
    # Load existing data if exists
    existing_data = []
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            print(f"Loaded {len(existing_data)} existing items.")
        except Exception:
            print("Failed to load existing file, starting fresh.")

    existing_ids = {item["id"] for item in existing_data if "id" in item}

    target = TARGET_COUNT
    tags = DEFAULT_TAGS
    
    if len(sys.argv) > 1:
        try:
            target = int(sys.argv[1])
        except ValueError:
            pass
            
    if len(sys.argv) > 2:
        tags = sys.argv[2]
            
    # Fetch posts
    new_posts = fetch_posts(tags, target)
    
    new_details_count = 0
    for p in new_posts:
        if p["id"] not in existing_ids:
            existing_data.append(p)
            existing_ids.add(p["id"])
            new_details_count += 1
            
    if new_details_count > 0:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
        print(f"Saved database. Total posts: {len(existing_data)} (New: {new_details_count})")
    else:
        print("No new data to save.")

if __name__ == "__main__":
    main()
