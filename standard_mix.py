import os

from fix_music_tags import update_dir
from metadata import Track
from tag_utils import convert_plex_artist_format


def convert_artist_tag(path):
    for file in os.listdir(path):
        filepath = os.path.join(path, file)
        if os.path.isdir(filepath):
            convert_artist_tag(filepath)
        elif any (file.lower().endswith(x) for x in [".flac", ".mp3"]):
            track = Track(filepath)
            convert_plex_artist_format(track)



path = r"C:\Users\Frnot\Desktop\QobuzDownloads"

if __name__ == "__main__":
    update_dir(path)
    convert_artist_tag(path)