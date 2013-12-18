"""
TVShowsManager manages the watched episode from the unwatched episode
Currently a simple version, it needs to be in the folder of a unique season
Feel free to change whatever you want :)

Created by Nicolas Svirchevsky the 17/12/2013
n.svirchevsky@gmail.com

TODO: Subtitle with MediaPlayer
TODO: Folder management
TODO: Paths modification with a command
"""

import subprocess
import os
import pickle
import sys

# Notice #
# MPC = MediaPlayerClassic
# VLC = VideoLan
# The paths can be wrong if you are in 64 or 32 bits or used a custom install
# You should set them right :)

mpc = os.path.join("C:/", "Program Files", "MPC-HC", "mpc-hc64.exe")
vlc = os.path.join("C:/", "Program Files", "VideoLAN", "VLC", "vlc.exe")
film_formats = [".avi", ".mp4"]
save_path = "tvs_manager.save"
mInformation = None

class information:
    currentEpisode = 1
    subtitle = None
    useVLC = None
    episode_format = None
    vlc = None
    mpc = None

    def getEpisodeFormat(self, string = ""):
        items = self.episode_format
        result = ""
        for item in items:
            if (item == "X"):
                result += string + str(self.currentEpisode)
            else:
                result += item
        return result

    def getEpisodeFromAnswer(self, answer):
        items = answer.split(',')
        if any("X" == item for item in items):
            return items
        else:
            print("I need at least a X field. (Spaces are important)")
            return None

    def answerEpisodeFormat(self):
        try:
            answer = input("ex: S02E01 = S02E,X> ")
        except KeyboardInterrupt:
            os.remove(save_path)
            exit()
        result = self.getEpisodeFromAnswer(answer)
        if (result == None):
            return False
        self.episode_format = result
        try:
            mAnswer = input("This will give " + self.getEpisodeFormat("") + " or " + self.getEpisodeFormat("0") + ". Is that right ? ([Yes] : No): ")
        except KeyboardInterrupt:
            os.remove(save_path)
            exit()
        if "no" in mAnswer.lower():
            return False
        return True
    
    def setEpisodeFormat(self):
        print("\nWhat is the episodes' format (X = season) (Spaces are important)")
        while(self.answerEpisodeFormat() == False): None

    def setDefaultLecteur(self):
        try:
            answer = input("\nDo you want to use VLC or MLC ? (MLC : [VLC]): ")
        except KeyboardInterrupt:
            os.remove(save_path)
            exit()
        if "mlc" in answer.lower():
            self.useVLC = False
        else:
            self.useVLC = True

    def setSubtitleMode(self):
        try:
            answer = input("\nDo you are using subtitles with the same episode's name (Yes : [No]): ")
        except KeyboardInterrupt:
            os.remove(save_path)
            exit()
        if "yes" in answer.lower():
            self.subtitle = True
        else:
            self.subtitle = False

    def setEpisodeNumber(self):
        try:
            answer = input("\nWhere do you wanna start ? (default episode: 1): ")
        except KeyboardInterrupt:
            exit()
        if (len(answer) == 0):
            self.currenEpisode = 1
        else:
            try:
                self.currentEpisode = int(answer)
            except ValueError as error:
                print("Error. Value set to 1")
                self.currentEpisode = 1

    def __init__(self):
        print("I need to be configure for this folder.")
        self.setDefaultLecteur()
        if self.useVLC == True:
            self.setSubtitleMode()
        else:
            self.subtitle = False
        self.setEpisodeFormat()        
        self.setEpisodeNumber()
        saveInformation()
        help()
        print("Everything is ok! Thanks for using me :)\n")
        
def saveInformation():
    file = open(save_path, 'wb')
    pickle.dump(mInformation, file)
    file.close()

def getInformation():
    global mInformation
    if (os.path.exists(save_path)):
        file = open(save_path, 'rb')
        try:
            mInformation = pickle.load(file)
        except EOFError as error:
            print(error)
        file.close()
    else:
        mInformation = None
    if (mInformation == None):
        mInformation = information()

