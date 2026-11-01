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
7. **Website**: copy MP3 + 1400² cover JPG to `assets/podcast/`, add the episode to `_podcast/episodes.py`,
   run `python build-podcast.py && python build-fa.py && python build-geo.py`.
