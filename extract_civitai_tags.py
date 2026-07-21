import json
import os
import sys
import time
import urllib.request
import urllib.parse
import ssl

OUTPUT_FILE = "civitai_raw_works.json"
CIVITAI_API_URL = "https://civitai.com/api/v1/images"

def fetch_civitai_images(target_count=200):
    existing_data = []
    existing_ids = set()

    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                existing_ids = {item["id"] for item in existing_data if isinstance(item, dict) and "id" in item}
            print(f"Loaded {len(existing_data)} existing items from {OUTPUT_FILE}.")
        except Exception as e:
            print(f"Error loading existing data: {e}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    context = ssl._create_unverified_context()
    items_fetched = 0
    next_cursor = None
    page = 1
    new_items = []

    print(f"Fetching images from Civitai API (Target: {target_count})...")

    while len(new_items) < target_count:
        params = {
            "limit": 100,
            "sort": "Most Reactions"
        }
        if next_cursor:
            params["cursor"] = next_cursor

        url = f"{CIVITAI_API_URL}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(req, context=context, timeout=15) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                items = data.get("items", [])
                metadata = data.get("metadata", {})
                next_cursor = metadata.get("nextCursor")

                if not items:
                    print("No more items returned from Civitai API.")
                    break

                for item in items:
                    if not isinstance(item, dict):
                        continue
                    item_id = item.get("id")
                    if not item_id or item_id in existing_ids:
                        continue

                    meta = item.get("meta")
                    if not isinstance(meta, dict):
                        meta = {}

                    prompt = meta.get("prompt") or ""
                    neg_prompt = meta.get("negativePrompt") or meta.get("negative_prompt") or ""

                    # We want entries with at least prompt or negative prompt
                    if not prompt and not neg_prompt:
                        continue

                    entry = {
                        "id": item_id,
                        "url": item.get("url", ""),
                        "width": item.get("width"),
                        "height": item.get("height"),
                        "prompt": str(prompt),
                        "negative_prompt": str(neg_prompt),
                        "sampler": meta.get("sampler", ""),
                        "steps": meta.get("steps", ""),
                        "cfgScale": meta.get("cfgScale", ""),
                        "stats": item.get("stats", {})
                    }

                    new_items.append(entry)
                    existing_ids.add(item_id)
                    if len(new_items) >= target_count:
                        break

                print(f"Page {page} fetched (Total new items count: {len(new_items)})")
                page += 1

                if not next_cursor:
                    print("No nextCursor found in metadata.")
                    break

                time.sleep(0.5)

        except Exception as e:
            print(f"Error fetching page {page} from Civitai API: {e}")
            break

    existing_data.extend(new_items)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

    print(f"Saved database to {OUTPUT_FILE}. Total entries: {len(existing_data)} (New: {len(new_items)})")

if __name__ == "__main__":
    count = 200
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            pass
    fetch_civitai_images(target_count=count)
