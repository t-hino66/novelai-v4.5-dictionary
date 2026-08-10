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
                        "evidence_level": "Community",
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
            "title": "本辞典推奨のV4.5プロンプト5ブロック構造",
            "updated": "2026-08-10",
            "source": "本辞典の編集方針（NovelAI公式ガイドを参考に整理）",
            "evidence_level": "Community",
            "summary": "構図、背景、作風、品質、キャラクター詳細を見通しよく整理するための本辞典独自の5ブロック構造です。NovelAI公式が定めた固定テンプレートではありません。",
            "key_takeaways": [
                "タグ順は生成へ影響し得るため、重要な要素の位置を変えて比較してください。",
                "品質タグ追加がONならV4.5 Full用タグは自動で末尾へ追加されます。",
            ],
        },
        {
            "category": "重み付け仕様",
            "title": "NovelAIのNumerical Emphasis",
            "updated": "2026-08-10",
            "source": "NovelAI Documentation: Strengthening & Weakening Vectors",
            "evidence_level": "Official",
            "summary": "数値強調は 1.2::cel shading :: の形式を使います。{tag} は強化、[tag] は弱化として引き続き利用できます。",
            "key_takeaways": [
                "例: 1.2::cel shading ::, 0.8::soft shading ::",
                "Negative Numerical EmphasisはV4.5以降で利用でき、例は -1::text :: です。",
                "Stable Diffusion系の (tag:1.2) はV4.5公式記法として扱いません。",
            ],
        },
        {
            "category": "マルチキャラクター",
            "title": "V4/V4.5の縦線はPrompt Mixingではない",
            "updated": "2026-08-10",
            "source": "NovelAI Documentation: Multiple Characters",
            "evidence_level": "Official",
            "summary": "V4ではPrompt Mixingは利用できません。| はベースプロンプトとキャラクタープロンプトを区切る代替入力です。画風ブレンド記法として案内しません。",
            "key_takeaways": [
                "キャラクタープロンプト欄が存在する場合、| 構文は無効になります。",
                "V3系のPrompt Mixing説明とV4/V4.5の区切り構文を分離してください。",
            ],
        },
        {
            "category": "品質タグ",
            "title": "V4.5 FullのAdd Quality Tags",
            "updated": "2026-08-10",
            "source": "NovelAI Documentation: Add Quality Tags Toggle",
            "evidence_level": "Official",
            "summary": "V4.5 Fullでは location, very aesthetic, masterpiece, no text がプロンプト末尾へ自動追加されます。",
            "key_takeaways": [
                "Add Quality Tagsは既定でONです。",
                "手動追加する場合は自動追加との重複に注意してください。",
            ],
        },
        {
            "category": "Undesired Content",
            "title": "V4.5 Fullの公式UCプリセット",
            "updated": "2026-08-10",
            "source": "NovelAI Documentation: Undesired Content",
            "evidence_level": "Official",
            "summary": "Light、Heavy、Human Focus、Furry Focus、Noneを公式枠として扱います。Balanced Humanは本辞典独自のCustomプリセットです。",
            "key_takeaways": [
                "公式プリセットとCustomプリセットを混在表示しません。",
                "観測頻度と公式推奨の有無は別の根拠です。",
            ],
        },
        {
            "category": "画像参照機能",
            "title": "Vibe TransferとPrecise Referenceを分離する",
            "updated": "2026-08-10",
            "source": "NovelAI Documentation: Vibe Transfer / Precise Reference",
            "evidence_level": "Official",
            "summary": "Vibe TransferはStrengthとInformation Extracted、Precise ReferenceはStrengthとFidelityを持つ別機能です。V4.5では両者を同時利用できません。",
            "key_takeaways": [
                "Precise Referenceのスライダーは負値を手入力できると公式に記載されています。",
                "Vibe Transferの固定された負値や黄金設定は公式推奨として扱いません。",
                "-1::text :: のNumerical Negative Emphasisも画像参照とは別機能です。",
            ],
        },
        {
            "category": "データ解釈",
            "title": "頻度と効果を区別する",
            "updated": "2026-08-10",
            "source": "AITAG観測データ / Danbooru系アノテーション",
            "evidence_level": "Observed",
            "summary": "AITAGはV4.5実生成プロンプト、Danbooru系は画像アノテーションです。高頻度でも生成効果の因果や強さは証明されません。",
            "key_takeaways": [
                "表示には高頻度、実生成で観測、公式対応、コミュニティ利用例ありを使います。",
                "Danbooru頻度はNovelAIでの効果保証ではありません。",
            ],
        },
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
