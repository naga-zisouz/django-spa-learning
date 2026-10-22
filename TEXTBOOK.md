# Django + Vue SPA 入門テキスト

この教材のゴールは、**モジュラーモノリス**のバックエンド（Django + PostgreSQL）と
**SPA** フロントエンド（TypeScript + Vue）が、JSON API でつながる流れを説明できる
ことです。SSR版の [django-sample](../django-sample) を先に触っていると、
「HTMLを返す」代わりに「JSONを返す」「ブラウザで描画する」違いが比較しやすくなります。

まず [README.md](README.md) の Docker 手順で起動し、<http://localhost:5173/> で
追加・完了・削除を試してください。

## 0. このアプリで学べること

- **アーキテクチャ**: 1つのデプロイ単位（モジュラーモノリス）の中でモジュールを分ける
- **バックエンド**: Django REST framework、レイヤー分離（application / api）
- **データベース**: PostgreSQL、マイグレーション
- **フロントエンド**: Vue 3、TypeScript、`fetch` による API 呼び出し
- **開発**: Docker Compose、CORS、API テスト

### SSR版との違い（ざっくり）

| 観点 | django-sample（SSR） | このリポジトリ（SPA） |
|------|----------------------|------------------------|
| 画面 | Django テンプレートが HTML を生成 | Vue がブラウザで DOM を更新 |
| 通信 | フォーム POST → リダイレクト | `fetch` で JSON の GET/POST/DELETE |
| DB | SQLite（学習用） | PostgreSQL |
| 起動 | web 1コンテナ | db + backend + frontend |

## 1. リクエストの流れ（全体像）

```text
ブラウザ（Vue on :5173）
    │ fetch JSON
    ▼
Django API（:8000）
    │ config/urls.py → tasks/api/urls.py → tasks/api/views.py
    ▼
application 層（commands / queries）
    ▼
models.py → PostgreSQL（db コンテナ）
```

フロントは **別オリジン**（ポートが違う）なので、開発時は `django-cors-headers` で
`http://localhost:5173` からの API 呼び出しを許可しています（`config/settings.py`）。

## 2. モジュラーモノリスとは

「マイクロサービス」のように**最初からサービスを分割してデプロイする**のではなく、
**1つの Django プロジェクト（1つの実行単位）**の中で、機能ごとに**モジュール**
（Django アプリ）を分け、境界をはっきりさせる考え方です。

この教材では `tasks` が 1 モジュールです。将来 `accounts`（ユーザー）を足すときも、
同じ `backend` リポジトリ内にアプリを追加する形がモジュラーモノリスです。

### `tasks` モジュールのレイヤー

| パス | 役割 |
|------|------|
| `tasks/models.py` | 永続化するデータの形（ドメインに近い） |
| `tasks/application/queries.py` | 読み取りユースケース（一覧の絞り込み） |
| `tasks/application/commands.py` | 書き込みユースケース（作成・切替・削除） |
| `tasks/api/serializers.py` | JSON ↔ Python の変換・入力検証 |
| `tasks/api/views.py` | HTTP ステータスとレスポンスの組み立て |

**ルールの例**: `application` は HTTP や DRF に依存しない。`api` は薄く保ち、
ビジネスの分岐は `application` に寄せる。

## 3. Docker Compose の3サービス

`compose.yaml` を読んでください。

1. **db** — PostgreSQL。`healthcheck` が通るまで backend は起動を待つ
2. **backend** — Django。起動時に `migrate` してから `runserver`
3. **frontend** — Vite 開発サーバー。ホットリロード用にソースをマウント

ブラウザは **frontend の URL** を開きます。API のベース URL は
`VITE_API_BASE_URL`（既定: `http://localhost:8000`）です。
※ ブラウザから見えるのは「あなたの PC の localhost」なので、コンテナ内の
`backend` というホスト名はフロントの `fetch` では使いません。

## 4. API を試す

起動後、ターミナルで:

