from pathlib import Path


class Constants:

    tmp_dir = Path("tmp")
    manga_dir = Path("/mnt/HD/Manga")
    res_dir = Path("res")
    cover_images_dir = res_dir / "cover"
    
    manga_source_path = Path("res/source.json")
    user_agents: list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.55",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"
    ]
    headers: dict = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com"
    }

    bar = '=' * 40

    driver_path: dict[str, Path] = {
        "Linux": "res/driver/geckodriver_linux",
        "Windows": "res/driver/geckodriver_win.exe",
        "macOS": "res/driver/geckodriver_macos"
    }