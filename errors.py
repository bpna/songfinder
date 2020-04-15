class StatusCodeError(Exception):
    """Raised when Musixmatch API returns any status code not 200 or 404"""
    def __init__(self, status_code):
        self.status_code = status_code

class SongNotFoundError(Exception):
    """Raised when a Musixmatch track id is not in the Musixmatch DB"""
    pass
