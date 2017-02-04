# discobot
An insult slack bot that queries various music apis and finds the songs you want to listen to, and post them in slack.

Overview

Right now, discobot only knows the Spotify Web API, and so can only find songs on spotify. 

Commands:

Discobot currently only supports the following commands, but the readme will be updated as new commands are added:

@discobot play song "song_name" by "artist_name"
@discobot play "album_name" by "artist_name"
@discobot show [albums] by "artist-name"

That's it. If the song or album is on spotify, Discobot will find it and send you a link to play it within slack. 
