import requests
import json
import sqlite3
from errors import StatusCodeError, SongNotFoundError

class SongScraper:
    def __init__(self, debug=False):
        self.base_url = 'https://api.musixmatch.com/ws/1.1/'
        # below is almost certainly a vulnerability
        self.apikey   = 'cba6ce94f03fdb7b881f441be6ebcbe1'
        self.conn     = sqlite3.connect('mxm_dataset.db')
        self.cursor   = self.conn.cursor()
        self.debug    = debug

    def get_track_info(self, mxm_tid):
        """Finds the artist and album names for a Musixmatch track ID

        Args:
            mxm_tid (string): Musixmatch track ID
        Returns:
            Dictionary containing:
                "artist": artist name (string)
                "album" : album name (string)
        Raises:
            SongNotFoundError when Musixmatch track ID is not contained in
            the Musixmatch DB"""
        track_info_req_url = self.base_url + \
                             'track.get?' + \
                             'commontrack_id=' + str(mxm_tid) + \
                             '&apikey=' + self.apikey
        track_info_res  = requests.get(track_info_req_url)
        track_info_json = json.loads(track_info_res.text)
        status_code = track_info_json['message']['header']['status_code']

        if self.debug:
            print('TRACK INFO REQUEST URL ====================================')
            print(track_info_req_url)
            print('TRACK INFO JSON ===========================================')
            print(json.dumps(track_info_json, indent=2))

        track_info = {}
        if status_code == 404:
            raise SongNotFoundError
        elif status_code != 200:
            raise StatusCodeError(status_code)
        else:
            track_info['artist'] = track_info_json['message']['body']['track']\
                                                  ['artist_name']
            track_info['album']  = track_info_json['message']['body']['track']\
                                                  ['album_name']
        return track_info

    def get_lyrics_info(self, mxm_tid):
        """Finds the lyrics for a Musixmatch track ID

        Args:
            mxm_tid (string): Musixmatch track ID
        Returns:
            Dictionary containing:
                "lyrics"     : track lyrics (string)
                "tracker_url": album name (string)
        Raises:
            None"""
        lyrics_req_url = self.base_url + \
                         'track.lyrics.get?' + \
                         'commontrack_id=' + str(mxm_tid) + \
                         '&apikey=' + self.apikey
        lyrics_res  = requests.get(lyrics_req_url)
        lyrics_json = json.loads(lyrics_res.text)
        status_code = lyrics_json['message']['header']['status_code']

        if self.debug:
            print('LYRICS REQUEST URL ========================================')
            print(lyrics_req_url)
            print('LYRICS JSON ===============================================')
            print(json.dumps(lyrics_json, indent=2))

        lyrics_info = {}
        lyrics_info['tracker_url'] = ''

        if status_code == 404:
            lyrics_info['lyrics']      = "Lyrics unavailable"
        elif status_code != 200:
            raise StatusCodeError(status_code)
        else:
            lyrics_info['lyrics']      = lyrics_json['message']['body']\
                                                    ['lyrics']['lyrics_body']
            lyrics_info['tracker_url'] = lyrics_json['message']['body']\
                                                    ['lyrics']\
                                                    ['script_tracking_url']
        return lyrics_info

    def search_lyric(self, term):
        """Given a search term, finds a song containing that search term

        Args:
            term (string): Search term entered by the user
        Returns:
            Dictionary containing:
                "count"      : occurrences of search term in song (string)
                "artist"     : artist name (string)
                "album"      : album name (string)
                "lyrics"     : track lyrics (string)
                "tracker_url": album name (string)
        Raises:
            None"""
        results = self.cursor.execute('SELECT mxm_tid, count ' +
                                      'FROM lyrics WHERE ' +
                                      'word="' + term + '" ' +
                                      'ORDER BY RANDOM() LIMIT 100')
        tracks_found = 0
        song_info = {}
        while tracks_found < 1:
            try:
                r       = results.fetchone()
                mxm_tid = r[0]
                count   = r[1]
                if self.debug:
                    print('mxm_tid = ' + str(mxm_tid))

                track_info    = self.get_track_info(mxm_tid)
                tracks_found += 1
                lyrics_info   = self.get_lyrics_info(mxm_tid)
            except SongNotFoundError:
                pass

        song_info['count']       = count
        song_info['artist']      = track_info['artist']
        song_info['album']       = track_info['album']
        song_info['lyrics']      = lyrics_info['lyrics']
        song_info['tracker_url'] = lyrics_info['tracker_url']

        return song_info
