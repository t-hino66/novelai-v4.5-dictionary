# NovelAI Diffusion & Danbooru Prompt Dictionary & Database

aitag.win および Danbooru API から抽出した統計データに基づく、NovelAI Diffusion 画像生成プロンプト（タグ）データベースおよび日本語タグ辞典リポジトリです。

本リポジトリに含まれるプログラムを実行することで、ファンアート投稿や本家Danbooruの統計から自動で最新のプロンプトデータベースを構築できます。

---

## 📂 構成ファイル

* **`novelai_v4_5_tag_dictionary.csv`**
  * 頻出タグの日本語辞典CSV。GitHub上で直接カラム整理されたテーブルとして閲覧・検索・ソートが可能です。
* **`novelai_v4_5_dictionary.md`**
  * 統計データに基づく、カテゴリ別の主要タグ（クオリティ、キャラクター、衣装、背景等）のまとめガイド。
* **`novelai_v4_5_database.csv` / `.json`**
  * 抽出した全画像データ（AITAGおよびDanbooru）を統一フォーマットで記録したフラットデータベース。
* **`extract_tags.py`**
  * aitag.win から NovelAI Diffusion V4.5 のデータをスクレイピングして `extracted_works.json` を保存するスクリプト。
* **`extract_danbooru_tags.py`**
  * Danbooru API から高スコアの投稿データ（NSFW含む）を抽出して `danbooru_raw_works.json` を保存するスクリプト。
* **`build_dictionary.py`**
  * 抽出された生データ（AITAG/Danbooruの片方または両方）を統合し、データベース（CSV/JSON）、タグ辞書CSV、Markdownガイドを自動生成するビルドスクリプト。実行時に自動的に日本語翻訳データ（Danbooru日本語タグマッピング）をWebからダウンロードしてマージします。

---

## 🚀 使い方（最新データへの更新手順）

### 1. GitHubのWeb画面から実行（推奨・最も簡単）
本リポジトリには GitHub Actions が設定されているため、ローカル PC に環境を構築せず、GitHub上だけでデータを安全に更新できます。
* **自動定期実行**: 毎週日曜日の深夜に、自動的に新規データをスクレイピングしてタグ辞書を更新します。
* **手動実行手順**:
  1. リポジトリ上部の「**Actions**」タブをクリックします。
  2. 左サイドバーから「**Update NovelAI Tags Dictionary**」をクリックします。
  3. 右上に表示される「**Run workflow**」ボタンをクリックし、さらに緑色の「Run workflow」を実行します。
  4. 数分でスクリプトが実行され、CSV や Markdown などの成果物が自動的に最新化され、コミット＆プッシュされます。

### 2. ローカル PC でスクレイピング（抽出）
ローカルで手動実行したい場合は、目的に応じて以下のスクリプトを実行します。

#### A. aitag.win（NovelAI V4.5 ギャラリー）から取得
```bash
# 引数で目標取得件数を指定可能（デフォルト1000件）
python3 extract_tags.py 1000
```

#### B. Danbooru（本家学習ソース・NSFW含む）から取得
```bash
# 引数1: 目標取得件数（デフォルト1000件）, 引数2: 検索クエリ（デフォルト "score:>=50"）
python3 extract_danbooru_tags.py 1000 "score:>=50"
```
* ※ NSFW（R-18）のデータをピンポイントで集めたい場合は、検索クエリに `rating:explicit` などを指定可能です。
  （例: `python3 extract_danbooru_tags.py 1000 "rating:explicit score:>=100"`）

### 3. ローカル PC でビルド（データベースと辞典の生成）
抽出された生データファイルを読み込み、CSV や Markdown を統合・生成します。
```bash
python3 build_dictionary.py
```
* ※ `extracted_works.json` と `danbooru_raw_works.json` の両方がフォルダにあれば、それらを自動的にマージして一つの巨大なタグ統計辞書をビルドします。

---

## 📝 開発環境・ライブラリ
* Python 3.x
* 外部ライブラリへの依存はありません（すべてPython標準ライブラリ `urllib`, `csv`, `json`, `collections` 等で動作します）。
