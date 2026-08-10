import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import build_dictionary
import extract_tags
import extract_aibooru_tags
import extract_civitai_tags


ROOT = Path(__file__).resolve().parents[1]


class TagStatisticsTests(unittest.TestCase):
    def test_occurrence_and_image_counts_are_distinct(self):
        stats = build_dictionary.summarize_prompts(
            ["masterpiece, masterpiece, {masterpiece}"]
        )

        self.assertEqual(stats["occurrence_count"]["masterpiece"], 3)
        self.assertEqual(stats["image_count"]["masterpiece"], 1)

    def test_usage_rate_never_exceeds_100_percent(self):
        stats = build_dictionary.summarize_prompts(
            ["masterpiece, masterpiece", "masterpiece"]
        )

        rates = build_dictionary.calculate_usage_rates(stats["image_count"], 2)
        self.assertTrue(all(0 <= rate <= 100 for rate in rates.values()))
        self.assertEqual(rates["masterpiece"], 100)

    def test_underscore_and_space_aliases_share_canonical_tag(self):
        self.assertEqual(
            build_dictionary.canonicalize_tag("white_shirt"),
            build_dictionary.canonicalize_tag(" White Shirt "),
        )


class AitagSchemaTests(unittest.TestCase):
    def test_clean_detail_preserves_generation_metadata(self):
        detail = {
            "work": {"id": 1, "title": "fixture", "tags": []},
            "images": [
                {
                    "model": "NovelAI Diffusion V4.5",
                    "prompt_text": "cel shading",
                    "negative_prompt": "lowres",
                    "steps": 28,
                    "scale": 5.5,
                    "sampler": "k_euler_ancestral",
                    "width": 832,
                    "height": 1216,
                    "image_path": "images/example.png",
                    "image_url": "https://example.test/example.png",
                    "ai_json": "{\"seed\": 1}",
                }
            ],
        }

        cleaned = extract_tags.clean_detail(detail)["images"][0]

        for field in (
            "steps",
            "scale",
            "sampler",
            "width",
            "height",
            "image_path",
            "image_url",
            "ai_json",
        ):
            self.assertEqual(cleaned[field], detail["images"][0][field])

    def test_build_record_prefers_image_url_and_preserves_metadata(self):
        work = {"id": 1, "title": "fixture"}
        image = {
            "model": "NovelAI Diffusion V4.5",
            "prompt_text": "cel shading",
            "negative_prompt": "lowres",
            "steps": 28,
            "scale": 5.5,
            "sampler": "k_euler_ancestral",
            "width": 832,
            "height": 1216,
            "image_path": "images/fallback.png",
            "image_url": "https://example.test/preferred.png",
            "ai_json": "{\"seed\": 1}",
        }

        record = build_dictionary.build_aitag_record(work, image)

        self.assertEqual(record["image_url"], image["image_url"])
        for field in ("steps", "scale", "sampler", "width", "height", "ai_json"):
            self.assertEqual(record[field], image[field])


class ExternalSourceSchemaTests(unittest.TestCase):
    def test_civitai_clean_image_preserves_public_prompt_metadata(self):
        item = {
            "id": 42, "postId": 7, "url": "https://example.test/image.webp",
            "width": 832, "height": 1216, "baseModel": "SDXL",
            "modelVersionIds": [11], "createdAt": "2026-01-01T00:00:00Z",
            "meta": {"prompt": "1girl, blue_hair", "negativePrompt": "lowres",
                     "sampler": "Euler", "steps": 28, "cfgScale": 6},
        }
        cleaned = extract_civitai_tags.clean_image(item)
        self.assertEqual(cleaned["prompt"], item["meta"]["prompt"])
        self.assertEqual(cleaned["negative_prompt"], "lowres")
        self.assertEqual(cleaned["model_version_ids"], [11])

    def test_civitai_item_without_prompts_is_skipped(self):
        self.assertIsNone(extract_civitai_tags.clean_image({"id": 42, "meta": {}}))

    def test_civitai_model_tags_are_marked_as_model_evidence(self):
        cleaned = extract_civitai_tags.clean_model({
            "id": 5, "name": "Fixture Model", "tags": ["anime", "base model"],
            "modelVersions": [],
        })
        self.assertEqual(cleaned["prompt"], "anime,base model")
        self.assertEqual(cleaned["evidence_type"], "model_tags")

    def test_aibooru_clean_post_preserves_annotation_categories(self):
        post = {
            "id": 9, "tag_string": "1girl blue_hair", "tag_string_general": "1girl",
            "tag_string_character": "example_(series)", "tag_string_model": "nai_diffusion",
            "rating": "g", "score": 12, "image_width": 1024, "image_height": 1024,
            "large_file_url": "https://example.test/post.webp",
        }
        cleaned = extract_aibooru_tags.clean_post(post)
        self.assertEqual(cleaned["tag_string"], post["tag_string"])
        self.assertEqual(cleaned["tag_string_model"], "nai_diffusion")
        self.assertEqual(cleaned["width"], 1024)


class WorksShardTests(unittest.TestCase):
    def test_shards_are_grouped_by_source_and_project_ui_fields(self):
        records = [
            {
                "source": "aitag.win", "work_id": str(index), "title": "Fixture",
                "prompt": "best quality", "negative_prompt": "lowres",
                "sampler": "Euler", "width": 832, "height": 1216,
                "image_url": "https://example.test/image.png", "scale": 5,
                "ai_json": "large internal metadata",
            }
            for index in range(3)
        ] + [{
            "source": "aibooru", "work_id": "9", "title": "AIbooru Post 9",
            "prompt": "1girl", "negative_prompt": "", "sampler": "",
            "width": 1024, "height": 1024, "image_url": "", "scale": 0,
            "ai_json": "",
        }]

        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = build_dictionary.write_works_shards(
                records, output_dir=temp_dir, shard_size=2
            )
            self.assertEqual(manifest["total_count"], 4)
            self.assertEqual(manifest["sources"]["aitag.win"]["count"], 3)
            self.assertEqual(len(manifest["sources"]["aitag.win"]["files"]), 2)
            first_path = Path(temp_dir) / manifest["sources"]["aitag.win"]["files"][0]
            first_records = __import__("json").loads(first_path.read_text(encoding="utf-8"))
            self.assertNotIn("ai_json", first_records[0])
            self.assertEqual(first_records[0]["prompt"], "best quality")


class SearchPromptsTests(unittest.TestCase):
    def test_cli_help_starts_successfully(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "search_prompts.py"), "--help"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--tags", result.stdout)


if __name__ == "__main__":
    unittest.main()
