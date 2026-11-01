# Original intro/outro music for the Forex School podcast (synthesised from scratch — no samples, no copyright issues).
# 112 BPM, A minor / C major pop progression (Am–F–C–G). Writes intro.wav and outro.wav (48 kHz stereo).
import numpy as np, wave
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
BPM = 112
BEAT = 60 / BPM
BAR = 4 * BEAT
rng = np.random.default_rng(7)

def t_(dur): return np.arange(int(dur * SR)) / SR
def midi(n): return 440.0 * 2 ** ((n - 69) / 12)
def lp(x, f, o=2): return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], "band", fs=SR, output="sos"), x)

def env_adsr(n, a=0.005, d=0.1, s=0.6, r=0.2, dur=None):
    e = np.zeros(n); A, D, R = int(a*SR), int(d*SR), int(r*SR)
    hold = n - R
    e[:A] = np.linspace(0, 1, A, endpoint=False) if A else 0
    e[A:A+D] = np.linspace(1, s, max(D, 1))[:len(e[A:A+D])]
    e[A+D:hold] = s
    e[hold:] = np.linspace(s, 0, n - hold)
    return e

def saw(f, t):
    # band-limited-ish saw via a few harmonics
    y = np.zeros_like(t)
    for k in range(1, 14):
        if f * k > 16000: break
        y += ((-1) ** (k + 1)) * np.sin(2 * np.pi * f * k * t) / k
    return y * 0.6

def place(buf, x, start, gain=1.0, pan=0.0):
    i = int(start * SR)
    if i >= buf.shape[0]: return
    x = x[: buf.shape[0] - i]
    l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    buf[i:i+len(x), 0] += x * gain * l * 1.414
    buf[i:i+len(x), 1] += x * gain * r * 1.414

# ---------------- instruments
def kick():
    t = t_(0.45)
    f = 45 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-t * 7.5)
    click = hp(rng.standard_normal(len(t)), 2000) * np.exp(-t * 300) * 0.25
    return np.tanh((y + click) * 1.6) * 0.9

def clap():
    t = t_(0.35)
    n = rng.standard_normal(len(t))
    e = np.zeros_like(t)
    for d in (0, 0.011, 0.022):
        e += np.where(t >= d, np.exp(-(t - d) * 60), 0)
    e += np.exp(-t * 14) * 0.5
    return bp(n, 900, 5000) * e * 0.5

def hat(open_=False):
    t = t_(0.25 if open_ else 0.06)
    return hp(rng.standard_normal(len(t)), 7000, 4) * np.exp(-t * (14 if open_ else 70)) * 0.22

def bass(note, dur):
    t = t_(dur); f = midi(note)
    y = saw(f, t) * 0.5 + np.sin(2 * np.pi * f * t) * 0.7
    y = lp(y, 900)
    return np.tanh(y * 1.3) * env_adsr(len(t), 0.004, 0.12, 0.7, 0.06) * 0.55

def pad(notes, dur):
    t = t_(dur); y = np.zeros_like(t)
    for n in notes:
        for det in (-0.08, 0.0, 0.09):
            y += saw(midi(n + det), t + rng.random())
    y = lp(y / (len(notes) * 3), 2200)
    return y * env_adsr(len(t), 0.25, 0.3, 0.8, 0.5) * 0.5

def pluck(note, dur=0.5):
    t = t_(dur); f = midi(note)
    y = (np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*2*f*t) * np.exp(-t*18) + 0.25*np.sin(2*np.pi*3*f*t) * np.exp(-t*30))
    return y * np.exp(-t * 6.5) * env_adsr(len(t), 0.002, 0.05, 1.0, 0.05) * 0.35

def bell(note, dur=1.6):
    t = t_(dur); f = midi(note)
    m = np.sin(2 * np.pi * f * 3.5 * t) * 2.2 * np.exp(-t * 3)
    return np.sin(2 * np.pi * f * t + m) * np.exp(-t * 2.6) * 0.3

def riser(dur):
    t = t_(dur)
    n = rng.standard_normal(len(t))
    y = np.zeros_like(t); seg = int(0.05 * SR)
    for i in range(0, len(t), seg):          # sweeping band-pass noise
        c = 400 + 7000 * (i / len(t)) ** 2
        y[i:i+seg] = bp(n[i:i+seg], c * 0.7, min(c * 1.4, 20000))
    return y * np.linspace(0, 1, len(t)) ** 2 * 0.35

def impact():
    t = t_(2.5)
    boom = np.sin(2*np.pi*(38 + 60*np.exp(-t*12))*t) * np.exp(-t*2.2)
    noise = lp(rng.standard_normal(len(t)), 3000) * np.exp(-t*4) * 0.3
    return (boom + noise) * 0.6

def reverb(x, secs=1.8, mix=0.22):
    ir_t = t_(secs)
    irl = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 4.0)
    irr = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 4.0)
    irl, irr = lp(irl, 6000), lp(irr, 6000)
    wl = fftconvolve(x[:, 0], irl)[: len(x)] * 0.03
    wr = fftconvolve(x[:, 1], irr)[: len(x)] * 0.03
    return x * (1 - mix) + np.stack([wl, wr], 1) * mix * 3

