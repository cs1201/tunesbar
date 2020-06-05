import applescript
from scripts import SpotifyAppleScripts


class SpotifyControllerException(Exception):
    pass


class SpotifyController:
    def __init__(self):
        self.scripts = SpotifyAppleScripts()
        if not self._run_script(self.scripts.check_installed):
            raise SpotifyControllerException("Spotify not found on system")

    @property
    def is_open(self):
        if self._run_script(self.scripts.check_running):
            self.__is_open = True
        else:
            self.__is_open = False

        return self.__is_open

    @property
    def is_playing(self):
        self.__is_playing = self._run_script(self.scripts.check_playing)
        return self.__is_playing

    def next_track(self):
        self._run_script(self.scripts.next_track)
        self.is_playing

    def prev_track(self):
        self._run_script(self.scripts.prev_track)
        self.is_playing

    def start_spotify(self):
        self.__is_open = self._run_script(self.scripts.start_spotify)

    def toggle_playing(self):
        self._run_script(self.scripts.toggle_play)

    def track_info(self):
        rtn = applescript.run(self.scripts.get_info).out.split(',')
        info = dict()
        if rtn != None:
            if len(rtn) != 4:
                rtn = [""] * 4
            info = {
                'name': rtn[0],
                'artist': rtn[1],
                'album': rtn[2],
                'artwork_url': rtn[3]
            }
        return info
        

    def show(self):
        self._run_script(self.scripts.show)

    def quit(self):
        self._run_script(self.scripts._quit)

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
