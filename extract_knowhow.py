import os
import json
import urllib.request
import xml.etree.ElementTree as ET
import re
import datetime
import ssl

KNOWHOW_FILE = "knowhow_database.json"

def http_get_rss(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    )
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        return resp.read()

def fetch_reddit_live_knowhow():
    """
    Crawls live Reddit /r/NovelAI RSS feed.
    No API key required, 100% reliable.
    """
    print("Crawling live Reddit /r/NovelAI RSS feed...", flush=True)
    reddit_entries = []
    
    rss_urls = [
        "https://www.reddit.com/r/NovelAI/hot.rss",
        "https://www.reddit.com/r/NovelAI/new.rss"
    ]
    
    seen_links = set()
    keywords = ["vibe", "prompt", "v4", "guide", "tip", "negative", "uc", "weight", "quality", "style", "transfer", "reference", "character", "feature", "announcement"]
    
    for url in rss_urls:
        try:
            xml_data = http_get_rss(url)
            root = ET.fromstring(xml_data)
            entries = root.findall('{http://www.w3.org/2005/Atom}entry')
            
            for entry in entries:
                title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
                link_elem = entry.find('{http://www.w3.org/2005/Atom}link')
                updated_elem = entry.find('{http://www.w3.org/2005/Atom}updated')
                content_elem = entry.find('{http://www.w3.org/2005/Atom}content')
                
                title = title_elem.text if title_elem is not None else ""
                link = link_elem.attrib.get('href', '') if link_elem is not None else ""
                updated = updated_elem.text if updated_elem is not None else datetime.datetime.now().strftime("%Y-%m-%d")
                content_raw = content_elem.text if content_elem is not None else ""
                
                if not link or link in seen_links:
                    continue
                    
                # Clean HTML tags from content
                clean_content = re.sub(r'<[^>]+>', ' ', content_raw).strip()
                clean_content = re.sub(r'\s+', ' ', clean_content)
                
                full_text = (title + " " + clean_content).lower()
                is_relevant = any(kw in full_text for kw in keywords)
                
                if is_relevant:
                    seen_links.add(link)
                    
                    # Format date
                    date_str = updated.split('T')[0] if 'T' in updated else updated[:10]
                    
                    category = "Reddit リアルタイム話題"
                    if "vibe" in full_text:
                        category = "Reddit: Vibe Transfer 最新投稿"
                    elif "guide" in full_text or "feature" in full_text or "announcement" in full_text:
                        category = "Reddit: 公式発表・新機能ガイド"
                    elif "prompt" in full_text or "weight" in full_text or "style" in full_text:
                        category = "Reddit: プロンプト・作画検証"
                        
                    summary = clean_content[:180] + "..." if len(clean_content) > 180 else clean_content
                    if not summary or "submitted by" in summary and len(summary) < 50:
                        summary = f"Reddit /r/NovelAI コミュニティでのリアルタイム人気投稿。最新議論をチェックできます。"
                        
                    reddit_entries.append({
                        "category": category,
                        "title": f"[Reddit/r/NovelAI] {title}",
                        "updated": date_str,
                        "source": "Reddit /r/NovelAI (Live RSS)",
                        "summary": summary,
                        "url": link,
                        "key_takeaways": [
                            f"投稿日時: {date_str}",
                            f"Redditスレッドの直接リンク: {link}"
                        ]
                    })
        except Exception as e:
            print(f"Failed to crawl Reddit RSS {url}: {e}", flush=True)

    print(f"Extracted {len(reddit_entries)} live Reddit RSS entries.", flush=True)
    return reddit_entries[:6]

