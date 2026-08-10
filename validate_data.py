import json
from pathlib import Path


DICTIONARY_FILES = (
    Path("novelai_v4_5_tag_dictionary.json"),
    Path("novelai_v4_5_neg_dictionary.json"),
)


def validate_dictionary(path):
    with path.open(encoding="utf-8") as file:
        rows = json.load(file)

    for row in rows:
        tag = row.get("tag", "<missing>")
        for field, usage_rate in row.items():
            if field != "usage_rate" and not field.endswith("_usage_rate"):
                continue
            assert isinstance(usage_rate, (int, float)), (
                f"{path}: {tag!r} {field} must be numeric, got {usage_rate!r}"
            )
            assert 0 <= usage_rate <= 100, (
                f"{path}: {tag!r} {field} out of range: {usage_rate}"
            )
        assert row.get("occurrence_count", 0) >= row.get("image_count", 0), (
            f"{path}: {tag!r} occurrence_count is below image_count"
        )
        assert row.get("canonical_tag") == tag, (
            f"{path}: {tag!r} canonical_tag mismatch"
        )

    return len(rows)


def main():
    validated = {str(path): validate_dictionary(path) for path in DICTIONARY_FILES}
    print("Validated dictionary rows:")
    for path, count in validated.items():
        print(f"- {path}: {count}")


if __name__ == "__main__":
    main()
