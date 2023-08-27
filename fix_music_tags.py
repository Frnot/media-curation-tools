# v2.1

import os
import re
from functools import cache

import music_tag

regex_list = [
    re.compile(r"\s*[({\[]explicit[)}\]]", re.IGNORECASE),  # explicit
    re.compile(r"\s*[({\[]\s*\d*\s*re[-]*master[ed]*\s*\d*\s*[)}\]]", re.IGNORECASE),  # remastered
    re.compile(r"\s*[({\[]\s*album\s+version\s*[)}\]]", re.IGNORECASE),  # "album version"
    re.compile(r"\s*[({\[].*release\s*[)}\]]", re.IGNORECASE),  # "US Release"
    re.compile(r"\s*[({\[]original.*\s*[)}\]]", re.IGNORECASE),  # "Original"
    re.compile(r"\s*[({\[].*version\s*[)}\]]", re.IGNORECASE),  # "* Version"
]

filename_regex_list = [
    re.compile(r"[\d|\.]+\s+-\s+", re.IGNORECASE),  # N - filename
    re.compile(r"\.[\w|\d]{2,5}$", re.IGNORECASE),  # file extensions
    re.compile(r"\s*[({\[].*[)}\]]$", re.IGNORECASE),  # anything in parenthesis (at the end of the title)
]

def update_dir(dir_path, dry_run=False):
    root, dir = os.path.split(dir_path)
    for file in os.listdir(dir_path):
        filepath = os.path.join(dir_path, file)
        if os.path.isdir(filepath):
            update_dir(dir_path=filepath, dry_run=dry_run)
        elif any (file.lower().endswith(x) for x in [".flac", ".mp3"]):
            update(filepath, dry_run)

    # Check directory names
    old_dirname = dirname = dir
    if dirname := clean(dirname):
        print(f"Old directory name: \"{old_dirname}\" ||| New directory name: \"{dirname}\"")
        if not dry_run:
            new_dirpath = os.path.join(root, dirname)
            os.rename(dir_path, new_dirpath)


def update(filepath, dry_run=False):
    root,file = os.path.split(filepath)
    save_tags = False
    try:
        ftag = music_tag.load_file(filepath)
    except KeyboardInterrupt:
        print("Exiting")
        quit()
    except Exception as e:
        print(f"Error loading file for edit: {e}")
        return None
    
    # Check title
    original_title = title = ftag['title'].value
    if title := clean(title):
        ftag['title'] = title
        save_tags = True

    # Check Album tag
    album = ftag['album'].value
    if album := clean(album):
        ftag['album'] = album
        save_tags = True

    # Save tags if something has changed
    if save_tags:
        print(f"Old title: \"{original_title}\" ||| New title: \"{title}\"")
        print(filepath)
        if not dry_run:
            ftag.save()
        
    # Check filename
    old_filename = filename = file
    if filename := clean(filename):
        print(f"Old filename: \"{old_filename}\" ||| New filename: \"{filename}\"")
        if not dry_run:
            new_filepath = os.path.join(root, filename)
            os.rename(filepath, new_filepath)


def clean(string, regexes=regex_list):
    hits = 0
    for regex in regexes:
        string, hit = regex.subn("", string)
        hits += hit

    return string.strip() if hits else None

@cache
def scrub_filename(filename):
    for regex in filename_regex_list + regex_list:
        filename, hit = regex.subn("", filename)
    return filename.lower()


if __name__ == "__main__":
    update_dir(r"V:\media\audio\Music")
    input()