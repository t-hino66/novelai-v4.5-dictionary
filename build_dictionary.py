import json
import csv
import os
import re
import urllib.request
from collections import Counter

# Inputs/Outputs
INPUT_AITAG = "extracted_works.json"
INPUT_DANBOORU = "danbooru_raw_works.json"
DATABASE_JSON = "novelai_v4_5_database.json"
DATABASE_CSV = "novelai_v4_5_database.csv"
TAG_DICT_CSV = "novelai_v4_5_tag_dictionary.csv"
MD_DICT_FILE = "novelai_v4_5_dictionary.md"

MANUAL_JP_URL = "https://raw.githubusercontent.com/boorutan/booru-japanese-tag/master/danbooru-jp.csv"
MACHINE_JP_URL = "https://raw.githubusercontent.com/boorutan/booru-japanese-tag/master/danbooru-machine-jp.csv"
MANUAL_JP_FILE = "danbooru-jp.csv"
MACHINE_JP_FILE = "danbooru-machine-jp.csv"

# Expert overrides for anime image generation context
AI_OVERRIDES = {
    "ultra-detailed": "\u6975\u3081\u3066\u8a73\u7d30\u306a\u63cf\u304d\u8fbc\u307f",
    "ultra detailed": "\u6975\u3081\u3066\u8a73\u7d30\u306a\u63cf\u304d\u8fbc\u307f",
    "year 2025": "2025\u5e74 (\u6295\u7a3f\u30fb\u5236\u4f5c\u5e74\u6307\u5b9a)",
    "year 2024": "2024\u5e74 (\u6295\u7a3f\u30fb\u5236\u4f5c\u5e74\u6307\u5b9a)",
    "year 2023": "2023\u5e74 (\u6295\u7a3f\u30fb\u5236\u4f5c\u5e74\u6307\u5b9a)",
    "in_idolmaster_style": "\u30a2\u30a4\u30c9\u30eb\u30de\u30b9\u30bf\u30fc\u98a8\u306e\u7d75\u67c4",
    "girl": "\u5973\u306e\u5b50",
    "high resolution": "\u9ad8\u89e3\u50cf\u5ea6",
    "8k": "8K\u89e3\u50cf\u5ea6 (\u30af\u30aa\u30ea\u30c6\u30a3\u30bf\u30b0)",
    "4k": "4K\u89e3\u50cf\u5ea6 (\u30af\u30aa\u30ea\u30c6\u30a3\u30bf\u30b0)",
    "close-up": "\u63a5\u5199 (\u30af\u30ed\u30fc\u30ba\u30a2\u30c3\u30d7)",
    "close_up": "\u63a5\u5199 (\u30af\u30ed\u30fc\u30ba\u30a2\u30c3\u30d7)",
    "masterpiece": "\u502a\u4f5c (\u57fa\u672c\u30af\u30aa\u30ea\u30c6\u30a3\u30bf\u30b0)",
    "very aesthetic": "\u975e\u5e38\u306b\u7f8e\u3057\u3044 (\u7f8e\u7684\u30bf\u30b0)",
    "ahegao": "\u30a2\u30d8\u9854",
    "ai-assisted": "AI\u652f\u63f4\u753b\u50cf",
    "ai-generated": "AI\u751f\u6210\u753b\u50cf",
    "official art": "\u516c\u5f0f\u30a4\u30e9\u30b9\u30c8\u30fb\u516c\u5f0f\u753b\u50cf",
    "looking at viewer": "\u30ab\u30e1\u30e9\u76ee\u7dda (\u3053\u3061\u3089\u3092\u898b\u3064\u3081\u308b)",
    "spread legs": "\u958b\u811a\u30dd\u30fc\u30ba",
    "nude": "\u88f8 (\u30cc\u30fc\u30c9)",
    "sweat": "\u6c57 (\u808c\u306e\u63cf\u5199)",
    "navel": "\u304a\u3078\u305d",
    "cleavage": "\u803c\u306e\u8c37\u9593",
    "large breasts": "\u5de8\u4e73",
    "medium breasts": "\u4e2d\u4e73 (\u666e\u901a\u306e\u803c)",
    "small breasts": "\u5fae\u4e73\u30fb\u8ca2\u4e73",
    "flat chest": "\u3055\u305b\u3061\u30fb\u8ca2\u4e73",
    "skirt": "\u30b9\u30ab\u30fc\u30c8",
    "panties": "\u30d1\u30f3\u30c6\u30a3 (\u4e0b\u7740)",
    "white panties": "\u767d\u30d1\u30f3\u30c6\u30a3",
    "striped panties": "\u3057\u307e\u30d1\u30f3\u30c6\u30a3",
    "thighhighs": "\u30a5\u30a4\u30cf\u30a4\u30bd\u30c3\u30af\u30b9",
    "knee highs": "\u819d\u4e0a\u30bd\u30c3\u30af\u30b9",
    "bare shoulders": "\u9732\u51fa\u3057\u305f\u80a9",
    "underwear": "\u4e0b\u7740",
    "swimsuit": "\u6c30\u7740",
    "bikini": "\u30d3\u30ad\u30cb",
    "school uniform": "\u5236\u670d",
    "serafuku": "\u30bb\u30fc\u30e9\u30fc\u670d",
    "sailor suit": "\u30bb\u30fc\u30e9\u30fc\u670d",
    "blazer": "\u30d6\u30ec\u30b6\u30fc",
    "pantihose": "\u30d5\u30f3\u30b9\u30c8",
    "pantyhose": "\u30d5\u30f3\u30b9\u30c8",
    "black pantyhose": "\u9ed2\u30d5\u30f3\u30b9\u30c8",
    "white pantyhose": "\u767d\u30d5\u30f3\u30b9\u30c8",
    "stockings": "\u30b9\u30c8\u30c3\u30ad\u30f3\u30b0",
    "thighs": "\u592a\u3082\u306e",
    "ass": "\u304a\u5c3b",
    "butt": "\u304a\u5c3b",
    "pussy": "\u5272\u308c\u76ee\u30fb\u79d8\u90e8",
    "breasts out": "\u88f8\u803c (\u803c\u3092\u5916\u306b\u51fa\u3059)",
    "under breast": "\u4e0b\u4e73 (\u30a2\u30f3\u30c0\u30fc\u30d6\u30ec\u30b9\u30c8)",
    "side breast": "\u6a2a\u4e73 (\u30b5\u30a4\u30c9\u30d6\u30ec\u30b9\u30c8)",
    "armpits": "\u8107 (\u308f\u305d)",
    "sitting": "\u5ea7\u3063\u3066\u3044\u308b",
    "standing": "\u7acb\u3063\u3066\u3044\u308b",
    "lying": "\u6a2a\u305f\u308f\u3063\u3066\u3044\u308b",
    "lying on back": "\u4ef0\u5411\u3051",
    "lying on stomach": "\u3046\u3064\u4f0f\u305b",
    "kneeling": "\u819d\u7acb\u3061",
    "squatting": "\u3057\u3083\u305c\u3093\u3060\u308a",
    "looking back": "\u632f\u308a\u8fd4\u308b",
    "head shot": "\u982d\u90e8\u30a2\u30c3\u30d7",
    "portrait": "\u8096\u50cf\u753b\u98a8 (\u80a9\u304b\u3089\u4e0a)",
    "upper body": "\u4e0a\u534a\u8eab",
    "cowboy shot": "\u817f\u304b\u3089\u4e0a\u306e\u30a2\u30f3\u30b0\u30eb",
    "full body": "\u5168\u8eab\u306e\u63cf\u5199",
    "wide shot": "\u5f15\u304d\u306e\u69cb\u56f3",
    "indoors": "\u5ba4\u5185",
    "outdoors": "\u5c4b\u5916",
    "bedroom": "\u5bdd\u5ba4",
    "living room": "\u30ea\u30d3\u30f3\u30b0",
    "bathroom": "\u6d74\u5ba4\u30fb\u304a\u98a8\u5442\u5834",
    "classroom": "\u6559\u5ba4",
    "beach": "\u5c42",
    "pool": "\u30d7\u30fc\u30eb",
    "bed": "\u30d9\u30c3\u30c9",
    "chair": "\u6905\u5b50",
    "sofa": "\u30bd\u30d5\u30a1",
    "night": "\u591c",
    "day": "\u663c",
    "sky": "\u7a7a",
    "sunset": "\u5915\u65e5",
    "simple background": "\u30b8\u30f3\u30d7\u30eb\u306a\u80cc\u666f",
    "white background": "\u767d\u80cc\u666f",
    "black background": "\u9ed2\u80cc\u666f",
    "transparent background": "\u8fe0\u660e\u80cc\u666f",
    "bokeh": "\u80cc\u666f\u306e\u307c\u3051\u3001\u7389\u307c\u3051",
    "depth of field": "\u88ab\u5199\u754c\u6df1\u5ea6 (\u80cc\u666f\u306e\u307c\u3051)",
    "sunlight": "\u65e5\u5149",
    "lens flare": "\u30ec\u30f3\u30ba\u30d5\u30ec\u30a2",
    "cinematic lighting": "\u6620\u753b\u98a8\u306e\u30c9\u30e9\u30de\u30c1\u30c3\u30af\u306a\u7167\u660e",
    "volumetric lighting": "\u7a7a\u6c17\u611f\u306e\u3042\u308b\u5149 (\u5149\u306e\u7b4b)",
    "backlighting": "\u9006\u5149",
    "rim lighting": "\u8f2a\u90ed\u3092\u969b\u7acb\u305b\u308b\u5149 (\u30ea\u30e0\u30e9\u30a4\u30c8)",
}

