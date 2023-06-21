import os
import music_tag
from operator import attrgetter

# local db
albums = {}

class Album:
    def __init__(self, name, tracks=None, dirpath=None):
        self.name = name
        self.tracks = sorted(tracks, key=attrgetter("tracknumber")) if tracks else []

        albums[self.name] = self

    def add_track(self, track):
        self.tracks.append(track)
        self.tracks.sort(key=lambda x: x.tracknumber)


class Track:
    def __init__(self, filepath):
        self.filepath = filepath
        self.ftag = music_tag.load_file(filepath)
        self.isflac = filepath.lower().endswith(".flac")
        self.ismp3 = filepath.lower().endswith(".mp3")

        self.title = self.ftag["title"].value
        self.tracknumber = self.ftag["tracknumber"].value
        self.album_name = self.ftag["album"].value
        self.genres = self.ftag["genre"].values
        self.artists = self.ftag["artist"].values
        self.album_artists = self.ftag["album artist"].values
        self.composers = self.ftag["composer"].values
        self.comments = self.ftag["comment"].values

        self.album = self.get_album()
        self.album.add_track(self)

    def get_album(self):
        if self.album_name in albums:
            return albums[self.album_name]
        else:
            return Album(self.album_name)
        
    def set_artists(self, artists):
        self.ftag["artist"] = artists
        self.ftag.save()
        
    def clear_comments(self):
        self.ftag["comment"] = None
        self.ftag.save()

    def append_comment(self, new_comment, first=False):
        comments = self.ftag["comment"].values
        if first:
            comments = [new_comment].extend(comments)
        else:
            comments.append(new_comment)

        self.ftag["comment"] = comments
        self.ftag.save()