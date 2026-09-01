import csv
import json
import os
from collections import Counter, defaultdict
from pathlib import Path

import build_dictionary as base


INPUT_AITAG = "extracted_works_v5.json"
DATABASE_JSON = "novelai_v5_database.json"
DATABASE_CSV = "novelai_v5_database.csv"
TAG_DICT_JSON = "novelai_v5_tag_dictionary.json"
TAG_DICT_CSV = "novelai_v5_tag_dictionary.csv"
NEG_DICT_JSON = "novelai_v5_neg_dictionary.json"
NEG_DICT_CSV = "novelai_v5_neg_dictionary.csv"
MD_DICT_FILE = "novelai_v5_dictionary.md"
TAG_SUMMARY_JSON = "v5_tags.json"
NEG_SUMMARY_JSON = "v5_negative.json"
NATURAL_LANGUAGE_JSON = "v5_natural_language.json"
MANIFEST_JSON = "v5_manifest.json"
WORKS_DIRECTORY = "v5_works"
MODEL_MARKER = "NovelAI Diffusion V5"


def parse_ai_json(value):
    if not value:
        return {}
    try:
        parsed = json.loads(value) if isinstance(value, str) else value
    except (TypeError, ValueError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def nested_caption(data, key):
    section = data.get(key, {}) if isinstance(data, dict) else {}
    caption = section.get("caption", {}) if isinstance(section, dict) else {}
    return caption.get("base_caption", "") if isinstance(caption, dict) else ""


def extract_negative_prompt(image):
    explicit = image.get("negative_prompt", "") or ""
    if explicit:
        return explicit
    ai_data = parse_ai_json(image.get("ai_json"))
    comment = ai_data.get("Comment", {})
    if isinstance(comment, str):
        comment = parse_ai_json(comment)
    if isinstance(comment, dict) and comment.get("uc"):
        return comment["uc"]
    return nested_caption(ai_data, "v4_negative_prompt")


def load_v5_records():
    with open(INPUT_AITAG, encoding="utf-8") as file:
        raw_works = json.load(file)

    records = []
    aliases = defaultdict(set)
    negative_aliases = defaultdict(set)
    occurrence = Counter()
    image_count = Counter()
    negative_occurrence = Counter()
    negative_image_count = Counter()

    for item in raw_works:
        work = item.get("work", {})
        for image in item.get("images", []):
            model = str(image.get("model") or "")
            if MODEL_MARKER not in model:
                continue

            prompt_tags = base.parse_prompt_tags(image.get("prompt_text", ""), aliases)
            negative_prompt = extract_negative_prompt(image)
            negative_tags = base.parse_prompt_tags(negative_prompt, negative_aliases)
            occurrence.update(prompt_tags)
            image_count.update(set(prompt_tags))
            negative_occurrence.update(negative_tags)
            negative_image_count.update(set(negative_tags))

            normalized = dict(image)
            normalized["negative_prompt"] = negative_prompt
            record = base.build_aitag_record(work, normalized, prompt_tags, negative_tags)
            record["source"] = "aitag.win-v5"
            records.append(record)

    return (
        records,
        aliases,
        negative_aliases,
        occurrence,
        image_count,
        negative_occurrence,
        negative_image_count,
    )


def write_json(path, value):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(value, file, ensure_ascii=False, indent=2)


def build_tag_rows(records, aliases, occurrence, image_count, trans_dict):
    sample_images = {}
    for record in records:
        for tag in record.get("prompt", "").split(","):
            tag = tag.strip().lower()
            if tag and tag not in sample_images and record.get("image_url"):
                sample_images[tag] = record["image_url"]

    total_images = len(records)
    usage_rates = base.calculate_usage_rates(image_count, total_images)
    rows = []
    for tag in sorted(occurrence, key=lambda value: (image_count[value], occurrence[value], value), reverse=True):
        category = base.get_category_enhanced(tag, {})
        minimum = 1 if category in ("Character", "Style", "Copyright") else 3
        if occurrence[tag] < minimum:
            continue
        meaning = base.get_meaning(tag, trans_dict) or base.format_english_tag(tag, category)
        rate = usage_rates.get(tag, 0.0)
        evidence = {
            "official": False,
            "nai_v45_observed": False,
            "nai_v5_observed": image_count[tag] > 0,
            "danbooru": False,
            "danbooru_observed": False,
            "community": False,
            "civitai": False,
            "aibooru": False,
        }
        rows.append({
            "tag": tag,
            "canonical_tag": tag,
            "aliases": sorted(aliases[tag]),
            "meaning": meaning,
            "ja": meaning,
            "category": category,
            "occurrence_count": occurrence[tag],
            "image_count": image_count[tag],
            "image_usage_rate": rate,
            "usage_rate": rate,
            "count": occurrence[tag],
            "nai_occurrence_count": occurrence[tag],
            "nai_image_count": image_count[tag],
            "nai_usage_rate": rate,
            "nai_v5_occurrence_count": occurrence[tag],
            "nai_v5_image_count": image_count[tag],
            "nai_v5_usage_rate": rate,
            "danbooru_count": 0,
            "safebooru_count": 0,
            "yandere_count": 0,
            "civitai_image_count": 0,
            "civitai_usage_rate": 0.0,
            "civitai_occurrence_count": 0,
            "aibooru_count": 0,
            "evidence": evidence,
            "stats": {
                "nai_v5_image_count": image_count[tag],
                "nai_v5_usage_rate": rate,
                "nai_v5_occurrence_count": occurrence[tag],
            },
            "related": [],
            "conflicts": [],
            "confidence": "high" if image_count[tag] >= 10 else "medium",
            "sample_image": sample_images.get(tag, ""),
        })
    return rows


def build_negative_rows(negative_aliases, negative_occurrence, negative_image_count, trans_dict, total_images):
    rates = base.calculate_usage_rates(negative_image_count, total_images)
    rows = []
    for tag in sorted(negative_occurrence, key=lambda value: (negative_image_count[value], negative_occurrence[value], value), reverse=True):
        if negative_occurrence[tag] < 2:
            continue
        meaning = base.get_meaning(tag, trans_dict) or base.format_english_tag(tag, "Negative Prompt")
        rate = rates.get(tag, 0.0)
        rows.append({
            "tag": tag,
            "canonical_tag": tag,
            "aliases": sorted(negative_aliases[tag]),
            "meaning": meaning,
            "category": base.get_negative_category(tag),
            "occurrence_count": negative_occurrence[tag],
            "image_count": negative_image_count[tag],
            "image_usage_rate": rate,
            "usage_rate": rate,
            "count": negative_occurrence[tag],
            "nai_occurrence_count": negative_occurrence[tag],
            "nai_image_count": negative_image_count[tag],
            "nai_usage_rate": rate,
            "nai_v5_occurrence_count": negative_occurrence[tag],
            "nai_v5_image_count": negative_image_count[tag],
            "nai_v5_usage_rate": rate,
            "danbooru_count": 0,
            "civitai_image_count": 0,
            "civitai_usage_rate": 0.0,
            "civitai_occurrence_count": 0,
            "aibooru_count": 0,
            "official_preset": False,
            "observed": negative_image_count[tag] > 0,
            "evidence": {
                "official": False,
                "nai_v45_observed": False,
                "nai_v5_observed": negative_image_count[tag] > 0,
                "danbooru": False,
                "danbooru_observed": False,
                "community": False,
                "civitai": False,
                "aibooru": False,
            },
            "stats": {
                "nai_v5_image_count": negative_image_count[tag],
                "nai_v5_usage_rate": rate,
                "nai_v5_occurrence_count": negative_occurrence[tag],
            },
            "related": [],
            "conflicts": [],
            "confidence": "high" if negative_image_count[tag] >= 10 else "medium",
        })
    return rows


def write_csv(path, rows):
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            serialized = dict(row)
            for field in ("aliases", "evidence", "stats", "related", "conflicts"):
                if field in serialized:
                    serialized[field] = json.dumps(serialized[field], ensure_ascii=False)
            writer.writerow(serialized)


def write_v5_works(records):
    output = Path(WORKS_DIRECTORY)
    output.mkdir(parents=True, exist_ok=True)
    for stale in output.glob("*.json"):
        stale.unlink()
    projected = [base.project_work_record(record) for record in records]
    files = []
    for start in range(0, len(projected), base.WORKS_SHARD_SIZE):
        name = f"aitag-win-v5-{start // base.WORKS_SHARD_SIZE + 1:03d}.json"
        write_json(output / name, projected[start:start + base.WORKS_SHARD_SIZE])
        files.append(name)
    write_json(output / "manifest.json", {
        "total_count": len(projected),
        "sources": {"aitag.win-v5": {"count": len(projected), "files": files}},
    })


def main():
    if not os.path.exists(INPUT_AITAG):
        raise FileNotFoundError(f"Missing {INPUT_AITAG}; run extract_tags_v5.py first")

    (
        records,
        aliases,
        negative_aliases,
        occurrence,
        image_count,
        negative_occurrence,
        negative_image_count,
    ) = load_v5_records()
    if not records:
        raise RuntimeError("No NovelAI Diffusion V5 observations found")

    trans_dict = base.load_translation_dict()
    tag_rows = build_tag_rows(records, aliases, occurrence, image_count, trans_dict)
    negative_rows = build_negative_rows(
        negative_aliases, negative_occurrence, negative_image_count, trans_dict, len(records)
    )

    write_json(DATABASE_JSON, records)
    write_csv(Path(DATABASE_CSV), records)
    write_json(TAG_DICT_JSON, tag_rows)
    write_json(NEG_DICT_JSON, negative_rows)
    write_csv(Path(TAG_DICT_CSV), tag_rows)
    write_csv(Path(NEG_DICT_CSV), negative_rows)
    write_json(TAG_SUMMARY_JSON, tag_rows)
    write_json(NEG_SUMMARY_JSON, negative_rows)
    from build_v5_natural_language import build_report

    write_json(NATURAL_LANGUAGE_JSON, build_report(INPUT_AITAG))
    write_v5_works(records)

    Path(MD_DICT_FILE).write_text(
        "# NovelAI Diffusion V5 Prompt Evidence Dictionary\n\n"
        "aitag.winでNovelAI Diffusion V5として観測された実生成Promptだけを集計した、V4.5とは独立した辞典です。\n\n"
        f"- V5観測画像数: {len(records)}\n"
        f"- ポジティブタグ数: {len(tag_rows)}\n"
        f"- ネガティブタグ数: {len(negative_rows)}\n",
        encoding="utf-8",
    )
    write_json(MANIFEST_JSON, {
        "model": "NovelAI Diffusion V5",
        "source": "aitag.win",
        "dictionary": TAG_SUMMARY_JSON,
        "negative_dictionary": NEG_SUMMARY_JSON,
        "natural_language": NATURAL_LANGUAGE_JSON,
        "works_manifest": f"{WORKS_DIRECTORY}/manifest.json",
        "database_json": DATABASE_JSON,
        "database_csv": DATABASE_CSV,
        "tag_count": len(tag_rows),
        "negative_tag_count": len(negative_rows),
        "work_count": len(records),
        "nai_v5_image_count": len(records),
    })
    print(f"Built V5 dictionary: {len(records)} images, {len(tag_rows)} positive tags, {len(negative_rows)} negative tags")


if __name__ == "__main__":
    main()
