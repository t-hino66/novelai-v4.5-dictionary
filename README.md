# NovelAI Diffusion Prompt Evidence Dictionary & Database

aitag.win、Civitai、およびDanbooru系APIから抽出したデータに基づく、NovelAI Diffusion V4.5のプロンプトデータベースおよび日本語タグ辞典です。プロンプトでの観測、コミュニティPrompt、画像Annotationを別の根拠として扱います。

本リポジトリに含まれるプログラムを実行することで、各サイトの公開Prompt・コミュニティ情報・Annotationから自動で最新のEvidenceデータベースを構築できます。

## Data Sources

* **AITAG**: NovelAI V4.5で実際に使用された生成プロンプト。`nai_occurrence_count`（総出現回数）と`nai_image_count`（1回以上含む画像数）を分けて集計します。
* **Danbooru**: 画像に付与されたアノテーションタグ。`danbooru_count`としてAITAGとは別に集計します。
* **Safebooru / Yande.re**: 補助的な画像アノテーション。`safebooru_count` / `yandere_count`として別々に保持します。
* **Civitai**: 公開画像の生成Prompt（APIが匿名公開する場合）または公開モデルのコミュニティタグ。`civitai_image_count` / `civitai_usage_rate`として独立集計し、NAI V4.5使用率には混ぜません。
* **AIbooru**: AI画像に付与されたAnnotationタグ。`aibooru_count`として独立集計します。

**外部サイトの頻度 ≠ NovelAIでの効果保証**です。また、AITAGでの高頻度も効果の強さや因果関係を証明するものではありません。辞典では`Official`、`NAI V4.5`、`Danbooru`、`Civitai`、`AIbooru`のEvidenceを区別します。

## Dictionary schema

主要フィールドは次のとおりです。

* `canonical_tag` / `aliases`: 小文字・空白区切りへ正規化したタグと、underscore表記などの元表記。
* `occurrence_count`: AITAGプロンプト内での総出現回数。
* `image_count`: AITAGでタグを1回以上含む画像数。
* `image_usage_rate`: `image_count / AITAG V4.5画像数 * 100`。後方互換の`usage_rate`も同じ値です。
* `stats`: AITAG、Danbooru、Safebooru、Yande.re、Civitai、AIbooruの根拠別集計。
* `evidence`: `official`、`nai_v45_observed`、`danbooru`、`civitai`、`aibooru`、`community`。
* `related` / `conflicts`: 将来拡張用の配列（現時点では空配列）。

---

## 📂 構成ファイル

* **`novelai_v4_5_tag_dictionary.csv`**
  * 頻出タグの日本語辞典CSV。GitHub上で直接カラム整理されたテーブルとして閲覧・検索・ソートが可能です。
* **`tags.json` / `negative.json` / `manifest.json`**
  * Web UIの初期表示に使う軽量辞典とデータmanifest。詳細schemaは従来名の辞典JSONに保持し、作品DBは検索時に遅延読込します。
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

## 検証

```bash
python3 -m py_compile extract_tags.py extract_danbooru_tags.py extract_booru_extra.py build_dictionary.py search_prompts.py extract_knowhow.py
python3 build_dictionary.py
python3 -m unittest discover -s tests
python3 validate_data.py
```
