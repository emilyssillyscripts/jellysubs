#!/usr/bin/python3
# jellysubs.py
# emilycheesecake

# Tries to find and move the subtitle files that
# sometimes come included with TV Shows to places
# that Jellyfin reads.

# Expected example file structure before moving and renaming
# Example TV Show S01
# ├── Subs
# │   ├── tests01e01-some-random-torrent
# │   │   └── 32_English.srt
# │   ├── tests01e02-some-random-torrent
# │   │   └── 32_English.srt
# │   ├── tests01e03-some-random-torrent
# │   │   └── 32_English.srt
# │   └── tests01e04-some-random-torrent
# │       └── 32_English.srt
# ├── tests01e01-some-random-torrent.mp4
# ├── tests01e02-some-random-torrent.mp4
# ├── tests01e03-some-random-torrent.mp4
# └── tests01e04-some-random-torrent.mp4


import sys, getopt, shutil, os

directory = ""

episodes = 0
video_files = []
video_types = [".mp4", ".mkv"]
video_type = ".mkv"

sub_files = []
language = "English"

failed = []

clean = ""
should_clean = False

verbose = False
test_run = False

def get_video_files():
    global episodes
    global video_type
    global directory

    print("Finding video files...")
    if len(directory) != 0:
        video_dir = os.listdir(directory)
    else:
        video_dir = os.listdir("./")
    for file in video_dir:
        split_name = os.path.splitext(file)
        file_type = split_name[1]
        if file_type in video_types:
            if verbose:
                print("Added " + split_name[0] + " to video files.")
            video_files.append(split_name[0])
            video_type = split_name[1]
            episodes += 1

    if episodes == 0:
        print("No video files found!")
    else:
        print(str(episodes) + " video files found!")

def get_sub_files():
    global language
    global directory

    if len(video_files) == 0:
            return
    print("Finding subtitle files...")

    if len(directory) != 0:
        sub_folder = os.path.exists(directory + "Subs/" + video_files[0])
    else:
        sub_folder = os.path.exists("Subs/" + video_files[0])
    if sub_folder:
        if verbose:
            print("Subtitle folders exist. (Subs/<episode>/)")
        for video in video_files:
            if len(directory) != 0:
                sub_dir = os.listdir(directory + "Subs/" + video + "/")
            else:
                sub_dir = os.listdir("./Subs/" + video + "/")
            for file in sub_dir:
                if language in file:
                    if verbose:
                        print("Added Subs/" + video + "/" + file + " to subtitle files.")
                    sub_files.append(file)
                    break
    print(str(len(sub_files)) + " subtitle files found!")

def get_files():
    get_video_files()
    get_sub_files()

def move_subs():

    if len(video_files) == 0:
        return

    print("Moving subtitle files...")

    for i in range(len(video_files)):
        if i < len(sub_files):
            if len(directory) != 0:
                oldsubs = directory + "Subs/" + video_files[i] + "/" + sub_files[i]
            else:
                oldsubs = "Subs/" + video_files[i] + "/" + sub_files[i]
            newsubs = video_files[i] + ".srt"
            try:
                if not test_run:
                    shutil.move(oldsubs, newsubs)
                if verbose:
                    print("[" + str(i + 1) + "] Moved " + oldsubs + " to " + newsubs)
            except FileNotFoundError:
                if verbose:
                    print("[" + str(i + 1) + "] Could not find " + oldsubs)
                failed.append(oldsubs)
                continue
        else:
            failed.append(video_files[i])
            print("Less subtitle files than videos!")
        
    if len(failed) > 0:
        print("[" + str(len(failed)) + "/" + str(len(video_files)) + "] subtitles failed to move")
    else:
        print("[" + str(len(video_files)) + "/" + str(len(video_files)) + "] subtitles moved successfully")

def clean_titles(clean):
    print("Cleaning video titles...")

    for video in video_files:
        if len(directory) != 0:
            old = directory + video + video_type
        else:
            old = video + video_type
        new = old.replace(clean, "")
        if verbose:
            print("Moved " + old + " to " + new)
        if not test_run:
            shutil.move(old, new)
    
    print("Cleaning subtitles...")

    for video in video_files:
        if len(directory) != 0:
            old = directory + video + ".srt"
        else:
            old = video + ".srt"
        new = old.replace(clean, "")
        if verbose:
            print("Moved " + old + " to " + new)
        if not test_run:
            shutil.move(old, new)

def main(argv):
    global verbose
    global language
    global directory
    global test_run

    try:
        opts, args = getopt.getopt(argv,"hd:l:c:vt",["dir=", "lang=" , "clean="])
    except getopt.GetoptError:
        print('jellysubs.py -d <directory> -l <language> -c <text to clean from filenames>')
        sys.exit(2)
    
    for opt,arg in opts:
        if opt == '-h':
            print('jellysubs: move subs from Subs/ to jellyfin acceptable place')
            print('jellysubs.py -d <directory> -l <language> -c <text to clean from filenames>')
            sys.exit()
        elif opt == '-v':
            verbose = True
        elif opt == '-t':
            test_run = True
        elif opt in ("-d", "--dir"):
            directory = arg
        elif opt in ("-l", "--lang"):
            language = arg
        elif opt in ("-c", "--clean"):
            should_clean = True
            clean = arg

    print("jellysubs.py")
    print("Hello <3\n")

    if len(directory) != 0:
        print("Using directory: " + directory + "\n")
    else:
        print("Using this directory...\n")
    
    get_files()
    move_subs()
    if should_clean:
        clean_titles(clean)

    print("\nDone!")

if __name__ == "__main__":
   main(sys.argv[1:])
