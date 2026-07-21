import json
import os
import sys
import time
import urllib.request
import ssl

OUTPUT_FILE = "booru_extra_raw_works.json"

def fetch_booru_extra(target_count=300):
    existing_data = []
    existing_ids = set()

    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                existing_ids = {f"{item.get('source')}_{item.get('id')}" for item in existing_data if isinstance(item, dict)}
            print(f"Loaded {len(existing_data)} existing items from {OUTPUT_FILE}.")
        except Exception as e:
            print(f"Error loading existing data: {e}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    context = ssl._create_unverified_context()
    new_items = []

    # 1. Safebooru
    print(f"Fetching posts from Safebooru API...")
    safe_page = 0
    while len(new_items) < target_count // 2:
        url = f"https://safebooru.org/index.php?page=dapi&s=post&q=index&json=1&limit=100&pid={safe_page}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, context=context, timeout=15) as r:
                posts = json.loads(r.read().decode('utf-8'))
                if not posts:
                    break
                for p in posts:
                    uid = f"safebooru_{p.get('id')}"
                    if uid in existing_ids:
                        continue
                    
                    tags = p.get('tags', '')
                    sample_url = f"https://safebooru.org/images/{p.get('directory')}/{p.get('image')}" if p.get('directory') and p.get('image') else ""
                    
                    new_items.append({
                        "source": "safebooru",
                        "id": p.get('id'),
                        "tag_string": tags,
                        "width": p.get('width'),
                        "height": p.get('height'),
                        "image_url": sample_url
                    })
                    existing_ids.add(uid)
                safe_page += 1
                time.sleep(0.5)
        except Exception as e:
            print(f"Safebooru fetch error at page {safe_page}: {e}")
            break

    # 2. Yande.re
    print(f"Fetching posts from Yande.re API...")
    yande_page = 1
    while len(new_items) < target_count:
        url = f"https://yande.re/post.json?limit=100&page={yande_page}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, context=context, timeout=15) as r:
                posts = json.loads(r.read().decode('utf-8'))
                if not posts:
                    break
                for p in posts:
                    uid = f"yandere_{p.get('id')}"
                    if uid in existing_ids:
                        continue
                    
                    tags = p.get('tags', '')
                    sample_url = p.get('sample_url') or p.get('file_url') or ""
                    
                    new_items.append({
                        "source": "yandere",
                        "id": p.get('id'),
                        "tag_string": tags,
                        "width": p.get('width'),
                        "height": p.get('height'),
                        "image_url": sample_url
                    })
                    existing_ids.add(uid)
                yande_page += 1
                time.sleep(0.5)
        except Exception as e:
            print(f"Yande.re fetch error at page {yande_page}: {e}")
            break

    existing_data.extend(new_items)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

    print(f"Saved {OUTPUT_FILE}. Total: {len(existing_data)} (New: {len(new_items)})")

if __name__ == "__main__":
    count = 300
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            pass
    fetch_booru_extra(target_count=count)
