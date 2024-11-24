import instagrapi

from pathlib import Path
from urllib.parse import urlparse


def handle_folder(folder):
    folder = Path("downloads") / folder
    folder.mkdir(parents=True, exist_ok=True)
    return folder

def get_filepath(url, filename, folder):
    url = str(url)
    fname = urlparse(url).path.rsplit("/", 1)[1]
    filename = "%s.%s" % (filename, fname.rsplit(".", 1)[1]) if filename else fname
    path = Path(folder) / filename
    return path


class Client(instagrapi.Client):

    def from_file(self, url: str, filename: str = "", folder: Path = "") -> Path:
        path = get_filepath(url, filename, folder)
        if path.exists():
            print("Getting", path, "from file")
            return path.resolve()
        print("Downloading", url, "into", path)
        return None

    def photo_download_by_url(self, url: str, filename: str = "", folder: Path = "") -> Path:
        folder = handle_folder(folder)
        return self.from_file(url, filename, folder) or super().photo_download_by_url(url, filename, folder)
        
    def video_download_by_url(self, url: str, filename: str = "", folder: Path = "") -> Path:
        folder = handle_folder(folder)
        return self.from_file(url, filename, folder) or super().video_download_by_url(url, filename, folder)
