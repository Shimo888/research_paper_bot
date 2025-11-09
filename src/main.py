"""研究論文Bot メインエントリーポイント

論文の収集 → 要約 → Discord通知の統合フロー
"""

import logging
import sys
from typing import List

from src.collectors.arxiv_collector import ArxivCollector
from src.summarizers.openrouter_summarizer import OpenRouterSummarizer
from src.notifiers.paper_notifier import PaperNotifier
from src.models import PaperResult
from src.config import config


# ログ設定
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)


class ResearchPaperBot:
    """研究論文Botのメインクラス"""
    
    def __init__(self, dry_run: bool = False):
        """
        Args:
            dry_run: Trueの場合、Discord通知を実際に送信しない
        """
        self.dry_run = dry_run
        
        # 設定の検証
        try:
            config.validate()
            logger.info("Configuration validated successfully")
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            raise
        
        # 各モジュールの初期化
        self.collector = ArxivCollector(
            search_query=config.ARXIV_SEARCH_QUERY,
            max_results=config.MAX_PAPERS_PER_DAY
        )
        
        self.summarizer = OpenRouterSummarizer()
        
        if not self.dry_run:
            self.notifier = PaperNotifier(webhook_url=config.DISCORD_WEBHOOK_URL)
        else:
            self.notifier = None
            logger.info("Dry-run mode: Discord notifications will not be sent")
    
    def collect_papers(self, days: int = 1) -> List[PaperResult]:
        """
        論文を収集
        
        Args:
            days: 何日前までの論文を収集するか
            
        Returns:
            収集した論文のリスト
        """
        logger.info(f"Step 1/3: Collecting papers from last {days} days...")
        papers = self.collector.collect_recent_papers(days=days)
        logger.info(f"Collected {len(papers)} papers")
        
        if not papers:
            logger.warning("No papers found")
        
        return papers
    
    def summarize_papers(self, papers: List[PaperResult]) -> List[PaperResult]:
        """
        論文を要約
        
        Args:
            papers: 要約する論文のリスト
            
        Returns:
            要約が追加された論文のリスト
        """
        logger.info(f"Step 2/3: Summarizing {len(papers)} papers...")
        summarized_papers = []
        
        for i, paper in enumerate(papers, 1):
            try:
                logger.info(f"Summarizing paper {i}/{len(papers)}: {paper.title[:50]}...")
                summarized_paper = self.summarizer.summarize(paper)
                summarized_papers.append(summarized_paper)
            except Exception as e:
                logger.error(f"Failed to summarize paper {paper.id}: {e}")
                # 要約失敗した論文もリストに含める（summaryがNone）
                summarized_papers.append(paper)
        
        logger.info(f"Summarized {len(summarized_papers)} papers")
        return summarized_papers
    
    def notify_papers(self, papers: List[PaperResult]) -> int:
        """
        論文をDiscordに通知
        
        Args:
            papers: 通知する論文のリスト
            
        Returns:
            成功した通知数
        """
        logger.info(f"Step 3/3: Notifying {len(papers)} papers to Discord...")
        
        if self.dry_run:
            logger.info("Dry-run mode: Skipping actual Discord notification")
            for i, paper in enumerate(papers, 1):
                logger.info(f"[DRY-RUN] Would notify paper {i}/{len(papers)}: {paper.title}")
            return len(papers)
        
        success_count = 0
        
        for i, paper in enumerate(papers, 1):
            try:
                logger.info(f"Notifying paper {i}/{len(papers)}: {paper.title[:50]}...")
                
                # Discord通知用のメッセージを作成
                self.notifier.send_paper_summary(paper)
                success_count += 1
                
            except Exception as e:
                logger.error(f"Failed to notify paper {paper.id}: {e}")
        
        logger.info(f"Successfully notified {success_count}/{len(papers)} papers")
        return success_count
    
    def run(self, days: int = 1) -> bool:
        """
        メイン処理を実行
        
        Args:
            days: 何日前までの論文を収集するか
            
        Returns:
            成功した場合True
        """
        logger.info("=" * 60)
        logger.info("Research Paper Bot Started")
        logger.info("=" * 60)
        
        try:
            # Step 1: 論文収集
            papers = self.collect_papers(days=days)
            
            if not papers:
                logger.info("No papers to process. Exiting.")
                return True
            
            # Step 2: 論文要約
            summarized_papers = self.summarize_papers(papers)
            
            # Step 3: Discord通知
            success_count = self.notify_papers(summarized_papers)
            
            logger.info("=" * 60)
            logger.info(f"Research Paper Bot Completed Successfully")
            logger.info(f"Total papers processed: {len(papers)}")
            logger.info(f"Successfully notified: {success_count}")
            logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            logger.error(f"Fatal error occurred: {e}", exc_info=True)
            return False


def main():
    """エントリーポイント"""
    # コマンドライン引数でdry-runモードを設定可能
    dry_run = "--dry-run" in sys.argv
    
    bot = ResearchPaperBot(dry_run=dry_run)
    success = bot.run(days=7)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
