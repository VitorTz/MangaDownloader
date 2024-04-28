from src.manga import Manga


class Chapter:

    def __init__(self, manga: Manga, chapter_name: str, chapter_link: str) -> None:
        self.manga = manga
        self.chapter_name = chapter_name
        self.chapter_link = chapter_link
        self.path = manga.path / self.chapter_name        
        self.path.mkdir(exist_ok=True)
    
    def __str__(self) -> str:
        return f"{self.manga.name}/{self.chapter_name}"