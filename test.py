from src.manga import Manga
from src.chapter import Chapter
from src.image import Image
from main import Http



http = Http()
manga = Manga("Kakegurui", "https://mangakakalot.com/read-ox1tq158504848061")
chapter = Chapter(manga, "Chapter 0", "https://mangakakalot.com/chapter/kakegurui/chapter_1")
image = Image(manga, chapter, "https://v10.mkklcdnv6tempv4.com/img/tab_10/00/15/60/pi952917/chapter_1_jyabami_yumeko/1-o.jpg", 0)
http.download_image_from_webdriver(image)
