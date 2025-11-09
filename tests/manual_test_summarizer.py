"""OpenRouter Summarizer の手動テストスクリプト"""

import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.summarizers.openrouter_summarizer import OpenRouterSummarizer
from src.models import PaperResult
from src.config import config


def test_summarizer():
    """OpenRouter Summarizerの手動テスト"""
    
    print("=" * 60)
    print("OpenRouter Summarizer Manual Test")
    print("=" * 60)
    
    # 設定の確認
    print("\n[Configuration Check]")
    print(f"API Key configured: {'Yes' if config.OPENROUTER_API_KEY else 'No'}")
    print(f"Model: {config.OPENROUTER_MODEL}")
    
    if not config.OPENROUTER_API_KEY:
        print("\n❌ Error: OPENROUTER_API_KEY is not set in .env file")
        return
    
    # テスト用の論文データ
    test_paper = PaperResult(
        id="2401.00001",
        title="Attention Is All You Need",
        authors="Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit",
        abstract="""The dominant sequence transduction models are based on complex recurrent or 
convolutional neural networks that include an encoder and a decoder. The best performing models 
also connect the encoder and decoder through an attention mechanism. We propose a new simple 
network architecture, the Transformer, based solely on attention mechanisms, dispensing with 
recurrence and convolutions entirely. Experiments on two machine translation tasks show these 
models to be superior in quality while being more parallelizable and requiring significantly 
less time to train.""",
        url="https://arxiv.org/abs/1706.03762",
        published="2017-06-12",
        source="arXiv",
        categories="cs.CL, cs.LG"
    )
    
    print(f"\n[Test Paper]")
    print(f"Title: {test_paper.title}")
    print(f"Authors: {test_paper.authors}")
    print(f"Abstract: {test_paper.abstract[:100]}...")
    
    # Summarizerの初期化とテスト
    try:
        print(f"\n[Initializing Summarizer]")
        summarizer = OpenRouterSummarizer()
        print("✅ Summarizer initialized successfully")
        
        print(f"\n[Generating Summary]")
        print("Calling OpenRouter API...")
        result = summarizer.summarize(test_paper)
        
        print("\n✅ Summary generated successfully!")
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(result.summary)
        print("=" * 60)
        
        # 要約の長さチェック
        if result.summary:
            print(f"\n✅ Summary length: {len(result.summary)} characters")
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {str(e)}")
    except Exception as e:
        print(f"\n❌ Error during summarization: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_summarizer()
