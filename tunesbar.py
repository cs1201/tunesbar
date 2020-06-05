import rumps
import os
import requests
from spotify import SpotifyControllerException, SpotifyController


class TunesBar(rumps.App):

    def __init__(self, name, icon):
        super(TunesBar, self).__init__(name="TunesBar",
                                       icon="resources/app_icon.png",
                                       quit_button=None)
        
        self.generate_menu()
        
        try:
            self.sp = SpotifyController()
        except SpotifyControllerException:
            raise SystemError()

        self.track_info = self.sp.track_info()

    def generate_menu(self):
        self.full_menu = [
                          rumps.MenuItem("🎵"),
                          rumps.MenuItem("👤"),
                          rumps.MenuItem("⏺"),
                          None,
                          rumps.MenuItem("▶️ Play", callback=self.play),
                          rumps.MenuItem("⏩ Next", callback=self.next),
                          rumps.MenuItem("⏪ Prev", callback=self.prev),
                          None,
                          rumps.MenuItem("Show"),
                          None,
                          rumps.MenuItem("Quit", callback=self.quit)]
        self.closed_menu = [rumps.MenuItem("Open Spotify", icon='resources/sp_icon.png', callback=self.start_spotify),
                            None,
                            rumps.MenuItem("Quit", callback=self.quit)]
        self.menu = self.full_menu

    def update_track_info(self):
        current_info = self.sp.track_info()
        if current_info != self.track_info and not any([x == "" for x in current_info]):
            self.menu["🎵"].title = f"🎵  {current_info['name']}"
            self.menu["👤"].title = f"👤 {current_info['artist']}"
            if self.get_artwork(current_info['artwork_url']):
                self.menu["⏺"].title = f"{current_info['album']}"
                self.menu["⏺"].icon = 'resources/album.png'
            else:
                self.menu["⏺"].title = f"⏺ {current_info['album']}"
            self.track_info = current_info

    def get_artwork(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            with open("resources/album.png", "wb+") as f:
                f.write(response.content)
            return True
        return False

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
            self.update_track_info()
        else:
            self.menu.clear()
            self.menu = self.closed_menu

    def next(self, _):
        self.sp.next_track()
        self.update_state()

    def prev(self, _):
        self.sp.prev_track()
        self.update_state()

    @rumps.clicked("Show")
    def show(self, _):
        self.sp.show()

    def quit(self, _):
        self.sp.quit()
        os.remove('resources/album.png')
        rumps.quit_application()
