"""
論文通知モジュール

論文情報を整形してDiscordに通知する機能を提供
"""
import logging
from src.models import PaperResult
from src.notifiers.discord_notifier import DiscordNotifier


logger = logging.getLogger(__name__)


class PaperNotifier:
    """論文情報をDiscordに通知するクラス"""
    
    def __init__(self, webhook_url: str):
        """
        Args:
            webhook_url: Discord Webhook URL
        """
        self.discord_notifier = DiscordNotifier(webhook_url)
        logger.info("PaperNotifier初期化完了")
    
    def send_paper_summary(self, paper: PaperResult) -> bool:
        """
        論文の要約をDiscordに送信
        
        Args:
            paper: 送信する論文情報
            
        Returns:
            bool: 送信成功の場合True
        """
        try:
            # タイトルを整形
            title = f"📄 {paper.title}"
            
            # 説明文を構築（要約がある場合は要約を、ない場合はアブストラクトを使用）
            if paper.summary:
                description = paper.summary
            else:
                description = f"*要約の生成に失敗しました*\n\n{paper.abstract[:1500]}"
            
            # フィールドを構築
            fields = [
                {
                    'name': '著者',
                    'value': paper.authors[:1024],
                    'inline': False
                },
                {
                    'name': '公開日',
                    'value': paper.published,
                    'inline': True
                },
                {
                    'name': 'ソース',
                    'value': paper.source,
                    'inline': True
                }
            ]
            
            # カテゴリがある場合は追加
            if paper.categories:
                fields.append({
                    'name': 'カテゴリ',
                    'value': paper.categories[:1024],
                    'inline': False
                })
            
            # リンクを追加
            fields.append({
                'name': 'リンク',
                'value': f'[論文を読む]({paper.url})',
                'inline': False
            })
            
            # Discord通知を送信
            success = self.discord_notifier.send_embed(
                title=title,
                description=description,
                color='3498db',
                fields=fields,
                url=paper.url
            )
            
            if success:
                logger.info(f"論文通知成功: {paper.title[:50]}...")
            else:
                logger.error(f"論文通知失敗: {paper.title[:50]}...")
            
            return success
                
        except Exception as e:
            logger.error(f"論文通知エラー: {e}", exc_info=True)
            return False
