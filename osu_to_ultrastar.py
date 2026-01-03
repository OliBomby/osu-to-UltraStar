import osureader

from os import path
import os
import shutil
from PIL import Image, ImageOps

including = {'[General]': True,
             '[Editor]': False,
             '[Metadata]': True,
             '[Difficulty]': True,
             '[Events]': False,
             '[TimingPoints]': True,
             '[Colours]': False,
             '[HitObjects]': True}

lyrics = ""


def copy_rename(old_file_name, new_file_name):
    src_dir = path.join(os.curdir, "Input")
    dst_dir = path.join(os.curdir, "Output")
    src_file = path.join(src_dir, old_file_name)
    shutil.copy(src_file, dst_dir)

    dst_file = path.join(dst_dir, old_file_name)
    new_dst_file_name = path.join(dst_dir, new_file_name)
    os.rename(dst_file, new_dst_file_name)


def findParam(filename, param):
    input_path = path.join(input_folder, filename)

    with open(input_path, 'rt', encoding="utf8") as file:
        for line in file:
            sline = line.strip()
            if sline.split(':')[0] == param:
                split = sline.split(':')
                if split[1][0] == ' ':
                    return split[1][1:]
                else:
                    return split[1]
    return ''


def findBGs(events):
    bgs = []
    finding_bg = False
    for line in events:
        sline = line.strip()
        if finding_bg:
            split = sline.split(',')
            if len(split) > 2:
                bgs.append((split[2][1:-1], int(split[1])))
        if sline == "//Background and Video events":
            finding_bg = True
    return bgs


def resizecrop(src, out, width, height):
    img = Image.open(src)
    img = ImageOps.fit(img, (width, height), Image.ANTIALIAS, 0, (0.5, 0.5))
    img.save(out)


def getNextLyric():
    global lyrics
    lyric = ""
    num = 0
    space_next = False
    newline = False
    plus = False

    if len(lyrics) == 0:
        return ("~", newline, plus)

    for ch in lyrics:
        num += 1
        if ch == '+':
            plus = True
            break
        if ch == '\n':
            space_next = True
            newline = True
            break
        if ch == ' ' and num > 1:
            space_next = True
            break
        lyric += ch

    lyrics = lyrics[num:]
    if space_next:
        lyrics = " " + lyrics
    return (lyric, newline, plus) if lyric != "" else ("~", newline, plus)


if __name__ == "__main__":
    folder = path.dirname(__file__)
    input_folder = path.join(folder, 'Input')
    output_folder = path.join(folder, 'Output')

    input_files = os.listdir(input_folder)
    osu_files = [file for file in input_files if file.endswith(".osu")]
    lyric_files = [file for file in input_files if file.endswith(".txt")]

    if len(osu_files) == 0:
        print("No osu! files found in the Input folder.")

    map_path = path.join(input_folder, osu_files[0])
    beatmap = osureader.readBeatmap(map_path)

    if len(lyric_files) > 0:
        with open(path.join(input_folder, lyric_files[0]), "r", encoding="utf8") as file:
            lyrics = file.read()

    output_path = path.join(output_folder, "%s - %s.txt" % (beatmap.Artist, beatmap.Title))

    language = input("Language: ")
    edition = input("Edition: ")
    genre = input("Genre: ")
    year = input("Year: ")
    creator = input("Creator: ")

    audio = beatmap.AudioFilename
    bgs = findBGs(beatmap.Events)
    bg = next((f for f, o in bgs if f.endswith(".jpg") or f.endswith(".png")), "")
    video, video_offset = next(((f, o) for f, o in bgs if f.endswith(".mp4") or f.endswith(".avi")), "")

    copy_rename(audio, audio)
    if bg != "":
        copy_rename(bg, bg)
    if video != "":
        copy_rename(video, video)

    redline = next(l for l in beatmap.TimingPoints if len(l) > 6 and l[6] == 1)
    mpb = redline[1]
    bpm = round(6000000 / mpb) / 100

    first_time = beatmap.HitObjects[0].time

    default_pitch = 0

    with open(output_path, "w+", encoding="utf8") as file:
        file.write("#TITLE:%s\n" % beatmap.Title)
        file.write("#ARTIST:%s\n" % beatmap.Artist)
        if language != "":
            file.write("#LANGUAGE:%s\n" % language)
        if edition != "":
            file.write("#EDITION:%s\n" % edition)
        if genre != "":
            file.write("#GENRE:%s\n" % genre)
        if year != "":
            file.write("#YEAR:%s\n" % year)
        if creator != "":
            file.write("#CREATOR:%s\n" % creator)
        file.write("#MP3:%s\n" % beatmap.AudioFilename)
        if bg != "":
            file.write("#COVER:%s\n" % bg)
            file.write("#BACKGROUND:%s\n" % bg)
        if video != "":
            file.write("#VIDEO:%s\n" % video)
            file.write("#VIDEOGAP:%s\n" % float(video_offset / -1000))
        file.write("#BPM:%s\n" % bpm)
        file.write("#GAP:%s\n" % first_time)

        last_nc = False
        next_beat = 0
        for i, ho in enumerate(beatmap.HitObjects):
            next_ho = beatmap.HitObjects[i+1] if i+1 < len(beatmap.HitObjects) else None
            next_nc = next_ho is not None and next_ho.type & 4
            beat = round((ho.time - first_time) / mpb * 4)
            next_beat = None if next_ho is None else round((next_ho.time - first_time) / mpb * 4)
            nextLyric, nc2, plus = getNextLyric()
            length = 32 if next_ho is None else min(round((next_ho.time - first_time) / mpb * 4) - beat, 32)

            if plus and next_nc:
                file.write(": %s %s %s %s-\n" % (beat, length, default_pitch, nextLyric))
            else:
                file.write(": %s %s %s %s\n" % (beat, length, default_pitch, nextLyric))
            
            if next_nc:
                file.write("- %s\n" % next_beat)
            
            last_nc = nc2
            next_beat = beat + length

        # Add fake notes for any extra lyrics
        while len(lyrics) > 0:
            nextLyric, nc2, plus = getNextLyric()
            length = 1
            file.write(": %s %s %s %s\n" % (beat, length, default_pitch, nextLyric))
            next_beat += 1
            
        file.write("E\n")

    print("Done!")


