# Podcast production kit (not deployed)

How Episode 1 was produced — reuse for the next episodes so they all sound and look the same.
Needs ffmpeg, Python 3 with numpy + scipy, and Node + Playwright (Chromium) for the artwork.

1. **Voice** (raw recording → `voice.wav`):
   `ffmpeg -i raw.m4a -ac 1 -ar 48000 -af "highpass=f=75:poles=2,afftdn=nr=8:nf=-60:tn=1,equalizer=f=200:t=q:w=1.2:g=-2.5,equalizer=f=3200:t=q:w=1.0:g=2.5,highshelf=f=9000:g=2,deesser=i=0.35:f=0.55,acompressor=threshold=-24dB:ratio=3:attack=8:release=180:makeup=6dB:knee=4,silenceremove=stop_periods=-1:stop_duration=0.85:stop_threshold=-46dB:stop_silence=0.6:detection=rms:window=0.03" voice.wav`
2. **Music**: `python synth.py` → `intro.wav`, `outro.wav` (original jingle, 112 BPM — same every episode).
3. **Loudness**: two-pass `loudnorm` (linear) — voice to −16 LUFS (mono), intro/outro to −17 LUFS → `*_n.wav`.
4. **Assemble**: `python assemble.py` → `episode_mix.wav` (voice enters over the intro's final chord, outro after).
   Social master: `alimiter=limit=0.84` → ≈ −14 LUFS. Podcast master: `volume=-2.3dB` + limiter → −16 LUFS, MP3 96 kbps joint stereo (`-b:a 96k -joint_stereo 1`)
   with the cover attached and ID3 tags.
5. **Artwork**: edit the title/episode texts in `design.html`, then `node render.js` → 3000² cover, show cover,
   1080² and 1080×1920 video backgrounds.
6. **Videos** (social): `CRF=24 ./mkvideo3.sh BG AUDIO OUT WX WY WW WH BX BY BW 20` — scrolling level-bars
   visualiser (`bars.py`, piped in as raw frames), x264 veryslow, AAC 128 kbps. ~1.7 MB/min, about 5x smaller than the
   old raw-waveform version (`mkvideo.sh`, kept for reference) at the same sharpness — the owner wanted small uploads.
   - square: `100 706 880 110 73 840 933` · reel: `100 1300 880 150 73 1490 933`
   - teaser = first ~75 s cut at a pause + the outro's final chord.
6b. **Reel cover** (1080×1920 JPG): `node render-rc.js` → `rc-bg.png` (design.html `#reelcover`: content inside Instagram's
   3:4 grid crop, no progress track); take one lively bars frame (`python bars.py teaser.wav 20 880 150 | ffmpeg … select=eq(n\,520)`)
   and overlay it with the same glow at x=100, y=1329 (`gblur=sigma=5`, alpha 0.55).
7. **Website**: copy MP3 + 1400² cover JPG to `assets/podcast/`, add the episode to `_podcast/episodes.py`,
   run `python build-podcast.py && python build-fa.py && python build-geo.py`.

8. **Deliver** to the owner in the chat (`display: "render"`): Reel teaser, square teaser, full-episode video, MP3,
   Reel cover, episode cover, Instagram image — plus the caption below.

## Caption template (Instagram + Facebook group) — always send one with each episode
```
🎙️ قسمت [اول/دوم/…] پادکست مکتب فارکس
[Dari title — as a hook question if possible]
[1–2 short lines: what the listener will learn]
🎧 قسمت کامل را در وب‌سایت بشنوید: forexschool.store (لینک در بیو)
#فارکس #مکتب_فارکس #پادکست #ترید #معامله_گری #مدیریت_ریسک #افغانستان #forex #trading [+ 2–4 topic tags]
```
Episode 1 example:
```
🎙️ قسمت اول پادکست مکتب فارکس
چرا اکثر معامله‌گران تازه‌کار ضرر می‌کنند؟ سه علت اصلی ضرر‌ده بودن تریدرهای تازه‌کار در بازار فارکس
🎧 قسمت کامل را در وب‌سایت بشنوید: forexschool.store (لینک در بیو)
#فارکس #مکتب_فارکس #پادکست #ترید #معامله_گری #مدیریت_ریسک #افغانستان #forex #trading
```
