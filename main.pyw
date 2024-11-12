import sys

from src import LiveChat

if __name__ == "__main__":
    show_sender = True
    if len(sys.argv) > 1:
        print(sys.argv[1].lower())
        show_sender = sys.argv[1].lower() == 'true'
    
    app = LiveChat(show_sender)
    app.exec()
