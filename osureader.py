import ast
import re


class HitObject:
    def __init__(self, x=0, y=0, time=0, type_bits=0, css_type="None", hitsound=0, addition=None,
                 slider_type="", curve_points=None, repeat=0, pixel_length=0.0,
                 edge_hitsounds=None, edge_additions=None, end_time=0):
        if addition is None:
            addition = [0, 0, 0, 0, ""]
        if edge_additions is None:
            edge_additions = []
        if curve_points is None:
            curve_points = []
        if edge_hitsounds is None:
            edge_hitsounds = []
        self.x = x
        self.y = y
        self.time = time
        self.type_bits = type_bits
        self.css_type = css_type
        self.hitsound = hitsound
        self.addition = addition
        self.slider_type = slider_type
        self.curve_points = curve_points
        self.repeat = repeat
        self.pixel_length = pixel_length
        self.edge_hitsounds = edge_hitsounds
        self.edge_additions = edge_additions
        self.end_time = end_time


class Beatmap:
    def __init__(self):
        self.audio_filename = ""
        self.audio_lead_in = 0
        self.preview_time = 0
        self.countdown = False
        self.sample_set = ""
        self.stack_leniency = 0.0
        self.mode = 0
        self.letterbox_in_breaks = False
        self.epilepsy_warning = False
        self.widescreen_storyboard = False

        self.bookmarks = []
        self.distance_spacing = 0.0
        self.beat_divisor = 0
        self.grid_size = 0
        self.timeline_zoom = 0

        self.title = ""
        self.title_unicode = ""
        self.artist = ""
        self.artist_unicode = ""
        self.creator = ""
        self.version = ""
        self.source = ""
        self.tags = []
        self.beatmap_id = 0
        self.beatmap_set_id = 0

        self.hp_drain_rate = 0.0
        self.circle_size = 0.0
        self.overall_difficulty = 0.0
        self.approach_rate = 0.0
        self.slider_multiplier = 1.0
        self.slider_tick_rate = 0.0

        self.events = []

        self.timing_points = []

        self.combo_colours = {}

        self.hit_objects = []

    def calculate_slider_durations(self):
        tbb = 300
        itv = -100
        tpindex = 0
        for ho in self.hit_objects:
            if ho.css_type == "slider":
                while tpindex < len(self.timing_points) and self.timing_points[tpindex][0] <= ho.time:
                    if self.timing_points[tpindex][6]:
                        tbb = self.timing_points[tpindex][1]
                    else:
                        itv = self.timing_points[tpindex][1]
                    tpindex += 1
                ho.end_time = int((tbb * itv * ho.pixel_length) // (-10000 * self.slider_multiplier))


def bitfield(n):
    return [1 if digit == '1' else 0 for digit in bin(n)[2:]][::-1]


def convert_type(string):
    try:
        return ast.literal_eval(string)

    except ValueError:
        return string
    except SyntaxError:
        return string


def read_line(line):
    split = line.split(":")
    return [s.strip() for s in split]


def convert_split(string, split):
    return [convert_type(k) for k in string.split(split)]


def to_snake_case(name):
    # Insert underscore before capital letters and convert to lowercase
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def read_beatmap(file_location):
    bm = Beatmap()
    section = ""
    with open(file_location, 'rt', encoding="utf8") as f:
        for l in f:
            ls = l.strip()
            split = read_line(ls)

            if len(ls) == 0:
                continue
            if ls[0] == "[":
                section = ls
                continue

            if section == "[General]":
                setattr(bm, to_snake_case(split[0]), convert_type(split[1]))

            elif section == "[Editor]":
                if split[0] == "Bookmarks":
                    bm.bookmarks = convert_split(split[1], ",")
                    continue
                setattr(bm, to_snake_case(split[0]), convert_type(split[1]))

            elif section == "[Metadata]":
                if split[0] == "Tags":
                    bm.tags = split[1].split(" ")
                setattr(bm, to_snake_case(split[0]), convert_type(split[1]))

            elif section == "[Difficulty]":
                setattr(bm, to_snake_case(split[0]), convert_type(split[1]))

            elif section == "[Events]":
                bm.events.append(ls)

            elif section == "[TimingPoints]":
                bm.timing_points.append(convert_split(ls, ","))

            elif section == "[Colours]":
                bm.combo_colours[split[0]] = convert_split(split[1], ",")

            elif section == "[HitObjects]":
                lss = convert_split(ls, ",")
                typebits = bitfield(lss[3])

                if typebits[0] == 1:  # Circle
                    bm.hit_objects.append(
                        HitObject(lss[0], lss[1], lss[2], lss[3], "circle", lss[4], convert_split(lss[5], ":")))

                elif typebits[1] == 1:  # Slider
                    bm.hit_objects.append(HitObject(lss[0], lss[1], lss[2], lss[3], "slider", lss[4], None,
                                                    lss[5].split("|")[0],
                                                    [convert_split(t, ":") for t in lss[5].split("|")[1:]],
                                                    lss[6], lss[7], None, None))
                    try:
                        bm.hit_objects[-1].edge_hitsounds = convert_split(lss[8], "|")
                        bm.hit_objects[-1].edge_additions = [convert_split(t, ":") for t in lss[9].split("|")]
                        bm.hit_objects[-1].addition = convert_split(lss[10], ":")
                    except IndexError:
                        pass

                elif typebits[3] == 1:  # Spinner
                    bm.hit_objects.append(
                        HitObject(lss[0], lss[1], lss[2], lss[3], "spinner", lss[4], convert_split(lss[6], ":"),
                                  end_time=lss[5]))

    bm.calculate_slider_durations()
    return bm
