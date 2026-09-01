"""Build a separate, safety-screened natural-language report for V5 prompts.

V5 prompts can mix comma-separated tags with prose fragments.  The existing
tag dictionary intentionally treats comma-separated values as tags, so this
module keeps the natural-language view separate and labels its classifier as
heuristic rather than presenting it as ground truth.
"""

import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


MODEL_MARKER = "NovelAI Diffusion V5"
DEFAULT_INPUT = "extracted_works_v5.json"
DEFAULT_OUTPUT = "v5_natural_language.json"

_FUNCTION_WORDS = re.compile(
    r"\b(?:a|an|the|and|or|with|without|in|on|at|from|to|of|for|by|is|are|was|were|"
    r"wearing|holding|looking|standing|sitting|casting|glow|light|background|"
    r"there|she|he|they|this|that)\b",
    re.IGNORECASE,
)
_JAPANESE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
_WORDS = re.compile(r"[A-Za-z][A-Za-z'-]*|[\u3040-\u30ff\u3400-\u9fff]+")
_UNSAFE = re.compile(
    r"nsfw|nude|sex|sexual|cum|penis|vagina|porn|fetish|anus|handjob|nipples|"
    r"breast|boob|explicit|condom|lewd|erotic|blood|bruise|wound|injur|"
    r"corpse|explod|pin(?:s|ned)?\s+.*wrist|pavement|punch|kick|fight|"
    r"naked|strangl|throat|crotch|french kiss|fellatio|urinat|foaming|drool|tongue|"
    r"slap|neck grab|grabbing.*neck|highleg|backside|topless|untied|bikini|"
    r"diaper|briefs|taken off|broken shoulder|nose hook|large nostrils|乳|尻|裸|胸|"
    r"性器|精液|自慰|流血|負傷|爆発|ボコ|壊して|殴|蹴|戦闘|首を|首|絞|"
    r"裸足|水着|下着|裸体|暴力|殺|死体|血",
    re.IGNORECASE,
)


def _language(text):
    has_ja = bool(_JAPANESE.search(text))
    has_latin = bool(re.search(r"[A-Za-z]", text))
    if has_ja and has_latin:
        return "mixed"
    if has_ja:
        return "ja"
    return "en"


def _normalize(text):
    return re.sub(r"\s+", " ", text).strip()


def is_safe_expression(text):
    """Return whether a public sample can show this expression by default."""

    if _UNSAFE.search(text):
        return False
    if re.search(r"(?:^|\s)text\s*:", text, re.IGNORECASE):
        return False
    if re.search(r"[\"“”「」『』]", text):
        return False
    return True


def is_natural_language_candidate(raw_text):
    """Classify a comma-delimited prompt fragment as prose-like.

    This is deliberately conservative and only detects longer fragments with
    sentence punctuation or common function words. Weight syntax, character
    routing syntax, and artist/year metadata stay in the tag pipeline.
    """

    text = _normalize(str(raw_text or ""))
    words = _WORDS.findall(text)
    if len(words) < 6 or len(text) < 24:
        return False
    if any(marker in text for marker in ("::", "|", "#")):
        return False
    if re.match(r"^(?:artist|year|meta|rating|score)\s*:", text, re.IGNORECASE):
        return False
    return bool(re.search(r"[.!?。！？]", text) or _FUNCTION_WORDS.search(text))


def extract_natural_language_fragments(prompt):
    return [
        _normalize(fragment)
        for fragment in str(prompt or "").split(",")
        if is_natural_language_candidate(fragment)
    ]


def _prompt_structure(prompt, fragments):
    if not fragments:
        return "tag_only"
    total = len(_WORDS.findall(prompt)) or 1
    prose = sum(len(_WORDS.findall(fragment)) for fragment in fragments)
    if prose / total >= 0.55:
        return "natural_language_dominant"
    return "natural_language_mixed"


