import subprocess
import sys
import unittest
from pathlib import Path

import build_dictionary
import extract_tags


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
