import requests
import json
import sqlite3

class SongScraper:
    def __init__(self):
        self.base_url = 'https://api.musixmatch.com/ws/1.1/'
        # below is almost certainly a vulnerability
        self.apikey   = 'cba6ce94f03fdb7b881f441be6ebcbe1'
        self.conn     = sqlite3.connect('mxm_dataset.db')
        self.cursor   = self.conn.cursor()

    def search_lyric(self, term):
        results    = self.cursor.execute('SELECT mxm_tid, count FROM lyrics WHERE ' +
                                         'word="' + term + '" ' +
                                         'ORDER BY RANDOM() LIMIT 1')
        r = results.fetchone()
        mxm_tid = r[0]
        count = r[1]

        song_info  = {}
        tstring = self.base_url + 'track.get?' +'commontrack_id=' + str(mxm_tid) +'&apikey=' + self.apikey
        track_info = requests.get(self.base_url + 'track.get?' +
                                  'commontrack_id=' + str(mxm_tid) +
                                  '&apikey=' + self.apikey)
        lyrics     = requests.get(self.base_url + 'track.lyrics.get?' +
                                  'commontrack_id=' + str(mxm_tid) +
                                  '&apikey=' + self.apikey)

        track_info_json = json.loads(track_info.text)
        lyrics_json     = json.loads(lyrics.text)
        # TODO: do something when status code not 200
        # if track_info_json['message']['header']['status_code'] != 200:
        #    raise(BadStatusCode)

        print('tstring is: ' + tstring)
        print('mxm_tid = ' + str(mxm_tid))
        print(json.dumps(track_info_json, indent=2))
        print(json.dumps(lyrics_json, indent=2))

        artist = track_info_json['message']['body']['track']['artist_name']
        album  = track_info_json['message']['body']['track']['album_name']
        if lyrics_json['message']['header']['status_code'] == 404:
            lyrics = "Unfortunately, Musixmatch doesn't have the rights to these lyrics. But, they say '" + term + "' in this song " + str(count) + " times"
        else:
            lyrics = lyrics_json['message']['body']['lyrics']['lyrics_body']
        song_info['artist'] = artist
        song_info['album']  = album
        song_info['lyrics'] = lyrics

        return song_info
