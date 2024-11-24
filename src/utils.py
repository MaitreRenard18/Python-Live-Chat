import os
import sys
import tempfile
import urllib.request


def resource_path(relative_path: str) -> str:
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), relative_path)


def get_file_from_url(url: str) -> str:
    if os.path.exists(url):
        return url

    request = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    })
    
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(urllib.request.urlopen(request).read())
        return temp.name
