"""論文検索結果のデータモデル"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PaperResult:
    """論文検索結果を表すデータクラス（ソース非依存）"""
    
    id: str
    title: str
    authors: str
    abstract: str
    url: str
    published: str
    source: str
    categories: Optional[str] = None
    
    def to_dict(self) -> dict:
        """辞書形式に変換"""
        return {
            "id": self.id,
            "title": self.title,
            "authors": self.authors,
            "abstract": self.abstract,
            "url": self.url,
            "published": self.published,
            "source": self.source,
            "categories": self.categories
        }