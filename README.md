# NovelAI Diffusion Prompt Evidence Dictionary & Database

aitag.win、Civitai、およびDanbooru系APIから抽出したデータに基づく、NovelAI Diffusion V4.5のプロンプトデータベースおよび日本語タグ辞典です。プロンプトでの観測、コミュニティPrompt、画像Annotationを別の根拠として扱います。

本リポジトリに含まれるプログラムを実行することで、各サイトの公開Prompt・コミュニティ情報・Annotationから自動で最新のEvidenceデータベースを構築できます。

Web UIにはNovelAI系の統計と分離した「ChatGPT画像Prompt」タブもあります。ChatGPT Images向けに、用途、主題、構図、照明、文字、変更しない条件などを自然言語で指定するオリジナルテンプレートを収録しています。これは外部サイトのタグ頻度をChatGPT向けに転用したものではありません。

## ChatGPT Images Prompt Library

* `chatgpt_image_prompts.json`: 日本語・英語の編集可能なオリジナルテンプレートと調査出典。小容量の手書きデータなのでGitで管理します。
* 設計原則はOpenAI公式の[Creating images with ChatGPT](https://openai.com/academy/image-generation/)と[Creating images in ChatGPT](https://help.openai.com/en/articles/11084440-images-in-chatgpt)を正本にしています。
* GitHub上の[Pixmind-io/awesome-gpt-image-2-prompts](https://github.com/Pixmind-io/awesome-gpt-image-2-prompts)、[jamez-bondos/awesome-gpt4o-images](https://github.com/jamez-bondos/awesome-gpt4o-images)、[YouMind-OpenLab/awesome-gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2)は用途カテゴリの調査対象です。権利条件やモデル世代が一様ではないため、Prompt本文は転載していません。
* 「best quality」のような特定語を効果保証として扱わず、作りたい結果と制約を具体的に書く方針です。

## Data Sources

* **AITAG**: NovelAI V4.5で実際に使用された生成プロンプト。`nai_occurrence_count`（総出現回数）と`nai_image_count`（1回以上含む画像数）を分けて集計します。
* **Danbooru**: 画像に付与されたアノテーションタグ。`danbooru_count`としてAITAGとは別に集計します。
* **Safebooru / Yande.re**: 補助的な画像アノテーション。`safebooru_count` / `yandere_count`として別々に保持します。
* **Civitai**: 公開画像の生成Prompt（APIが匿名公開する場合）または公開モデルのコミュニティタグ。現在の匿名Image APIはPrompt metadataを返さないため、公開モデルタグを使用しています。`civitai_image_count` / `civitai_usage_rate`として独立集計し、NAI V4.5使用率には混ぜません。
* **AIbooru**: AI画像に付与されたAnnotationタグ。生成時のPromptではありません。`aibooru_count`として独立集計します。

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

## 📂 データ配信構成

* Web UI用の`tags.json`、`negative.json`、`works/*.json`はGitHub Actionsで生成し、Pages artifactとして直接デプロイします。
* 作品DBはソース別・最大5,000件のshardに分け、検索時に選択されたソースだけを遅延ロードします。
* 完全版JSON/CSVと増分更新用の元データは、Git履歴ではなく[`data-snapshot` Release](https://github.com/t-hino66/novelai-v4.5-dictionary/releases/tag/data-snapshot)で保持します。
* 生成物は`.gitignore`対象です。ローカルでは`build_dictionary.py`で再生成できます。
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
  2. 左サイドバーから「**Build and deploy prompt evidence dictionary**」をクリックします。
  3. 右上に表示される「**Run workflow**」ボタンをクリックし、さらに緑色の「Run workflow」を実行します。
  4. スクリプトが元データを更新し、完全版をReleaseへ保存した後、Web用データをGitHub Pagesへデプロイします。生成データはGitへコミットされません。

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
python3 -m py_compile extract_tags.py extract_danbooru_tags.py extract_booru_extra.py build_dictionary.py build_site.py search_prompts.py extract_knowhow.py
python3 build_dictionary.py
python3 -m unittest discover -s tests
python3 validate_data.py
python3 build_site.py
```
