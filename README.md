# osu! to UltraStar

This project is a simple converter that converts osu! beatmaps to UltraStar file format, so you can time songs in the osu! editor and use them for karaoke.

## Usage

Clone the project:

```bash
git clone https://github.com/OliBomby/osu-to-UltraStar.git
cd osu-to-UltraStar
```

Install Python and dependencies:

```bash
pip install -r requirements.txt
```

Put your `lyrics.txt` and `.osu` file and any accompanied audio, video, or backgrounds in the `Input` folder next to `osu_to_ultrastar.py`.
The `lyrics.txt` should contain only the lyrics and each syllable should be separated with a `+`.

Then run the script:

``` bash
python ./osu_to_ultrastar.py
```

It will prompt you for additional metadata and then write the resulting UltraStar file in the `Output` folder.

## Conversion

The converter reads any circles and sliders in the map and assigns the next syllable to the note.
The beatmap should contain notes only on the vocals of the song.

The duration of the note is determined like this:
- Circles hold until the next note
- Sliders hold for the duration of the slider

If the number of notes in the beatmap and the number of syllables in the lyrics do not match there will be some errors, but this is easy to fix in Yass editor by rolling syllables left or right.
