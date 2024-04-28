from src.constants import Constants
from src.manga import Manga
from src.chapter import Chapter


class Image:
    
    def __init__(self, manga: Manga, chapter: Chapter, link: str, num: int) -> None:
        self.manga = manga
        self.link = link
        self.num = int(num)
        self.chapter = chapter
        self.path = chapter.path / f"{self.num}.png"    
    
    def __str__(self) -> str:
        return f"{self.path}"