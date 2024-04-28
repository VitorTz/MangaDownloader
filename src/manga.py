from src.constants import Constants


class Manga:

    def __init__(self, name: str, link: str) -> None:
        self.name = name
        self.link = link
        self.path = Constants.manga_dir / name
        self.path.mkdir(exist_ok=True, parents=True)        
        
    def __str__(self) -> str:
        return self.name