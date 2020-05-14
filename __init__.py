from tunesbar import TunesBar
import sys

if __name__ == "__main__":
    try:
        tb = TunesBar(name='', icon='')
    except SystemError:
        print("Could not start TunesBar - check Spotify is installed")
        sys.exit()
    tb.run()
