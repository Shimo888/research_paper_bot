"""環境変数と設定管理"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """アプリケーション設定クラス"""
    
    # OpenRouter API設定
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
    
    # Discord Webhook設定
    DISCORD_WEBHOOK_URL: str = os.getenv("DISCORD_WEBHOOK_URL", "")
    
    # 論文検索設定
    ARXIV_SEARCH_QUERY: str = os.getenv("ARXIV_SEARCH_QUERY", "cat:cs.AI OR cat:cs.LG")
    MAX_PAPERS_PER_DAY: int = int(os.getenv("MAX_PAPERS_PER_DAY", "5"))
    
    # ログ設定
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls) -> bool:
        """必須設定の検証"""
        if not cls.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is required")
        if not cls.DISCORD_WEBHOOK_URL:
            raise ValueError("DISCORD_WEBHOOK_URL is required")
        return True


# シングルトンインスタンス
config = Config()
