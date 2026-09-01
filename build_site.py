import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SITE_DIR = ROOT / "_site"
SITE_FILES = (
    "index.html",
    "tags.json",
    "negative.json",
    "analytics_data.json",
    "knowhow_database.json",
    "chatgpt_image_prompts.json",
    "manifest.json",
    "v5_manifest.json",
    "v5_tags.json",
    "v5_negative.json",
)


def build_site():
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir()
    for filename in SITE_FILES:
        source = ROOT / filename
        if not source.exists():
            raise FileNotFoundError(f"Required site file is missing: {filename}")
        shutil.copy2(source, SITE_DIR / filename)
    works_dir = ROOT / "works"
    if not (works_dir / "manifest.json").exists():
        raise FileNotFoundError("Required works/manifest.json is missing")
    shutil.copytree(works_dir, SITE_DIR / "works")
    v5_works_dir = ROOT / "v5_works"
    if not (v5_works_dir / "manifest.json").exists():
        raise FileNotFoundError("Required v5_works/manifest.json is missing")
    shutil.copytree(v5_works_dir, SITE_DIR / "v5_works")
    print(f"Built Pages artifact at {SITE_DIR}")


if __name__ == "__main__":
    build_site()
