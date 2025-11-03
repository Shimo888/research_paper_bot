"""arXiv論文収集モジュール"""

import logging
from datetime import datetime, timedelta
from typing import List
import arxiv

from src.models import PaperResult

logger = logging.getLogger(__name__)


class ArxivCollector:
    """arXiv APIを使用して論文を収集するクラス"""
    
    def __init__(self, search_query: str, max_results: int = 5):
        """
        Args:
            search_query: arXiv検索クエリ（例: "cat:cs.AI OR cat:cs.LG"）
            max_results: 取得する最大論文数
        """
        self.search_query = search_query
        self.max_results = max_results
        logger.info(f"ArxivCollector initialized with query: {search_query}")
    
    def collect_recent_papers(self, days: int = 1) -> List[PaperResult]:
        """
        指定日数以内に公開された論文を収集
        
        Args:
            days: 何日前までの論文を取得するか
            
        Returns:
            論文情報のリスト
        """
        try:
            logger.info(f"Collecting papers from last {days} days...")
            
            # arXiv検索クライアント
            client = arxiv.Client()
            search = arxiv.Search(
                query=self.search_query,
                max_results=self.max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
            
            papers = []
            cutoff_date = datetime.now() - timedelta(days=days)
            
            for result in client.results(search):
                # 公開日チェック
                published = result.published.replace(tzinfo=None)
                if published < cutoff_date:
                    logger.debug(f"Paper {result.entry_id} is too old, skipping")
                    continue
                
                paper_info = PaperResult(
                    id=result.entry_id,
                    title=result.title,
                    authors=", ".join([author.name for author in result.authors]),
                    abstract=result.summary,
                    url=result.entry_id,
                    published=published.isoformat(),
                    categories=", ".join(result.categories),
                    source="arXiv"
                )
                papers.append(paper_info)
                logger.info(f"Collected paper: {result.title}")
            
            logger.info(f"Total papers collected: {len(papers)}")
            return papers
            
        except Exception as e:
            logger.error(f"Error collecting papers from arXiv: {e}")
            raise
    
    def collect_papers(self) -> List[PaperResult]:
        """
        最新論文を収集（デフォルト: 過去1日）
        
        Returns:
            論文情報のリスト
        """
        return self.collect_recent_papers(days=1)