def build_report(input_path=DEFAULT_INPUT):
    source = Path(input_path)
    raw_works = json.loads(source.read_text(encoding="utf-8"))
    records = []
    for item in raw_works:
        work = item.get("work", {})
        for image in item.get("images", []):
            model = str(image.get("model") or "")
            if MODEL_MARKER not in model:
                continue
            prompt = str(image.get("prompt_text") or "")
            fragments = extract_natural_language_fragments(prompt)
            quoted = bool(re.search(r"[\"“”「」『』]", prompt))
            text_instruction = bool(re.search(r"(?:^|\s)Text\s*:", prompt, re.IGNORECASE))
            records.append({
                "work_id": str(work.get("id") or ""),
                "prompt": prompt,
                "fragments": fragments,
                "quoted": quoted,
                "text_instruction": text_instruction,
            })

    phrase_occurrence = Counter()
    phrase_images = defaultdict(set)
    safe_occurrence = Counter()
    safe_images = defaultdict(set)
    samples = []
    seen_samples = set()
    structures = Counter()
    candidate_records = 0
    japanese_prompts = 0
    quoted_prompts = 0
    text_instruction_prompts = 0

    for record in records:
        fragments = record["fragments"]
        if fragments:
            candidate_records += 1
        structures[_prompt_structure(record["prompt"], fragments)] += 1
        japanese_prompts += bool(_JAPANESE.search(record["prompt"]))
        quoted_prompts += record["quoted"]
        text_instruction_prompts += record["text_instruction"]

        for fragment in fragments:
            key = fragment.casefold()
            phrase_occurrence[key] += 1
            phrase_images[key].add(record["work_id"])
            if is_safe_expression(fragment) and is_safe_expression(record["prompt"]):
                safe_occurrence[key] += 1
                safe_images[key].add(record["work_id"])
                if key not in seen_samples and len(samples) < 40:
                    seen_samples.add(key)
                    samples.append({
                        "text": fragment,
                        "language": _language(fragment),
                        "work_id": record["work_id"],
                        "source_url": f"https://aitag.win/i/{record['work_id']}",
                        "safe_screened": True,
                    })

    total = len(records)

    def phrase_rows(occurrence, images, limit, include_safety=False):
        rows = []
        for key, count in occurrence.most_common():
            image_count = len(images[key])
            row = {
                "text": key,
                "language": _language(key),
                "occurrence_count": count,
                "image_count": image_count,
                "usage_rate": round(image_count / total * 100, 2) if total else 0.0,
            }
            if include_safety:
                row["safe_screened"] = is_safe_expression(key)
                row["safe_sample_eligible"] = key in safe_occurrence
            rows.append(row)
            if len(rows) >= limit:
                break
        return rows

    all_phrases = phrase_rows(phrase_occurrence, phrase_images, 100, include_safety=True)
    safe_phrases = phrase_rows(safe_occurrence, safe_images, 60)
    unsafe_candidate_count = sum(
        count for key, count in phrase_occurrence.items() if key not in safe_occurrence
    )
    return {
        "schema_version": "v5-natural-language-heuristic-v1",
        "model": "NovelAI Diffusion V5",
        "source": "aitag.win",
        "total_images": total,
        "metrics": {
            "candidate_record_count": candidate_records,
            "candidate_record_rate": round(candidate_records / total * 100, 2) if total else 0.0,
            "unique_candidate_expression_count": len(phrase_occurrence),
            "safe_expression_count": len(safe_occurrence),
            "observed_expression_count": len(phrase_occurrence),
            "unsafe_candidate_occurrence_count": unsafe_candidate_count,
            "japanese_prompt_count": japanese_prompts,
            "quoted_text_prompt_count": quoted_prompts,
            "text_instruction_prompt_count": text_instruction_prompts,
            "structure_counts": dict(structures),
        },
        "top_phrases": all_phrases,
        "top_safe_phrases": safe_phrases,
        "safe_samples": samples,
        "methodology": {
            "description": "カンマ区切りPromptから、長い文章らしい断片を保守的な規則で抽出した候補集計です。自然文の確定分類や効果の保証ではありません。",
            "safe_default": "サンプルはPrompt全体に安全判定語がない候補だけを初期公開します。",
            "provenance": "AITAGでNovelAI Diffusion V5として観測された公開Prompt。外部タグ・画像Annotationとは合算しません。",
        },
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def main():
    report = build_report()
    Path(DEFAULT_OUTPUT).write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        f"Built V5 natural-language report: {report['metrics']['candidate_record_count']} candidate records, "
        f"{len(report['top_safe_phrases'])} safe phrases"
    )


if __name__ == "__main__":
    main()
