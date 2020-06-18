class Song(object):
    def __init__(self):
        self._singer: str = None
        self._title: str = None

    @property
    def singer(self):
        return self._singer

    @singer.getter
    def singer(self, arg):
        self._singer = arg

    @property
    def title(self):
        return self._title

    @title.getter
    def title(self, arg):
        self._title = arg


class Playlist(object):
    def __init__(self):
        self._tracks: [Song] = []
        self._singers: dict = {}

    def add(self, song):
        self._tracks.append(song)
        self._singers[song.singer] = song.title

    @property
    def tracks(self):
        return self._tracks

    @property
    def singers(self):
        return self._singers


class PersonalPlaylist(Playlist):
    def remove(self, song):
        self.tracks.remove(song)
