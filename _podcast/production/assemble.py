# Assemble: intro music -> voice (enters over the intro's ringing tail, music ducked) -> outro music.
import numpy as np, wave
SR = 48000
BAR = 4 * 60 / 112

def load(p):
    with wave.open(p) as w:
        ch = w.getnchannels(); x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float32) / 32768
    x = x.reshape(-1, ch)
    return np.repeat(x, 2, 1) if ch == 1 else x

def save(p, x):
    with wave.open(p, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())

intro, voice, outro = load("intro_n.wav"), load("voice_n.wav"), load("outro_n.wav")
v_start = 5 * BAR + 0.55            # voice starts just after the intro's final hit
o_start = v_start + len(voice) / SR + 0.7

total = int((o_start + len(outro) / SR) * SR)
mix = np.zeros((total, 2), np.float32)

# duck the intro tail under the voice (-14 dB, 0.4 s ramp) then let it fade out
duck = np.ones(len(intro), np.float32)
i0 = int(v_start * SR) - int(0.15 * SR); ramp = int(0.4 * SR)
duck[i0:i0 + ramp] = np.linspace(1, 0.2, ramp); duck[i0 + ramp:] = 0.2
mix[: len(intro)] += intro * duck[:, None]

vi = int(v_start * SR); mix[vi: vi + len(voice)] += voice
oi = int(o_start * SR); mix[oi: oi + len(outro)] += outro

save("episode_mix.wav", mix)
print("voice in at %.2fs, outro at %.2fs, total %.1fs (%.1f min)" % (v_start, o_start, total / SR, total / SR / 60))
