"""OpenRouter Summarizer のテスト"""

import pytest
from unittest.mock import Mock, patch
from src.summarizers.openrouter_summarizer import OpenRouterSummarizer
from src.models import PaperResult


@pytest.fixture
def sample_paper():
    """テスト用の論文データ"""
    return PaperResult(
        id="2401.00001",
        title="Test Paper on Machine Learning",
        authors="John Doe, Jane Smith",
        abstract="This paper presents a novel approach to machine learning. We propose a new algorithm that improves performance by 20%. Our experiments show significant improvements over baseline methods.",
        url="https://arxiv.org/abs/2401.00001",
        published="2024-01-01",
        source="arXiv",
        categories="cs.LG"
    )


@pytest.fixture
def mock_api_response():
    """モックAPIレスポンス (OpenAI completion object)"""
    mock_response = Mock()
    mock_message = Mock()
    mock_message.content = "この論文は機械学習の新しいアプローチを提案しています。提案された新しいアルゴリズムは、パフォーマンスを20%改善します。実験結果は、ベースライン手法と比較して大幅な改善を示しています。"
    mock_choice = Mock()
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    return mock_response


class TestOpenRouterSummarizer:
    """OpenRouterSummarizerのテストクラス"""
    
    def test_initialization_with_api_key(self):
        """APIキーを指定した初期化のテスト"""
        summarizer = OpenRouterSummarizer(api_key="test_key", model="test_model")
        assert summarizer.api_key == "test_key"
        assert summarizer.model == "test_model"
    
    def test_initialization_without_api_key(self):
        """APIキーなしの初期化でエラーが発生することをテスト"""
        with patch('src.summarizers.openrouter_summarizer.config') as mock_config:
            mock_config.OPENROUTER_API_KEY = ""
            with pytest.raises(ValueError, match="OpenRouter API key is required"):
                OpenRouterSummarizer()
    
    @patch('src.summarizers.openrouter_summarizer.OpenAI')
    def test_summarize_success(self, mock_openai, sample_paper, mock_api_response):
        """正常に要約が生成されることをテスト"""
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_api_response
        mock_openai.return_value = mock_client
        
        summarizer = OpenRouterSummarizer(api_key="test_key")
        result = summarizer.summarize(sample_paper)
        
        assert result.summary is not None
        assert len(result.summary) > 0
        assert "機械学習" in result.summary
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('src.summarizers.openrouter_summarizer.OpenAI')
    def test_summarize_with_retry(self, mock_openai, sample_paper, mock_api_response):
        """リトライが機能することをテスト"""
        # 1回目は失敗、2回目は成功
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = [
            Exception("API Error"),
            mock_api_response
        ]
        mock_openai.return_value = mock_client
        
        summarizer = OpenRouterSummarizer(api_key="test_key", retry_delay=0)
        result = summarizer.summarize(sample_paper)
        
        assert result.summary is not None
        assert mock_client.chat.completions.create.call_count == 2
    
    @patch('src.summarizers.openrouter_summarizer.OpenAI')
    def test_summarize_all_retries_fail(self, mock_openai, sample_paper):
        """全てのリトライが失敗した場合のテスト"""
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai.return_value = mock_client
        
        summarizer = OpenRouterSummarizer(
            api_key="test_key",
            max_retries=2,
            retry_delay=0
        )
        
        with pytest.raises(Exception):
            summarizer.summarize(sample_paper)
        
        assert mock_client.chat.completions.create.call_count == 2
    
    def test_create_prompt(self, sample_paper):
        """プロンプト生成のテスト"""
        summarizer = OpenRouterSummarizer(api_key="test_key")
        prompt = summarizer._create_prompt(sample_paper.title, sample_paper.abstract)
        
        assert sample_paper.title in prompt
        assert sample_paper.abstract in prompt
        assert "要約" in prompt
        assert "日本語" in prompt
    
    def test_extract_summary_success(self, mock_api_response):
        """要約の抽出が成功することをテスト"""
        summarizer = OpenRouterSummarizer(api_key="test_key")
        summary = summarizer._extract_summary(mock_api_response)
        
        assert summary == mock_api_response.choices[0].message.content
    
    def test_extract_summary_invalid_response(self):
        """不正なレスポンスの場合にエラーが発生することをテスト"""
        summarizer = OpenRouterSummarizer(api_key="test_key")
        invalid_response = Mock()
        invalid_response.choices = []
        
        with pytest.raises(ValueError, match="Invalid API response format"):
            summarizer._extract_summary(invalid_response)
    
    def test_extract_summary_empty_content(self):
        """空の要約が返された場合にエラーが発生することをテスト"""
        summarizer = OpenRouterSummarizer(api_key="test_key")
        empty_response = Mock()
        mock_message = Mock()
        mock_message.content = "   "
        mock_choice = Mock()
        mock_choice.message = mock_message
        empty_response.choices = [mock_choice]
        
        with pytest.raises(ValueError, match="Empty summary returned from API"):
            summarizer._extract_summary(empty_response)
