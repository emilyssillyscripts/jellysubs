# jellysubs.py
# meant to move subtitle files from Subs/ folder to where jellyfin expects

import sys, getopt, shutil

video_base_title = "testS01E01"
episodes = 0
videos = []
failed = []
original_sub = "2_English.srt"

def move_subs():
    for i in range(len(videos)):
        oldsubs = "Subs/" + videos[i] + "/" + original_sub
        newsubs = videos[i] + ".srt"
        try:
            shutil.move(oldsubs, newsubs)
            print("[" + str(i + 1) + "] Moved " + oldsubs + " to " + newsubs)
        except FileNotFoundError:
            print("[" + str(i + 1) + "] Could not find " + oldsubs)
            failed.append(oldsubs)
            continue
        
    if len(failed) > 0:
        print("jellysubs: [" + str(len(failed)) + "/" + str(len(videos)) + "] subtitles failed to move")
    else:
        print("jellysubs: [" + str(len(videos)) + "/" + str(len(videos)) + "] subtitles moved successfully")


def main(argv):
    global original_sub

    try:
        opts, args = getopt.getopt(argv,"hv:e:s:",["video=","episodes=","subname="])
    except getopt.GetoptError:
        print('jellysubs.py -v <first video name> -e <# of episodes> -s <old subs name>')
        sys.exit(2)
    
    for opt,arg in opts:
        if opt == '-h':
            print('jellysubs: move subs from Subs/ to jellyfin acceptable place')
            print('jellysubs.py -v <first video name> -e <# of episodes> -s <old subs name>')
            sys.exit()
        elif opt in ("-v", "--video"):
            video_base_title = arg
        elif opt in ("-e", "--episodes"):
            episodes = int(arg)
        elif opt in ("-s", "--subs"):
            original_sub = arg

    for i in range(1, episodes + 1):
        new_episode = "E" + str(i).zfill(2)
        temp_title = video_base_title.replace("E01", new_episode)
        videos.append(temp_title)

    move_subs()


if __name__ == "__main__":
   main(sys.argv[1:])