QUALITY_KEYWORDS = {'masterpiece', 'best quality', 'very aesthetic', 'absurdres', 'newest', 'highres', 'normal quality', 'low quality', 'worst quality', 'artistic error', 'aesthetic'}
STYLE_KEYWORDS = {'anime coloring', 'official style', 'game cg', 'sketch', 'monochrome', 'watercolor', 'flat color'}

def download_file(url, filepath):
    if os.path.exists(filepath):
        return
    print(f"Downloading reference translation file: {url} -> {filepath}...")
    import ssl
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=context) as response, open(filepath, 'wb') as out_file:
        out_file.write(response.read())

def get_category(tag):
    tag_lower = tag.lower()
    if tag_lower in QUALITY_KEYWORDS or "quality" in tag_lower or "aesthetic" in tag_lower:
        return "Quality"
    elif tag_lower in STYLE_KEYWORDS or tag_lower.startswith("artist:") or "style" in tag_lower:
        return "Style"
    elif any(word in tag_lower for word in {'uniform', 'dress', 'skirt', 'panties', 'shirt', 'socks', 'shoes', 'boots', 'blazer', 'pantihose', 'pantyhose', 'stockings', 'swimsuit', 'bikini', 'underwear', 'bra', 'clothes', 'clothing', 'hat', 'ribbon', 'tie'}):
        return "Clothing"
    elif any(word in tag_lower for word in {'sitting', 'standing', 'lying', 'leaning', 'holding', 'looking at viewer', 'looking back', 'kneeling', 'squatting', 'spread legs', 'arms', 'legs', 'pose', 'touching', 'hand'}):
        return "Pose"
    elif any(word in tag_lower for word in {'background', 'indoors', 'outdoors', 'bedroom', 'room', 'sky', 'night', 'day', 'scenery', 'wall', 'bed', 'chair', 'floor', 'window', 'nature', 'forest', 'street', 'light', 'shadow', 'sunlight'}):
        return "Background"
    elif any(word in tag_lower for word in {'girl', 'boy', 'solo', 'eyes', 'hair', 'breast', 'skin', 'blush', 'smile', 'mouth', 'face', 'cleavage', 'navel', 'thighs'}):
        return "Character"
    else:
        return "Others"