```bash
curl -s http://localhost:8000/api/tasks/?status=open | python3 -m json.tool
curl -s -X POST http://localhost:8000/api/tasks/ \
  -H 'Content-Type: application/json' \
  -d '{"title":"APIから作成","description":"curl"}'
```

エンドポイント一覧（`tasks/api/urls.py`）:

| メソッド | パス | 説明 |
|----------|------|------|
| GET | `/api/tasks/?status=open\|done\|all` | 一覧 |
| POST | `/api/tasks/` | 作成（JSON body） |
| POST | `/api/tasks/<id>/toggle/` | 完了の反転 |
| DELETE | `/api/tasks/<id>/` | 削除 |

## 5. フロントエンドの読み方

- `src/api/client.ts` — 共通の `fetch`、エラー処理
- `src/api/tasks.ts` — タスク API の関数
- `src/types/task.ts` — TypeScript の型（API の JSON と一致させる）
- `src/App.vue` — 画面と状態（`ref`）、イベントで API を呼ぶ

Vue 3 の **Composition API**（`<script setup>`）を使っています。
`onMounted` で初回一覧を取得し、ボタンやフォーム送信で `loadTasks()` を再度呼びます。

## 6. マイグレーションと shell

```bash
docker compose run --rm backend python manage.py migrate
docker compose run --rm backend python manage.py shell
```

```python
from tasks.models import Task
Task.objects.create(title="shell から")
```

モデルを変えたら `makemigrations` → `migrate` の順です（SSR版と同じ）。

## 7. テスト

```bash
docker compose run --rm backend python manage.py test
```

`tasks/tests.py` は DRF の `APIClient` で HTTP として振る舞いを検証します。
ユースケースを `application` に寄せているので、将来は application 単体のテストを
足すこともできます。

## 8. おすすめ学習順

1. Compose で起動し、ブラウザと curl で API を触る
2. `tasks/api/views.py` と `application/commands.py` を往復で読む
3. フロントの `App.vue` で、どの操作がどの API を呼ぶか対応づける
4. DevTools の Network タブで JSON とステータスコードを確認する
5. 下の演習を実装する

## 9. 演習

### 初級: 作成時のバリデーションエラーを表示

空タイトルを POST したときの API レスポンスを読み、フロントで
`errorMessage` に DRF のメッセージを出す。

### 中級: 完了フィルタを URL に反映

`?status=done` のように **Vue Router** を入れ、リロードしても同じフィルタが開くようにする。

### 発展: 認証モジュールを足す

新しい Django アプリ `accounts` を作り、ログイン API と JWT またはセッション認証を学ぶ。
（本番向けの設定は別教材に回してよい）

### 発展: 本番に近い構成

`frontend` を `npm run build` し、Django または nginx で静的ファイルを配信する
「1オリジン」構成を調べる（CORS が不要になる理由を理解する）。

## 10. つまずいたとき

| 症状 | 確認すること |
|------|----------------|
| frontend が API に繋がらない | `VITE_API_BASE_URL`、CORS、backend が :8000 で起動しているか |
| `connection refused`（DB） | `db` の healthcheck、`POSTGRES_*` 環境変数 |
| マイグレーションエラー | `docker compose run --rm backend python manage.py migrate` |
| フロントの変更が反映されない | Vite のログ、ブラウザのハードリロード |
| CORS エラー | `CORS_ALLOWED_ORIGINS` にブラウザのオリジンが含まれるか |

エラーは **Network タブ（フロント）** と **backend のターミナルログ** の両方を見る習慣をつけてください。

## 11. 次に学ぶテーマ

- OpenAPI（drf-spectacular）で API 仕様を共有する
- Pinia でフロントの状態管理を整理する
- 認証・認可、ユーザーごとのタスク分離
- CI で `test` と `npm run build` を回す
- デプロイ（Compose / PaaS / Kubernetes の基礎）

SSR版で学んだ「モデル・マイグレーション・テスト」の感覚はそのまま活きます。
変わるのは **画面を誰が描くか** と **HTTP が HTML か JSON か** です。
