# Research Paper Bot

最新の技術論文を自動収集し、AIが要約して、Discordに定期通知するBot

## 概要

arXivやGoogle Scholar等から最新の技術論文を自動収集し、OpenAI GPT APIを使用して要約を生成し、Discord Webhookを通じて定期的に通知するシステム。GitHub Actionsによる自動実行により、日々の論文チェックを効率化する。

## 技術スタック

- 言語: Python 3.11+
- 論文収集: arXiv API, Semantic Scholar API
- AI要約: OpenAI GPT-4 API
- 通知: Discord Webhook
- 依存管理: pip (requirements.txt)

## ローカル環境でのセットアップ

### 1. 仮想環境の作成

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

### 2. 依存パッケージのインストール

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. テストの実行

```bash
# 仮想環境をアクティベート
source venv/bin/activate

# すべてのテストを実行
python -m pytest tests/ -v

# 特定のテストファイルを実行
python -m pytest tests/test_arxiv_collector.py -v

# カバレッジ付きでテスト実行
python -m pytest tests/ --cov=src --cov-report=html
```

## ディレクトリ構成

```
research_paper_bot/
├── .github/
│   └── copilot-instructions.md       # 開発ガイドライン
├── src/
│   ├── collectors/                   # 論文収集モジュール
│   ├── summarizers/                  # 要約生成モジュール
│   ├── notifiers/                    # 通知モジュール
│   └── config.py                     # 設定管理
├── tests/                            # テストコード
├── venv/                             # 仮想環境（Git管理外）
├── requirements.txt                  # Python依存パッケージ
├── TODO.md                           # 実装TODOリスト
└── README.md                         
```

## 開発について

- 開発ガイドライン: `.github/copilot-instructions.md`を参照
- 実装タスク管理: `TODO.md`でチェックリスト形式で管理
- 仮想環境: `venv/`ディレクトリはGit管理外

## 注意事項

- `venv/`ディレクトリは`.gitignore`に含まれている
- 機密情報は`.env`ファイルで管理する(ignore対象)