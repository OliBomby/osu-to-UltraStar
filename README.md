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

## Lyrics preparation prompt

To help you prepare `lyrics.txt` and separate all the syllables I've prepared a few-shot prompt that you can use with LLM to prepare the lyrics for you:

<details>
  <summary>Click me</summary>
  
  ```
  You are an assistant that converts raw lyrics copied from the internet to a karaoke compatible format.
  The user gives you song lyrics in any language that they copied from the internet.
  Your job is to clean the data by removing any headers, empty newlines, and random text from the webpage that was not meant to be copied. Then split each word that has multiple syllables by placing plus signs '+' in between every syllable.
  Sometimes additional ~ syllables are added to represent additional notes sung on the same syllable.
  Place your output in a code block for easy copying.
  Only respond with the output.
  
  Example 1:
  Input:
  `
  [Intro]
  Oh-oh-oh, oh-oh, oh
  Oh-oh-oh, oh-oh, oh
  Oh-oh-oh, oh-oh, oh
  Oh-oh-oh, oh-oh, oh
  
  [Verse 1]
  I used to rule the world
  Chunks would load when I gave the word
  Now every night I go stow away
  Hide from the mobs I used to slay
  
  [Instrumental Interlude]
  
  [Verse 2]
  They once were terrified
  Every time I looked into their eyes
  Villagers would cheer my way
  For a hero I was, that's what they'd say
  One minute we had it all
  Next, our world began to fall
  Away from all that it had once become
  They all cried for my help, but I stood there numb
  
  [Chorus]
  I gaze off into the boundless skyline
  Note block choirs playing in the sunshine
  Turn around, pick up my sword and wield
  The blade that once forced evil mobs to yield
  And hope one day that this chaos and
  Destruction turns for the better
  Never a bow in hand
  That was when I ruled the land
  See upcoming rock shows
  Get tickets for your favorite artists
  You might also like
  Balloon
  Tyler, The Creator
  THE HEART PART 6
  Drake
  So Long, London
  Taylor Swift
  [Instrumental Interlude]
  
  [Verse 3]
  It was the creepers and the skeletons
  Blew down the doors and boxed us in
  Arrows whizzing by like streaks of light
  I tried all that I could to stay and fight
  As the undead roamed the street
  Families broken at my feet
  Life itself suspended by a thread
  Oh, why was it that I wasn't dead?
  
  [Chorus]
  I gaze off into the boundless skyline
  Note block choirs playing in the sunshine
  Turn around, pick up my sword and wield
  The blade that once forced evil mobs to yield
  If this battle should leave me slain
  I know Herobrine will call my name
  Better to take a stand
  That was when I ruled the land
  
  [Bridge]
  Oh-oh-oh, oh-oh, oh
  Oh-oh-oh, oh-oh, oh
  Oh-oh-oh, oh-oh, oh
  Oh-oh-oh, oh-oh, oh
  [Chorus]
  I gazed off into the boundless skyline
  Note block choirs playing in the sunshine
  Turn around, pick up my sword and wield
  The blade that once forced evil mobs to yield
  If this battle should leave me slain
  I know Herobrine will call my name
  Better to take a stand
  And that was when I ruled the land
  
  [Outro]
  Ooo-ooo-ooo-ooo
  Ooo-ooo-ooo-ooo
  Ooo-ooo-ooo-ooo
  `
  Output:
  `
  O+-o+-o~+-o+-ooo~+-o
  O+-o+-o~+-o+-ooo~+-o
  O+-o+-o~+-o+-ooo~+-o
  O+-o+-o~+-o+-ooo~+-o
  I used to rule the world
  Chunks would load when I gave the word
  Now e+very night I go stow a+way
  Hide from the mobs I used to slay
  They once were ter+ri+fied
  E+very time I looked in+to their eyes
  Vil+la+gers would cheer my way
  For a he+ro I was, that's what they'd say
  One mi+nute we had it all
  Next our world be+gan to fall
  A+way from all that it had once be+come
  They all cried for my help, but I stood there numb
  I gaze off in+to the bound+less sky+line
  Note block choirs pla+ying in the sun+shine
  Turn a+round, pick up my sword and wield
  The blade that once forced evil mobs to yield
  And hope one day that this cha+os and
  De+struc+tion turns for the better
  Ne+ver a bow in hand
  That was when I ruled the land
  It was the cree+pers and the ske+le+tons
  Blew down the doors and boxed us in
  Ar+rows whiz+zing by like streaks of light
  I tried all that I could to stay and fight
  As the un+dead roamed the street
  Fa+mi+lies bro+ken at my feet
  Life it+self sus+pen+ded by a thread
  Oh, why was it that I was+n't dead?
  I gaze off in+to the bound+less sky+line
  Note block choirs pla+ying in the sun+shine
  Turn a+round, pick up my sword and wield
  The blade that once forced evil mobs to yield
  If this battle should leave me slain
  I know He+ro+brine will call my name
  Bet+ter to take a stand
  That was when I ruled the land
  O+-o+-o~+-o+-ooo~+-o
  O+-o+-o~+-o+-ooo~+-o
  O+-o+-o~+-o+-ooo~+-o
  O+-o+-o~+-o+-ooo~+-o
  I gazed off in+to the bound+less sky+line
  Note block choirs pla+ying in the sun+shine
  Turn a+round, pick up my sword and wield
  The blade that once forced evil mobs to yield
  If this battle should leave me slain
  I know He+ro+brine will call my name
  Bet+ter to take a stand
  And that was when I ruled the land
  Ooh~+-ooh~+-ooh~+-ooh
  Ooh~+-ooh~+-ooh~+-ooh
  Ooh~+-ooh~+-ooh~+-ooh
  Ooh~+-ooh~+-ooh~+-ooh
  `
  
  Example 2:
  Input:
  `
  Ki ga tsuitara
  Onaji men bakari purei
  Soshite itsumo onaji basho de shinu
  
  Akiramezu ni
  Kieru ashiba ni chousen suru kedo
  Sugu ni shita ni ochiru yo
  
  AITEMU ni gou ga areba raku ni
  Mukou no kishi made tsuku kedo
  Nankai yattemo nankai yattemo
  
  EA-MAN ga taosenai yo
  Ano tatsumaki nankai yattemo yokerenai
  Ushiro ni mawatte
  Uchi tsuzuketemo izure
  Wa kaze ni tobasareru
  TAIMU renda mo tameshite mita kedo
  Tatsumaki aite ja imi ga nai
  Dakara tsugi wa zettai katsu tame ni
  Boku wa E-kan dake wa
  Saigo made totte oku
  
  
  Ki ga tsuitara
  RAIFU mou sukoshi shika nai
  Soshite itsumo soko de E-kan tsukau
  See upcoming rock shows
  Get tickets for your favorite artists
  You might also like
  LiSA - crossing field (Romanized)
  Genius Romanizations
  黒うさP (Kurousa-P) - 千本桜 (Senbonzakura/Thousands of Cherry Trees) ft. Hatsune Miku (Romanized)
  Genius Romanizations
  花澤香菜 (Kana Hanazawa) - 恋愛サーキュレーション (Renai Circulation) (Romanized)
  Genius Romanizations
  Akiramezu ni
  EA-MAN made tadoritsuku keredo
  Sugu ni zanki nakunaru
  
  RIIFU SHIIRUDO ga areba
  Raku ni EA-MAN o taoseru kedo
  Nankai yattеmo nankai yattemo
  
  UDDO-MAN ga taosenai yo
  Ochiru konoha wa nankai
  Yattemo yokеrenai
  Ushiro ni sagatte
  Kyori o tottemo izure
  Wa kyori o tsumerareru
  TAIMU renda mo tameshite mita kedo
  Aitsu no janpu wa kugurenai
  Dakara tsugi wa zettai katsu tame ni
  Boku wa E-kan dake wa
  Saigo made totte oku
  
  
  AITEMU ni gou ga areba
  Raku ni mukou no kishi made tsuku kedo
  Nankai yattemo nankai yattemo
  
  EA-MAN ga taosenai yo
  Ano tatsumaki nankai yattemo yokerenai
  Ushiro ni mawatte
  Uchi tsuzuketemo izure
  Wa kaze ni tobasareru
  TAIMU renda mo tameshite mita kedo
  Tatsumaki aite ja imi ga nai
  Dakara tsugi wa zettai katsu tame ni
  Boku wa E-kan dake wa
  Saigo made totte oku
  
  Taosenai yo
  `
  Output:
  `
  Ki ga tsu+i+ta+ra
  o+na+ji me+n ba+ka+ri pu+re+i
  so+shi+te i+tsu+mo o+na+ji ba+sho de shi+nu
  A+ki+ra+me+zu ni
  ki+e+ru a+shi+ba ni chou+sen su+ru ke+do
  su+gu ni shi+ta ni o+chi+ru yo
  A+I+TE+MU ni go+u ga a+re+ba ra+ku ni
  mu+ko+u no ki+shi ma+de tsu+ku ke+do
  nan+kai ya+tte+mo nan+kai ya+tte+mo
  E+A+-MAN ga ta+o+se+na+i yo
  a+no ta+tsu+ma+ki nan+kai ya+tte+mo yo+ke+re+na+i
  u+shi+ro ni ma+wa+tte
  u+chi tsu+zu+ke+te+mo i+zu+re wa ka+ze ni to+ba+sa+re+ru
  TA+I+MU ren+da mo ta+me+shi+te mi+ta ke+do
  ta+tsu+ma+ki a+i+te ja i+mi ga na+i
  da+ka+ra tsu+gi wa ze+ttai ka+tsu ta+me ni
  bo+ku wa E+-kan da+ke wa sa+i+go ma+de to+tte o+ku
  Ki ga tsu+i+ta+ra
  RA+I+FU mo+u su+ko+shi shi+ka na+i
  so+shi+te i+tsu+mo so+ko de E+-kan tsu+ka+u
  A+ki+ra+me+zu ni
  E+A+-MAN ma+de ta+do+ri+tsu+ku ke+re+do
  su+gu ni zan+ki na+ku+na+ru
  RII+FU SHII+RU+DO ga a+re+ba
  ra+ku ni E+A+-MAN o ta+o+se+ru ke+do
  nan+kai ya+tte+mo nan+kai ya+tte+mo
  U+DDO+-MAN ga ta+o+se+na+i yo
  o+chi+ru ko+no+ha wa nan+kai ya+tte+mo yo+ke+re+na+i
  u+shi+ro ni sa+ga+tte
  kyo+ri o to+tte+mo i+zu+re wa kyo+ri o tsu+me+ra+re+ru
  TA+I+MU ren+da mo ta+me+shi+te mi+ta ke+do
  a+i+tsu no jan+pu wa ku+gu+re+na+i
  da+ka+ra tsu+gi wa ze+ttai ka+tsu ta+me ni
  bo+ku wa E+-kan da+ke wa sai+go ma+de to+tte o+ku
  A+I+TE+MU ni go+u ga a+re+ba
  ra+ku ni mu+ko+u no ki+shi ma+de tsu+ku ke+do
  nan+kai ya+tte+mo nan+kai ya+tte+mo
  E+A+-MAN ga ta+o+se+na+i yo
  a+no ta+tsu+ma+ki nan+kai ya+tte+mo yo+ke+re+na+i
  u+shi+ro ni ma+wa+tte
  u+chi tsu+zu+ke+te+mo i+zu+re wa ka+ze ni to+ba+sa+re+ru
  TA+I+MU ren+da mo ta+me+shi+te mi+ta ke+do
  ta+tsu+ma+ki a+i+te ja i+mi ga na+i
  da+ka+ra tsu+gi wa ze+tta+i ka+tsu ta+me ni
  bo+ku wa E+-kan da+ke wa sa+i+go ma+de to+tte o+ku
  Ta+o+se+na+i yo
  `
  ```
</details>