def clean_tag(tag):
    tag = tag.strip()
    tag = re.sub(r'^\d+(\.\d+)?::', '', tag)
    tag = re.sub(r'::$', '', tag)
    tag = re.sub(r'[(){}\[\]]', '', tag)
    tag = re.sub(r':\d+(\.\d+)?$', '', tag)
    return tag.strip()

def load_translation_dict():
    trans_dict = {}
    try:
        download_file(MANUAL_JP_URL, MANUAL_JP_FILE)
        download_file(MACHINE_JP_URL, MACHINE_JP_FILE)
    except Exception as e:
        print(f"Failed to download translation lists: {e}")

    # Load manual translations
    if os.path.exists(MANUAL_JP_FILE):
        with open(MANUAL_JP_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    tag = row[0].strip().lower()
                    meaning = row[1].strip()
                    if tag and meaning:
                        trans_dict[tag] = meaning
                        
    # Load machine translations
    if os.path.exists(MACHINE_JP_FILE):
        with open(MACHINE_JP_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    tag = row[0].strip().lower()
                    meaning = row[1].strip()
                    if tag and meaning and tag not in trans_dict:
                        trans_dict[tag] = meaning
                        
    return trans_dict

def get_meaning(tag, trans_dict):
    tag_lower = tag.lower().strip()
    if tag_lower in AI_OVERRIDES:
        return AI_OVERRIDES[tag_lower]
        
    if tag_lower.startswith("artist:"):
        return f"\u7d75\u5e2b: {tag[7:]}\u98a8"
        
    if tag_lower.startswith("in_") and tag_lower.endswith("_style"):
        style_name = tag[3:-6].replace("_", " ")
        return f"{style_name}\u98a8\u306e\u7d75\u67c4"
        
    hair_match = re.match(r'^(black|white|blonde|brown|silver|grey|red|blue|green|pink|purple|orange|yellow|light\s+blue|dark\s+blue|light\s+green|dark\s+green)\s+hair$', tag_lower)
    if hair_match:
        color_map = {
            "black": "\u9ed2", "white": "\u767d", "blonde": "\u91d1", "brown": "\u8336",
            "silver": "\u9280", "grey": "\u7070", "red": "\u8d64", "blue": "\u9752",
            "green": "\u7d20\u9ed2", "pink": "\u6843\u8272", "purple": "\u7d2b",
            "orange": "\u6a59", "yellow": "\u9ec4",
            "light blue": "\u6c34\u8272", "dark blue": "\u5c3e\u9752",
            "light green": "\u82e5\u8349\u8272", "dark green": "\u6df1\u7d20"
        }
        color_jp = color_map.get(hair_match.group(1), hair_match.group(1))
        return f"{color_jp}\u9aea"

    eyes_match = re.match(r'^(black|white|blonde|brown|silver|grey|red|blue|green|pink|purple|orange|yellow|light\s+blue|dark\s+blue|light\s+green|dark\s+green)\s+eyes$', tag_lower)
    if eyes_match:
        color_map = {
            "black": "\u9ed2", "white": "\u767d", "blonde": "\u91d1", "brown": "\u8336",
            "silver": "\u9280", "grey": "\u7070", "red": "\u8d64", "blue": "\u9752",
            "green": "\u7d20\u9ed2", "pink": "\u6843\u8272", "purple": "\u7d2b",
            "orange": "\u6a59", "yellow": "\u9ec4",
            "light blue": "\u6c34\u8272", "dark blue": "\u5c3e\u9752",
            "light green": "\u82e5\u8349\u8272", "dark green": "\u6df1\u7d20"
        }
        color_jp = color_map.get(eyes_match.group(1), eyes_match.group(1))
        return f"{color_jp}\u306e\u76ee"

    lookup_tag = tag_lower.replace(" ", "_")
    if tag_lower in trans_dict:
        m = trans_dict[tag_lower]
        if m == "\u9589\u3058\u308b" and "close" in tag_lower:
            return "\u63a5\u5199 (\u30af\u30ed\u30fc\u30ba\u30a2\u30c3\u30d7)"
        return m
    elif lookup_tag in trans_dict:
        m = trans_dict[lookup_tag]
        if m == "\u9589\u3058\u308b" and "close" in tag_lower:
            return "\u63a5\u5199 (\u30af\u30ed\u30ba\u30a2\u30c3\u30d7)"
        return m

    return ""

def process_data():
    flat_records = []
    all_tags = []
    total_images = 0

    # 1. Parse AITAG (NovelAI 4.5) data if exists
    if os.path.exists(INPUT_AITAG):
        print(f"Parsing NovelAI gallery data: {INPUT_AITAG}...")
        with open(INPUT_AITAG, 'r', encoding='utf-8') as f:
            raw_works = json.load(f)
            
        for item in raw_works:
            work = item.get("work", {})
            images = item.get("images", [])
            
            work_id = work.get("id")
            title = work.get("title", "")
            pixiv_tags = work.get("tags", [])
            
            for img in images:
                model = img.get("model", "")
                if "NovelAI Diffusion V4.5" not in model:
                    continue
                    
                total_images += 1
                prompt = img.get("prompt_text", "")
                neg_prompt = img.get("negative_prompt", "")
                
                clean_prompt_list = [clean_tag(t) for t in prompt.split(",") if t.strip()]
                clean_neg_list = [clean_tag(t) for t in neg_prompt.split(",") if t.strip()]
                all_tags.extend(clean_prompt_list)
                
                flat_records.append({
                    "source": "aitag.win",
                    "work_id": str(work_id),
                    "title": title,
                    "model": model,
                    "prompt": ",".join(clean_prompt_list),
                    "negative_prompt": ",".join(clean_neg_list),
                    "steps": img.get("steps"),
                    "scale": img.get("scale"),
                    "sampler": img.get("sampler"),
                    "width": img.get("width"),
                    "height": img.get("height")
                })
    else:
        print(f"Skipping {INPUT_AITAG} (not found).")

    # 2. Parse Danbooru raw posts data if exists
    if os.path.exists(INPUT_DANBOORU):
        print(f"Parsing Danbooru posts data: {INPUT_DANBOORU}...")
        with open(INPUT_DANBOORU, 'r', encoding='utf-8') as f:
            danbooru_posts = json.load(f)
            
        for post in danbooru_posts:
            total_images += 1
            tag_string = post.get("tag_string", "")
            # Convert space separated tag string to comma separated NAI style prompt
            clean_prompt_list = [clean_tag(t) for t in tag_string.split(" ") if t.strip()]
            all_tags.extend(clean_prompt_list)
            
            # Danbooru rating mapping: e -> explicit, q -> questionable, s -> sensitive, g -> general
            rating_map = {"e": "Explicit / NSFW", "q": "Questionable", "s": "Sensitive", "g": "General"}
            rating_str = rating_map.get(post.get("rating", ""), "Unknown")
            
            flat_records.append({
                "source": "danbooru",
                "work_id": str(post.get("id")),
                "title": f"Danbooru Post {post.get('id')}",
                "model": f"Danbooru Base ({rating_str})",
                "prompt": ",".join(clean_prompt_list),
                "negative_prompt": "", # Danbooru has no negative prompt
                "steps": "",
                "scale": post.get("score"), # Use score as scaling parameter equivalent in database
                "sampler": "",
                "width": post.get("width"),
                "height": post.get("height")
            })
    else:
        print(f"Skipping {INPUT_DANBOORU} (not found).")

    if not flat_records:
        print("No source database found to build dictionary. Please run extract_tags.py or extract_danbooru_tags.py.")
        return

    # Save flattened database
    print(f"Saving flattened database: {DATABASE_JSON} & {DATABASE_CSV} ({len(flat_records)} total entries)")
    with open(DATABASE_JSON, 'w', encoding='utf-8') as f:
        json.dump(flat_records, f, ensure_ascii=False, indent=2)

    headers = list(flat_records[0].keys())
    with open(DATABASE_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in flat_records:
            writer.writerow(r)

    # Build Tag Dictionary CSV
    print("Building tag frequency dictionary...")
    tag_counts = Counter(all_tags)
    trans_dict = load_translation_dict()
    
    tag_dict_rows = []
    for tag, count in tag_counts.most_common():
        if count < 10:  # Size threshold for GitHub table preview (count >= 10)
            continue
        
        meaning = get_meaning(tag, trans_dict)
        category = get_category(tag)
        usage_rate = (count / total_images) * 100 if total_images else 0
        
        tag_dict_rows.append({
            "tag": tag,
            "meaning": meaning,
            "category": category,
            "count": count,
            "usage_rate": f"{usage_rate:.2f}%"
        })

    # Output tag dictionary CSV
    print(f"Saving tag dictionary: {TAG_DICT_CSV} ({len(tag_dict_rows)} tags)")
    with open(TAG_DICT_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["tag", "meaning", "category", "count", "usage_rate"])
        writer.writeheader()
        for r in tag_dict_rows:
            writer.writerow(r)

    # Build Markdown Dictionary Guide
    print(f"Generating markdown dictionary guide: {MD_DICT_FILE}...")
    generate_markdown_guide(flat_records, tag_dict_rows, total_images)

def generate_markdown_guide(records, tags, total_images):
    samplers = Counter([r["sampler"] for r in records if r.get("sampler")]).most_common(5)
    resolutions = Counter([f"{r['width']}x{r['height']}" for r in records if r.get("width") and r.get("height")]).most_common(5)
    sources = Counter([r["source"] for r in records if r.get("source")]).most_common()
    
    md_content = """# NovelAI Diffusion V4.5 & Danbooru \u30d7\u30ed\u30f3\u30d7\u30c8\u8f9e\u5178

aitag.win\u304a\u3088\u3073 Danbooru API \u304b\u3089\u62bd\u51fa\u3057\u305f\u7d71\u8a08\u30c7\u30fc\u30bf\u306b\u57fa\u3065\u304f\u3001NovelAI\u306e\u9244\u677f\u30bf\u30b0\u30ea\u30b9\u30c8\u306e\u958b\u767a\u30ac\u30a4\u30c9\u3067\u3059\u3002

## \ud83d\udcca \u30c7\u30fc\u30bf\u30bd\u30fc\u30b9\u7d71\u8a08 (Data Source)
"""
    for src, c in sources:
        md_content += f"- **{src}**: {c} \u4ef6 ({c/total_images*100:.1f}%)\n"

    md_content += """
## ⚙\ufe0f \u63a8\u5968\u8a2d\u5b9a\u30d1\u30bf\u30fc\u30f3 (\u7d71\u8a08)

### \u30b5\u30f3\u30d7\u30e9\u30fc (Sampler - NovelAI)
"""
    for s, c in samplers:
        md_content += f"- **{s}**: {c} \u4ef6\n"
        
    md_content += "\n### \u89e3\u50cf\u5ea6 (Resolution)\n"
    for r, c in resolutions:
        md_content += f"- **{r}**: {c} \u4ef6 ({c/total_images*100:.1f}%)\n"

    md_content += "\n## \ud83d\udd11 \u30af\u30aa\u30ea\u30c6\u30a3\u30bf\u30b0\u9244\u677f\u30bb\u30c3\u30c8\n"
    quality_tags = [t for t in tags if t["category"] == "Quality"][:10]
    md_content += "| \u30bf\u30b0 | \u610f\u5473 | \u51fa\u73fe\u56de\u6570 | \u4f7f\u7528\u7387 |\n|---|---|---|---|\n"
    for t in quality_tags:
        md_content += f"| `{t['tag']}` | {t['meaning']} | {t['count']} | {t['usage_rate']} |\n"

    md_content += "\n## \ud83d\udc57 \u4e3b\u8981\u8863\u88c5\u30bf\u30b0\n"
    cloth_tags = [t for t in tags if t["category"] == "Clothing"][:15]
    md_content += "| \u30bf\u30b0 | \u610f\u5473 | \u51fa\u73fe\u56de\u6570 | \u4f7f\u7528\u7387 |\n|---|---|---|---|\n"
    for t in cloth_tags:
        md_content += f"| `{t['tag']}` | {t['meaning']} | {t['count']} | {t['usage_rate']} |\n"

    md_content += "\n## \ud83c\udfed \u80cc\u666f\u30fb\u7167\u660e\u30bf\u30b0\n"
    bg_tags = [t for t in tags if t["category"] == "Background"][:15]
    md_content += "| \u30bf\u30b0 | \u610f\u5473 | \u51fa\u73fe\u56de\u6570 | \u4f7f\u7528\u7387 |\n|---|---|---|---|\n"
    for t in bg_tags:
        md_content += f"| `{t['tag']}` | {t['meaning']} | {t['count']} | {t['usage_rate']} |\n"

    with open(MD_DICT_FILE, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print("Markdown file generated.")

if __name__ == "__main__":
    process_data()
