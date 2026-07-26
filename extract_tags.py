import urllib.request
import urllib.parse
import json
import time
import os
import sys

BASE_URL = "https://aitag.win"
SEARCH_QUERY = "NovelAI Diffusion V4.5"
OUTPUT_FILE = "extracted_works.json"
TARGET_COUNT = 1000  # Default target count
PAGE_SIZE = 60
DELAY = 0.5  # API call delay in seconds

def http_get(url, params=None, retries=3):
    import ssl
    if params:
        query_string = urllib.parse.urlencode(params)
        url = f"{url}?{query_string}"
    
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
    )
    
    context = ssl._create_unverified_context()
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=12, context=context) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            if attempt == retries - 1:
                raise e
            time.sleep(1.0 * (attempt + 1))

def get_monthly_rank_works(target_count):
    works = []
    page = 1
    
    print(f"Fetching monthly rank IDs for '{SEARCH_QUERY}'...", flush=True)
    while len(works) < target_count:
        url = f"{BASE_URL}/api/rank/monthly"
        params = {
            "q": SEARCH_QUERY,
            "page": page,
            "page_size": PAGE_SIZE
        }
        try:
            data = http_get(url, params=params)
            items = data.get("items", [])
            if not items:
                print("No more items found.", flush=True)
                break
                
            for item in items:
                works.append({
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "tags": item.get("tags"),
                    "AI_type": item.get("AI_type")
                })
                if len(works) >= target_count:
                    break
            
            print(f"Page {page} fetched (Total ID count: {len(works)})", flush=True)
            page += 1
            time.sleep(DELAY)
        except Exception as e:
            print(f"Error fetching page {page}: {e}", flush=True)
            break
            
    return works[:target_count]

def clean_detail(detail):
    if not isinstance(detail, dict):
        return None
    work = detail.get("work", {})
    images = detail.get("images", [])
    
    cleaned_images = []
    for img in images:
        if not isinstance(img, dict):
            continue
        cleaned_images.append({
            "model": img.get("model"),
            "prompt_text": img.get("prompt_text"),
            "negative_prompt": img.get("negative_prompt"),
            "ai_json": img.get("ai_json"),
            "image_url": img.get("image_url") or img.get("sample_url")
        })
        
    return {
        "work": {
            "id": work.get("id"),
            "title": work.get("title"),
            "tags": work.get("tags")
        },
        "images": cleaned_images
    }

def get_work_details(work_id):
    url = f"{BASE_URL}/api/work/{work_id}"
    try:
        data = http_get(url)
        return clean_detail(data)
    except Exception as e:
        print(f"Failed to fetch details for work ID {work_id}: {e}", flush=True)
        return None

def main():
    # Load existing data if exists
    existing_data = []
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            print(f"Loaded {len(existing_data)} existing items.", flush=True)
        except Exception:
            print("Failed to load existing file, starting fresh.", flush=True)

    existing_ids = {item["work"]["id"] for item in existing_data if "work" in item}

    target = TARGET_COUNT
    if len(sys.argv) > 1:
        try:
            target = int(sys.argv[1])
        except ValueError:
            pass
            
    # Fetch rank works up to target
    works_list = get_monthly_rank_works(target)
    print(f"Found {len(works_list)} works to process.", flush=True)

    new_details_count = 0
    consecutive_errors = 0
    
    try:
        for idx, work_summary in enumerate(works_list, 1):
            work_id = work_summary["id"]
            if work_id in existing_ids:
                continue
                
            print(f"[{idx}/{len(works_list)}] Fetching detail... ID: {work_id}", flush=True)
            detail = get_work_details(work_id)
            if detail:
                existing_data.append(detail)
                existing_ids.add(work_id)
                new_details_count += 1
                consecutive_errors = 0
                
                if new_details_count % 10 == 0:
                    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                        json.dump(existing_data, f, ensure_ascii=False, separators=(',', ':'))
            else:
                consecutive_errors += 1
                if consecutive_errors >= 5:
                    print("Too many consecutive errors. Stopping fetch gracefully to save progress.", flush=True)
                    break
                        
            time.sleep(DELAY)
            
    except KeyboardInterrupt:
        print("\nInterrupted by user. Saving progress...", flush=True)
    finally:
        if new_details_count > 0:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, separators=(',', ':'))
            print(f"Saved file. Total: {len(existing_data)} (New: {new_details_count})", flush=True)
        else:
            print("No new data to save.", flush=True)

if __name__ == "__main__":
    main()
