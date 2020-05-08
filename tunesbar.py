import rumps
import applescript
from scripts import *
from spotify import SpotifyControllerException, SpotifyController

class TunesBar(rumps.App):

    def __init__(self, name, icon):
        super(TunesBar, self).__init__(name, icon=icon)
        self.full_menu = [rumps.MenuItem("▶️ Play", callback=self.play),
                     rumps.MenuItem("⏩ Next", callback=self.next),
                     rumps.MenuItem("⏪ Prev", callback=self.prev),
                     None,
                     ["Share", [rumps.MenuItem("Song", callback=self.share('song')),
                                rumps.MenuItem("Artist", callback=self.share('artist')),
                                rumps.MenuItem("Album", callback=self.share('album'))]],
                     None,
                     rumps.MenuItem("Quit", callback=self.quit)]
        self.menu = self.full_menu
        self.sp = SpotifyController()

    def check_spotify_state(self):
        rtn = applescript.run(as_check_running)
        if rtn.out == "true":
            self.menu.clear()
            self.menu = self.full_menu
            print("Spotify Running")
            return True
        elif rtn.out == "false":
            self.menu.clear()
            self.menu = self.off_menu
            print("Spotify Not Running")
            return False
        else:
            print(rtn.out)

    def share(self,_):
        pass

    def start_spotify(self, _):
        """
            Open spotify app and update menu to show transport controls
        """
        self.sp.start_spotify()
        self.menu.clear()
        self.menu = self.full_menu
        
    def play(self, _):
        """
            Toggle spotify to play/pause - update menu item title
        """
        self.menu["▶️ Play"] = "⏸ Pause" if self.sp.is_playing else "▶️ Play"
        self.sp.toggle_playing()

    @rumps.timer(1)
    def update_state(self, _):
        if self.sp.is_open:
            self.menu["▶️ Play"].title = "⏸ Pause" if self.sp.is_playing else "▶️ Play"
        else:
            self.menu.clear()
            self.menu = [rumps.MenuItem("Open Spotify", callback=self.start_spotify), rumps.MenuItem("Quit", callback=self.quit)]

    def next(self, _):
        self.sp.next_track()
        self.update_state()

    def prev(self, _):
        self.sp.prev_track()
        self.update_state()

    def quit(self, _):
        self.sp.quit()
        rumps.quit_application()


if __name__ == "__main__":
    rumps.debug_mode(True)
    tb = TunesBar(name="TunesBar", icon = 'app_icon.png')
    tb.run()