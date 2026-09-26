#!/usr/bin/env python3
"""Build the RESET logo kit, every platform size, from the 5316px master.

    python3 build_kit.py [out_dir]        # default ../KIT

The drawing is never changed. The script colours it: bone lines, a lit iris
(amber core to ember rim), a two-stage glow, feathers running bone to sand
to ember at the tips. Change the palette below and rerun.
"""
import sys, pathlib, shutil
from PIL import Image, ImageFilter, ImageDraw
import numpy as np

here = pathlib.Path(__file__).parent.resolve()
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else here / '../KIT').resolve()

# ---- palette -------------------------------------------------------------
GROUND = (11, 10, 8)
BONE   = (242, 237, 232)
SAND   = (217, 195, 163)
EMBER  = (228, 87, 46)
AMBER  = (255, 176, 71)
HOT    = (255, 122, 60)

# ---- master geometry (measured once on the 5316 master) ------------------
src = Image.open(here / 'assets/RESET_master_5316.png').convert('RGBA')
A = np.array(src)[:, :, 3].astype(np.float32) / 255
H, W = A.shape
WORD = (1303, 1759); EYE = (1921, 3144); FEATH = (3145, 4843)
X0, X1 = 853, 4473
cx = (1338 + 3977) / 2; cy = (EYE[0] + EYE[1]) / 2; r = (EYE[1] - EYE[0]) / 2 - 38
yy, xx = np.mgrid[0:H, 0:W]
dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
DISC = dist <= r

def lerp(c0, c1, t):
    t = np.clip(t, 0, 1)[..., None]
    return np.array(c0) * (1 - t) + np.array(c1) * t

def colour_field():
    """RGB per pixel for the vivid treatment."""
    rgb = np.broadcast_to(np.array(BONE, np.float32), (H, W, 3)).copy()
    # iris: amber core -> hot -> ember rim
    t = np.clip(dist / r, 0, 1)
    iris = np.where(t[..., None] < .55, lerp(AMBER, HOT, t / .55), lerp(HOT, EMBER, (t - .55) / .45))
    rgb[DISC] = iris[DISC]
    # feathers: bone at the strings -> sand -> ember at the tips
    ft = np.clip((yy - FEATH[0]) / (FEATH[1] - FEATH[0]), 0, 1)
    feath = np.where(ft[..., None] < .5, lerp(BONE, SAND, ft / .5), lerp(SAND, EMBER, (ft - .5) / .5))
    fm = yy >= FEATH[0]
    rgb[fm] = feath[fm]
    return rgb

RGB = colour_field()

def layer(mask):
    im = Image.fromarray(np.dstack([RGB, mask * 255]).astype(np.uint8), 'RGBA')
    return im

def glow_layers(mask):
    """Two-stage glow behind the iris: wide ember, tight amber."""
    out = []
    for colour, blur, alpha in ((EMBER, 220, .75), (AMBER, 70, .45)):
        g = Image.new('RGBA', (W, H), colour + (0,))
        g.putalpha(Image.fromarray((mask * DISC * 255).astype(np.uint8)))
        g = g.filter(ImageFilter.GaussianBlur(blur))
        ga = np.array(g)[:, :, 3] * alpha
        g.putalpha(Image.fromarray(ga.astype(np.uint8)))
        out.append(g)
    return out

LOCKUPS = {
    'full':         ((yy >= WORD[0]), (X0, WORD[0], X1, FEATH[1])),
    'eye_wordmark': ((yy >= WORD[0]) & (yy <= EYE[1]), (X0, WORD[0], X1, EYE[1])),
    'eye':          ((yy >= EYE[0]) & (yy <= EYE[1]), (1338, EYE[0], 3977, EYE[1])),
    'wordmark':     ((yy >= WORD[0]) & (yy <= WORD[1]), (X0, WORD[0], X1, WORD[1])),
}
PAD = 300

