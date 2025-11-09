"""OpenRouter APIを使用した論文要約機能"""

import logging
import time
from typing import Optional

from ..models import PaperResult
from ..config import config
from openai import OpenAI

logger = logging.getLogger(__name__)


class OpenRouterSummarizer:
    """OpenRouter APIを使用して論文を要約するクラス"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: int = 2
    ):
        """
        Args:
            api_key: OpenRouter APIキー（Noneの場合は設定から取得）
            model: 使用するモデル名（Noneの場合は設定から取得）
            max_retries: 最大リトライ回数
            retry_delay: リトライ間隔（秒）
        """
        self.api_key = api_key or config.OPENROUTER_API_KEY
        self.model = model or config.OPENROUTER_MODEL
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")
        
        logger.info(f"OpenRouterSummarizer initialized with model: {self.model}")
    
    def summarize(self, paper: PaperResult) -> PaperResult:
        """
        論文を要約してPaperResultに格納
        
        Args:
            paper: 要約する論文のPaperResultオブジェクト
            
        Returns:
            要約が追加されたPaperResultオブジェクト
            
        Raises:
            Exception: API呼び出しに失敗した場合
        """
        logger.info(f"Summarizing paper: {paper.title}")
        
        try:
            summary = self._generate_summary(paper.title, paper.abstract)
            paper.summary = summary
            logger.info(f"Successfully summarized paper: {paper.id}")
            return paper
        except Exception as e:
            logger.error(f"Failed to summarize paper {paper.id}: {str(e)}")
            raise
    
    def _generate_summary(self, title: str, abstract: str) -> str:
        """
        OpenRouter APIを使用して要約を生成
        
        Args:
            title: 論文タイトル
            abstract: 論文アブストラクト
            
        Returns:
            日本語の要約文
        """
        prompt = self._create_prompt(title, abstract)
        
        for attempt in range(self.max_retries):
            try:
                response = self._call_api(prompt)
                summary = self._extract_summary(response)
                return summary
            except Exception as e:
                if attempt < self.max_retries - 1:
                    logger.warning(
                        f"API call failed (attempt {attempt + 1}/{self.max_retries}): {str(e)}"
                    )
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    logger.error(f"All retry attempts failed: {str(e)}")
                    raise
    
    def _create_prompt(self, title: str, abstract: str) -> str:
        """要約用のプロンプトを作成"""
        return f"""以下の技術論文のタイトルとアブストラクトを読み、日本語で簡潔に要約してください。
要約は3-5文程度で、論文の主な貢献・手法・結果を含めてください。

タイトル: {title}

アブストラクト:
{abstract}

要約:"""
    
    def _call_api(self, prompt: str):
        """
        OpenRouter APIを呼び出し
        
        Args:
            prompt: 送信するプロンプト
            
        Returns:
            OpenAI completion object
        """

        client = OpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
            timeout=60
        )

        completion = client.chat.completions.create(
            extra_headers= {
                "HTTP-Referer": "https://github.com/research-paper-bot",
                "X-Title": "Research Paper Summarizer Bot"
            },
            extra_body={},
            model= self.model,
            messages=
            [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=500,
            stream=False,
        )
        
        return completion
    
    def _extract_summary(self, response) -> str:
        """
        APIレスポンスから要約テキストを抽出
        
        Args:
            response: OpenAI completion object
            
        Returns:
            要約テキスト
        """
        try:
            summary = response.choices[0].message.content.strip()
            finish_reason = response.choices[0].finish_reason
            if (finish_reason != "stop"):
                logger.warning(f"Completion finished with reason: {finish_reason}")
            if not summary:
                raise ValueError("Empty summary returned from API")
            return summary
        except (AttributeError, IndexError) as e:
            logger.error(f"Failed to extract summary from response: {response}")
            raise ValueError(f"Invalid API response format: {str(e)}")
