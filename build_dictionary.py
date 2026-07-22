import json
import csv
import os
import re
import urllib.request
from collections import Counter

# Inputs/Outputs
INPUT_AITAG = "extracted_works.json"
INPUT_DANBOORU = "danbooru_raw_works.json"
INPUT_BOORU_EXTRA = "booru_extra_raw_works.json"
DATABASE_JSON = "novelai_v4_5_database.json"
DATABASE_CSV = "novelai_v4_5_database.csv"
TAG_DICT_CSV = "novelai_v4_5_tag_dictionary.csv"
MD_DICT_FILE = "novelai_v4_5_dictionary.md"
NEG_DICT_JSON = "novelai_v4_5_neg_dictionary.json"

MANUAL_JP_URL = "https://raw.githubusercontent.com/boorutan/booru-japanese-tag/master/danbooru-jp.csv"
MACHINE_JP_URL = "https://raw.githubusercontent.com/boorutan/booru-japanese-tag/master/danbooru-machine-jp.csv"
MANUAL_JP_FILE = "danbooru-jp.csv"
MACHINE_JP_FILE = "danbooru-machine-jp.csv"

# Expert overrides for anime image generation context
AI_OVERRIDES = {
    "ultra-detailed": "極めて詳細な描き込み",
    "ultra detailed": "極めて詳細な描き込み",
    "year 2025": "2025年 (投稿・制作年指定)",
    "year 2024": "2024年 (投稿・制作年指定)",
    "year 2023": "2023年 (投稿・制作年指定)",
    "in_idolmaster_style": "アイドルマスター風の絵柄",
    "girl": "女の子",
    "high resolution": "高解像度",
    "8k": "8K解像度 (クオリティタグ)",
    "4k": "4K解像度 (クオリティタグ)",
    "close-up": "接写 (クローズアップ)",
    "close_up": "接写 (クローズアップ)",
    "masterpiece": "傑作 (基本クオリティタグ)",
    "very aesthetic": "非常に美しい (美的タグ)",
    "ahegao": "アヘ顔",
    "ai-assisted": "AI支援画像",
    "ai-generated": "AI生成画像",
    "official art": "公式イラスト・公式画像",
    "looking at viewer": "カメラ目線 (こちらを見つめる)",
    "spread legs": "開脚ポーズ",
    "nude": "裸 (ヌード)",
    "sweat": "汗 (肌の描写)",
    "navel": "おへそ",
    "cleavage": "胸の谷間",
    "large breasts": "巨乳",
    "medium breasts": "中乳 (普通の胸)",
    "small breasts": "微乳・貧乳",
    "flat chest": "平らな胸 (絶壁)",
    "skirt": "スカート",
    "panties": "パンティ (下着)",
    "white panties": "白パンティ",
    "striped panties": "しまパン",
    "thighhighs": "サイハイソックス",
    "knee highs": "膝上ソックス (ニーソ)",
    "bare shoulders": "露出した肩",
    "underwear": "下着",
    "swimsuit": "水着",
    "bikini": "ビキニ",
    "school uniform": "制服",
    "serafuku": "セーラー服",
    "sailor suit": "セーラー服",
    "blazer": "ブレザー",
    "pantihose": "パンスト (パンティストッキング)",
    "pantyhose": "パンスト (パンティストッキング)",
    "black pantyhose": "黒パンスト",
    "white pantyhose": "白パンスト",
    "stockings": "ストッキング",
    "thighs": "太もも",
    "ass": "お尻",
    "butt": "お尻",
    "pussy": "割れ目・秘部",
    "breasts out": "裸胸 (胸を外に出す)",
    "under breast": "下乳 (アンダーブレスト)",
    "side breast": "横乳 (サイドブレスト)",
    "armpits": "脇 (わき)",
    "sitting": "座っている",
    "standing": "立っている",
    "lying": "横たわっている",
    "lying on back": "仰向け",
    "lying on stomach": "うつ伏せ",
    "kneeling": "膝立ち",
    "squatting": "しゃがみポーズ",
    "looking back": "振り返る",
    "head shot": "頭部アップ",
    "portrait": "肖像画風 (肩から上)",
    "upper body": "上半身",
    "cowboy shot": "腿から上のアングル",
    "full body": "全身の描写",
    "wide shot": "引きの構図",
    "indoors": "室内",
    "outdoors": "屋外",
    "bedroom": "寝室",
    "living room": "リビング",
    "bathroom": "浴室・お風呂場",
    "classroom": "教室",
    "beach": "砂浜 (ビーチ)",
    "pool": "プール",
    "bed": "ベッド",
    "chair": "椅子",
    "sofa": "ソファ",
    "night": "夜",
    "day": "昼",
    "sky": "空",
    "sunset": "夕日",
    "simple background": "シンプルな背景",
    "white background": "白背景",
    "black background": "黒背景",
    "transparent background": "透明背景",
    "bokeh": "背景のぼけ、玉ぼけ",
    "depth of field": "被写界深度 (背景のぼけ)",
    "sunlight": "日光",
    "lens flare": "レンズフレア",
    "cinematic lighting": "映画風のドラマチックな照明",
    "volumetric lighting": "空気感のある光 (光の筋)",
    "backlighting": "逆光",
    "rim lighting": "輪郭を際立たせる光 (リムライト)",
    
    # 主要な作品・キャラクター・絵師タグの日本語修正
    "precure": "プリキュア",
    "umamusume": "ウマ娘 プリティーダービー",
    "blue_archive": "ブルーアーカイブ",
    "goddess_of_victory:_nikke": "勝利の女神：ニッケ",
    "zenless_zone_zero": "ゼンレスゾーンゼロ",
    "genshin_impact": "原神",
    "honkai:_star_rail": "崩壊：スターレイル",
    "honkai_series": "崩壊シリーズ",
    "wuthering_waves": "鳴潮 (Wuthering Waves)",
    "arknights": "アークナイツ",
    "azur_lane": "アズールレーン",
    "touhou": "東方Project",
    "mushoku_tensei": "無職転生",
    "fate_series": "Fateシリーズ",
    "fate/grand_order": "Fate/Grand Order",
    "fgo": "Fate/Grand Order",
    "virtual_youtuber": "バーチャルYouTuber",

    # ネガティブプロンプト専用用語
    "worst quality": "最低品質 (作画崩壊防止)",
    "low quality": "低品質 (品質維持)",
    "normal quality": "標準品質 (高品質化のため除外)",
    "bad quality": "悪品質 (粗い描画防止)",
    "poorly drawn": "下手なデッサン・崩れた描き込み",
    "bad anatomy": "破綻した解剖学 (身体構造崩れ防止)",
    "bad hands": "破綻した手・崩れた指",
    "missing fingers": "指の欠損",
    "extra digit": "指の増殖 (指多発防止)",
    "extra fingers": "指の増殖 (指多発防止)",
    "fused fingers": "融合した指 (指くっつき防止)",
    "too many fingers": "多すぎる指",
    "bad feet": "破綻した足・崩れたつま先",
    "missing arms": "腕の欠損",
    "missing legs": "脚の欠損",
    "extra arms": "余分な腕 (腕の増殖防止)",
    "extra legs": "余分な脚 (脚の増殖防止)",
    "mutated hands": "変異した手",
    "mutation": "変異・作画崩壊",
    "deformed": "変形・歪み",
    "disfigured": "醜い変形・顔体の崩れ",
    "malformed limbs": "不自然な形の四肢",
    "long neck": "不自然に長い首",
    "cross-eyed": "寄り目・ロンパリ",
    "watermark": "ウォーターマーク (透かし文字除去)",
    "signature": "絵師のサイン (署名ロゴ除去)",
    "username": "ユーザー名・テキストロゴ除去",
    "text": "余計な文字・ロゴテキスト除去",
    "error": "エラー文字・ノイズ",
    "cropped": "画面からはみ出たフレーミング",
    "out of frame": "画面外への見切れ",
    "jpeg artifacts": "JPEG圧縮ノイズ・画質劣化",
    "blurry": "ぼやけた画像・ピント外れ",
    "bad proportions": "不自然な頭身バランス",
    "gross proportions": "極端に崩れたプロポーション",
    "cloned face": "複製された同じ顔 (コピペ顔)",
    "duplicate": "要素の重複・二重化",
    "ugly": "醜い作画",
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

def get_category_enhanced(tag, tag_to_category):
    tag_lower = tag.lower().strip()
    if tag_lower in tag_to_category:
        return tag_to_category[tag_lower]
    return get_category(tag)

def format_english_tag(tag, category):
    clean_name = tag.replace("artist:", "")
    clean_name = clean_name.replace("_", " ").strip()
    
    # Capitalize words
    formatted = " ".join([word.capitalize() for word in clean_name.split(" ") if word])
    
    if category == "Style" and tag.startswith("artist:"):
        return f"絵師: {formatted}風の絵柄"
    elif category == "Style":
        return f"{formatted}風の絵柄"
    elif category == "Copyright":
        return f"作品: {formatted}"
    elif category == "Character":
        return f"キャラ: {formatted}"
        
    return formatted

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
    all_neg_tags = []
    total_images = 0
    tag_to_category = {}
    danbooru_tag_counts = Counter()

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
                
                ai_json_str = img.get("ai_json")
                if ai_json_str and not neg_prompt:
                    try:
                        ai_data = json.loads(ai_json_str)
                        comment = ai_data.get("Comment", {})
                        if isinstance(comment, str):
                            try:
                                comment = json.loads(comment)
                            except:
                                comment = {}
                        if isinstance(comment, dict):
                            neg_prompt = comment.get("uc") or ""
                        if not neg_prompt:
                            v4_neg = ai_data.get("v4_negative_prompt", {})
                            if isinstance(v4_neg, dict):
                                neg_prompt = v4_neg.get("caption", {}).get("base_caption", "")
                    except Exception as e:
                        pass
                
                clean_prompt_list = [clean_tag(t) for t in prompt.split(",") if t.strip()]
                clean_neg_list = [clean_tag(t) for t in neg_prompt.split(",") if t.strip()]
                all_tags.extend(clean_prompt_list)
                all_neg_tags.extend(clean_neg_list)
                
                image_path = img.get("image_path", "")
                image_url = ""
                if image_path:
                    image_url = f"https://ai-img.10118899.xyz/{image_path}"

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
                    "height": img.get("height"),
                    "image_url": image_url
                })
    else:
        print(f"Skipping {INPUT_AITAG} (not found).")

    # 2. Parse Danbooru raw posts data if exists
    if os.path.exists(INPUT_DANBOORU):
        print(f"Parsing Danbooru posts data: {INPUT_DANBOORU}...")
        with open(INPUT_DANBOORU, 'r', encoding='utf-8') as f:
            danbooru_posts = json.load(f)
            
        for post in danbooru_posts:
            tag_string = post.get("tag_string", "")
            # Convert space separated tag string to comma separated NAI style prompt
            clean_prompt_list = [clean_tag(t) for t in tag_string.split(" ") if t.strip()]
            
            # Count Danbooru tags
            for t in clean_prompt_list:
                danbooru_tag_counts[t.lower()] += 1
            
            # Map categories based on Danbooru tag fields
            chars = post.get("tag_string_character", "")
            if chars:
                for t in chars.split(" "):
                    t_clean = clean_tag(t)
                    if t_clean:
                        tag_to_category[t_clean.lower()] = "Character"
            
            artists = post.get("tag_string_artist", "")
            if artists:
                for t in artists.split(" "):
                    t_clean = clean_tag(t)
                    if t_clean:
                        tag_to_category[t_clean.lower()] = "Style"

            copyrights = post.get("tag_string_copyright", "")
            if copyrights:
                for t in copyrights.split(" "):
                    t_clean = clean_tag(t)
                    if t_clean:
                        tag_to_category[t_clean.lower()] = "Copyright"
            
            # Danbooru rating mapping: e -> explicit, q -> questionable, s -> sensitive, g -> general
            rating_map = {"e": "Explicit / NSFW", "q": "Questionable", "s": "Sensitive", "g": "General"}
            rating_str = rating_map.get(post.get("rating", ""), "Unknown")
            
            image_url = post.get("large_file_url") or post.get("preview_file_url") or ""
            
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
                "height": post.get("height"),
                "image_url": image_url
            })
    else:
        print(f"Skipping {INPUT_DANBOORU} (not found).")

    # 3. Parse Safebooru & Yande.re raw posts data if exists
    if os.path.exists(INPUT_BOORU_EXTRA):
        print(f"Parsing Safebooru & Yande.re posts data: {INPUT_BOORU_EXTRA}...")
        with open(INPUT_BOORU_EXTRA, 'r', encoding='utf-8') as f:
            booru_posts = json.load(f)
            
        for post in booru_posts:
            tag_string = post.get("tag_string", "")
            clean_prompt_list = [clean_tag(t) for t in tag_string.split(" ") if t.strip()]
            
            for t in clean_prompt_list:
                danbooru_tag_counts[t.lower()] += 1

            src = post.get("source", "booru")
            work_id = str(post.get("id"))
            flat_records.append({
                "source": src,
                "work_id": work_id,
                "title": f"{src.capitalize()} Post {work_id}",
                "model": f"{src.capitalize()} Base",
                "prompt": ",".join(clean_prompt_list),
                "negative_prompt": "",
                "steps": "",
                "scale": "",
                "sampler": "",
                "width": post.get("width"),
                "height": post.get("height"),
                "image_url": post.get("image_url", "")
            })
    else:
        print(f"Skipping {INPUT_BOORU_EXTRA} (not found).")
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
    
    # Build tag sample image lookup
    tag_sample_images = {}
    for r in flat_records:
        img_url = r.get("image_url")
        if img_url:
            for t in r.get("prompt", "").split(","):
                t_clean = t.strip().lower()
                if t_clean and t_clean not in tag_sample_images:
                    tag_sample_images[t_clean] = img_url

    # AITAGとDanbooruの両方のユニークタグの和集合を走査対象とする
    all_unique_tags = set(tag_counts.keys()).union(set(danbooru_tag_counts.keys()))
    
    # AITAG出現数 + Danbooru出現数 の合計が多い順にソート
    sorted_tags = sorted(all_unique_tags, key=lambda t: (tag_counts.get(t, 0) + danbooru_tag_counts.get(t, 0)), reverse=True)
    
    tag_dict_rows = []
    for tag in sorted_tags:
        count = tag_counts.get(tag, 0)  # AITAGでの出現数
        dan_count = danbooru_tag_counts.get(tag, 0)  # Danbooruでの出現数
        
        category = get_category_enhanced(tag, tag_to_category)
        
        # しきい値の適用
        if category in ("Character", "Style", "Copyright"):
            # キャラクター・作品・絵師は、AITAGで1回以上、またはDanbooruで3回以上出現していれば採用
            if count >= 1 or dan_count >= 3:
                pass
            else:
                continue
        else:
            # 一般タグはAITAGで3回以上出現しているもののみ
            if count >= 3:
                pass
            else:
                continue
        
        meaning = get_meaning(tag, trans_dict)
        if not meaning:
            meaning = format_english_tag(tag, category)
            
        usage_rate = (count / total_images) * 100 if total_images else 0
        sample_img = tag_sample_images.get(tag.lower(), "")
        
        tag_dict_rows.append({
            "tag": tag,
            "meaning": meaning,
            "category": category,
            "count": count,  # AITAGでの出現数を表示（実用頻度）
            "usage_rate": f"{usage_rate:.2f}%",
            "sample_image": sample_img
        })

    # Output tag dictionary CSV
    print(f"Saving tag dictionary: {TAG_DICT_CSV} ({len(tag_dict_rows)} tags)")
    with open(TAG_DICT_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["tag", "meaning", "category", "count", "usage_rate", "sample_image"])
        writer.writeheader()
        for r in tag_dict_rows:
            writer.writerow(r)

    # Output tag dictionary JSON for Web UI
    TAG_DICT_JSON = "novelai_v4_5_tag_dictionary.json"
    print(f"Saving tag dictionary JSON: {TAG_DICT_JSON}")
    with open(TAG_DICT_JSON, 'w', encoding='utf-8') as f:
        json.dump(tag_dict_rows, f, ensure_ascii=False, indent=2)

    # Build & Output Negative Tag Dictionary JSON for Web UI
    neg_tag_counts = Counter(all_neg_tags)
    neg_dict_rows = []
    for neg_tag, c in neg_tag_counts.most_common():
        if c < 2:
            continue
        meaning = get_meaning(neg_tag, trans_dict)
        if not meaning:
            meaning = format_english_tag(neg_tag, "Negative Prompt")
        usage_rate = (c / total_images) * 100 if total_images else 0
        neg_dict_rows.append({
            "tag": neg_tag,
            "meaning": meaning,
            "category": "Negative",
            "count": c,
            "usage_rate": f"{usage_rate:.2f}%"
        })

    print(f"Saving negative tag dictionary JSON: {NEG_DICT_JSON} ({len(neg_dict_rows)} neg tags)")
    with open(NEG_DICT_JSON, 'w', encoding='utf-8') as f:
        json.dump(neg_dict_rows, f, ensure_ascii=False, indent=2)

    # Build Markdown Dictionary Guide
    print(f"Generating markdown dictionary guide: {MD_DICT_FILE}...")
    generate_markdown_guide(flat_records, tag_dict_rows, total_images)

