import sys
import platform

print("python implementation:", platform.python_implementation()) # CPython

def find_song_by_word(SONGSs, word):
    songs_list = [] # first ref create here
    for songs in SONGSs:
        if word in str(songs[1]).lower():
            pass  # need put here brackpoint for debug this if
            songs_list.append(songs[1])
    print("list ref:", id(songs_list), ", count:", sys.getrefcount(songs_list))
    return songs_list


def main():
    SONGS = [["Avril Lavigne", "Keep Holding On", 2007],
              ["Oasis", "All Around The World", 1998],
              ["Christina Aguilera", "Fighter", 2002],
              ["Pink", "Try", 2012],
              ["Christina Aguilera", "Reflection", 1998],
              ["Alicia Keys", "Girl On Fire", 2012],
              ["Michael Jackson", "Heal The World", 1991],
              ["Pink", "Just like Fire", 2016],
              ["Christina Aguilera", "Beautiful", 2002]]
    songs_list1 = find_song_by_word(SONGS, "world")
    print(songs_list1)

    print("list ref:", id(songs_list1), ", count:", sys.getrefcount(songs_list1)) # second ref create here


if __name__ == '__main__':
    main()
