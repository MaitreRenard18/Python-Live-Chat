import os
import sys


def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), relative_path)
