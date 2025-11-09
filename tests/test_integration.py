"""
統合テストスクリプト

論文収集→要約→Discord通知の統合フローをテスト
"""
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import ResearchPaperBot
from src.config import config
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_integration_dry_run():
    """統合テスト（Dry-runモード：Discord通知なし）"""
    logger.info("=" * 60)
    logger.info("統合テスト開始（Dry-runモード）")
    logger.info("=" * 60)
    
    try:
        # Dry-runモードで実行（Discord通知なし）
        bot = ResearchPaperBot(dry_run=True)
        success = bot.run(days=7)  # 7日分で試す
        
        if success:
            logger.info("✅ 統合テスト成功（Dry-run）")
            return True
        else:
            logger.error("❌ 統合テスト失敗（Dry-run）")
            return False
            
    except Exception as e:
        logger.error(f"❌ 統合テストでエラー発生: {e}", exc_info=True)
        return False


def test_integration_real():
    """統合テスト（実際にDiscordに通知）"""
    logger.info("=" * 60)
    logger.info("統合テスト開始（実通知モード）")
    logger.info("=" * 60)
    
    # 確認プロンプト
    response = input("⚠️  実際にDiscordに通知します。続行しますか？ (yes/no): ")
    if response.lower() != 'yes' or response.lower() != 'y':
        logger.info("テストをキャンセルしました")
        return False
    
    try:
        # 実通知モードで実行
        bot = ResearchPaperBot(dry_run=False)
        success = bot.run(days=7)  # 7日分で試す
        
        if success:
            logger.info("✅ 統合テスト成功（実通知）")
            return True
        else:
            logger.error("❌ 統合テスト失敗（実通知）")
            return False
            
    except Exception as e:
        logger.error(f"❌ 統合テストでエラー発生: {e}", exc_info=True)
        return False


def check_environment():
    """環境変数のチェック"""
    logger.info("=" * 60)
    logger.info("環境変数チェック")
    logger.info("=" * 60)
    
    checks = {
        "OPENROUTER_API_KEY": bool(config.OPENROUTER_API_KEY),
        "OPENROUTER_MODEL": bool(config.OPENROUTER_MODEL),
        "DISCORD_WEBHOOK_URL": bool(config.DISCORD_WEBHOOK_URL),
        "ARXIV_SEARCH_QUERY": bool(config.ARXIV_SEARCH_QUERY),
        "MAX_PAPERS_PER_DAY": config.MAX_PAPERS_PER_DAY > 0
    }
    
    all_ok = True
    for key, is_ok in checks.items():
        status = "✅" if is_ok else "❌"
        value = getattr(config, key)
        # APIキーは一部のみ表示
        if "KEY" in key or "URL" in key:
            display_value = f"{str(value)[:10]}..." if value else "(未設定)"
        else:
            display_value = value
        logger.info(f"{status} {key}: {display_value}")
        if not is_ok:
            all_ok = False
    
    if all_ok:
        logger.info("✅ すべての環境変数が設定されています")
    else:
        logger.error("❌ 一部の環境変数が未設定です")
    
    return all_ok


def main():
    """メイン処理"""
    print("\n" + "=" * 60)
    print("Research Paper Bot - 統合テスト")
    print("=" * 60)
    print("\n以下のテストを選択してください:")
    print("1. 環境変数チェック")
    print("2. 統合テスト（Dry-run：Discord通知なし）")
    print("3. 統合テスト（実通知：実際にDiscordに送信）")
    print("0. 終了")
    print()
    
    choice = input("選択 (0-3): ")
    
    if choice == "1":
        check_environment()
    elif choice == "2":
        if not check_environment():
            logger.warning("環境変数に問題がありますが、続行します...")
        test_integration_dry_run()
    elif choice == "3":
        if not check_environment():
            logger.error("環境変数に問題があります。先に修正してください。")
            return
        test_integration_real()
    elif choice == "0":
        logger.info("終了します")
    else:
        logger.error("無効な選択です")


if __name__ == "__main__":
    main()
