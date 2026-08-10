import json
import os
import ssl
import sys
import time
import urllib.parse
import urllib.request


OUTPUT_FILE = "aibooru_raw_works.json"
AIBOORU_API_URL = "https://aibooru.online/posts.json"
HEADERS = {"User-Agent": "NovelAI-V4.5-Prompt-Dictionary/2.0"}


def verified_ssl_context():
    macos_ca = "/etc/ssl/cert.pem"
    return ssl.create_default_context(cafile=macos_ca if os.path.exists(macos_ca) else None)


def clean_post(post):
    if not isinstance(post, dict) or not post.get("id") or not post.get("tag_string"):
        return None
    return {
        "id": post["id"],
        "tag_string": post.get("tag_string") or "",
        "tag_string_general": post.get("tag_string_general") or "",
        "tag_string_character": post.get("tag_string_character") or "",
        "tag_string_copyright": post.get("tag_string_copyright") or "",
        "tag_string_artist": post.get("tag_string_artist") or "",
        "tag_string_model": post.get("tag_string_model") or "",
        "rating": post.get("rating") or "",
        "score": post.get("score") or 0,
        "width": post.get("image_width"),
        "height": post.get("image_height"),
        "image_url": post.get("large_file_url") or post.get("file_url") or post.get("preview_file_url") or "",
        "created_at": post.get("created_at") or "",
    }


def fetch_aibooru_posts(target_count=500):
    existing_data = []
    existing_ids = set()
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, encoding="utf-8") as file:
                existing_data = json.load(file)
            existing_ids = {item.get("id") for item in existing_data if isinstance(item, dict)}
            print(f"Loaded {len(existing_data)} existing items from {OUTPUT_FILE}.")
        except (OSError, json.JSONDecodeError) as error:
            print(f"Error loading existing data: {error}")

    new_items = []
    page = 1
    print(f"Fetching public annotations from AIbooru (target: {target_count})...")
    while len(new_items) < target_count:
        params = {"limit": min(200, target_count - len(new_items)), "page": page}
        request = urllib.request.Request(
            f"{AIBOORU_API_URL}?{urllib.parse.urlencode(params)}", headers=HEADERS
        )
        try:
            with urllib.request.urlopen(request, timeout=30, context=verified_ssl_context()) as response:
                posts = json.loads(response.read().decode("utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            print(f"AIbooru fetch error on page {page}: {error}")
            break
        if not isinstance(posts, list) or not posts:
            break
        for post in posts:
            cleaned = clean_post(post)
            if not cleaned or cleaned["id"] in existing_ids:
                continue
            new_items.append(cleaned)
            existing_ids.add(cleaned["id"])
            if len(new_items) >= target_count:
                break
        print(f"Page {page} fetched (new annotated posts: {len(new_items)})")
        page += 1
        time.sleep(0.5)

    existing_data.extend(new_items)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=2)
    print(f"Saved {len(existing_data)} entries to {OUTPUT_FILE} (new: {len(new_items)})")


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    fetch_aibooru_posts(count)
