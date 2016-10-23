import os
import time, logging
from slackclient import SlackClient
import spotipy

#Configure logging
logging.basicConfig(filename='.\discobot.log', format='%(levelname)s:%(asctime)s %(message)s', \
                datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)


# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
PLAY = "play"
FU = 'fuck off'
WHY = 'why the hell'
WAKE = 'are you awake?'
AWARE = 'are you aware?'
# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
spotify = spotipy.Spotify()

def validate_play_command(command):
    search_string = ((command.strip()).strip('play')).split("by")
    print "The search string we're returning is: " + str(search_string)
    return search_string

def return_song(query):
    requested_track = query[0].strip()
    artist_name = query[1].strip()
    print "The requested track we heard was: " + str(requested_track)
    print "The requested artist we heard was: " + str(artist_name)
    search_object = spotify.search(q=artist_name, limit=50)
    for i, t in enumerate(search_object['tracks']['items']):
        print t['name']
        if t['name'].lower() == requested_track.lower():
            return t['external_urls']['spotify']

    return False




def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """

    response = "No compute."

    if command.startswith(PLAY):
        query = validate_play_command(command)
        song_url = return_song(query)
        if song_url == False:
            response = "Sorry, I couldn't find that song. Huh, must be your own fault. Layer eight issue I'll assume"
        else:
            response = song_url
    
    if command.startswith(FU):
                response = "And fuck you, too, of course."
    
    if command.startswith(WHY):
                response = "Yeah, well, what are you going to do?"
    
    if command.startswith(WAKE):
                response = "I am awake"
    
    if command.startswith(AWARE):
                response = "The fire is out. The master is in"
    
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
