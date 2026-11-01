# Scrolling level-bars visualiser for the audiogram videos (voice-memo style).
# Writes raw RGBA frames (W x H) to stdout: python bars.py AUDIO.wav FPS W H
# Each bar = loudness of 2 frames of audio; bars scroll left by PITCH/2 px per frame (integer shift ->
# very cheap for the video encoder), newest bar enters on the right; edges fade out.
import sys, wave, numpy as np

path, FPS, W, H = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
BAR, GAP = 8, 6
PITCH = BAR + GAP                 # 14 px
STEP = PITCH // 2                 # 7 px per frame -> one new bar every 2 frames
ORANGE = np.array([0xFA, 0x99, 0x39], np.float32)
HI = np.array([0xFF, 0xC5, 0x6B], np.float32)

with wave.open(path) as w:
    sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
    x = np.frombuffer(w.readframes(n), "<i2").astype(np.float32).reshape(-1, ch).mean(1) / 32768

frames = int(np.ceil(n / sr * FPS))
spb = sr * 2 / FPS                                  # samples per bar (2 frames)
nbars = int(np.ceil(len(x) / spb)) + 1
lvl = np.zeros(nbars, np.float32)
for i in range(nbars):
    seg = x[int(i * spb): int((i + 1) * spb)]
    if len(seg):
        db = 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9)
        lvl[i] = np.clip((db + 48) / 40, 0, 1)
lvl = np.maximum(lvl, 0.05)                          # tiny dots during silence
heights = np.round(lvl ** 1.15 * (H - 8) / 2) * 2    # even px, symmetric about centre

ncols = W // PITCH + 3
yy = np.arange(H, dtype=np.float32)[:, None] - (H - 1) / 2
xs = np.arange(W)
fade = np.clip(np.minimum(xs, W - 1 - xs) / 90.0, 0, 1) ** 1.3          # soft edges
grad = (np.abs(yy) / (H / 2))                                          # brighter in the middle
colour = (HI[None, None, :] * (1 - grad[..., None]) + ORANGE[None, None, :] * grad[..., None])
colour = np.ascontiguousarray(np.broadcast_to(colour, (H, W, 3)))
out = sys.stdout.buffer
for f in range(frames):
    newest = f // 2                                   # bar index at the right edge
    sub = (f % 2) * STEP                              # half-step scroll between bars
    img_a = np.zeros((H, W), np.float32)
    for k in range(ncols):                            # k = 0 is the newest (rightmost) bar
        bi = newest - k
        if bi < 0: break
        x0 = W - PITCH - k * PITCH + (PITCH - STEP) - sub
        x1 = x0 + BAR
        if x1 <= 0: break
        if x0 >= W: continue
        h = heights[min(bi, nbars - 1)]
        r = BAR / 2
        a, b = max(x0, 0), min(x1, W)
        # rounded-cap bar: |y| <= h/2 with round ends (distance to the capsule)
        cx = (x0 + x1 - 1) / 2
        dxc = np.abs(np.arange(a, b) - cx)[None, :]
        half = max(h / 2 - r, 0)
        dy = np.maximum(np.abs(yy) - half, 0)
        d = np.sqrt(dxc ** 2 + dy ** 2)
        img_a[:, a:b] = np.maximum(img_a[:, a:b], np.clip(r + 0.5 - d, 0, 1))
    alpha = img_a * fade[None, :]
    frame = np.dstack([colour, alpha[..., None] * 255]).astype(np.uint8)
    out.write(frame.tobytes())