def render_lockup(name, glow=True):
    rows, (x0, y0, x1, y1) = LOCKUPS[name]
    m = A * rows
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if glow and name != 'wordmark':
        for g in glow_layers(m): canvas.alpha_composite(g)
    canvas.alpha_composite(layer(m))
    return canvas.crop((x0 - PAD, y0 - PAD, x1 + PAD, y1 + PAD))

def fit(im, w, h, scale):
    im = im.copy(); im.thumbnail((int(w * scale), int(h * scale)), Image.LANCZOS); return im

def on_ground(lockup, w, h, scale=.72, dx=0, vignette=True):
    bg = Image.new('RGBA', (w, h), GROUND + (255,))
    if vignette:
        v = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(v)
        rr = int(max(w, h) * .55); d.ellipse((w/2 + dx - rr, h/2 - rr, w/2 + dx + rr, h/2 + rr), fill=EMBER + (40,))
        v = v.filter(ImageFilter.GaussianBlur(max(w, h) * .18)); bg.alpha_composite(v)
    art = fit(lockup, w, h, scale)
    bg.alpha_composite(art, (int((w - art.width) / 2 + dx), (h - art.height) // 2))
    return bg.convert('RGB')

def save(im, rel):
    p = OUT / rel; p.mkdir(parents=True, exist_ok=True) if p.suffix == '' else p.parent.mkdir(parents=True, exist_ok=True)
    im.save(p, optimize=True); print(rel)

def main():
    if OUT.exists(): shutil.rmtree(OUT)
    L = {k: render_lockup(k) for k in LOCKUPS}
    # 1. transparent masters
    for k, im in L.items():
        for s in (4096, 2048, 1024, 512):
            save(fit(im, s, s, 1.0), f'01_masters_transparent/RESET_{k}_{s}.png')
    # 2. on ground, square
    for k in ('full', 'eye_wordmark', 'eye'):
        for s in (2048, 1080, 512):
            save(on_ground(L[k], s, s, .72 if k != 'eye' else .78), f'02_on_ground/RESET_{k}_on_ground_{s}.png')
    # 3. avatars, eye only (circle-safe)
    for s in (1080, 800, 720, 512, 400, 320, 200, 180):
        save(on_ground(L['eye'], s, s, .74, vignette=False), f'03_avatars/RESET_avatar_{s}.png')
    # 4. platform pack
    P = {
        'instagram/profile_1080':          ('eye', 1080, 1080, .74, 0),
        'instagram/post_1080x1080':        ('full', 1080, 1080, .70, 0),
        'instagram/portrait_1080x1350':    ('full', 1080, 1350, .62, 0),
        'instagram/story_1080x1920':       ('full', 1080, 1920, .66, 0),
        'facebook/profile_720':            ('eye', 720, 720, .74, 0),
        'facebook/cover_1640x624':         ('eye_wordmark', 1640, 624, .52, 0),
        'facebook/event_cover_1920x1005':  ('full', 1920, 1005, .82, 0),
        'x/profile_400':                   ('eye', 400, 400, .74, 0),
        'x/header_1500x500':               ('eye_wordmark', 1500, 500, .58, 140),
        'youtube/avatar_800':              ('eye', 800, 800, .74, 0),
        'youtube/banner_2560x1440':        ('eye_wordmark', 2560, 1440, .24, 0),
        'tiktok/profile_400':              ('eye', 400, 400, .74, 0),
        'soundcloud/avatar_1000':          ('eye', 1000, 1000, .74, 0),
        'soundcloud/banner_2480x520':      ('eye_wordmark', 2480, 520, .62, 260),
        'spotify/profile_750':             ('eye', 750, 750, .74, 0),
        'spotify/header_2660x1140':        ('eye_wordmark', 2660, 1140, .40, 0),
        'linkedin/profile_400':            ('eye', 400, 400, .74, 0),
        'linkedin/cover_1128x191':         ('eye_wordmark', 1128, 191, .70, 150),
        'partiful/host_avatar_512':        ('eye', 512, 512, .74, 0),
        'partiful/event_cover_1200x1200':  ('full', 1200, 1200, .70, 0),
        'web/og_image_1200x630':           ('eye_wordmark', 1200, 630, .52, 0),
        'web/apple_touch_180':             ('eye', 180, 180, .80, 0),
        'web/icon_512':                    ('eye', 512, 512, .78, 0),
        'web/icon_192':                    ('eye', 192, 192, .78, 0),
    }
    for rel, (k, w, h, sc, dx) in P.items():
        save(on_ground(L[k], w, h, sc, dx, vignette=(w == h)), f'04_platforms/{rel}.png')
    # favicons: tighter crop, no glow so it stays crisp
    eye_crisp = render_lockup('eye', glow=False)
    for s in (16, 32, 48, 64):
        save(on_ground(eye_crisp, s, s, .92, vignette=False), f'04_platforms/web/favicon_{s}.png')
    ico = [on_ground(eye_crisp, s, s, .92, vignette=False) for s in (16, 32, 48)]
    (OUT / '04_platforms/web').mkdir(parents=True, exist_ok=True)
    ico[0].save(OUT / '04_platforms/web/favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[1:]); print('04_platforms/web/favicon.ico')
    # 5. print: one-colour versions, black on transparent and black on white, plus the SVG
    for k in ('full', 'eye_wordmark', 'eye', 'wordmark'):
        rows, (x0, y0, x1, y1) = LOCKUPS[k]
        m = Image.fromarray(((A * rows) * 255).astype(np.uint8)).crop((x0 - PAD, y0 - PAD, x1 + PAD, y1 + PAD))
        blk = Image.new('RGBA', m.size, (0, 0, 0, 0)); blk.putalpha(m); save(fit(blk, 4096, 4096, 1), f'05_print_one_colour/RESET_{k}_black_4096.png')
        wht = Image.new('RGBA', m.size, (255, 255, 255, 0)); wht.putalpha(m); save(fit(wht, 4096, 4096, 1), f'05_print_one_colour/RESET_{k}_white_4096.png')
        bw = Image.new('RGB', m.size, (255, 255, 255)); bw.paste((0, 0, 0), mask=m); save(fit(bw, 4096, 4096, 1), f'05_print_one_colour/RESET_{k}_black_on_white_4096.png')
    shutil.copy(here / 'assets/RESET_lockup.svg', OUT / '05_print_one_colour/RESET_full_vector.svg'); print('05_print_one_colour/RESET_full_vector.svg')
    # 6. contact sheet
    sheet = Image.new('RGB', (2200, 1400), (36, 36, 36)); d = ImageDraw.Draw(sheet)
    tiles = [('full', L['full']), ('eye + wordmark', L['eye_wordmark']), ('eye', L['eye']), ('wordmark', L['wordmark'])]
    x = 40
    for t, im in tiles:
        g = on_ground(im, 500, 500, .74); sheet.paste(g, (x, 40)); d.text((x, 550), t, fill=(230, 230, 230)); x += 540
    x = 40
    for s in (512, 180, 72, 32):
        av = Image.open(OUT / f'03_avatars/RESET_avatar_{512 if s > 180 else 180}.png').resize((s, s), Image.LANCZOS) if s > 32 else Image.open(OUT / '04_platforms/web/favicon_32.png')
        m = Image.new('L', (s, s), 0); ImageDraw.Draw(m).ellipse((0, 0, s - 1, s - 1), fill=255)
        sheet.paste(av, (x, 640), m); d.text((x, 640 + s + 6), f'{s}px', fill=(230, 230, 230)); x += s + 60
    for i, rel in enumerate(['x/header_1500x500', 'facebook/cover_1640x624', 'soundcloud/banner_2480x520']):
        b = Image.open(OUT / f'04_platforms/{rel}.png'); b.thumbnail((1000, 240)); sheet.paste(b, (1100, 620 + i * 260)); d.text((1100, 620 + i * 260 + b.height + 4), rel, fill=(230, 230, 230))
    sheet.save(OUT / '_kit_contact_sheet.jpg', quality=88); print('_kit_contact_sheet.jpg')

if __name__ == '__main__':
    main()
