"""Fetch NovelAI Diffusion V5 observations from aitag.win.

The shared extractor keeps the request and resume behavior identical to the
V4.5 pipeline while using a separate source snapshot and output file.
"""

import extract_tags as _extractor


_extractor.SEARCH_QUERY = "NovelAI Diffusion V5"
_extractor.OUTPUT_FILE = "extracted_works_v5.json"


if __name__ == "__main__":
    _extractor.main()
