# 概要
最新の技術論文を自動収集し、AIが要約して、Discordに定期通知するBot

## プロジェクトの目的
- arXiv、Google Scholar等から最新の技術論文を自動収集
- OpenAI GPT APIを使用して論文を要約
- Discord Webhookを通じて定期的に要約を通知
- GitHub Actionsで定期実行（例：毎日朝9時）

## 技術スタック
- **言語**: Python 3.11+
- **論文収集**: arXiv API, Semantic Scholar API
- **AI要約**: OpenAI GPT-4 API
- **通知**: Discord Webhook
- **スケジューリング**: GitHub Actions (cron)
- **依存管理**: pip (requirements.txt)

## ディレクトリ構成
```
research_paper_bot/ 
├── .github/
│   ├── workflows/
│   │   └── daily_paper_summary.yml  # GitHub Actions定期実行設定
│   └── copilot-instructions.md
│
├── src/
│   ├── __init__.py
│   ├── main.py                      # エントリーポイント
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── arxiv_collector.py       # arXiv論文収集
│   │   └── scholar_collector.py     # Google Scholar収集
│   ├── summarizers/
│   │   ├── __init__.py
│   │   └── openai_summarizer.py     # GPT-4による要約
│   ├── notifiers/
│   │   ├── __init__.py
│   │   └── discord_notifier.py      # Discord通知
│   └── config.py                     # 設定管理
│
├── tests/
│   └── (テストコード)
│
├── requirements.txt                  # Python依存パッケージ
├── .env.example                      # 環境変数のサンプル
├── .gitignore
├── TODO.md                           # 実装TODOリスト
└── README.md
```

## 環境変数
```env
OPENAI_API_KEY=your_openai_api_key
DISCORD_WEBHOOK_URL=your_discord_webhook_url
ARXIV_SEARCH_QUERY=cat:cs.AI OR cat:cs.LG
MAX_PAPERS_PER_DAY=5
```

## 主な機能要件
1. **論文収集**: 指定したキーワード・カテゴリで最新論文を取得
2. **重複排除**: 既に通知済みの論文は除外（ローカルDBまたはGitHub Issues管理）
3. **AI要約**: 論文のアブストラクトから日本語で要約を生成
4. **Discord通知**: 埋め込み形式でタイトル、著者、要約、URLを送信
5. **エラーハンドリング**: API失敗時のリトライとログ記録

## 開発ガイドライン
- Pythonのコーディング規約（PEP 8）に準拠
- 型ヒント（Type Hints）を使用
- エラーハンドリングを適切に実装
- ログを標準出力に記録（GitHub Actions対応）
- 機密情報はGitHub Secretsで管理

## プロジェクト管理
- **TODO管理**: プロジェクトルートの`TODO.md`でStep by stepの実装タスクを管理
- Markdown形式のチェックリスト（`- [ ]`, `- [x]`）を使用
- フェーズごとにタスクを整理し、進捗を記録