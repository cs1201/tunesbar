as_check_installed = """try
                        	tell application "Finder" to get application file id "com.spotify.client"
                        	set appExists to true
                        on error
                        	set appExists to false
                        end try
                    """

as_check_running = """ if application "Spotify" is running then
                            set is_running to true
                        else
                            set is_running to false
                        end if
                    """

as_check_playing = """tell application "Spotify"
	                        if player state is playing then
		                        set is_playing to true
	                        else if player state is paused then
		                        set is_playing to false
	                      end if
                        end tell
                    """

as_start_spotify =  """ tell application "Spotify" to activate
                        set return to true
                    """

as_toggle_play =  """   tell application "Spotify"
                            set state to player state
                            if state = playing then
                                pause
                            else if state = paused then
                                play
                            end if
                            set return to true
                        end tell
                    """

as_next_track = """ tell application "Spotify"
	                    next track
                        set return to true
                    end tell
                """

as_prev_track = """ tell application "Spotify"
	                    previous track
                        set return to true
                    end tell
                """

as_quit = """
            if application "Spotify" is running then
                tell application "Spotify" to quit
            end if
            set return to true
          """