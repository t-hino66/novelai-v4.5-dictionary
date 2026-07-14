import json
import sys
import argparse
from collections import Counter

DATABASE_FILE = "novelai_v4_5_database.json"

def main():
    parser = argparse.ArgumentParser(description="NovelAI & Danbooru Prompt Search CLI Tool")
    parser.add_argument("--tags", "-t", type=str, default="", help="AND検索するタグ (カンマ区切り)")
    parser.add_argument("--sampler", "-s", type=str, default="all", help="サンプラー指定 (k_euler_ancestral, k_euler 等)")
    parser.add_argument("--aspect", "-a", type=str, default="all", choices=["all", "portrait", "landscape", "square"], help="縦横比")
    parser.add_argument("--source", "-src", type=str, default="all", choices=["all", "aitag.win", "danbooru"], help="データソース")
    parser.add_argument("--limit", "-l", type=int, default=10, help="参考作品の表示上限")
    
    args = parser.parse_args()
    
    if not os.path.exists(DATABASE_FILE):
        print(f"Error: Database file '{DATABASE_FILE}' not found. Please build it first.")
        return
        
    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
        db = json.load(f)
        
    # Parse filter tags
    search_tags = [t.strip().lower() for t in args.tags.split(",") if t.strip()]
    
    # Filter database
    filtered = []
    for item in db:
        # Source filter
        if args.source != "all" and item.get("source") != args.source:
            continue
            
        # Sampler filter
        if args.sampler != "all" and item.get("sampler") != args.sampler:
            continue
            
        # Aspect filter
        if args.aspect != "all":
            w = int(item.get("width") or 0)
            h = int(item.get("height") or 0)
            if w and h:
                if args.aspect == "portrait" and w >= h:
                    continue
                if args.aspect == "landscape" and w <= h:
                    continue
                if args.aspect == "square" and w != h:
                    continue
            else:
                continue
                
        # Tag filter (AND match)
        if search_tags:
            item_tags = [t.strip().lower() for t in item.get("prompt", "").split(",") if t.strip()]
            match_all = True
            for s_tag in search_tags:
                if not any(s_tag in it or s_tag == it for it in item_tags):
                    match_all = False
                    break
            if not match_all:
                continue
                
        filtered.append(item)
        
    print(f"=== 検索条件 ===")
    print(f"ソース: {args.source} | サンプラー: {args.sampler} | 縦横比: {args.aspect} | 検索タグ: {search_tags}")
    print(f"合致件数: {len(filtered)} 件 / 全 {len(db)} 件")
    print(f"=================
")
    
    if not filtered:
        print("合致する作品がありません。検索条件を緩めてください。")
        return
        
    # Calculate Co-occurrence
    all_prompt_tags = []
    all_neg_tags = []
    for item in filtered:
        if item.get("prompt"):
            all_prompt_tags.extend([t.strip() for t in item["prompt"].split(",") if t.strip()])
        if item.get("negative_prompt"):
            all_neg_tags.extend([t.strip() for t in item["negative_prompt"].split(",") if t.strip()])
            
    tag_counts = Counter(all_prompt_tags)
    neg_counts = Counter(all_neg_tags)
    
    # Exclude quality tags and search input tags from co-occurrence
    common_quality = ['masterpiece', 'very aesthetic', 'best quality', 'absurdres', 'highres']
    for t in common_quality + search_tags:
        if t in tag_counts:
            del tag_counts[t]
            
    top_co_tags = [t[0] for t in tag_counts.most_common(12)]
    
    # 1. Output copypasta prompts
    print("📋 [おすすめコピペ用プロンプト]")
    print("--- POSITIVE PROMPT ---")
    pos_prompt = common_quality + search_tags + top_co_tags
    print(", ".join(pos_prompt))
    print("
--- NEGATIVE PROMPT ---")
    neg_prompt = [n[0] for n in neg_counts.most_common(10)]
    if not neg_prompt:
        neg_prompt = ['lowres', 'bad anatomy', 'bad hands', 'text', 'error', 'missing fingers', 'extra digit', 'worst quality', 'low quality']
    print(", ".join(neg_prompt))
    print("------------------------
")
    
    # 2. Co-occurrence list
    print("🤝 [同時によく使われる共起タグ (Top 15)]")
    for idx, (tag, count) in enumerate(tag_counts.most_common(15), 1):
        print(f"  {idx}. {tag} ({count}回)")
    print("")
    
    # 3. References List
    print(f"🔗 [参考作品URL・パラメータ (最新 {args.limit} 件)]")
    for idx, item in enumerate(filtered[:args.limit], 1):
        url = f"https://aitag.win/work/{item['work_id']}" if item["source"] == "aitag.win" else f"https://danbooru.donmai.us/posts/{item['work_id']}"
        source_name = "NovelAI 4.5" if item["source"] == "aitag.win" else "Danbooru"
        
        print(f"  {idx}. [{source_name}] {item.get('title') or '無題'} (ID: {item['work_id']})")
        print(f"     URL: {url}")
        print(f"     設定: Sampler: {item.get('sampler') or 'N/A'}, Scale: {item.get('scale') or 'N/A'}, Size: {item.get('width')}x{item.get('height')}")
        print(f"     プロンプト: {item.get('prompt')[:120]}...")
        print("")

if __name__ == "__main__":
    main()
