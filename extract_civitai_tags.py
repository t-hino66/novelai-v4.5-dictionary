import json
import os
import ssl
import sys
import time
import urllib.parse
import urllib.request


OUTPUT_FILE = "civitai_raw_works.json"
CIVITAI_API_URL = "https://civitai.com/api/v1/images"
CIVITAI_MODELS_API_URL = "https://civitai.com/api/v1/models"
HEADERS = {"User-Agent": "NovelAI-V4.5-Prompt-Dictionary/2.0"}


def verified_ssl_context():
    macos_ca = "/etc/ssl/cert.pem"
    return ssl.create_default_context(cafile=macos_ca if os.path.exists(macos_ca) else None)


def clean_image(item):
    """Keep only public generation evidence needed by the dictionary."""
    if not isinstance(item, dict):
        return None
    meta = item.get("meta") if isinstance(item.get("meta"), dict) else {}
    prompt = meta.get("prompt") or ""
    negative_prompt = meta.get("negativePrompt") or meta.get("negative_prompt") or ""
    if not prompt and not negative_prompt:
        return None
    model_version_ids = item.get("modelVersionIds") or []
    return {
        "id": item.get("id"),
        "post_id": item.get("postId"),
        "url": item.get("url") or "",
        "width": item.get("width"),
        "height": item.get("height"),
        "prompt": str(prompt),
        "negative_prompt": str(negative_prompt),
        "model": str(meta.get("Model") or meta.get("model") or item.get("baseModel") or ""),
        "model_version_ids": model_version_ids if isinstance(model_version_ids, list) else [],
        "sampler": meta.get("sampler") or "",
        "steps": meta.get("steps") or "",
        "cfg_scale": meta.get("cfgScale") or meta.get("cfg_scale") or "",
        "created_at": item.get("createdAt") or "",
        "nsfw": item.get("nsfw"),
        "stats": item.get("stats") if isinstance(item.get("stats"), dict) else {},
        "evidence_type": "generation_prompt",
    }


def clean_model(item):
    """Convert public model-listing tags into community metadata evidence."""
    if not isinstance(item, dict) or not item.get("id"):
        return None
    tags = [str(tag).strip() for tag in (item.get("tags") or []) if str(tag).strip()]
    if not tags:
        return None
    versions = item.get("modelVersions") or []
    first_version = versions[0] if versions and isinstance(versions[0], dict) else {}
    images = first_version.get("images") or []
    first_image = images[0] if images and isinstance(images[0], dict) else {}
    return {
        "id": item["id"], "post_id": None,
        "url": first_image.get("url") or "",
        "width": first_image.get("width"), "height": first_image.get("height"),
        "prompt": ",".join(tags), "negative_prompt": "",
        "model": item.get("name") or "", "model_version_ids": [],
        "sampler": "", "steps": "", "cfg_scale": "",
        "created_at": first_version.get("publishedAt") or "", "nsfw": item.get("nsfw"),
        "stats": item.get("stats") if isinstance(item.get("stats"), dict) else {},
        "evidence_type": "model_tags",
    }


def fetch_model_tag_evidence(target_count, existing_ids):
    results = []
    cursor = None
    page = 1
    while len(results) < target_count:
        params = {"limit": min(100, target_count - len(results)),
                  "sort": "Highest Rated", "period": "AllTime"}
        if cursor:
            params["cursor"] = cursor
        request = urllib.request.Request(
            f"{CIVITAI_MODELS_API_URL}?{urllib.parse.urlencode(params)}", headers=HEADERS
        )
        try:
            with urllib.request.urlopen(request, timeout=30, context=verified_ssl_context()) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            print(f"Civitai model fetch error on page {page}: {error}")
            break
        for item in payload.get("items") or []:
            cleaned = clean_model(item)
            if not cleaned or cleaned["id"] in existing_ids:
                continue
            results.append(cleaned)
            existing_ids.add(cleaned["id"])
            if len(results) >= target_count:
                break
        print(f"Model page {page} fetched (new tagged models: {len(results)})")
        cursor = (payload.get("metadata") or {}).get("nextCursor")
        page += 1
        if not cursor:
            break
        time.sleep(0.5)
    return results


def fetch_civitai_images(target_count=200):
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
    next_cursor = None
    next_page = None
    page_number = 1
    print(f"Fetching public prompt metadata from Civitai (target: {target_count})...")

    while len(new_items) < target_count:
        params = {"limit": min(200, target_count - len(new_items)), "sort": "Most Reactions"}
        if next_cursor:
            params["cursor"] = next_cursor
            url = f"{CIVITAI_API_URL}?{urllib.parse.urlencode(params)}"
            request = urllib.request.Request(url, headers=HEADERS)
        elif next_page:
            # The API currently publishes both nextCursor and nextPage. Prefer the cursor,
            # but keep the documented next-page URL as a compatibility fallback.
            url = next_page
            request = urllib.request.Request(url, headers=HEADERS)
        else:
            url = f"{CIVITAI_API_URL}?{urllib.parse.urlencode(params)}"
            request = urllib.request.Request(url, headers=HEADERS)

        try:
            with urllib.request.urlopen(request, timeout=30, context=verified_ssl_context()) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            print(f"Civitai fetch error on page {page_number}: {error}")
            break

        items = payload.get("items") or []
        metadata = payload.get("metadata") or {}
        if not items:
            break
        for item in items:
            cleaned = clean_image(item)
            if not cleaned or not cleaned.get("id") or cleaned["id"] in existing_ids:
                continue
            new_items.append(cleaned)
            existing_ids.add(cleaned["id"])
            if len(new_items) >= target_count:
                break

        next_cursor = metadata.get("nextCursor")
        next_page = metadata.get("nextPage")
        print(f"Page {page_number} fetched (new prompt-bearing images: {len(new_items)})")
        page_number += 1
        if not next_cursor and not next_page:
            break
        if page_number > 3 and not new_items:
            print("Anonymous image responses contain no prompt metadata; using public model tags instead.")
            break
        time.sleep(0.5)

    if not new_items:
        new_items = fetch_model_tag_evidence(target_count, existing_ids)

    existing_data.extend(new_items)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=2)
    print(f"Saved {len(existing_data)} entries to {OUTPUT_FILE} (new: {len(new_items)})")


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    fetch_civitai_images(count)
