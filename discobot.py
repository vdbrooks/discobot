import os, sys
import time, logging
from slackclient import SlackClient
import spotipy

#Configure logging -- there is no logging yet, fyi
logging.basicConfig(filename='.\discobot.log', format='%(levelname)s:%(asctime)s %(message)s', \
                datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)


# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# Command CONSTANTS
AT_BOT = "<@" + BOT_ID + ">"
PLAY_SONG = "play song"
PLAY_ALBUM = "play album"
FU = 'fuck off'
WHY = 'why the hell'
WAKE = 'are you awake?'
AWARE = 'are you aware?'
HELP = 'help'
ASSHOLE = 'you\'re an asshole'
VERSION = 'what version are you running'

# instantiate Slack & Spotify clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
spotify = spotipy.Spotify()

def process_play_command(command):
    result = command.split('by')
    song_name = result[0].split('play song')[1].strip()
    artist_name = result[1].strip()
    search_string = [song_name, artist_name]
    return search_string

def process_album_command(command):
    result = command.split('by')
    album_name = result[0].split('play album')[1].strip()
    artist_name = result[1].strip()
    search_string = [album_name,artist_name]
    return search_string

def return_song(artist,requested_track):
    try:
        print "The requested track we heard was: " + unicode(requested_track)
        print "The requested artist we heard was: " + unicode(artist['name'])
    except Exception as e:
        print "Ran into the following error: " + str(e)
        return False 
    count = 0
    response = spotify.search(q=artist['name'], limit=50)
    while response:


        tracks = response['tracks']
        if tracks['items'] == []:
            return False
        for i, item in enumerate(tracks['items']):
            try:
                print "The value of items['name'].lower()" + unicode(item['name'].lower()) + " while the name of the requested track is " + unicode(requested_track.lower())
            except (UnicodeEncodeError, spotipy.client.SpotifyException) as e:
                print "Couldn't compare this song because it contained a unicode character. Fix this asshole."
                pass
            if item['type'] == 'track' and requested_track.lower() in item['name'].lower():
                for entry in item['artists']:
                    if entry['id'] == artist['id']:
                        return item['external_urls']['spotify']
            count += 1
        if tracks['next']:
            response = spotify.next(tracks)
        else:
            message = [count,False]
            return message

    return False

def get_requested_album(search_list,albums):
    if not albums:
        return False
    try:
        requested_album = search_list[0]
        requested_artist = search_list[1]
    except Exception as e:
        return False

    
    for album in albums:
        if album['name'].lower() == requested_album.lower():
            return album['external_urls']['spotify']   

    return False
 
def get_artist(name):
    results = spotify.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None

def get_artist_name(query):
    artist_name = query[1].strip()
    return artist_name

def get_requested_track(query):
    requested_track = query[0].strip()
    return requested_track

def show_artist_albums(artist):
    if artist == None:
        return False
    albums = []
    results = spotify.artist_albums(artist['id'], album_type=None)
    albums.extend(results['items'])
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    if albums:
        return albums
    else:
        return False



def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """

    response = "No compute."

    if command.startswith(PLAY_SONG):
        search_list = process_play_command(command)
        artist = get_artist(get_artist_name(search_list))
        print artist
        if artist == None:
            response = "There is no artist by the name of " + search_list[1] + "\n\n Please check your spelling and try again...dumb muther fucker"
        else:
            requested_track = get_requested_track(search_list)
            song_url = return_song(artist,requested_track)
            print str(song_url[1])
            if song_url[1] == False:
                response = "Sorry, I couldn't find a song called " + unicode(search_list[0]) + " by an artist named " + unicode(search_list[1]) + "\n\n We checked over " + str(song_url[0]) + " songs but no luck" + "\n\n Please check that you spelled either the artist or song name correctly"
            else:
                response = song_url

    if command.startswith(PLAY_ALBUM):
        search_list = process_album_command(command)
        artist = get_artist(get_artist_name(search_list))
        albums = show_artist_albums(artist)
        album_url = get_requested_album(search_list, albums)
        if album_url == False:
            response = "Sorry, I couldn't find an album called " + unicode(search_list[0]) + " by the artist " + unicode(search_list[1]) + "\n\n please check that you spelled the album and/or artist name correctly"
        else:
            response = album_url

    
    if command.startswith(FU):
                response = "And fuck you, too, of course."
    
    if command.startswith(WHY):
                response = "Yeah, well, what are you going to do?"
    
    if command.startswith(WAKE):
                response = "I am awake"
    
    if command.startswith(AWARE):
                response = "The fire is out. The master is in"

    if command.startswith(VERSION):
                response = "development-version-1.1 on EC2" 

    if command.startswith(HELP):
        response = "\"Oh help me, help me!\" I'm a little fucking baby that needs help \n\n To play a particular song use: @discobot play song song_name by artist_name \n\n To play a particular album use: @discobot play album album_name by artist_name . \n\n Obviously, we're only able to play songs that actually exists in spotify\n\n"  
  
    if command.startswith(ASSHOLE):
                response = "And you're a prick, so suck a dick"

    
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("DiscoBot! connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
                print "The command we received is: " + str(command)
                print "It's type is: " + str(type(command))
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