def generate_markdown_guide(records, tags, total_images):
    samplers = Counter([r["sampler"] for r in records if r.get("sampler")]).most_common(5)
    resolutions = Counter([f"{r['width']}x{r['height']}" for r in records if r.get("width") and r.get("height")]).most_common(5)
    sources = Counter([r["source"] for r in records if r.get("source")]).most_common()
    
    md_content = """# NovelAI Diffusion V4.5 & Danbooru \u30d7\u30ed\u30f3\u30d7\u30c8\u8f9e\u5178

aitag.win\u304a\u3088\u3073 Danbooru API \u304b\u3089\u62bd\u51fa\u3057\u305f\u7d71\u8a08\u30c7\u30fc\u30bf\u306b\u57fa\u3065\u304f\u3001NovelAI\u306e\u9244\u677f\u30bf\u30b0\u30ea\u30b9\u30c8\u306e\u958b\u767a\u30ac\u30a4\u30c9\u3067\u3059\u3002

## \U0001f4ca \u30c7\u30fc\u30bf\u30bd\u30fc\u30b9\u7d71\u8a08 (Data Source)
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

    md_content += "\n## \U0001f511 \u30af\u30aa\u30ea\u30c6\u30a3\u30bf\u30b0\u9244\u677f\u30bb\u30c3\u30c8\n"
    quality_tags = [t for t in tags if t["category"] == "Quality"][:10]
    md_content += "| \u30bf\u30b0 | \u610f\u5473 | \u51fa\u73fe\u56de\u6570 | \u4f7f\u7528\u7387 |\n|---|---|---|---|\n"
    for t in quality_tags:
        md_content += f"| `{t['tag']}` | {t['meaning']} | {t['count']} | {t['usage_rate']} |\n"

    md_content += "\n## \U0001f457 \u4e3b\u8981\u8863\u88c5\u30bf\u30b0\n"
    cloth_tags = [t for t in tags if t["category"] == "Clothing"][:15]
    md_content += "| \u30bf\u30b0 | \u610f\u5473 | \u51fa\u73fe\u56de\u6570 | \u4f7f\u7528\u7387 |\n|---|---|---|---|\n"
    for t in cloth_tags:
        md_content += f"| `{t['tag']}` | {t['meaning']} | {t['count']} | {t['usage_rate']} |\n"

    md_content += "\n## \U0001f3ed \u80cc\u666f\u30fb\u7167\u660e\u30bf\u30b0\n"
    bg_tags = [t for t in tags if t["category"] == "Background"][:15]
    md_content += "| \u30bf\u30b0 | \u610f\u5473 | \u51fa\u73fe\u56de\u6570 | \u4f7f\u7528\u7387 |\n|---|---|---|---|\n"
    for t in bg_tags:
        md_content += f"| `{t['tag']}` | {t['meaning']} | {t['count']} | {t['usage_rate']} |\n"

    with open(MD_DICT_FILE, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print("Markdown file generated.")

if __name__ == "__main__":
    process_data()
