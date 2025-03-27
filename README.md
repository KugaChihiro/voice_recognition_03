# 議事録作成ツール

**本ツールは会議録画の音声を解析し、議事録作成を支援するツールです。**<br/>
**mp4またはwav形式のファイルをアップロードするだけで、要約された議事録を生成してくれます。**<br>
**生成された議事録ファイルはSharepointへ格納することができ、ローカルにダウンロードすることもできます。**<br>
**いずれもワードファイル形式での保存となります。**<br>

---

## 使用技術スタック

| **分類**         | **技術・ツール**                         |
|--------------|--------------------------------|
| **フロントエンド** | React（Material UI）        |
| **バックエンド**   | FastAPI                    |
| **クラウドサービス** | Azure Speech Service, Azure OpenAI |
| **ストレージ**     | Azure Blob Storage         |
| **コンテナ技術**   | Docker（docker-compose）   |

---

## フロントエンド技術スタック一覧

| **用途・カテゴリ**          | **ライブラリ名**           | **説明・用途**                                       |
|---------------------|--------------------|-----------------------------------------------|
| **UIライブラリ**        | `@mui/material`    | Material UIによるデザインコンポーネント               |
| **HTTP通信**           | `axios`            | APIとのHTTP通信（データ取得・送信）                   |
| **状態管理**           | `jotai`            | シンプルで軽量なグローバル状態管理                    |
| **非同期データ取得**     | `swr`              | APIから取得したデータのキャッシュと再取得管理            |
| **ファイル操作**        | `file-saver`       | ファイル（Wordなど）のクライアント側での保存機能        |
| **ファイル生成（Word）** | `docx`             | JavaScriptによるWordドキュメントの作成                |
| **フォーム管理**        | `react-hook-form`  | フォーム入力値の管理、バリデーション処理の効率化         |
| **ファイルアップロード**  | `react-dropzone`   | ドラッグ&ドロップによるファイルアップロード操作  |
| **クエリパラメータ**         | `react-router-dom` | クエリパラメータの取得・管理               |

## バックエンド技術スタック一覧

| **用途・カテゴリ**      | **ライブラリ名**         | **説明・用途**                                       |
|-------------------|------------------|-------------------------------------------|
| **非同期通信**       | `aiohttp`         | 非同期HTTPリクエストを扱うライブラリ                |
| **クラウドストレージ**   | `azure-storage-blob` | Azure Blob Storageとのやり取りを行うライブラリ      |
| **Webフレームワーク**   | `fastapi`         | 高速なPython製Webフレームワーク                    |
| **動画処理**        | `imageio-ffmpeg`  | FFmpegを利用した動画処理                        |
| **サーバー管理**     | `gunicorn`        | WSGIサーバー、FastAPIの本番運用向け                 |
| **認証・認可**       | `msal`            | Microsoft認証ライブラリ（Azure AD認証など）         |
| **AI・LLM**       | `openai`          | OpenAI APIを利用するためのクライアントライブラリ      |
| **データバリデーション** | `pydantic`        | データスキーマ定義とバリデーション                 |
| **環境変数管理**     | `python-dotenv`   | `.env`ファイルを使った環境変数の管理               |
| **ドキュメント操作**   | `python-docx`     | Word（.docx）ドキュメントの作成・編集              |
| **マルチパート処理**   | `python-multipart` | ファイルアップロードなどのマルチパートデータ処理     |
| **HTTP通信**       | `requests`        | シンプルなHTTPリクエストライブラリ                 |
| **Webフレームワーク**   | `starlette`        | FastAPIの基盤となるASGIフレームワーク               |
| **トークン処理**     | `tiktoken`        | OpenAIのトークナイザー（トークン計算など）         |
| **非同期サーバー**   | `uvicorn[standard]` | ASGIサーバー、FastAPIの実行に使用                  |

---

## 環境構築

### 1. リポジトリをクローン

```bash
git clone https://github.com/sakuya10969/voice_recognition.git
cd voice_recognition
```

### 2. 依存関係のセットアップ

**フロントエンド (React)**
```bash
cd client
yarn install
```

**バックエンド (FastAPI)**
```bash
cd ../api
docker-compose build
```

---

## 3. アプリケーションの起動と使用方法

1. フロントエンドのサーバーを起動。
```bash
cd client
yarn start
```

2. バックエンドのサーバーを起動
```bash
cd api
docker-compose up -d
```

3. ブラウザで以下のURLにアクセスし、音声ファイルをアップロードしてください。
```
http://localhost:3000
```

4. 議事録の生成後、ワードファイルとしてダウンロードすることができます。

---

## 注意事項と前提条件
- 本ツールのご利用には、AzureアカウントおよびAPIキーが必要です。
- APIキーや環境変数の設定方法については、各サービスの公式ドキュメントを参照してください。

