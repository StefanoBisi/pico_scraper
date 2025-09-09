from dataclasses import dataclass
from datetime import datetime


@dataclass
class GameMetadata:
    id: int
    title: str
    cart_url: str
    cover_url: str
    developer: str
    release_date: datetime
    tags: list[str]
    description: str

    @staticmethod
    def empty():
        return GameMetadata(0, '', '', '', '', datetime.fromtimestamp(0), [], '')    
