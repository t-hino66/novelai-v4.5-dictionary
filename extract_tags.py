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

def http_get(url, params=None):
    import ssl
    if params:
        query_string = urllib.parse.urlencode(params)
        url = f"{url}?{query_string}"
    
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
    )
    
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(req, timeout=10, context=context) as response:
        return json.loads(response.read().decode('utf-8'))

def get_monthly_rank_works(target_count):
    works = []
    page = 1
    
    print(f"Fetching monthly rank IDs for '{SEARCH_QUERY}'...")
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
                print("No more items found.")
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
            
            print(f"Page {page} fetched (Total ID count: {len(works)})")
            page += 1
            time.sleep(DELAY)
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break
            
    return works[:target_count]

def get_work_details(work_id):
    url = f"{BASE_URL}/api/work/{work_id}"
    try:
        return http_get(url)
    except Exception as e:
        print(f"Failed to fetch details for work ID {work_id}: {e}")
        return None

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

    existing_ids = {item["work"]["id"] for item in existing_data if "work" in item}

    target = TARGET_COUNT
    if len(sys.argv) > 1:
        try:
            target = int(sys.argv[1])
        except ValueError:
            pass
            
    # Fetch rank works up to target
    works_list = get_monthly_rank_works(target)
    print(f"Found {len(works_list)} works to process.")

    new_details_count = 0
    
    try:
        for idx, work_summary in enumerate(works_list, 1):
            work_id = work_summary["id"]
            if work_id in existing_ids:
                continue
                
            print(f"[{idx}/{len(works_list)}] Fetching detail... ID: {work_id}")
            detail = get_work_details(work_id)
            if detail:
                existing_data.append(detail)
                existing_ids.add(work_id)
                new_details_count += 1
                
                if new_details_count % 10 == 0:
                    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                        json.dump(existing_data, f, ensure_ascii=False, indent=2)
                        
            time.sleep(DELAY)
            
    except KeyboardInterrupt:
        print("\nInterrupted by user. Saving progress...")
    finally:
        if new_details_count > 0:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
            print(f"Saved file. Total: {len(existing_data)} (New: {new_details_count})")
        else:
            print("No new data to save.")

if __name__ == "__main__":
    main()
