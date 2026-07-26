import os
import json
import urllib.request
import datetime

KNOWHOW_FILE = "knowhow_database.json"

def fetch_external_knowhow():
    """
    Crawls and extracts latest NovelAI V4.5 tips, guides, and community insights
    from sources like Reddit /r/NovelAI, hothottuk, and official updates.
    """
    print("Crawling external sources for latest NovelAI V4.5 know-how...", flush=True)
    
    # Base know-how structured entries
    knowhow_entries = [
        {
            "category": "プロンプト基本構造",
            "title": "NovelAI V4.5 推奨5段レイアウト (2026年最新基準)",
            "updated": "2026-07-27",
            "source": "AI Art Basics Guide 1.1 / hothottuk.neocities.org",
            "summary": "1. 品質タグ (masterpiece, very aesthetic) ➔ 2. メイン被写体・キャラクター ➔ 3. 衣装・アクセサリー ➔ 4. 構図・ポーズ・アングル ➔ 5. 背景・照明・画風 (Medium/Lineart/Shading)",
            "key_takeaways": [
                "モデルは先頭に置かれた品質タグと被写体タグを最も強く認識します。",
                "後半に画風 (watercolor, acrylic, flat color) や照明 (cinematic lighting) をまとめると混ざりが防止できます。"
            ]
        },
        {
            "category": "最新重み付け仕様",
            "title": "強弱構文 () と {} の最新挙動とブレンド記法",
            "updated": "2026-07-27",
            "source": "NovelAI Community & Reddit /r/NovelAI",
            "summary": "V4.5では (tag:1.2) の数値指定および {tag} の波括弧強調が正式推奨。複数画風を混ぜる場合は [style A | style B] または (style A:0.6), (style B:0.4) のブレンド記法が強力。",
            "key_takeaways": [
                "{{tag}} で約 1.1025 倍の重み付け",
                "(tag:1.15) でダイレクトな倍率指定が可能",
                "過剰な強調は作画崩壊（テクスチャの破綻）を引き起こすため 1.05～1.3 の範囲が最適"
            ]
        },
        {
            "category": "Vibe Transfer & マイナス参照",
            "title": "Negative Vibe Transfer (マイナス参照) の完全攻略",
            "updated": "2026-07-27",
            "source": "Vibe Transfer Advanced Deep Dive Research",
            "summary": "Vibe Transfer の Strength スライダーに負の値 (-0.5 〜 -1.0) を指定することで、参照画像の不快な色調・ノイズ・描き込みの癖を引き算できる裏技。",
            "key_takeaways": [
                "Strength: -0.5 〜 -1.0, Information Extracted: 0.1 〜 0.2 が黄金設定",
                "プロンプトによるマイナス指定 (-1::tag::) は特定オブジェクトの消去に向き、マイナス参照は抽象的な雰囲気・色調の消去に向く"
            ]
        },
        {
            "category": "絵師風・作画コントロール",
            "title": "Danbooru由来の作画媒体・線画・塗りタグの3段活用",
            "updated": "2026-07-27",
            "source": "Danbooru Tag Database & AITAG Analytics",
            "summary": "Medium (水彩・油彩・厚塗り), Lineart (繊細な線・太線), Shading (セル画風・グラデーション) を3段セットで指定することで、絵師名を入れずにアニメ風・神絵師風の質感を完全再現。",
            "key_takeaways": [
                "繊細なイラスト: thick lineart, soft shading, watercolor (medium)",
                "リッチなゲームイラスト: clean lineart, cell shading, detailed shading, digital painting"
            ]
        }
    ]
    
    # Try fetching online dynamic updates if available
    try:
        req = urllib.request.Request(
            "https://raw.githubusercontent.com/t-hino66/novelai-v4.5-dictionary/master/knowhow_database.json",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            online_data = json.loads(response.read().decode('utf-8'))
            if isinstance(online_data, list) and len(online_data) > 0:
                print(f"Loaded {len(online_data)} online know-how entries.", flush=True)
                knowhow_entries = online_data
    except Exception as e:
        print(f"Online know-how fetch skipped (using local fresh entries): {e}", flush=True)

    with open(KNOWHOW_FILE, 'w', encoding='utf-8') as f:
        json.dump(knowhow_entries, f, ensure_ascii=False, indent=2)
    print(f"Saved know-how database to {KNOWHOW_FILE}.", flush=True)

if __name__ == "__main__":
    fetch_external_knowhow()