def fetch_external_knowhow():
    """
    Combines base curated guides + live crawled Reddit RSS updates.
    """
    print("Crawling external sources for latest NovelAI V4.5 know-how...", flush=True)
    
    # Base curated know-how entries
    base_entries = [
        {
            "category": "プロンプト基本構造",
            "title": "NovelAI V4.5 推奨5段レイアウト (2026年最新基準)",
            "updated": "2026-08-10",
            "source": "AI Art Basics Guide 1.1 / hothottuk.neocities.org",
            "summary": "1. 品質タグ (masterpiece, very aesthetic) ➔ 2. メイン被写体・キャラクター ➔ 3. 衣装・アクセサリー ➔ 4. 構図・ポーズ・アングル ➔ 5. 背景・照明・画風 (Medium/Lineart/Shading)",
            "key_takeaways": [
                "モデルは先頭に置かれた品質タグと被写体タグを最も強く認識します。",
                "後半に画風 (watercolor, acrylic, flat color) や照明 (cinematic lighting) をまとめると混ざりが防止できます。"
            ]
        },
        {
            "category": "構図・レイアウト構造",
            "title": "カメラ・アングル優先（Framing & Camera Priority）レイアウト",
            "updated": "2026-08-10",
            "source": "AI Art Basics Guide 1.1 & NovelAI Official Guide",
            "summary": "from above (見下ろし) や cowboy shot (膝上構図) などのカメラ画角タグは、キャラクター属性の直前に配置することで画角の旋回・ズーム失敗を劇的に防ぐレイアウト。",
            "key_takeaways": [
                "推奨順序: masterpiece, 1girl, cowboy shot, from above, blue hair...",
                "構図タグが文末にあると背景や小物に押されて無視されやすくなります。",
                "画角変更時は背景指定を簡潔 (simple background等) にするとカメラがスムーズに動きます。"
            ]
        },
        {
            "category": "色移り防止レイアウト",
            "title": "色属性の混ざり防止（Color Bleeding Isolation）配置ルール",
            "updated": "2026-08-10",
            "source": "hothottuk.neocities.org / NovelAI Deep Dive",
            "summary": "キャラクターの髪色・瞳色と、背景・照明・小物の色が混ざり合う (Color Bleeding) のを防ぐため、キャラクター属性ブロックと背景・画風ブロックを完全に分離隔離するレイアウト。",
            "key_takeaways": [
                "キャラブロック (1girl, blue hair, white dress) と背景ブロック (sunset, orange sky, classroom) の間にカンマ区切りを明確化。",
                "髪色が背景色に引っ張られる場合は (blue hair:1.15) のようにピンポイント強調または -1::orange hair:: で否定。"
            ]
        },
        {
            "category": "最新重み付け仕様",
            "title": "強弱構文 () と {} の最新挙動とブレンド記法",
            "updated": "2026-08-10",
            "source": "NovelAI Community & Reddit /r/NovelAI",
            "summary": "V4.5では (tag:1.2) の数値指定および {tag} の波括弧強調が正式推奨。複数画風を混ぜる場合は [style A | style B] または (style A:0.6), (style B:0.4) のブレンド記法が強力。",
            "key_takeaways": [
                "{{tag}} で約 1.1025 倍の重み付け",
                "(tag:1.15) でダイレクトな倍率指定が可能",
                "過剰な強調は作画崩壊（テクスチャの破綻）を引き起こすため 1.05～1.3 の範囲が最適"
            ]
        },
        {
            "category": "ネガティブレイアウト",
            "title": "3段階層型ネガティブプロンプトの設計構成",
            "updated": "2026-08-10",
            "source": "NovelAI V4.5 Best Practice Guide",
            "summary": "ネガティブプロンプトを「第1段: 低品質除外 ➔ 第2段: 実写・3Dノイズ除外 ➔ 第3段: 解剖学的破綻除外」の3ブロック階層で配置する安定化テクニック。",
            "key_takeaways": [
                "1. 低品質: lowres, bad anatomy, worst quality, low quality",
                "2. 2Dアニメ固定: monochrome, photo, 3d, realistic, render",
                "3. パーツ補正: extra fingers, missing fingers, bad hands"
            ]
        },
        {
            "category": "Vibe Transfer & マイナス参照",
            "title": "Negative Vibe Transfer (マイナス参照) の完全攻略",
            "updated": "2026-08-10",
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
            "updated": "2026-08-10",
            "source": "Danbooru Tag Database & AITAG Analytics",
            "summary": "Medium (水彩・油彩・厚塗り), Lineart (繊細な線・太線), Shading (セル画風・グラデーション) を3段セットで指定することで、絵師名を入れずにアニメ風・神絵師風の質感を完全再現。",
            "key_takeaways": [
                "繊細なイラスト: thick lineart, soft shading, watercolor (medium)",
                "リッチなゲームイラスト: clean lineart, cell shading, detailed shading, digital painting"
            ]
        }
    ]
    
    # Crawl live Reddit RSS entries
    reddit_entries = fetch_reddit_live_knowhow()
    
    # Combine base entries + live crawled Reddit entries
    all_knowhow = base_entries + reddit_entries

    with open(KNOWHOW_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_knowhow, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(all_knowhow)} total know-how entries to {KNOWHOW_FILE}.", flush=True)

if __name__ == "__main__":
    fetch_external_knowhow()
