"""
Discord Webhook通知モジュール

指定されたメッセージをDiscordに送信する機能を提供
"""
import logging
from typing import Optional
from discord_webhook import DiscordWebhook, DiscordEmbed


logger = logging.getLogger(__name__)


class DiscordNotifier:
    """Discord Webhookを使用してメッセージを通知するクラス"""
    
    def __init__(self, webhook_url: str):
        """
        Args:
            webhook_url: Discord Webhook URL
        
        Raises:
            ValueError: webhook_urlが空の場合
        """
        if not webhook_url:
            raise ValueError("Discord Webhook URLが設定されていません")
        
        self.webhook_url = webhook_url
        logger.info("DiscordNotifier初期化完了")
    
    def send_message(
        self,
        content: str,
        title: Optional[str] = None,
        color: str = '03b2f8',
        url: Optional[str] = None
    ) -> bool:
        """
        テキストメッセージをDiscordに送信
        
        Args:
            content: 送信するメッセージ内容
            title: メッセージのタイトル（オプション）
            color: 埋め込みメッセージの色（16進数カラーコード）
            url: メッセージに関連するURL（オプション）
        
        Returns:
            bool: 送信成功の場合True
        """
        try:
            webhook = DiscordWebhook(url=self.webhook_url, timeout = 10)
            
            if title:
                # 埋め込み形式で送信
                embed = DiscordEmbed(
                    title=self._truncate(title, 256),
                    description=self._truncate(content, 4096),
                    color=color
                )
                
                if url:
                    embed.url = url
                
                embed.set_footer(text="Research Paper Bot")
                embed.set_timestamp()
                
                webhook.add_embed(embed)
            else:
                # プレーンテキストで送信
                webhook.set_content(self._truncate(content, 2000))
            
            response = webhook.execute()
            
            if response.status_code in [200, 204]:
                logger.info("メッセージ送信成功")
                return True
            else:
                logger.error(f"メッセージ送信失敗: ステータスコード {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Discord通知エラー: {e}", exc_info=True)
            return False
    
    def send_embed(
        self,
        title: str,
        description: str,
        color: str = '03b2f8',
        fields: Optional[list[dict]] = None,
        url: Optional[str] = None
    ) -> bool:
        """
        カスタマイズされた埋め込みメッセージを送信
        
        Args:
            title: タイトル
            description: 説明文
            color: 埋め込みメッセージの色（16進数カラーコード）
            fields: フィールドのリスト [{'name': '名前', 'value': '値', 'inline': True/False}]
            url: タイトルのリンクURL（オプション）
        
        Returns:
            bool: 送信成功の場合True
        """
        try:
            webhook = DiscordWebhook(url=self.webhook_url, timeout = 10)
            
            embed = DiscordEmbed(
                title=self._truncate(title, 256),
                description=self._truncate(description, 2000),
                color=color
            )
            
            if url:
                embed.url = url
            
            # カスタムフィールドを追加
            if fields:
                for field in fields:
                    embed.add_embed_field(
                        name=self._truncate(field.get('name', ''), 256),
                        value=self._truncate(field.get('value', ''), 1024),
                        inline=field.get('inline', False)
                    )
            
            embed.set_footer(text="Research Paper Bot")
            embed.set_timestamp()
            
            webhook.add_embed(embed)
            response = webhook.execute()
            
            if response.status_code in [200, 204]:
                logger.info(f"埋め込みメッセージ送信成功: {title[:50]}...")
                return True
            else:
                logger.error(f"埋め込みメッセージ送信失敗: ステータスコード {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Discord埋め込み通知エラー: {e}", exc_info=True)
            return False
    
    @staticmethod
    def _truncate(text: str, max_length: int) -> str:
        """
        テキストを指定の長さで切り詰める
        
        Args:
            text: 元のテキスト
            max_length: 最大文字数
        
        Returns:
            str: 切り詰められたテキスト
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - 3] + "..."
    
    def test_connection(self) -> bool:
        """
        Discord Webhookの接続テスト
        
        Returns:
            bool: 接続成功の場合True
        """
        try:
            webhook = DiscordWebhook(url=self.webhook_url, timeout = 10)
            
            embed = DiscordEmbed(
                title="🔧 接続テスト",
                description="Research Paper BotのDiscord Webhook接続テストです。",
                color='9b59b6'
            )
            embed.set_footer(text="Research Paper Bot - Test")
            embed.set_timestamp()
            
            webhook.add_embed(embed)
            response = webhook.execute()
            
            if response.status_code in [200, 204]:
                logger.info("Discord Webhook接続テスト成功")
                return True
            else:
                logger.error(f"Discord Webhook接続テスト失敗: ステータスコード {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Discord Webhook接続テストエラー: {e}", exc_info=True)
            return False
