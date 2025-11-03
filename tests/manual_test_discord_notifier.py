"""
Discord Notifierの手動テストスクリプト

実際のDiscord Webhookに通知を送信して動作確認を行う
.envファイルにDISCORD_WEBHOOK_URLを設定して実行すること
"""
import os
import sys
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from src.notifiers.discord_notifier import DiscordNotifier

# 環境変数を読み込み
load_dotenv()


def test_connection():
    """接続テスト"""
    print("\n=== Discord Webhook 接続テスト ===")
    
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print("❌ エラー: DISCORD_WEBHOOK_URLが設定されていません")
        print("   .envファイルにDISCORD_WEBHOOK_URLを設定してください")
        return False
    
    try:
        notifier = DiscordNotifier(webhook_url)
        result = notifier.test_connection()
        
        if result:
            print("✅ 接続テスト成功")
            return True
        else:
            print("❌ 接続テスト失敗")
            return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False


def test_plain_text_message():
    """プレーンテキストメッセージ送信テスト"""
    print("\n=== プレーンテキストメッセージ送信テスト ===")
    
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    notifier = DiscordNotifier(webhook_url)
    
    result = notifier.send_message(
        content="これはプレーンテキストメッセージのテストです。"
    )
    
    if result:
        print("✅ プレーンテキストメッセージ送信成功")
    else:
        print("❌ プレーンテキストメッセージ送信失敗")
    
    return result


def test_embed_message():
    """埋め込みメッセージ送信テスト"""
    print("\n=== 埋め込みメッセージ送信テスト ===")
    
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    notifier = DiscordNotifier(webhook_url)
    
    result = notifier.send_message(
        content="これは埋め込み形式のメッセージテストです。タイトルと説明が表示されます。",
        title="📝 テストメッセージ",
        color='03b2f8'
    )
    
    if result:
        print("✅ 埋め込みメッセージ送信成功")
    else:
        print("❌ 埋め込みメッセージ送信失敗")
    
    return result


def test_embed_with_url():
    """URL付き埋め込みメッセージテスト"""
    print("\n=== URL付き埋め込みメッセージ送信テスト ===")
    
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    notifier = DiscordNotifier(webhook_url)
    
    result = notifier.send_message(
        content="タイトルをクリックするとリンク先に飛びます。",
        title="🔗 リンク付きメッセージ",
        url="https://github.com",
        color='2ecc71'
    )
    
    if result:
        print("✅ URL付き埋め込みメッセージ送信成功")
    else:
        print("❌ URL付き埋め込みメッセージ送信失敗")
    
    return result


def test_custom_embed():
    """カスタムフィールド付き埋め込みメッセージテスト"""
    print("\n=== カスタムフィールド付き埋め込みメッセージ送信テスト ===")
    
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    notifier = DiscordNotifier(webhook_url)
    
    fields = [
        {'name': '📊 統計情報', 'value': '通知数: 5件', 'inline': True},
        {'name': '⏰ 実行時刻', 'value': '2025-11-03 16:30', 'inline': True},
        {'name': '📝 詳細', 'value': 'これはカスタムフィールドのテストです。', 'inline': False}
    ]
    
    result = notifier.send_embed(
        title="📚 論文サマリー例",
        description="本日の最新論文をお届けします。",
        fields=fields,
        color='9b59b6',
        url="https://arxiv.org"
    )
    
    if result:
        print("✅ カスタムフィールド付き埋め込みメッセージ送信成功")
    else:
        print("❌ カスタムフィールド付き埋め込みメッセージ送信失敗")
    
    return result


def test_long_text():
    """長文メッセージの切り詰めテスト"""
    print("\n=== 長文メッセージ切り詰めテスト ===")
    
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    notifier = DiscordNotifier(webhook_url)
    
    long_description = "これは非常に長い説明文のテストです。" * 200
    
    result = notifier.send_embed(
        title="📏 長文テスト",
        description=long_description,
        color='e74c3c'
    )
    
    if result:
        print("✅ 長文メッセージ送信成功（自動切り詰め適用）")
    else:
        print("❌ 長文メッセージ送信失敗")
    
    return result


def test_paper_notification_example():
    """論文通知の実例テスト"""
    print("\n=== 論文通知実例テスト ===")
    
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    notifier = DiscordNotifier(webhook_url)
    
    fields = [
        {
            'name': '著者',
            'value': 'John Doe, Jane Smith, et al.',
            'inline': False
        },
        {
            'name': 'カテゴリ',
            'value': 'cs.AI, cs.LG',
            'inline': False
        },
        {
            'name': '公開日',
            'value': '2025-11-03',
            'inline': True
        },
        {
            'name': '論文リンク',
            'value': '[PDFを開く](https://arxiv.org/abs/2501.12345)',
            'inline': True
        }
    ]
    
    result = notifier.send_embed(
        title="Attention Is All You Need (サンプル論文)",
        description="""
        本論文では、Transformerという新しいネットワークアーキテクチャを提案します。
        従来のRNNやCNNを使用せず、アテンション機構のみに基づいた構造により、
        並列処理が可能で高速な学習を実現しています。
        機械翻訳タスクにおいて最高精度を達成しました。
        """,
        fields=fields,
        color='03b2f8',
        url="https://arxiv.org/abs/1706.03762"
    )
    
    if result:
        print("✅ 論文通知実例送信成功")
    else:
        print("❌ 論文通知実例送信失敗")
    
    return result


def main():
    """メインテスト実行"""
    print("=" * 60)
    print("Discord Notifier 手動テスト開始")
    print("=" * 60)
    
    results = []
    
    # 各テストを実行
    results.append(("接続テスト", test_connection()))
    
    if not results[0][1]:
        print("\n❌ 接続テストに失敗したため、以降のテストをスキップします")
        return
    
    print("\n⏳ 2秒待機...")
    import time
    time.sleep(2)
    
    results.append(("プレーンテキスト", test_plain_text_message()))
    time.sleep(1)
    
    results.append(("埋め込みメッセージ", test_embed_message()))
    time.sleep(1)
    
    results.append(("URL付き埋め込み", test_embed_with_url()))
    time.sleep(1)
    
    results.append(("カスタムフィールド", test_custom_embed()))
    time.sleep(1)
    
    results.append(("長文切り詰め", test_long_text()))
    time.sleep(1)
    
    results.append(("論文通知実例", test_paper_notification_example()))
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print("テスト結果サマリー")
    print("=" * 60)
    
    success_count = 0
    for test_name, result in results:
        status = "✅ 成功" if result else "❌ 失敗"
        print(f"{test_name}: {status}")
        if result:
            success_count += 1
    
    print(f"\n合計: {success_count}/{len(results)} 件成功")
    
    if success_count == len(results):
        print("\n🎉 すべてのテストが成功しました！")
    else:
        print(f"\n⚠️  {len(results) - success_count} 件のテストが失敗しました")


if __name__ == '__main__':
    main()
