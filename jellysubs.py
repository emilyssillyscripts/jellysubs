# jellysubs.py
# meant to move subtitle files from Subs/ folder to where jellyfin expects

import sys, getopt, shutil, os

video_base_title = "testS01E01"
episodes = 0
videos = []
failed = []
original_sub = "2_English.srt"

video_files = []
video_types = [".mp4", ".mkv"]
video_type = ".mkv"

sub_files = []

language = "English"

def get_video_files():
    global episodes

    print("Finding video files...")
    directory = os.listdir("./")
    for file in directory:
        split_name = os.path.splitext(file)
        video_type = split_name[1]
        if video_type in video_types:
            print("Added " + split_name[0] + " to video files.")
            video_files.append(split_name[0])
            episodes += 1

def get_sub_files():
    print("Finding subtitle files...")

    sub_folder = os.path.exists("Subs/" + video_files[0])
    if sub_folder:
        print("Subtitle folders exist. Trying to find files.")
        for video in video_files:
            directory = os.listdir("./Subs/" + video + "/")
            for file in directory:
                if language in file:
                    print("Added Subs/" + video + "/" + file + " to subtitle files.")
                    sub_files.append(file)
                    break

def get_files():
    get_video_files()
    get_sub_files()

def move_subs():
    print("Moving subtitle files...")

    for i in range(len(video_files)):
        if i < len(sub_files):
            oldsubs = "Subs/" + video_files[i] + "/" + sub_files[i]
            newsubs = video_files[i] + ".srt"
            try:
                #shutil.move(oldsubs, newsubs)
                print("[" + str(i + 1) + "] Moved " + oldsubs + " to " + newsubs)
            except FileNotFoundError:
                print("[" + str(i + 1) + "] Could not find " + oldsubs)
                failed.append(oldsubs)
                continue
        else:
            print("Less subtitle files than videos!")
        
    if len(failed) > 0:
        print("jellysubs: [" + str(len(failed)) + "/" + str(len(videos)) + "] subtitles failed to move")
    else:
        print("jellysubs: [" + str(len(videos)) + "/" + str(len(videos)) + "] subtitles moved successfully")



def main(argv):
    global original_sub

    get_files()

    try:
        opts, args = getopt.getopt(argv,"hl:",["lang="])
    except getopt.GetoptError:
        print('jellysubs.py -l <language>')
        sys.exit(2)
    
    for opt,arg in opts:
        if opt == '-h':
            print('jellysubs: move subs from Subs/ to jellyfin acceptable place')
            print('jellysubs.py -l <language>')
            sys.exit()
        elif opt in ("-l", "--lang"):
            language = arg

    for i in range(1, episodes + 1):
        new_episode = "E" + str(i).zfill(2)
        temp_title = video_base_title.replace("E01", new_episode)
        videos.append(temp_title)

    move_subs()


if __name__ == "__main__":
   main(sys.argv[1:])
