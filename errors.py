class StatusCodeError(Exception):
    """Raised when Musixmatch API returns any status code not 200 or 404"""
    def __init__(self, status_code):
        self.status_code = status_code

class SongNotFoundError(Exception):
    """Raised when a Musixmatch track id is not in the Musixmatch DB"""
    pass

class TermNotAvailableError(Exception):
    """Raised when a search term not in the 5000 word search set is used"""
    def __init__(self, term):
        self.term = term