# ---------------- song
# Am – F – C – G  (vi–IV–I–V in C)
CHORDS = [(57, [57, 60, 64, 69]), (53, [53, 57, 60, 65]), (48, [55, 60, 64, 67]), (55, [55, 59, 62, 67])]
# catchy hook (one note per 8th, None = rest), one bar per chord
HOOK = [[76, None, 72, 76, None, 79, 76, 72],
        [77, None, 72, 77, None, 81, 79, 77],
        [79, None, 76, 72, None, 76, 79, 84],
        [83, None, 79, 74, None, 79, 83, 86]]

def section(n_bars, drums=True, hook=True, bass_on=True, start_bar=0):
    dur = n_bars * BAR + 3.0
    drums_b = np.zeros((int(dur * SR), 2)); music = np.zeros_like(drums_b)
    K, C = kick(), clap()
    for b in range(n_bars):
        root, notes = CHORDS[(b + start_bar) % 4]
        t0 = b * BAR
        place(music, pad(notes, BAR + 0.4), t0, 0.55, 0.0)
        if bass_on:
            for e in range(8):   # driving 8th-note bass with octave pops
                n = root - 12 + (12 if e in (3, 7) else 0)
                place(music, bass(n, BEAT / 2 * 0.9), t0 + e * BEAT / 2, 0.8, 0.0)
        if hook:
            for e, n in enumerate(HOOK[(b + start_bar) % 4]):
                if n is not None:
                    place(music, pluck(n), t0 + e * BEAT / 2, 0.9, -0.25 if e % 2 else 0.25)
                    place(music, pluck(n + 12, 0.3), t0 + e * BEAT / 2 + BEAT * 0.75, 0.18, 0.6)  # echo
        if drums:
            for q in range(4):
                place(drums_b, K, t0 + q * BEAT, 0.95)
                if q in (1, 3): place(drums_b, C, t0 + q * BEAT, 0.7, 0.1)
                place(drums_b, hat(), t0 + q * BEAT + BEAT / 2, 0.8, 0.35)
                place(drums_b, hat(), t0 + q * BEAT + BEAT * 0.25, 0.35, -0.35)
            place(drums_b, hat(True), t0 + 3.5 * BEAT, 0.6, 0.3)
    # sidechain-style pumping on the music from the kick
    if drums:
        pump = np.ones(len(music)); tt = t_(BEAT)
        shape = 1 - 0.45 * np.exp(-tt * 14)
        for b in range(n_bars * 4):
            i = int(b * BEAT * SR); seg = pump[i:i+len(shape)]; seg *= shape[:len(seg)]
        music *= pump[:, None]
    return reverb(music) + drums_b * 0.85

def master(x, ceil=0.89):
    x = np.tanh(x * 1.1) / np.tanh(1.1)
    return x / (np.max(np.abs(x)) + 1e-9) * ceil

def save(name, x):
    x = np.clip(x, -1, 1)
    with wave.open(name, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())

# INTRO: bar 1 pad + bell + riser, bars 2–4 full groove, impact + held chord (voice enters over the tail)
intro_len = 5 * BAR + 4.5
intro = np.zeros((int(intro_len * SR), 2))
place(intro, pad(CHORDS[0][1], BAR + 0.5), 0, 0.6)
for i, n in enumerate([69, 72, 76, 81]):
    place(intro, bell(n), i * BEAT, 0.55, -0.3 + 0.2 * i)
place(intro, riser(BAR), 0, 0.8)
body = section(4, start_bar=0)
intro[int(BAR*SR):int(BAR*SR)+len(body)] += body[: len(intro) - int(BAR*SR)]
end = 5 * BAR
place(intro, impact(), end, 0.9)
place(intro, kick(), end, 1.0)
tail = pad([57, 60, 64, 69, 72], 4.4)
place(intro, tail, end, 0.75)
for i, n in enumerate([81, 84, 88]):
    place(intro, bell(n, 2.5), end + i * 0.09, 0.4, -0.3 + 0.3 * i)
intro = reverb(intro, 2.4, 0.15)
fade = np.ones(len(intro)); fl = int(3.0 * SR); fade[-fl:] = np.linspace(1, 0, fl) ** 1.5
intro = master(intro * fade[:, None])
save("intro.wav", intro)

# OUTRO: 4 bars full groove, 2 bars without drums (hook only), final C-major chord + bells, long fade
outro_len = 6 * BAR + 5.0
outro = np.zeros((int(outro_len * SR), 2))
body = section(4, start_bar=0)
outro[: len(body)] += body[: len(outro)]
soft = section(2, drums=False, bass_on=False, start_bar=0)
place(outro, soft[:, 0] * 0, 0)  # (keeps place() signature exercise)
outro[int(4*BAR*SR):int(4*BAR*SR)+len(soft)] += soft[: len(outro) - int(4*BAR*SR)] * 0.9
endc = 6 * BAR
place(outro, pad([48, 55, 60, 64, 67, 72], 5.0), endc, 0.8)
place(outro, impact(), endc, 0.6)
for i, n in enumerate([72, 76, 79, 84]):
    place(outro, bell(n, 3.0), endc + i * 0.12, 0.4, -0.3 + 0.2 * i)
fin = np.ones(len(outro)); fi = int(1.2 * SR); fin[:fi] = np.linspace(0, 1, fi)
fo = int(4.0 * SR); fin[-fo:] *= np.linspace(1, 0, fo) ** 1.6
outro = master(reverb(outro, 2.4, 0.15) * fin[:, None])
save("outro.wav", outro)
print("intro %.1fs, outro %.1fs, bar %.3fs" % (len(intro) / SR, len(outro) / SR, BAR))
