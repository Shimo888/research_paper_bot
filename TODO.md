# Research Paper Bot - 実装TODO

## Phase 1: プロジェクト基盤構築
- [x] プロジェクト構造の作成（ディレクトリ、__init__.py）
- [x] requirements.txtの作成
- [x] .env.exampleの作成
- [x] .gitignoreの作成
- [x] 環境変数読み込み（config.py）の実装

## Phase 2: 論文収集機能
- [ ] arXiv collector実装（arxiv_collector.py）
  - [ ] arXiv APIとの連携
  - [ ] 検索クエリのパース
  - [ ] 論文データの取得・パース
- [ ] Scholar collector実装（scholar_collector.py）
  - [ ] Semantic Scholar APIとの連携
  - [ ] 論文データの取得・パース

## Phase 3: AI要約機能
- [ ] OpenAI summarizer実装（openai_summarizer.py）
  - [ ] OpenAI API連携
  - [ ] プロンプト設計
  - [ ] 日本語要約生成
  - [ ] エラーハンドリング・リトライ機能

## Phase 4: Discord通知機能
- [ ] Discord notifier実装（discord_notifier.py）
  - [ ] Webhook連携
  - [ ] 埋め込み形式のメッセージ作成
  - [ ] エラーハンドリング

## Phase 5: メイン処理とオーケストレーション
- [ ] main.py実装
  - [ ] 各モジュールの統合
  - [ ] 論文収集→要約→通知のフロー
  - [ ] ログ記録
- [ ] 重複排除機能の実装
  - [ ] 通知済み論文の記録方法決定
  - [ ] 重複チェック機能

## Phase 6: GitHub Actions設定
- [ ] daily_paper_summary.ymlの作成
  - [ ] cronスケジュール設定
  - [ ] Python環境のセットアップ
  - [ ] Secrets設定の確認

## Phase 7: テストとドキュメント
- [ ] ユニットテストの作成
- [ ] 統合テストの実行
- [ ] README.mdの作成
- [ ] 使用方法のドキュメント整備

## Phase 8: 最終調整とデプロイ
- [ ] ローカル環境での動作確認
- [ ] GitHub Actionsでの動作確認
- [ ] エラーケースの検証
- [ ] 本番デプロイ

---

## 進捗メモ
- 作成日: 2025-11-01
- 最終更新: 2025-11-01
- Phase 1完了: プロジェクト基盤構築完了（ディレクトリ構造、設定ファイル、依存関係管理）
