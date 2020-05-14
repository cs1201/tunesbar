from dataclasses import dataclass


@dataclass
class SpotifyAppleScripts:
    check_installed: str = """try
                                tell application "Finder" to get application file id "com.spotify.client"
                                set appExists to true
                            on error
                                set appExists to false
                            end try
                            """

    check_running: str = """ if application "Spotify" is running then
                                set is_running to true
                            else
                                set is_running to false
                            end if
                        """

    check_playing: str = """tell application "Spotify"
                                if player state is playing then
                                    set is_playing to true
                                else if player state is paused then
                                    set is_playing to false
                            end if
                            end tell
                        """

    start_spotify: str = """ tell application "Spotify" to activate
                            set return to true
                        """

    toggle_play: str = """   tell application "Spotify"
                                set state to player state
                                if state = playing then
                                    pause
                                else if state = paused then
                                    play
                                end if
                                    set return to true
                              end tell
                        """

    next_track: str = """ tell application "Spotify"
                            next track
                            set return to true
                        end tell
                    """

    prev_track: str = """ tell application "Spotify"
                            previous track
                            set return to true
                        end tell
                    """

    _quit: str = """
                if application "Spotify" is running then
                    tell application "Spotify" to quit
                end if
                set return to true
            """

    show: str = """
                tell application "Finder"
                    set foremost to true
                end tell
                tell application "Spotify"
                    activate
                    set minituarized to false
                    set foremost to true
                end tell
            """
