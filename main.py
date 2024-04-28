from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from src.constants import Constants
from multiprocessing.pool import ThreadPool
from src.manga import Manga
from src.chapter import Chapter
from src.image import Image
from src import util
from PIL import Image as PilImage
import shutil
import requests
import time
import random


class Http:

    def __init__(self) -> None:        
        self.session = requests.Session()        

    def get(self, url: str) -> requests.Response:
        while True:
            headers = Constants.headers
            headers["User-Agent"] = random.choice(Constants.user_agents)
            try:
                print(f"[GET REQUEST -> {url}]")
                time.sleep(random.random())
                return self.session.get(url, stream=True, timeout=10, headers=headers)
            except Exception as e:
                print(f"HTTP EXCEPTION -> {e}. url -> {url}") 
        
    def download_image(self, image: Image) -> None:    
        r = self.get(image.link)
        with open(image.path, "wb") as file:
            for chunk in r.iter_content(1024):
                file.write(chunk)
        PilImage.open(image.path).convert("RGBA").save(image.path)
        print(f"[IMAGE {image.path} DOWNLOADED]") 

    def download_images(self, images: list[Image]) -> None:                
        with ThreadPool(4) as pool:
            pool.map(self.download_image, images)
        pool.join()                


class MangaScraper(ABC):
    
    @abstractmethod
    def __init__(self) -> None:
        super().__init__()
        
    def download_cover_image(self, manga: Manga) -> None:
        print(f"[Downloading cover image for {manga}...]")
        src = Constants.cover_images_dir / f"{manga.name}.png"
        dest = manga.path / "cover.png"
        shutil.copy(src, dest)        

    @abstractmethod
    def get_chaters_list(self, manga: Manga, soup: BeautifulSoup) -> list[Chapter]:
        pass

    @abstractmethod
    def get_images_list(self, chapter: Chapter, soup: BeautifulSoup) -> list[Image]:
        pass

    def run(self, manga: Manga, http: Http) -> None:                
        util.clear_terminal()
        self.download_cover_image(manga) 
        manga_page_soup = BeautifulSoup(http.get(manga.link).text, "lxml")
        chapters: list[Chapter] = self.get_chaters_list(manga, manga_page_soup)
        for chapter in chapters:
            chapter_soup = BeautifulSoup(http.get(chapter.chapter_link).text, "lxml")
            images: list[Image] = self.get_images_list(chapter, chapter_soup)
            http.download_images( images)            
            

class ReadMangaOnlineScrapper(MangaScraper):

    def __init__(self) -> None:
        super().__init__()
    
    def get_chaters_list(self, manga: Manga, soup: BeautifulSoup) -> list[Chapter]:
        div = soup.find("div", class_="page-content-listing single-page")
        chapters: list[str] = []
        for a in div.find_all("a"):
            chapters.append(a["href"])
        chapters = chapters[::-1]
        return [Chapter(manga, f"Chapter {i}", link) for i, link in enumerate(chapters)]
        

    def get_images_list(self, chapter: Chapter, soup: BeautifulSoup) -> list[Image]:
        div = soup.find("div", class_="reading-content")
        images: list[Image] = []
        for i, img in enumerate(div.find_all("img", class_="wp-manga-chapter-img")):
            images.append(Image(chapter.manga, chapter, img["src"].strip(), i))
        return images


class KakeguruiScrapper(MangaScraper):

    def __init__(self) -> None:
        super().__init__()
    
    def get_chaters_list(self, manga: Manga, soup: BeautifulSoup) -> list[Chapter]:
        div = soup.find("div", class_="manga-info-chapter")
        chapters: list[str] = []
        for a in div.find_all("a"):
            if "Kakegurui" in a["title"]:
                chapters.append(a["href"])
                
        chapters = chapters[::-1]        
        return [Chapter(manga, f"Chapter {i}", link) for i, link in enumerate(chapters)]

    def get_images_list(self, chapter: Chapter, soup: BeautifulSoup) -> list[Image]:
        div = soup.find("div", class_="container-chapter-reader")
        images: list[Image] = []
        for i, img in enumerate(div.find_all("img")):
            images.append(Image(chapter.manga, chapter, img["src"].strip(), i))
        return images
    

class ToondexScrapper(MangaScraper):

    def __init__(self) -> None:
        super().__init__()
    
    def get_chaters_list(self, manga: Manga, soup: BeautifulSoup) -> list[Chapter]:
        div = soup.find("div", {"id": "chapters-box"})
        chapters: list[str] = []
        for a in div.find_all("a"):
            href = a["href"]
            if "https://toondex.net" not in href:
                href = "https://toondex.net" + href
            chapters.append(href)
        chapters = chapters[::-1]
        return [Chapter(manga, f"Chapter {i}", link) for i, link in enumerate(chapters)]

    def get_images_list(self, chapter: Chapter, soup: BeautifulSoup) -> list[Image]:
        index = 0
        images: list[Image] = []
        for img in soup.find_all("img"):
            if "row" in img.get("id", ""):
                src = img.get("src", img.get("data-src"))
                images.append(Image(chapter.manga,chapter, src, index))
                index += 1
        return images


def choose(l: list[object]) -> object:
    while True:
        util.clear_terminal()
        print(Constants.bar)
        for i, item in enumerate(l):
            print(f"[{i}] -> {item}")
        n = input("Num: ")
        try:
            n = int(n)
            if n not in range(len(l)):
                raise ValueError()
            return l[n]
        except Exception:
            print("Choose a valid number...")
            time.sleep(1.5)



MANGA_SCRAPPER_BY_MANGA_NAME = {
    "Domestic Girlfriend": ReadMangaOnlineScrapper,
    "Jujutsu Kaisen": ReadMangaOnlineScrapper,
    "Battle Angel Alita": ReadMangaOnlineScrapper,
    "Kakegurui": KakeguruiScrapper,
    "Dorohedoro": ReadMangaOnlineScrapper,
    "Daughter Friend": ToondexScrapper
}


def main() -> None:
    Constants.tmp_dir.mkdir(exist_ok=True)
    Constants.res_dir.mkdir(exist_ok=True)
    Constants.cover_images_dir.mkdir(exist_ok=True, parents=True)    
    http = Http()
    mangas: dict[str, str] = util.read_json(Constants.manga_source_path)
    mangas: dict[str, Manga] = {k: Manga(k, v) for k, v in mangas.items()}
    manga_to_download: str = choose([x for x in mangas.keys()])
    scrapper: MangaScraper = MANGA_SCRAPPER_BY_MANGA_NAME[manga_to_download]()
    scrapper.run(mangas[manga_to_download], http)


if __name__ == "__main__":
    main()