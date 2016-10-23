import spotipy

#instantiate spotify object
spotify = spotipy.Spotify()

#create artist search object
name = 'ilias katelanos'
requested_track = 'Crying - Ilias Katelanos Remix'
track_list = dict()
f = open('spotify3.txt', 'w')

artist_object = (spotify.search(q='artist:' + name, type='artist'))['artists']['items']
artist_name = artist_object[0]['name']
artist_uri = artist_object[0]['uri'].split(":")[2]
search_object = spotify.search(q=artist_name, limit=90)

for i, t in enumerate(search_object['tracks']['items']):
    #track_list.update({(t['name']):(t)})
    if t['name'] == requested_track.spl
    if t['album']:
        f.write("This is an album named: " + t['name'] + "\n\n" + str(t['album']))
    else:
        f.write("This is not an album: " + "\n\n\n\n\n\n\n" + str(t))
f.close()
        



if len(items) > 0:
    artist = items[0]
    print artist['name'], artist['images'][0]['url']


And the actual dictionary:

[{u'genres': [], u'name': u'Agent Atari', u'external_urls': {u'spotify': u'https://open.spotify.com/artist/32VsmWsajBJi6o3YyTrHFr'}, u'popularity': 0, u'uri': u'spotify:artist:32VsmWsajBJi6o
3YyTrHFr', u'href': u'https://api.spotify.com/v1/artists/32VsmWsajBJi6o3YyTrHFr', u'followers': {u'total': 1, u'href': None}, u'images': [{u'url': u'https://i.scdn.co/image/64b389e8ec6ba56b5
95d22794a69c4346765c780', u'width': 640, u'height': 640}, {u'url': u'https://i.scdn.co/image/c790a820bd5d29b83e5ebbd262782960ac80d679', u'width': 300, u'height': 300}, {u'url': u'https://i.s
cdn.co/image/d073e1313eb3a2bf6fbdbc3cc67b1dfd189d88f5', u'width': 64, u'height': 64}], u'type': u'artist', u'id': u'32VsmWsajBJi6o3YyTrHFr'}]


