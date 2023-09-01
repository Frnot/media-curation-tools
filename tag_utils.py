import os
import re
import unittest

from metadata import Album,Track


def homogenize_tags(album: Album, edit_filename=True):
    # Sanitizes music tags
    # Will regenerate filename to equal '<track_num> - <title>' unless edit_filename is False

    # removes text like: 'remastered', '2011 remaster', studio version and puts this info into the comment
    # leaves text like: 'acoustic version'
    for track in album.tracks:
        pass



def rename_track(track: Track):
    new_filename = f"{track.tracknumber} - {track.title}"
    new_filepath = os.path.join(os.path.dirname(track.filepath),new_filename)
    os.rename(track.filepath, new_filepath)
    return new_filepath



def convert_plex_artist_format(track: Track):
    """Converts multiple artist fields into a comma-separated string for plexamp support\n
    Appends old artist list to comment field in a reversible format:\n
    before: ["artist1", "artist2", "artist3"]\n
    after: "artist1, artist2, artist3"\n
    comment field: "#artists::artist1\\artist2\\artist3"
    """
    
    artist_list = track.artists
    track.set_artists(", ".join(artist_list))
    track.append_comment("#artists::" + r"\\".join(artist_list))



def fix_title(track: Track): #TODO: func name
    pass





title_regex = [
    re.compile(r"\s*[({\[]explicit[)}\]]", re.IGNORECASE),  # explicit
    re.compile(r"\s*[({\[]\s*\d*\s*re[-]*master[ed]*\s*\d*\s*[)}\]]", re.IGNORECASE),  # remastered
    re.compile(r"\s*[({\[]\s*album\s+version\s*[)}\]]", re.IGNORECASE),  # "album version"
    re.compile(r"\s*[({\[].*release\s*[)}\]]", re.IGNORECASE),  # "US Release"
]


""" TODO: implement unittests
class TestTagEditing(unittest.TestCase):
    def test_regex(self):
        tests = [
            ("Test Title (2009 Re-Mastered)", "Test Title"),
            ("Test (explicit)", "Test"),
            ("8 - Test Title (feat. Dude #1, Dude #2, & Dude #3) [2005 Remaster].flac", "8 - Test Title (feat. Dude #1, Dude #2, & Dude #3).flac"),
            ("Test (2005 Remaster)", "Test"),
            ("Test (Remastered 2011)", "Test"),
            ("Test (album version) [Explicit]", "Test"),
            ("Test Title (US Domestic Release)", "Test Title"),
        ]

        for r, m in tests:
            self.assertEqual(fix_music_tags.clean(r), m)

if __name__ == "__main__":
    unittest.main()
"""