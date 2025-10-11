from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class GameMetadata:
    id: int
    title: str
    cart_url: str
    cover_url: str
    developer: str
    release_date: datetime
    tags: List[str]
    description: str

    @staticmethod
    def empty():
        return GameMetadata(0, '', '', '', '', datetime.fromtimestamp(0), [], '')    
