import applescript
from scripts import *

class SpotifyControllerException(Exception):
    pass

class SpotifyController:
    def __init__(self):
        if not self._run_script(as_check_installed):
            raise SpotifyControllerException("Spotify not found on system")
        else:
            print("Spotify found on system")

    @property
    def is_open(self):
        if self._run_script(as_check_running):
            self.__is_open =  True
        else:
            self.__is_open = False

        return self.__is_open

    @property
    def is_playing(self):
        self.__is_playing = self._run_script(as_check_playing)
        return self.__is_playing

    def next_track(self):
        self._run_script(as_next_track)
        self.is_playing

    def prev_track(self):
        self._run_script(as_prev_track)
        self.is_playing

    def start_spotify(self):
        self.__is_open = self._run_script(as_start_spotify)

    def toggle_playing(self):
        self._run_script(as_toggle_play)

    def quit(self):
        self._run_script(as_quit)

    def _run_script(self, script):
        rtn = applescript.run(script)
        if rtn.out == 'true':
            return True
        elif rtn.out == 'false':
            return False
        else:
            raise SpotifyControllerException("Error: unrecognised spotify OSA response")



if __name__ == "__main__":
    sp = SpotifyController()
    print(f"Open: {sp.is_open}")
    print(f"Playing: {sp.is_playing}")
    sp.toggle_playing()