def startFilmMPC(episode):
    if os.path.exists(mpc) & os.path.exists(episode):
        print("\nEpisode: ", episode, "\nLecteur: MPC")
        return subprocess.call([mpc, "/new", "/play", "/close", "/fullscreen", episode])
    elif os.path.exists(episode):
        print("Could not found mpc-hc.exe: ", mpc)
    elif os.path.exists(mpc):
        print("Could not found the episode: ", episode)
    else:
        print("Error: \n" + mpc + "\n", episode)

def startFilmVLC(episode):
    if os.path.exists(vlc) & os.path.exists(episode):
        print("\nEpisode:", episode, "\nLecteur: VLC")
        if (mInformation.subtitle):
            return subprocess.call([vlc, episode, "--sub-autodetect-file"])
        else:
            return subprocess.call([vlc, episode])
    elif os.path.exists(episode):
        print("Could not find vlc.exe: ", vlc)
    elif os.path.exists(vlc):
        print("Could not find the episode: ", episode)
    else:
        print("Error: \n" + vlc + "\n", episode)

def getFilms(path="."):
    files = os.listdir(path)
    film = []
    for file in files:
        for film_format in film_formats:
            if (os.path.splitext(file)[1] == film_format):
                film.append(file)
                break
    return film

def getEpisode(films):
    episode_format = mInformation.getEpisodeFormat("0")
    for film in films:
        if episode_format in film:
            return os.getcwd() + "\\" + film
    episode_format = mInformation.getEpisodeFormat("")
    for film in films:
        if episode_format in film:
            return os.getcwd() + "\\" + film
    return None

def TVSManager():
    films = getFilms()
    episode = getEpisode(films)
    saveInformation()
    if (episode):
        if mInformation.useVLC:
            startFilmVLC(episode)
        else:
            startFilmMPC(episode)
    else:
        print("\nSorry I haven't found the episode n°", mInformation.currentEpisode)
        print("Format is ", mInformation.getEpisodeFormat(""), " use reset if it's wrong")
    print()
    return True

def help():
    print('')
    print("[ls | list]: list all films in the current folder")
    print("[start | play | continue | load | 'Nothing' ]: play the current episode")
    print("[next | avoid | jump | step]: select next episode")
    print("[previous | precedent | back | prev | previous]: select previous episode")
    print("[Stop | exit | quit | C^C]: stop the program")
    print("[reset]: reset the config file")
    print("[set <integer>]: set the episode's cursor")
    print("[help]: display this doc")
    print()

def jacky():
    while (42):
        try:
            answer = input(os.getcwd() + "> (episode " + str(mInformation.currentEpisode) + ") ")
        except KeyboardInterrupt:
            break
        answer = answer.lower()
        if (any(x == answer for x in ["next", "avoid", "jump", "step"])):
            mInformation.currentEpisode += 1
        elif any(x == answer for x in ["stop", "sleep", "exit", "quit"]):
            break
        elif any(x == answer for x in ["load", "play", "start", "continue"]) or (len(answer) == 0):
            if (TVSManager() == False):
                break
            mInformation.currentEpisode += 1
        elif any(x == answer for x in ["previous", "precedent", "back", "prev", "previous"]):
            mInformation.currentEpisode -= 1
        elif any (x in answer for x in ["ls", "list"]):
            for film in getFilms():
                print(film)
            print();
        elif ((any (x in answer for x in ["which", "what is"]))):
            print("episode", mInformation.currentEpisode)
        elif "set " in answer:
            temp = mInformation.currentEpisode
            try:
                mInformation.currentEpisode = int(answer[4:]) - 1
            except ValueError as valueError:
                mInformation.currentEpisode = temp
                print(valueError)
        elif "reset" == answer:
            os.remove(save_path)
            getInformation()
            saveInformation()
        elif "help" == answer:
            help()
        else:
            help()
        saveInformation()
    print("See you :)")
    
getInformation()
jacky()


