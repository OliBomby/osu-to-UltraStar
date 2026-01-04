import os
import shutil
from os import path

import osureader

including = {'[General]': True,
             '[Editor]': False,
             '[Metadata]': True,
             '[Difficulty]': True,
             '[Events]': False,
             '[TimingPoints]': True,
             '[Colours]': False,
             '[HitObjects]': True}


def copy_rename(old_file_name, new_file_name):
    src_dir = path.join(os.curdir, "Input")
    dst_dir = path.join(os.curdir, "Output")
    src_file = path.join(src_dir, old_file_name)
    shutil.copy(src_file, dst_dir)

    dst_file = path.join(dst_dir, old_file_name)
    new_dst_file_name = path.join(dst_dir, new_file_name)
    os.rename(dst_file, new_dst_file_name)


def find_backgrounds(events):
    backgrounds = []
    finding_bg = False
    for line in events:
        sline = line.strip()
        if finding_bg:
            split = sline.split(',')
            if len(split) > 2:
                backgrounds.append((split[2][1:-1], int(split[1])))
        if sline == "//Background and Video events":
            finding_bg = True
    return backgrounds


def get_next_lyric(lyrics):
    lyric = ""
    num = 0
    space_next = False
    used_plus = False

    if len(lyrics) == 0:
        return lyrics, "~", used_plus

    for ch in lyrics:
        num += 1
        if ch == '+':
            used_plus = True
            break
        if ch == '\n':
            space_next = True
            break
        if ch == ' ' and num > 1:
            space_next = True
            break
        lyric += ch

    lyrics = lyrics[num:]
    if space_next:
        lyrics = " " + lyrics

    return (lyrics, lyric, used_plus) if lyric != "" else (lyrics, "~", used_plus)


def main():
    folder = path.dirname(__file__)
    input_folder = path.join(folder, 'Input')
    output_folder = path.join(folder, 'Output')

    # Ensure input and output folder exists
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    input_files = os.listdir(input_folder)
    osu_files = [file for file in input_files if file.endswith(".osu")]
    lyric_files = [file for file in input_files if file.endswith(".txt")]

    if len(osu_files) == 0:
        print("No osu! files found in the Input folder.")

    map_path = path.join(input_folder, osu_files[0])
    beatmap = osureader.read_beatmap(map_path)

    if len(lyric_files) > 0:
        with open(path.join(input_folder, lyric_files[0]), "r", encoding="utf8") as f:
            lyrics = f.read()
    else:
        print("No lyric file found in the Input folder. Proceeding with empty lyrics.")
        lyrics = ""

    output_path = path.join(output_folder, f"{beatmap.artist} - {beatmap.title}.txt")

    language = input("Language: ")
    edition = input("Edition: ")
    genre = input("Genre: ")
    year = input("Year: ")
    creator = input("Creator: ")

    audio = beatmap.audio_filename
    bgs = find_backgrounds(beatmap.events)
    bg = next((f for f, o in bgs if f.endswith(".jpg") or f.endswith(".png")), "")
    video, video_offset = next(((f, o) for f, o in bgs if f.endswith(".mp4") or f.endswith(".avi")), "")

    copy_rename(audio, audio)
    if bg != "":
        copy_rename(bg, bg)
    if video != "":
        copy_rename(video, video)

    redline = next(l for l in beatmap.timing_points if len(l) > 6 and l[6] == 1)
    mpb = redline[1]
    bpm = round(6000000 / mpb) / 100

    first_time = beatmap.hit_objects[0].time

    default_pitch = 0

    with open(output_path, "w+", encoding="utf8") as file:
        file.write(f"#TITLE:{beatmap.title}\n")
        file.write(f"#ARTIST:{beatmap.artist}\n")
        if language != "":
            file.write(f"#LANGUAGE:{language}\n")
        if edition != "":
            file.write(f"#EDITION:{edition}\n")
        if genre != "":
            file.write(f"#GENRE:{genre}\n")
        if year != "":
            file.write(f"#YEAR:{year}\n")
        if creator != "":
            file.write(f"#CREATOR:{creator}\n")
        file.write(f"#MP3:{beatmap.audio_filename}\n")
        if bg != "":
            file.write(f"#COVER:{bg}\n")
            file.write(f"#BACKGROUND:{bg}\n")
        if video != "":
            file.write(f"#VIDEO:{video}\n")
            file.write(f"#VIDEOGAP:{float(video_offset / -1000)}\n")
        file.write(f"#BPM:{bpm}\n")
        file.write(f"#GAP:{first_time}\n")

        next_beat = 0
        for i, ho in enumerate(beatmap.hit_objects):
            next_ho = beatmap.hit_objects[i + 1] if i + 1 < len(beatmap.hit_objects) else None
            next_nc = next_ho is not None and next_ho.type_bits & 4
            beat = round((ho.time - first_time) / mpb * 4)
            next_beat = None if next_ho is None else round((next_ho.time - first_time) / mpb * 4)
            lyrics, nextLyric, plus = get_next_lyric(lyrics)
            length = 32 if next_ho is None else min(round((next_ho.time - first_time) / mpb * 4) - beat, 32)

            if plus and next_nc:
                file.write(f": {beat} {length} {default_pitch} {nextLyric}-\n")
            else:
                file.write(f": {beat} {length} {default_pitch} {nextLyric}\n")

            if next_nc:
                file.write(f"- {next_beat}\n")

            next_beat = beat + length

        # Add fake notes for any extra lyrics
        while len(lyrics) > 0:
            lyrics, nextLyric, plus = get_next_lyric(lyrics)
            length = 1
            file.write(f": {beat} {length} {default_pitch} {nextLyric}\n")
            next_beat += 1

        file.write("E\n")

    print("Done!")


if __name__ == "__main__":
    main()
