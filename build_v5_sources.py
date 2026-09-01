"""Build a provenance-first catalog of additional NovelAI V5 sources.

The catalog intentionally keeps official documentation, public Explore examples,
community references, and strict Civitai matches separate from AITAG frequency
statistics. It does not ingest private/user PNGs.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_OUTPUT = "v5_sources.json"
DEFAULT_CIVITAI_PATHS = ("civitai_raw_works.json", "works")

SOURCES = [
    {
        "id": "novelai-explore-v5",
        "type": "official_observed",
        "title": "NovelAI Explore（V5公開Prompt）",
        "url": "https://novelai.net/explore",
        "role": "V5公開作品のPrompt・UC・キャラPrompt・設定値を確認する",
        "ingestion": "公開ページの個別実例を構造化して参照。頻度統計には合算しない",
        "status": "active",
    },
    {
        "id": "novelai-image-metadata",
        "type": "official_tool",
        "title": "NovelAI Image Metadata（公式）",
        "url": "https://github.com/NovelAI/novelai-image-metadata",
        "role": "NovelAI生成画像のPrompt・設定値・署名を検証する公式ツール",
        "ingestion": "検証方法として掲載。個人PNGの自動取り込みは行わない",
        "status": "reference_only",
    },
    {
        "id": "novelai-docs-tags",
        "type": "official",
        "title": "NovelAI公式 Tagging",
        "url": "https://docs.novelai.net/en/image/tags/",
        "role": "V5専用タグ、Complexity、透明背景、Dataset Tagsなどの仕様",
        "ingestion": "公式仕様・用語集として参照",
        "status": "active",
    },
    {
        "id": "novelai-docs-basics",
        "type": "official",
        "title": "NovelAI公式 Prompt Basics",
        "url": "https://docs.novelai.net/en/image/basics/",
        "role": "自然文とタグ、Prompt順序、重み付け、冗長性の公式ガイド",
        "ingestion": "公式設計原則として参照",
        "status": "active",
    },
    {
        "id": "novelai-docs-text",
        "type": "official",
        "title": "NovelAI公式 Text Rendering",
        "url": "https://docs.novelai.net/en/image/textrendering/",
        "role": "V5の日本語・英語・中国語Text RenderingとText指定",
        "ingestion": "Text構造・制限値の公式仕様として参照",
        "status": "active",
    },
    {
        "id": "novelai-docs-multiple-characters",
        "type": "official",
        "title": "NovelAI公式 Multiple Characters",
        "url": "https://docs.novelai.net/en/image/multiplecharacters/",
        "role": "V5の複数キャラクター・位置関係・source/target指定",
        "ingestion": "複数キャラ設計の公式仕様として参照",
        "status": "active",
    },
    {
        "id": "novelai-journal",
        "type": "official",
        "title": "NovelAI Journal / RSS",
        "url": "https://journal.novelai.net/",
        "role": "リリースノート、機能発表、公式チュートリアルの更新確認",
        "ingestion": "更新履歴・仕様変更の参照先",
        "status": "active",
    },
    {
        "id": "novelai-discord",
        "type": "community",
        "title": "NovelAI公式Discord",
        "url": "https://discord.gg/novelai",
        "role": "Prompt共有・ユーザー検証・公式コミュニティの事例",
        "ingestion": "自動収集せず、許諾確認済みの手動キュレーションのみ",
        "status": "manual_only",
    },
    {
        "id": "novelai-reddit",
        "type": "community",
        "title": "r/NovelAi",
        "url": "https://www.reddit.com/r/NovelAi/",
        "role": "V5の使用感・比較・Prompt設計のコミュニティ事例",
        "ingestion": "投稿本文を転載せず、出典リンク付きの要約・検証メモのみ",
        "status": "manual_only",
    },
    {
        "id": "novelai-community-guides",
        "type": "community",
        "title": "V5コミュニティ解説記事",
        "url": "https://note.com/aiillust000/n/n239e76e3d07d?hl=en",
        "role": "V5の自然文・Complexity・複数キャラの実践例",
        "ingestion": "手動参照。効果の断定や本文の転載はしない",
        "status": "manual_only",
    },
    {
        "id": "civitai-v5",
        "type": "community_observed",
        "title": "Civitai（NovelAI V5明示データ）",
        "url": "https://civitai.com/api/v1/images",
        "role": "公開生成メタデータのうち、NovelAIとV5がモデル情報に明記された記録",
        "ingestion": "モデル名・タイトルの厳格一致のみ。V5不明の画像は対象外",
        "status": "strict_match_only",
    },
]

EXPLORE_EXAMPLES = [
    {
        "id": "explore-what-will-you-do-v5",
        "source_id": "novelai-explore-v5",
        "title": "What will you do?",
        "url": "https://novelai.net/explore/image/63f87c2d-1e37-4bcd-a716-4043a1699cb8",
        "model": "NAI Diffusion V5 Full",
        "published": "2026-08-21",
        "observations": [
            "自然文の場面描写",
            "Complexity / depthness",
            "Text指定",
            "Character Prompt",
            "Steps / Guidance / Seed / Sampler",
        ],
        "verification": "public_page_observed",
    },
    {
        "id": "explore-v5-celebration",
        "source_id": "novelai-explore-v5",
        "title": "V5 celebration",
        "url": "https://novelai.net/explore/image/4c4b7db4-41f7-417b-b07a-264ccad20b4d",
        "model": "NAI Diffusion V5 Full",
        "published": "2026-08-21",
        "observations": [
            "複数キャラクター",
            "自然文の画面・雰囲気描写",
            "Complexity / depthness",
            "meta:novel era",
            "キャラクターごとのPrompt",
        ],
        "verification": "public_page_observed",
    },
]


def _iter_json_records(path):
    candidate = Path(path)
    if candidate.is_file() and candidate.suffix == ".json":
        try:
            payload = json.loads(candidate.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return
        if isinstance(payload, list):
            yield from payload
        return
    if candidate.is_dir():
        for child in sorted(candidate.glob("civitai-*.json")):
            yield from _iter_json_records(child)


def _is_strict_civitai_v5(record):
    """Require model identity, not merely a V5 word in the prompt."""

    if not isinstance(record, dict):
        return False
    meta = record.get("meta") if isinstance(record.get("meta"), dict) else {}
    model_identity = " ".join(
        str((meta if field.startswith("meta:") else record).get(field.removeprefix("meta:")) or "")
        for field in ("model", "model_name", "baseModel", "title", "meta:Model", "meta:model")
    )
    return bool(
        re.search(r"(?:novelai|nai\s+diffusion)", model_identity, re.IGNORECASE)
        and re.search(r"\bv5(?:\b|[^a-z0-9])", model_identity, re.IGNORECASE)
    )


def find_strict_civitai_v5_records(paths=DEFAULT_CIVITAI_PATHS):
    results = []
    seen = set()
    for path in paths:
        for record in _iter_json_records(path):
            if not _is_strict_civitai_v5(record):
                continue
            key = str(record.get("work_id") or record.get("id") or record.get("url") or "")
            if not key or key in seen:
                continue
            seen.add(key)
            meta = record.get("meta") if isinstance(record.get("meta"), dict) else {}
            prompt = record.get("prompt") or meta.get("prompt") or ""
            results.append({
                "id": key,
                "title": str(record.get("title") or ""),
                "model": str(record.get("model") or record.get("model_name") or meta.get("Model") or meta.get("model") or ""),
                "source_url": str(record.get("url") or record.get("image_url") or ""),
                "evidence_type": "generation_prompt" if prompt else "model_metadata",
            })
    return results


def build_report(civitai_paths=DEFAULT_CIVITAI_PATHS):
    civitai_records = find_strict_civitai_v5_records(civitai_paths)
    source_rows = []
    for source in SOURCES:
        row = dict(source)
        if source["id"] == "civitai-v5":
            row["record_count"] = len(civitai_records)
            row["status"] = "active" if civitai_records else "awaiting_strict_matches"
        source_rows.append(row)

    return {
        "schema_version": "v5-source-catalog-v1",
        "model": "NovelAI Diffusion V5",
        "personal_png_import": False,
        "sources": source_rows,
        "official_explore_examples": EXPLORE_EXAMPLES,
        "civitai_v5_records": civitai_records[:100],
        "metrics": {
            "source_count": len(source_rows),
            "official_source_count": sum(row["type"].startswith("official") for row in source_rows),
            "community_source_count": sum(row["type"].startswith("community") for row in source_rows),
            "explore_example_count": len(EXPLORE_EXAMPLES),
            "strict_civitai_v5_record_count": len(civitai_records),
        },
        "methodology": {
            "provenance": "公式ドキュメント、NovelAI Explore公開ページ、公式ツール、公開コミュニティ参照先を出典別に管理します。",
            "civitai_rule": "Civitaiはモデル情報にNovelAI/Nai DiffusionとV5が明示された記録だけを採用します。",
            "community_rule": "コミュニティは発見・比較用であり、AITAGのV5使用率や効果の証拠へ合算しません。",
            "privacy_rule": "個人PNG・個人履歴・認証が必要なデータは取り込みません。",
        },
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def main():
    report = build_report()
    Path(DEFAULT_OUTPUT).write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        f"Built V5 source catalog: {report['metrics']['source_count']} sources, "
        f"{report['metrics']['explore_example_count']} Explore examples, "
        f"{report['metrics']['strict_civitai_v5_record_count']} strict Civitai V5 records"
    )


if __name__ == "__main__":
    main()
