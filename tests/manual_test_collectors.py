"""手動テスト用スクリプト"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.collectors.arxiv_collector import ArxivCollector


def test_arxiv():
    print("=" * 60)
    print("Testing ArxivCollector...")
    print("=" * 60)
    
    collector = ArxivCollector("cat:cs.AI OR cat:cs.LG", max_results=3)
    papers = collector.collect_recent_papers(days=7)  # 過去7日分
    
    print(f"\nCollected {len(papers)} papers:")
    for i, paper in enumerate(papers, 1):
        print(f"\n{i}. {paper.title}")
        print(f"   Authors: {paper.authors[:100]}...")
        print(f"   URL: {paper.url}")
        print(f"   Published: {paper.published}")
        print(f"   Categories: {paper.categories}")


if __name__ == "__main__":
    test_arxiv()