# Django + Vue 学習用 ToDoアプリ（SPA）

SSR版の [django-sample](../django-sample) と同じ ToDo 機能を、**モジュラーモノリス + REST API + SPA** で学ぶためのリポジトリです。

## 必要なもの

Docker Desktop など、`docker compose` を実行できる環境だけを使います。

## 起動方法

```bash
docker compose up --build
```

- フロントエンド（Vue）: <http://localhost:5173/>
- バックエンド API: <http://localhost:8000/api/tasks/>
- Django 管理画面: <http://localhost:8000/admin/>

終了は `Ctrl+C`。バックグラウンド起動:

```bash
docker compose up --build -d
docker compose logs -f
docker compose down
```

データベース（PostgreSQL）は `postgres_data` ボリュームに保存されます。完全に消す場合:

```bash
docker compose down -v
```

## テスト

```bash
docker compose run --rm backend python manage.py test
```

フロントの型チェック（任意）:

```bash
docker compose run --rm frontend npm run build
```

## 構成

| ディレクトリ | 役割 |
|-------------|------|
| `backend/` | Django（モジュラーモノリス）。`tasks` モジュールが API を提供 |
| `frontend/` | Vue 3 + TypeScript + Vite |

教材は [TEXTBOOK.md](TEXTBOOK.md) です。

## 管理ユーザーの作成

```bash
docker compose run --rm backend python manage.py createsuperuser
```
