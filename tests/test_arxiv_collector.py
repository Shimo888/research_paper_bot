"""arXiv collectorのテスト"""

import pytest
from datetime import datetime
from src.collectors.arxiv_collector import ArxivCollector


def test_arxiv_collector_initialization():
    """ArxivCollectorの初期化テスト"""
    collector = ArxivCollector("cat:cs.AI", max_results=3)
    assert collector.search_query == "cat:cs.AI"
    assert collector.max_results == 3


def test_collect_papers():
    """論文収集のテスト"""
    collector = ArxivCollector("cat:cs.AI", max_results=3)
    papers = collector.collect_papers()
    
    # 論文が取得できること
    assert isinstance(papers, list)
    
    # 各論文が必要なフィールドを持つこと
    if papers:
        paper = papers[0]
        assert "id" in paper
        assert "title" in paper
        assert "authors" in paper
        assert "abstract" in paper
        assert "url" in paper
        assert "published" in paper
        assert "categories" in paper
        assert paper["source"] == "arXiv"
        
        # URLが正しい形式であること
        assert "arxiv.org" in paper["url"]


def test_collect_recent_papers_with_days():
    """指定日数の論文収集テスト"""
    collector = ArxivCollector("cat:cs.AI", max_results=5)
    papers = collector.collect_recent_papers(days=3)
    
    assert isinstance(papers, list)
    assert len(papers) <= 5


if __name__ == "__main__":
    # 簡易動作確認
    print("Testing ArxivCollector...")
    collector = ArxivCollector("cat:cs.AI OR cat:cs.LG", max_results=3)
    papers = collector.collect_papers()
    
    print(f"\nCollected {len(papers)} papers:")
    for i, paper in enumerate(papers, 1):
        print(f"\n{i}. {paper['title']}")
        print(f"   Authors: {paper['authors'][:100]}...")
        print(f"   URL: {paper['url']}")
        print(f"   Published: {paper['published']}")
