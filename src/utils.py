import os
import sys
import tempfile
import urllib.request


def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), relative_path)


def get_file_from_url(url:str) -> str:
    if os.path.exists(url):
        return url
    
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(urllib.request.urlopen(url).read())
        return temp.name
