#!/usr/bin/env python3
"""
EŞİĞİN ARDINDA — prosedürel varlık üretici.

Arka planları (1280x720 JPG), karakter silüetlerini (PNG) ve tüm sesleri (OGG)
sıfırdan üretir. Hiçbir dış dosyaya ihtiyaç duymaz; lisans sorunu yoktur.

Kullanım:
    python tools/gen_assets.py            # hepsini üret
    python tools/gen_assets.py --only bg  # yalnızca arka planlar (bg|char|audio)
    python tools/gen_assets.py --list     # üretilecek dosya listesi

Gereken: Python 3.9+, numpy, Pillow, ffmpeg (ses için).

Daha iyi bir görsel/ses bulduğunda, aynı dosya adıyla game/ altındaki dosyanın
üzerine yazman yeterli. Kod yalnızca dosya adına bakar.
"""

import argparse
import math
import os
import shutil
import subprocess
import sys
import tempfile
import wave
import zlib

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.join(ROOT, "game")
W, H = 1280, 720
SR = 44100

rng = np.random.default_rng(1106)


def h32(s):
    return zlib.crc32(s.encode())


# =============================================================================
# Görsel yardımcılar
# =============================================================================

def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def vgrad(top, bottom, w=W, h=H, curve=1.0):
    t = np.linspace(0, 1, h)[:, None] ** curve
    a = np.array(hexrgb(top), float)
    b = np.array(hexrgb(bottom), float)
    img = a[None, None, :] * (1 - t[..., None]) + b[None, None, :] * t[..., None]
    return np.repeat(img, w, axis=1)


def smooth_noise(w, h, scale, seed=None):
    r = np.random.default_rng(seed) if seed is not None else rng
    sw, sh = max(2, int(w / scale)), max(2, int(h / scale))
    small = (r.random((sh, sw)) * 255).astype(np.uint8)
    im = Image.fromarray(small).resize((w, h), Image.BICUBIC)
    return np.asarray(im, float) / 255.0


def fbm(w, h, base=200, octaves=4, seed=0):
    out = np.zeros((h, w))
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        out += amp * smooth_noise(w, h, base / (2 ** o), seed=seed + o)
        tot += amp
        amp *= 0.5
    return out / tot


def to_img(arr):
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def to_arr(img):
    return np.asarray(img.convert("RGB"), float)


def add_fog(arr, color="#8a9098", strength=0.35, ybias=0.6, seed=3):
    n = fbm(W, H, base=320, octaves=4, seed=seed)
    y = np.linspace(0, 1, H)[:, None]
    mask = np.clip((n - 0.35) * 1.8, 0, 1) * np.clip(1 - abs(y - ybias) * 1.6, 0, 1)
    mask = mask * strength
    c = np.array(hexrgb(color), float)
    return arr * (1 - mask[..., None]) + c * mask[..., None]


def vignette(arr, strength=0.75, power=2.2):
    y, x = np.mgrid[0:H, 0:W]
    d = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2) / math.sqrt(2)
    v = 1 - strength * np.clip(d, 0, 1) ** power
    return arr * v[..., None]


def grain(arr, amount=9):
    g = rng.normal(0, amount, (H, W, 1))
    return arr + g


def glow(arr, cx, cy, radius, color, strength=1.0):
    y, x = np.mgrid[0:H, 0:W]
    d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / radius
    m = np.exp(-d * d * 2.2) * strength
    c = np.array(hexrgb(color), float)
    return arr + c * m[..., None]


def finish(arr, name, fog=None, vig=0.75, gr=8, blur=0.0):
    if fog:
        arr = add_fog(arr, **fog)
    arr = vignette(arr, vig)
    arr = grain(arr, gr)
    img = to_img(arr)
    if blur:
        img = img.filter(ImageFilter.GaussianBlur(blur))
    path = os.path.join(GAME, "images", "bg", name + ".jpg")
    img.save(path, quality=88)
    return path


# ---------- Orman / dış mekân ----------

def draw_trees(img, n, ymin, ymax, wmin, wmax, color, seed, lean=0.0, branches=True):
    r = np.random.default_rng(seed)
    d = ImageDraw.Draw(img)
    for _ in range(n):
        x = r.uniform(-50, W + 50)
        w = r.uniform(wmin, wmax)
        top = r.uniform(-200, ymin)
        bottom = r.uniform(ymin, ymax) + 300
        lx = lean * r.uniform(-1, 1) * 60
        d.polygon([(x - w / 2, bottom), (x + w / 2, bottom), (x + w * 0.3 + lx, top), (x - w * 0.3 + lx, top)], fill=color)
        if branches:
            for _ in range(int(r.integers(2, 6))):
                by = r.uniform(top + 50, (top + bottom) / 2)
                dirn = r.choice([-1, 1])
                ln = r.uniform(40, 160) * (w / 30 + 0.5)
                d.line([(x, by), (x + dirn * ln, by - ln * r.uniform(0.2, 0.7))], fill=color, width=max(2, int(w / 6)))
    return img


def forest(name, sky=("#05070b", "#141a22"), layers=4, fog_color="#7d8792", fog_strength=0.35,
           road=False, fence=False, broken=False, tower=False, headlights=False, dawn=False, sign=False, moon=True):
    arr = vgrad(*sky, curve=0.8)
    if moon and not dawn:
        arr = glow(arr, W * 0.78, H * 0.16, 90, "#3b4250", 0.7)
    if dawn:
        arr = glow(arr, W * 0.5, H * 0.62, 520, "#6b4a3a", 0.7)
        arr = glow(arr, W * 0.5, H * 0.66, 260, "#b07a52", 0.5)
    img = to_img(arr)
    d = ImageDraw.Draw(img)
    def draw_tower(img):
        d = ImageDraw.Draw(img)
        tx, ty = W * 0.62, H * 0.18
        col = (16, 18, 24)
        d.polygon([(tx - 70, H * 0.66), (tx + 70, H * 0.66), (tx + 12, ty), (tx - 12, ty)], outline=col, fill=None, width=6)
        for k in range(10):
            yy = ty + (H * 0.66 - ty) * k / 10
            half = 12 + (58 * k / 10)
            yn = ty + (H * 0.66 - ty) * (k + 1) / 10
            halfn = 12 + (58 * (k + 1) / 10)
            d.line([(tx - half, yy), (tx + halfn, yn)], fill=col, width=3)
            d.line([(tx + half, yy), (tx - halfn, yn)], fill=col, width=3)
        d.line([(tx, ty), (tx, ty - 60)], fill=col, width=4)
        a = to_arr(img)
        a = glow(a, tx, ty - 60, 18, "#ff2a1a", 1.4)
        return to_img(a)

    # hill / ground
    ground_y = H * (0.70 if not road else 0.62)
    shades = []
    for i in range(layers):
        t = i / max(1, layers - 1)
        base = np.array(hexrgb(sky[1])) * (1 - t) * 0.9 + np.array([4, 5, 6]) * t
        if dawn:
            base = base * 0.8 + np.array([30, 22, 20]) * (1 - t)
        shades.append(tuple(int(c) for c in base))
    for i, col in enumerate(shades):
        draw_trees(img, n=14 + i * 6, ymin=H * 0.25, ymax=ground_y, wmin=6 + i * 6, wmax=14 + i * 14,
                   color=col, seed=h32(name) % 1000 + i, lean=0.2)
        if tower and i == 1:
            img = draw_tower(img)
        if i < layers - 1:
            a = add_fog(to_arr(img), fog_color, fog_strength * 0.55, ybias=0.55, seed=10 + i)
            img = to_img(a)
    d = ImageDraw.Draw(img)
    d.rectangle([0, ground_y + 40, W, H], fill=(6, 7, 8))
    if road:
        d.polygon([(W * 0.47, ground_y), (W * 0.53, ground_y), (W * 0.95, H), (W * 0.05, H)], fill=(22, 22, 24))
        for k in range(8):
            t0 = (k / 8) ** 1.8
            t1 = ((k + 0.45) / 8) ** 1.8
            y0 = ground_y + (H - ground_y) * t0
            y1 = ground_y + (H - ground_y) * t1
            d.polygon([(W / 2 - 1 - 4 * t0, y0), (W / 2 + 1 + 4 * t0, y0), (W / 2 + 1 + 6 * t1, y1), (W / 2 - 1 - 6 * t1, y1)], fill=(70, 66, 52))
    if fence:
        for k in range(9):
            t = (k / 9) ** 1.5
            x = W * 0.05 + (W * 0.47 - W * 0.05) * (1 - t)
            y = H - (H - ground_y) * t
            hgt = 140 * (1 - t) + 12
            d.rectangle([x - 5 * (1 - t) - 1, y - hgt, x + 5 * (1 - t) + 1, y], fill=(12, 12, 12))
            if k:
                d.line([(x, y - hgt * 0.7), (px, py - ph * 0.7)], fill=(30, 30, 30), width=2)
                d.line([(x, y - hgt * 0.4), (px, py - ph * 0.4)], fill=(30, 30, 30), width=2)
            px, py, ph = x, y, hgt
    if sign:
        d.rectangle([W * 0.16, H * 0.52, W * 0.27, H * 0.62], fill=(48, 44, 30))
        d.rectangle([W * 0.165, H * 0.53, W * 0.265, H * 0.61], outline=(110, 96, 54), width=3)
        d.text((W * 0.185, H * 0.555), "ECHO", fill=(140, 120, 70))
    if broken:
        d.polygon([(W * 0.3, H), (W * 0.36, H), (W * 0.35, H * 0.45), (W * 0.32, H * 0.48)], fill=(8, 8, 9))
        d.polygon([(W * 0.35, H * 0.45), (W * 0.32, H * 0.48), (W * 0.62, H * 0.86), (W * 0.64, H * 0.83)], fill=(9, 9, 10))
    arr = to_arr(img)
    if headlights:
        y, x = np.mgrid[0:H, 0:W]
        for cx in (W * 0.38, W * 0.62):
            cone = np.clip(1 - np.abs(x - cx - (y - H) * (cx - W / 2) / 900) / (40 + (H - y) * 0.9), 0, 1) * (y > ground_y)
            arr += np.array([120, 110, 80]) * cone[..., None] * 0.45
        arr = glow(arr, W * 0.38, H * 0.92, 50, "#fff0c0", 1.0)
        arr = glow(arr, W * 0.62, H * 0.92, 50, "#fff0c0", 1.0)
    return finish(arr, name, fog=dict(color=fog_color, strength=fog_strength, ybias=0.62, seed=h32(name) % 97))


# ---------- Koridor / iç mekân ----------

def corridor(name, wall="#2a2618", floor="#16140e", ceil="#0f0e0a", light="#e0b850", stripe=None,
             pipes=False, glass=False, doors=True, lights=6, depth=0.18, haze=0.25, alarm=False,
             dark=False, blood=False, lockers=False):
    vx, vy = W / 2, H * 0.46
    bw, bh = W * depth, H * depth * 1.1
    img = Image.new("RGB", (W, H), hexrgb(ceil))
    d = ImageDraw.Draw(img)
    # far wall
    fw = [vx - bw, vy - bh, vx + bw, vy + bh]
    # floor
    d.polygon([(0, H), (W, H), (fw[2], fw[3]), (fw[0], fw[3])], fill=hexrgb(floor))
    # ceiling
    d.polygon([(0, 0), (W, 0), (fw[2], fw[1]), (fw[0], fw[1])], fill=hexrgb(ceil))
    # walls
    d.polygon([(0, 0), (fw[0], fw[1]), (fw[0], fw[3]), (0, H)], fill=hexrgb(wall))
    wr = tuple(int(c * 0.82) for c in hexrgb(wall))
    d.polygon([(W, 0), (fw[2], fw[1]), (fw[2], fw[3]), (W, H)], fill=wr)
    d.rectangle(fw, fill=tuple(int(c * 0.4) for c in hexrgb(wall)))

    def lerp(a, b, t):
        return a + (b - a) * t

    # ribs / segments
    for k in range(1, 9):
        t = 1 - (1 - k / 9) ** 2.2
        x0, y0 = lerp(0, fw[0], t), lerp(0, fw[1], t)
        x1, y1 = lerp(W, fw[2], t), lerp(H, fw[3], t)
        y1b = lerp(H, fw[3], t)
        rib = tuple(int(c * 0.55) for c in hexrgb(wall))
        d.line([(x0, y0), (x0, lerp(H, fw[3], t))], fill=rib, width=max(1, int(8 * (1 - t))))
        d.line([(x1, lerp(0, fw[1], t)), (x1, y1b)], fill=rib, width=max(1, int(8 * (1 - t))))
        if doors and k in (2, 5):
            dx0 = x0 + 6
            dxa = lerp(0, fw[0], 1 - (1 - (k + 0.6) / 9) ** 2.2)
            dtop = lerp(0, fw[1], t) + (lerp(H, fw[3], t) - lerp(0, fw[1], t)) * 0.25
            dtopa = lerp(0, fw[1], 1 - (1 - (k + 0.6) / 9) ** 2.2)
            d.polygon([(dx0, dtop), (dxa, dtopa + (lerp(H, fw[3], 1 - (1 - (k + 0.6) / 9) ** 2.2) - dtopa) * 0.25),
                       (dxa, lerp(H, fw[3], 1 - (1 - (k + 0.6) / 9) ** 2.2)), (dx0, lerp(H, fw[3], t))],
                      fill=tuple(int(c * 0.5) for c in hexrgb(wall)))
        if lockers and k in (1, 2, 3):
            xa = lerp(W, fw[2], 1 - (1 - (k + 0.8) / 9) ** 2.2)
            for j in range(3):
                xx = lerp(x1, xa, j / 3)
                d.line([(xx, lerp(0, fw[1], t) + 120 * (1 - t)), (xx, lerp(H, fw[3], t) - 20 * (1 - t))], fill=(30, 32, 34), width=2)
    if pipes:
        for j, off in enumerate((0.06, 0.1, 0.14)):
            d.line([(0, H * off), (fw[0], fw[1] + bh * 0.2 * (j + 1) / 3)], fill=(40, 36, 28), width=int(14 - j * 3))
            d.line([(W, H * (off + 0.02)), (fw[2], fw[1] + bh * 0.2 * (j + 1) / 3)], fill=(36, 32, 26), width=int(12 - j * 3))
    if glass:
        for k in range(1, 7):
            t = 1 - (1 - k / 7) ** 2.0
            tn = 1 - (1 - (k + 0.8) / 7) ** 2.0
            for side in (0, 1):
                if side == 0:
                    xa, xb = lerp(0, fw[0], t), lerp(0, fw[0], tn)
                else:
                    xa, xb = lerp(W, fw[2], t), lerp(W, fw[2], tn)
                ya0, ya1 = lerp(0, fw[1], t) + 40 * (1 - t), lerp(H, fw[3], t) - 60 * (1 - t)
                yb0, yb1 = lerp(0, fw[1], tn) + 40 * (1 - tn), lerp(H, fw[3], tn) - 60 * (1 - tn)
                d.polygon([(xa, ya0), (xb, yb0), (xb, yb1), (xa, ya1)], outline=(120, 170, 210), fill=None, width=2)
    if stripe:
        d.polygon([(W / 2 - 60, H), (W / 2 + 60, H), (vx + 6, fw[3]), (vx - 6, fw[3])], fill=hexrgb(stripe))
    arr = to_arr(img)
    # ceiling lights
    for k in range(lights):
        t = 1 - (1 - (k + 0.5) / lights) ** 2.0
        cy = lerp(0, fw[1], t) + 8
        r = 140 * (1 - t) + 14
        flick = 1.0 if not dark else (0.25 if k % 2 else 0.05)
        arr = glow(arr, vx, cy, r, light, 0.8 * flick)
        arr = glow(arr, vx, lerp(H, fw[3], t) - 4, r * 1.6, light, 0.18 * flick)
    if alarm:
        arr = glow(arr, W * 0.12, H * 0.12, 260, "#ff1a10", 0.6)
        arr = glow(arr, W * 0.9, H * 0.2, 200, "#ff1a10", 0.45)
    if blood:
        for _ in range(5):
            bx, by = rng.uniform(W * 0.05, W * 0.25), rng.uniform(H * 0.45, H * 0.8)
            arr = glow(arr, bx, by, rng.uniform(14, 34), "#3a0000", -0.9)
    if dark:
        arr *= 0.55
    return finish(arr, name, fog=dict(color=light, strength=haze, ybias=0.48, seed=h32(name) % 91), vig=0.85)


def room(name, wall="#1d1b19", floor="#0f0e0d", lamp=None, window=False, desk=False, monitors=0,
         shelves=False, phone=False, table_map=False, warm=False, door=False):
    arr = vgrad(wall, floor, curve=1.3)
    img = to_img(arr)
    d = ImageDraw.Draw(img)
    hz = H * 0.62
    d.rectangle([0, hz, W, H], fill=hexrgb(floor))
    d.line([(0, hz), (W, hz)], fill=tuple(int(c * 0.6) for c in hexrgb(wall)), width=3)
    if window:
        wx0, wy0, wx1, wy1 = W * 0.62, H * 0.12, W * 0.86, H * 0.5
        d.rectangle([wx0, wy0, wx1, wy1], fill=(18, 24, 34) if not warm else (120, 140, 160))
        d.line([((wx0 + wx1) / 2, wy0), ((wx0 + wx1) / 2, wy1)], fill=(8, 8, 9), width=8)
        d.line([(wx0, (wy0 + wy1) / 2), (wx1, (wy0 + wy1) / 2)], fill=(8, 8, 9), width=8)
        d.rectangle([wx0, wy0, wx1, wy1], outline=(8, 8, 9), width=10)
    if shelves:
        for k in range(4):
            y = H * (0.18 + k * 0.12)
            d.rectangle([W * 0.05, y, W * 0.4, y + 8], fill=(40, 34, 26))
            r = np.random.default_rng(k + 40)
            x = W * 0.06
            while x < W * 0.39:
                bw = r.uniform(10, 40)
                bh = r.uniform(40, 80)
                c = int(r.uniform(20, 50))
                d.rectangle([x, y - bh, x + bw, y], fill=(c, int(c * 0.9), int(c * 0.75)))
                x += bw + r.uniform(1, 6)
    if door:
        d.rectangle([W * 0.08, H * 0.2, W * 0.22, hz], fill=(24, 24, 26), outline=(50, 50, 52), width=4)
    if desk:
        d.polygon([(W * 0.2, H * 0.72), (W * 0.8, H * 0.72), (W * 0.9, H * 0.86), (W * 0.1, H * 0.86)], fill=(34, 26, 18))
        d.rectangle([W * 0.12, H * 0.86, W * 0.15, H], fill=(20, 16, 12))
        d.rectangle([W * 0.85, H * 0.86, W * 0.88, H], fill=(20, 16, 12))
    if table_map:
        d.polygon([(W * 0.18, H * 0.66), (W * 0.82, H * 0.66), (W * 0.95, H * 0.98), (W * 0.05, H * 0.98)], fill=(150, 134, 100))
        for k in range(12):
            r = 30 + k * 26
            d.ellipse([W * 0.5 - r * 1.6, H * 0.82 - r * 0.35, W * 0.5 + r * 1.6, H * 0.82 + r * 0.35], outline=(120, 104, 74), width=2)
        pts = [(W * 0.3, H * 0.72), (W * 0.68, H * 0.71), (W * 0.82, H * 0.86), (W * 0.5, H * 0.95), (W * 0.2, H * 0.88)]
        for p in pts:
            d.line([p, (W * 0.5, H * 0.82)], fill=(150, 30, 20), width=3)
            d.ellipse([p[0] - 9, p[1] - 5, p[0] + 9, p[1] + 5], fill=(170, 30, 20))
        d.ellipse([W * 0.5 - 12, H * 0.82 - 6, W * 0.5 + 12, H * 0.82 + 6], outline=(20, 20, 20), width=3)
    arr = to_arr(img)
    for i in range(monitors):
        mx = W * (0.2 + 0.6 * (i + 0.5) / monitors)
        my = H * 0.42
        img2 = to_img(arr)
        d2 = ImageDraw.Draw(img2)
        d2.rectangle([mx - 90, my - 60, mx + 90, my + 60], fill=(12, 30, 26), outline=(30, 30, 30), width=6)
        for ln in range(8):
            yy = my - 50 + ln * 13
            d2.line([(mx - 80, yy), (mx - 80 + rng.uniform(30, 160), yy)], fill=(40, 120, 90), width=2)
        arr = to_arr(img2)
        arr = glow(arr, mx, my, 160, "#1f6b55", 0.35)
    if lamp:
        arr = glow(arr, lamp[0], lamp[1], lamp[2], lamp[3], 0.9)
    if phone:
        img2 = to_img(arr)
        d2 = ImageDraw.Draw(img2)
        px, py = W * 0.5, H * 0.78
        d2.rounded_rectangle([px - 60, py - 30, px + 60, py + 30], 8, fill=(170, 200, 230))
        for k in range(22):
            hh = abs(math.sin(k * 1.7)) * 18 + 2
            d2.line([(px - 50 + k * 4.6, py - hh / 2), (px - 50 + k * 4.6, py + hh / 2)], fill=(40, 60, 90), width=2)
        arr = to_arr(img2)
        arr = glow(arr, px, py, 260, "#6a90c0", 0.6)
    if window:
        arr = glow(arr, W * 0.74, H * 0.3, 260, "#2a3446" if not warm else "#d8c8a0", 0.5)
    return finish(arr, name, vig=0.8)


# ---------- Özel sahneler ----------

def z0(name, bridge=False, core=False, collapse=False):
    arr = vgrad("#020203", "#07080b")
    img = to_img(arr)
    d = ImageDraw.Draw(img)
    cx, cy = W / 2, H * 0.52
    ends = [(-100, H * 0.1), (W * 0.18, -80), (W * 0.82, -80), (W + 100, H * 0.1), (W / 2, -120)]
    for (ex, ey) in ends:
        for wdt, col in ((60, (14, 15, 18)), (36, (22, 24, 28))):
            d.line([(ex, ey), (cx, cy)], fill=col, width=wdt)
    d.ellipse([cx - 120, cy - 90, cx + 120, cy + 90], fill=(4, 4, 6), outline=(30, 34, 40), width=6)
    d.ellipse([cx - 70, cy - 52, cx + 70, cy + 52], fill=(0, 0, 0))
    if bridge:
        d.polygon([(0, H * 0.78), (W, H * 0.72), (W, H * 0.76), (0, H * 0.83)], fill=(26, 26, 28))
        for k in range(20):
            x = W * k / 19
            y = H * 0.78 - (H * 0.06) * k / 19
            d.line([(x, y), (x, y - 70)], fill=(40, 40, 42), width=3)
        d.line([(0, H * 0.78 - 70), (W, H * 0.72 - 70)], fill=(48, 48, 50), width=4)
    arr = to_arr(img)
    arr = glow(arr, cx, cy, 160, "#3a2a60", 0.5)
    arr = glow(arr, cx, cy, 60, "#9080ff", 0.2)
    if core:
        arr = glow(arr, W * 0.2, H * 0.5, 160, "#304050", 0.4)
        arr = glow(arr, W * 0.8, H * 0.5, 160, "#304050", 0.4)
    if collapse:
        arr = glow(arr, cx, cy, 420, "#5040a0", 0.35)
    return finish(arr, name, fog=dict(color="#202436", strength=0.3, ybias=0.5, seed=5), vig=0.9)


def isolation(name):
    arr = vgrad("#06080a", "#030304")
    img = to_img(arr)
    d = ImageDraw.Draw(img)
    d.rectangle([W * 0.2, H * 0.14, W * 0.8, H * 0.74], fill=(16, 22, 26), outline=(60, 66, 72), width=14)
    d.line([(W * 0.5, H * 0.14), (W * 0.5, H * 0.74)], fill=(50, 56, 60), width=6)
    arr = to_arr(img)
    arr = glow(arr, W * 0.5, H * 0.4, 260, "#6a8a90", 0.35)
    return finish(arr, name, vig=0.85)


def shaft(name):
    arr = vgrad("#050505", "#0d0c0a")
    img = to_img(arr)
    d = ImageDraw.Draw(img)
    for k in range(12):
        t = k / 12
        inset = W * 0.45 * t
        d.rectangle([inset * 0.6, H * 0.5 * t, W - inset * 0.6, H - H * 0.35 * t], outline=(30 - k, 28 - k, 24 - k), width=4)
    d.polygon([(W * 0.15, H * 0.8), (W * 0.85, H * 0.8), (W * 0.95, H), (W * 0.05, H)], fill=(40, 36, 20))
    for k in range(10):
        d.line([(W * (0.1 + k * 0.08), H * 0.8), (W * (0.07 + k * 0.088), H)], fill=(70, 60, 20), width=3)
    arr = to_arr(img)
    arr = glow(arr, W / 2, H * 0.45, 120, "#40302a", 0.4)
    return finish(arr, name, vig=0.9)


def archive_unknown(name):
    arr = vgrad("#0a0a0b", "#050505")
    img = to_img(arr)
    d = ImageDraw.Draw(img)
    for i, (txt, col) in enumerate((("TESİS 01 — ÇAMLIK / KAPATILDI", (130, 130, 130)),
                                    ("TESİS 02 — KONUM GİZLİ / AKTİF", (170, 40, 30)))):
        x0 = W * (0.12 + i * 0.42)
        d.polygon([(x0, H * 0.25), (x0 + W * 0.32, H * 0.22), (x0 + W * 0.34, H * 0.8), (x0 + 10, H * 0.83)], fill=(200, 196, 184))
        d.text((x0 + 30, H * 0.3), txt, fill=col)
        for ln in range(14):
            d.line([(x0 + 30, H * 0.36 + ln * 18), (x0 + 30 + rng.uniform(120, 340), H * 0.36 + ln * 18)], fill=(150, 146, 138), width=3)
    arr = to_arr(img)
    arr = glow(arr, W / 2, H * 0.2, 400, "#4a4a40", 0.4)
    return finish(arr, name, vig=0.9)


def kitchen(name):
    room(name, wall="#5a4c3c", floor="#3a3028", window=True, warm=True, desk=True,
         lamp=(W * 0.5, H * 0.05, 420, "#d0b080"))


def title(name):
    forest(name, sky=("#020305", "#0e1218"), tower=True, fog_strength=0.45, layers=5)


def gen_backgrounds():
    os.makedirs(os.path.join(GAME, "images", "bg"), exist_ok=True)
    jobs = {
        "title": lambda n: title(n),
        "phone_dark": lambda n: room(n, wall="#0a0b0e", floor="#060607", phone=True),
        "mert_room": lambda n: room(n, wall="#14161b", floor="#0a0a0c", window=True, desk=True, lamp=(W * 0.25, H * 0.55, 200, "#4a3a26"), door=True),
        "town_night": lambda n: town(n),
        "town_morning": lambda n: town(n, morning=True),
        "forest_night": lambda n: forest(n),
        "forest_fog": lambda n: forest(n, fog_strength=0.6, fog_color="#8a929c"),
        "forest_loop": lambda n: forest(n, fog_strength=0.5, broken=True, sky=("#04060a", "#10161e")),
        "service_road": lambda n: forest(n, road=True, fence=True, sign=True),
        "road_car": lambda n: forest(n, road=True, headlights=True, fog_strength=0.4),
        "forest_dawn": lambda n: forest(n, sky=("#20283a", "#6a5a58"), road=True, dawn=True, fog_color="#b0a4a0", fog_strength=0.4, moon=False),
        "tower": lambda n: forest(n, tower=True, layers=3, fog_strength=0.3),
        "depot": lambda n: room(n, wall="#1a1a18", floor="#0d0d0c", shelves=True, lamp=(W * 0.6, H * 0.3, 260, "#5a5040"), desk=True),
        "map_table": lambda n: room(n, wall="#16130f", floor="#0c0a08", table_map=True, lamp=(W * 0.5, H * 0.45, 340, "#6a5636")),
        "relay_station": lambda n: room(n, wall="#1a1c18", floor="#0c0d0b", monitors=2, shelves=True, lamp=(W * 0.7, H * 0.25, 180, "#4a5a40")),
        "echo_gate": lambda n: gate(n),
        "b3_corridor": lambda n: corridor(n, stripe="#8a7020", pipes=True),
        "b3_dark": lambda n: corridor(n, stripe="#5a4a18", pipes=True, dark=True, haze=0.15),
        "security_hall": lambda n: corridor(n, wall="#2c2e30", floor="#151617", ceil="#101112", light="#d8e0e8", lockers=True, doors=True, haze=0.18),
        "safe_room": lambda n: room(n, wall="#22221f", floor="#121210", desk=True, monitors=1, lamp=(W * 0.32, H * 0.55, 220, "#7a6040"), door=True),
        "d_corridor": lambda n: corridor(n, wall="#2a1414", floor="#140909", ceil="#0e0606", light="#ff3a2a", alarm=True, haze=0.3),
        "d14": lambda n: corridor(n, wall="#251010", floor="#120707", ceil="#0b0505", light="#d02a20", alarm=True, dark=True, blood=True, depth=0.24),
        "b1_office": lambda n: corridor(n, wall="#4a4e52", floor="#2a2c2e", ceil="#3a3c3e", light="#f0f4ff", doors=True, haze=0.12, lights=5),
        "b2_glass": lambda n: corridor(n, wall="#10202c", floor="#081018", ceil="#060c12", light="#6ab0e0", glass=True, doors=False, haze=0.3),
        "b2_archive": lambda n: room(n, wall="#101820", floor="#080c10", shelves=True, monitors=1, lamp=(W * 0.65, H * 0.2, 220, "#305070")),
        "drain": lambda n: drain(n),
        "control_room": lambda n: room(n, wall="#0e1214", floor="#07090a", monitors=4, desk=True),
        "transfer_room": lambda n: corridor(n, wall="#2a2a24", floor="#14140f", ceil="#0f0f0c", light="#c0b080", depth=0.3, lights=3, doors=False),
        "platform_shaft": lambda n: shaft(n),
        "z0_core": lambda n: z0(n),
        "z0_bridge": lambda n: z0(n, bridge=True),
        "core_room": lambda n: z0(n, core=True),
        "z0_collapse": lambda n: z0(n, collapse=True),
        "isolation": lambda n: isolation(n),
        "b3_exit": lambda n: corridor(n, stripe="#8a7020", pipes=True, light="#d0c8b8", haze=0.5, lights=3),
        "kitchen": lambda n: kitchen(n),
        "archive_unknown": lambda n: archive_unknown(n),
    }
    for name, fn in jobs.items():
        fn(name)
        print("  bg", name)
    return list(jobs)


def town(name, morning=False):
    sky = ("#3a4048", "#7a7c7e") if morning else ("#05070b", "#161c26")
    arr = vgrad(*sky)
    img = to_img(arr)
    d = ImageDraw.Draw(img)
    r = np.random.default_rng(77)
    x = -20
    while x < W:
        w = r.uniform(110, 220)
        h = r.uniform(140, 260)
        base = H * 0.72
        col = (40, 42, 46) if morning else (10, 11, 14)
        d.rectangle([x, base - h, x + w, base], fill=col)
        d.polygon([(x - 10, base - h), (x + w / 2, base - h - r.uniform(50, 90)), (x + w + 10, base - h)], fill=col)
        for _ in range(int(r.integers(1, 4))):
            wx = x + r.uniform(15, w - 40)
            wy = base - h + r.uniform(30, h - 60)
            lit = r.random() < (0.2 if morning else 0.45)
            d.rectangle([wx, wy, wx + 22, wy + 30], fill=(150, 120, 60) if lit else (20, 22, 26))
        x += w + r.uniform(5, 40)
    d.rectangle([0, H * 0.72, W, H], fill=(30, 30, 32) if morning else (8, 8, 9))
    arr = to_arr(img)
    if not morning:
        for lx in (W * 0.2, W * 0.55, W * 0.88):
            arr = glow(arr, lx, H * 0.5, 120, "#b08040", 0.5)
    if morning:
        arr = glow(arr, W * 0.3, H * 0.85, 200, "#202020", -0.3)
    return finish(arr, name, fog=dict(color="#9aa0a8" if morning else "#5a606a", strength=0.3, ybias=0.7, seed=12))


def gate(name):
    arr = vgrad("#141516", "#0a0a0b")
    img = to_img(arr)
    d = ImageDraw.Draw(img)
    d.rectangle([W * 0.28, H * 0.12, W * 0.72, H * 0.85], fill=(36, 38, 36), outline=(20, 20, 20), width=16)
    d.rectangle([W * 0.31, H * 0.17, W * 0.69, H * 0.85], fill=(48, 50, 46))
    for k in range(9):
        d.line([(W * 0.31, H * (0.2 + k * 0.07)), (W * 0.69, H * (0.2 + k * 0.07))], fill=(38, 40, 36), width=3)
    d.text((W * 0.46, H * 0.25), "E C H O", fill=(170, 150, 80))
    d.rectangle([W * 0.43, H * 0.24, W * 0.57, H * 0.3], outline=(130, 110, 60), width=3)
    r = np.random.default_rng(9)
    for _ in range(14):
        x0 = r.uniform(W * 0.33, W * 0.67)
        y0 = r.uniform(H * 0.4, H * 0.8)
        d.line([(x0, y0), (x0 + r.uniform(-30, 30), y0 + r.uniform(40, 90))], fill=(80, 80, 76), width=2)
    d.rectangle([0, H * 0.85, W, H], fill=(14, 14, 12))
    arr = to_arr(img)
    arr = glow(arr, W * 0.36, H * 0.6, 40, "#3a0000", -0.8)
    arr = glow(arr, W * 0.5, H * 0.05, 300, "#4a4a40", 0.3)
    return finish(arr, name, fog=dict(color="#6a6e70", strength=0.3, ybias=0.8, seed=21))


def drain(name):
    arr = vgrad("#0a0c0c", "#050606")
    img = to_img(arr)
    d = ImageDraw.Draw(img)
    for k in range(14):
        t = 1 - (1 - k / 14) ** 1.6
        rx, ry = W * 0.55 * (1 - t) + 30, H * 0.7 * (1 - t) + 20
        c = int(36 - 24 * t)
        d.ellipse([W / 2 - rx, H * 0.48 - ry, W / 2 + rx, H * 0.48 + ry], outline=(c, c + 2, c), width=max(2, int(18 * (1 - t))))
    d.polygon([(W * 0.3, H), (W * 0.7, H), (W * 0.51, H * 0.5), (W * 0.49, H * 0.5)], fill=(18, 26, 26))
    arr = to_arr(img)
    arr = glow(arr, W / 2, H * 0.48, 60, "#40504a", 0.4)
    return finish(arr, name, fog=dict(color="#3a4440", strength=0.3, ybias=0.5, seed=31), vig=0.9)


# =============================================================================
# Silüetler
# =============================================================================

CHARS = {
    # ad: (yükseklik ölçeği, omuz genişliği, saç tipi, rim rengi, ekstra)
    "mert": (1.0, 1.0, "short", "#c8a24a", None),
    "aras": (1.02, 1.04, "messy", "#6fa8dc", None),
    "deniz": (0.88, 0.86, "short", "#e0e0e0", "hood"),
    "duru": (0.94, 0.88, "long", "#d58aa0", None),
    "idil": (0.95, 0.88, "pony", "#b0a0e0", None),
    "kemal": (1.0, 1.06, "bald", "#9ec0a0", "collar"),
    "adrian": (1.04, 1.1, "slick", "#d04a3a", "collar"),
    "hakan": (1.05, 1.18, "cap", "#7aa0c0", None),
    "riza": (0.97, 1.0, "bald", "#a09070", "beard"),
    "bora": (1.04, 1.16, "short", "#c09060", None),
    "kaan": (1.0, 1.0, "messy", "#80b080", None),
    "elif": (0.93, 0.86, "long", "#e0a070", None),
    "emir": (0.97, 0.94, "short", "#a0a0d0", None),
}


def silhouette(name, hs, sw, hair, rim, extra):
    w, h = 520, 720
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    cx = w / 2
    top = h - 600 * hs
    head_w, head_h = 112, 140
    hy = top + 20
    d.ellipse([cx - head_w / 2, hy, cx + head_w / 2, hy + head_h], fill=255)
    if hair == "short":
        d.ellipse([cx - head_w / 2 - 6, hy - 10, cx + head_w / 2 + 6, hy + head_h * 0.55], fill=255)
    elif hair == "messy":
        for k in range(7):
            a = math.pi * (0.1 + 0.8 * k / 6)
            d.polygon([(cx - math.cos(a) * 40, hy + 30), (cx - math.cos(a) * 70, hy - 18 - (k % 2) * 10), (cx - math.cos(a) * 20, hy + 20)], fill=255)
        d.ellipse([cx - head_w / 2 - 8, hy - 8, cx + head_w / 2 + 8, hy + head_h * 0.5], fill=255)
    elif hair == "long":
        d.ellipse([cx - head_w / 2 - 12, hy - 10, cx + head_w / 2 + 12, hy + head_h * 0.62], fill=255)
        for sgn in (-1, 1):
            d.polygon([(cx + sgn * (head_w / 2 + 12), hy + 40), (cx + sgn * (head_w / 2 - 4), hy + 40),
                       (cx + sgn * (head_w / 2 - 6), hy + head_h + 40), (cx + sgn * (head_w / 2 + 26), hy + head_h + 70)], fill=255)
    elif hair == "pony":
        d.ellipse([cx - head_w / 2 - 6, hy - 8, cx + head_w / 2 + 6, hy + head_h * 0.55], fill=255)
        d.ellipse([cx + head_w / 2 - 6, hy + 10, cx + head_w / 2 + 34, hy + 120], fill=255)
    elif hair == "slick":
        d.ellipse([cx - head_w / 2 - 4, hy - 6, cx + head_w / 2 + 10, hy + head_h * 0.45], fill=255)
    elif hair == "cap":
        d.ellipse([cx - head_w / 2 - 6, hy - 14, cx + head_w / 2 + 6, hy + 50], fill=255)
        d.rectangle([cx - head_w / 2 - 6, hy + 26, cx + head_w / 2 + 50, hy + 40], fill=255)
    if extra == "hood":
        d.ellipse([cx - head_w / 2 - 26, hy - 24, cx + head_w / 2 + 26, hy + head_h + 30], fill=255)
    if extra == "beard":
        d.ellipse([cx - 46, hy + 70, cx + 46, hy + head_h + 26], fill=255)
    neck_y = hy + head_h - 10
    d.rectangle([cx - 28, neck_y, cx + 28, neck_y + 50], fill=255)
    sh = 160 * sw
    sy = neck_y + 34
    pts = [(cx - 34, sy - 6), (cx - sh * 0.62, sy + 18), (cx - sh * 0.92, sy + 52), (cx - sh, sy + 120),
           (cx - sh * 0.96, h + 10), (cx + sh * 0.96, h + 10), (cx + sh, sy + 120), (cx + sh * 0.92, sy + 52),
           (cx + sh * 0.62, sy + 18), (cx + 34, sy - 6)]
    d.polygon(pts, fill=255)
    # kol çizgisi (koyu boşluk) gövdeye hacim verir
    for sgn in (-1, 1):
        d.line([(cx + sgn * sh * 0.78, sy + 150), (cx + sgn * sh * 0.74, h)], fill=200, width=3)
    if extra == "collar":
        d.polygon([(cx - 60, sy - 20), (cx, sy + 60), (cx + 60, sy - 20), (cx + 70, sy + 10), (cx, sy + 90), (cx - 70, sy + 10)], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(2.0))
    ma = np.asarray(m, float) / 255
    # rim light: shift mask and take difference
    shifted = np.roll(ma, -7, axis=1)
    rimm = np.clip(ma - shifted, 0, 1)
    rimm = np.asarray(Image.fromarray((rimm * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)), float) / 255
    body = np.zeros((h, w, 3))
    yy = np.linspace(0, 1, h)[:, None, None]
    body += np.array([14, 15, 18]) * (1 - yy * 0.6)
    rc = np.array(hexrgb(rim), float)
    body = body + rc * rimm[..., None] * 1.6
    if extra == "glasses":
        gl = Image.new("L", (w, h), 0)
        gd = ImageDraw.Draw(gl)
        gd.ellipse([cx - 40, hy + 52, cx - 6, hy + 74], outline=255, width=3)
        gd.ellipse([cx + 6, hy + 52, cx + 40, hy + 74], outline=255, width=3)
        g = np.asarray(gl, float)[..., None] / 255
        body = body * (1 - g) + np.array([34, 40, 40]) * g
    alpha = np.clip(ma * 255 * (1 - np.clip((yy[..., 0] - 0.86) * 5, 0, 1)), 0, 255)
    rgba = np.dstack([np.clip(body, 0, 255), alpha]).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(os.path.join(GAME, "images", "char", name + ".png"))


def creature(name):
    w, h = 900, 720
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    r = np.random.default_rng(len(name) * 13)
    cx = w / 2
    if name == "nobetci":
        d.ellipse([cx - 260, 140, cx + 260, 760], fill=255)
        d.ellipse([cx - 110, 40, cx + 110, 230], fill=255)
        for s in (-1, 1):
            d.polygon([(cx + s * 220, 260), (cx + s * 420, 520), (cx + s * 380, 740), (cx + s * 300, 740), (cx + s * 320, 520), (cx + s * 160, 360)], fill=255)
    elif name == "surungen":
        d.ellipse([cx - 200, 300, cx + 200, 470], fill=255)
        d.ellipse([cx + 150, 280, cx + 300, 400], fill=255)
        for k in range(6):
            x0 = cx - 150 + k * 60
            sgn = 1 if k % 2 else -1
            d.line([(x0, 380), (x0 + sgn * 90, 200 + r.uniform(0, 60)), (x0 + sgn * 160, 700)], fill=255, width=14)
    elif name == "kirpinti":
        d.ellipse([cx - 120, 480, cx + 120, 640], fill=255)
        d.ellipse([cx + 60, 470, cx + 170, 560], fill=255)
        for k in range(4):
            x0 = cx - 90 + k * 60
            d.line([(x0, 600), (x0 - 30 + k * 10, 720)], fill=255, width=10)
    elif name == "taklitci":
        d.ellipse([cx - 52, 60, cx + 52, 200], fill=255)
        d.rectangle([cx - 24, 190, cx + 24, 260], fill=255)
        d.rounded_rectangle([cx - 150, 240, cx + 150, 900], 60, fill=255)
        for s in (-1, 1):
            d.line([(cx + s * 140, 280), (cx + s * 210, 560), (cx + s * 200, 760)], fill=255, width=34)
    m = m.filter(ImageFilter.GaussianBlur(4))
    ma = np.asarray(m, float) / 255
    noise = fbm(w, h, base=60, octaves=3, seed=len(name))
    ma = np.clip(ma * (0.75 + noise * 0.5), 0, 1)
    body = np.zeros((h, w, 3)) + np.array([6, 6, 8])
    if name == "nobetci":
        slit = Image.new("L", (w, h), 0)
        ImageDraw.Draw(slit).ellipse([cx - 16, 330, cx + 16, 520], fill=255)
        s = np.asarray(slit.filter(ImageFilter.GaussianBlur(8)), float)[..., None] / 255
        body = body + np.array([140, 40, 30]) * s
    alpha = np.clip(ma * 255, 0, 255)
    rgba = np.dstack([np.clip(body, 0, 255), alpha]).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(os.path.join(GAME, "images", "char", name + ".png"))


def gen_chars():
    os.makedirs(os.path.join(GAME, "images", "char"), exist_ok=True)
    for n, args in CHARS.items():
        silhouette(n, *args)
        print("  char", n)
    for n in ("nobetci", "surungen", "kirpinti", "taklitci"):
        creature(n)
        print("  char", n)
    # sis katmanı ve pencere simgesi
    n = fbm(W, H, base=300, octaves=4, seed=99)
    a = np.clip((n - 0.4) * 2.2, 0, 1) * 110
    fog = np.dstack([np.full((H, W), 150), np.full((H, W), 156), np.full((H, W), 164), a]).astype(np.uint8)
    Image.fromarray(fog, "RGBA").save(os.path.join(GAME, "images", "fog.png"))
    os.makedirs(os.path.join(GAME, "gui"), exist_ok=True)
    ic = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    d = ImageDraw.Draw(ic)
    d.ellipse([8, 8, 248, 248], fill=(12, 12, 14, 255), outline=(200, 162, 74, 255), width=10)
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        d.line([(128, 128), (128 + math.cos(a) * 96, 128 + math.sin(a) * 96)], fill=(200, 162, 74, 255), width=8)
        d.ellipse([128 + math.cos(a) * 96 - 12, 128 + math.sin(a) * 96 - 12, 128 + math.cos(a) * 96 + 12, 128 + math.sin(a) * 96 + 12], fill=(200, 40, 30, 255))
    d.ellipse([108, 108, 148, 148], fill=(0, 0, 0, 255), outline=(200, 162, 74, 255), width=6)
    ic.save(os.path.join(GAME, "gui", "window_icon.png"))
    # Ren'Py buton stilleri için şeffaf yedek arka plan
    os.makedirs(os.path.join(GAME, "gui", "button"), exist_ok=True)
    Image.new("RGBA", (8, 8), (0, 0, 0, 0)).save(os.path.join(GAME, "gui", "button", "background.png"))
    print("  fog + icon")


def gen_overlays():
    """Film greni kareleri ve vinyet katmanları (sinematik görünüm)."""
    d = os.path.join(GAME, "images", "fx")
    os.makedirs(d, exist_ok=True)
    gw, gh = 640, 360
    for i in range(4):
        r = np.random.default_rng(500 + i)
        n = r.normal(128, 60, (gh, gw))
        a = np.clip(np.abs(n - 128) * 1.4, 0, 255)
        g = np.clip(n, 0, 255)
        rgba = np.dstack([g, g, g, a]).astype(np.uint8)
        Image.fromarray(rgba, "RGBA").save(os.path.join(d, "grain%d.png" % i))
    y, x = np.mgrid[0:H, 0:W]
    dd = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2) / math.sqrt(2)
    a = np.clip((dd - 0.35) / 0.65, 0, 1) ** 1.8 * 235
    z = np.zeros((H, W))
    Image.fromarray(np.dstack([z, z, z, a]).astype(np.uint8), "RGBA").save(os.path.join(d, "vignette.png"))
    a2 = np.clip((dd - 0.25) / 0.75, 0, 1) ** 1.4 * 255
    Image.fromarray(np.dstack([z + 140, z, z, a2]).astype(np.uint8), "RGBA").save(os.path.join(d, "vignette_red.png"))
    print("  fx grain + vignette")


def gen_ui():
    """Harita işaretçileri ve arayüz panelleri."""
    md = os.path.join(GAME, "gui", "map")
    os.makedirs(md, exist_ok=True)
    n = 256
    y, x = np.mgrid[0:n, 0:n]
    d = np.sqrt((x - n / 2) ** 2 + (y - n / 2) ** 2) / (n / 2)
    ring = np.exp(-((d - 0.85) / 0.05) ** 2) * 255
    w = np.full((n, n), 255.0)
    Image.fromarray(np.dstack([w, w, w, ring]).astype(np.uint8), "RGBA").save(os.path.join(md, "ring.png"))
    n = 64
    y, x = np.mgrid[0:n, 0:n]
    d = np.sqrt((x - n / 2) ** 2 + (y - n / 2) ** 2) / (n / 2)
    core = np.clip(1 - d / 0.32, 0, 1) ** 0.6
    halo = np.exp(-(d / 0.55) ** 2) * 0.55
    a = np.clip(core + halo, 0, 1) * 255
    w = np.full((n, n), 255.0)
    Image.fromarray(np.dstack([w, w, w, a]).astype(np.uint8), "RGBA").save(os.path.join(md, "dot.png"))

    gd = os.path.join(GAME, "gui")
    # Diyalog kutusu: alttan yukarı degrade + üstte ortası parlak altın çizgi
    tw, th = 1280, 220
    yy = np.linspace(0, 1, th)[:, None]
    alpha = np.clip(0.25 + yy * 1.1, 0, 0.93) * 255
    alpha = np.repeat(alpha, tw, axis=1)
    rgb = np.zeros((th, tw, 3)) + np.array([5, 6, 8])
    xs = np.linspace(-1, 1, tw)[None, :]
    line = np.exp(-(xs / 0.55) ** 2)
    rgb[0:2, :, :] = np.array([200, 162, 74]) * line[0][:, None]
    alpha[0:2, :] = 255 * line[0] * 0.8
    Image.fromarray(np.dstack([rgb, alpha]).astype(np.uint8), "RGBA").save(os.path.join(gd, "textbox.png"))
    # İsim şeridi: solda dikey vurgu çizgisi
    nw, nh = 300, 40
    a = np.zeros((nh, nw))
    xs = np.linspace(0, 1, nw)[None, :]
    a[:, :] = np.clip(1 - xs * 1.1, 0, 1) * 170
    rgb = np.zeros((nh, nw, 3)) + np.array([14, 13, 10])
    rgb[:, 0:4] = [200, 162, 74]
    a[:, 0:4] = 255
    Image.fromarray(np.dstack([rgb, a]).astype(np.uint8), "RGBA").save(os.path.join(gd, "namebox.png"))
    # Seçim düğmeleri
    for state, edge, fill, glow in (("idle", (90, 80, 60), (10, 11, 13), 0.0), ("hover", (220, 180, 90), (34, 28, 16), 1.0)):
        bw, bh = 800, 56
        img = np.zeros((bh, bw, 4))
        img[..., :3] = fill
        xs = np.linspace(0, 1, bw)[None, :]
        img[..., 3] = (200 - xs * 60) if state == "idle" else 235
        img[:, 0:5, :3] = edge
        img[:, 0:5, 3] = 255
        if glow:
            g = np.exp(-xs * 6)[0]
            img[:, :, :3] += np.array([120, 90, 30]) * g[None, :, None] * 0.6
        img[0, :, :3] = edge
        img[0, :, 3] = 120
        img[-1, :, :3] = edge
        img[-1, :, 3] = 120
        Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGBA").save(os.path.join(gd, "choice_%s.png" % state))
    # Ana menü sol paneli
    pw, ph = 420, 720
    xs = np.linspace(0, 1, pw)[None, :]
    a = np.repeat(np.clip(1 - xs ** 1.6, 0, 1) * 235, ph, axis=0)
    rgb = np.zeros((ph, pw, 3)) + np.array([3, 4, 6])
    Image.fromarray(np.dstack([rgb, a]).astype(np.uint8), "RGBA").save(os.path.join(gd, "menu_panel.png"))
    print("  ui: ring, dot, textbox, namebox, choice, menu_panel")


# =============================================================================
# Ses
# =============================================================================

def t_axis(sec):
    return np.arange(int(sec * SR)) / SR


def bandnoise(sec, lo, hi, seed=None):
    r = np.random.default_rng(seed) if seed is not None else rng
    n = r.normal(0, 1, int(sec * SR))
    f = np.fft.rfft(n)
    fr = np.fft.rfftfreq(len(n), 1 / SR)
    mask = ((fr >= lo) & (fr <= hi)).astype(float)
    # yumuşak kenar
    mask = np.convolve(mask, np.ones(64) / 64, mode="same")
    out = np.fft.irfft(f * mask, len(n))
    return out / (np.max(np.abs(out)) + 1e-9)


def lowpass(x, cutoff):
    f = np.fft.rfft(x)
    fr = np.fft.rfftfreq(len(x), 1 / SR)
    f *= 1 / (1 + (fr / cutoff) ** 4)
    return np.fft.irfft(f, len(x))


def env_ad(n, a, dcy):
    t = np.arange(n) / SR
    e = np.minimum(t / max(a, 1e-4), 1.0) * np.exp(-np.maximum(t - a, 0) / max(dcy, 1e-4))
    return e


def slowmod(sec, rate, depth, seed=None):
    r = np.random.default_rng(seed) if seed is not None else rng
    pts = max(4, int(sec * rate) + 2)
    v = r.random(pts)
    xs = np.linspace(0, sec, pts)
    return 1 - depth + depth * np.interp(t_axis(sec), xs, v)


def reverb(x, sec=1.6, mix=0.3, seed=5):
    r = np.random.default_rng(seed)
    n = int(sec * SR)
    ir = r.normal(0, 1, n) * np.exp(-np.arange(n) / (SR * sec / 5))
    ir = lowpass(ir, 5000)
    L = len(x) + n
    y = np.fft.irfft(np.fft.rfft(x, L) * np.fft.rfft(ir, L), L)[:len(x)]
    y /= (np.max(np.abs(y)) + 1e-9)
    return x * (1 - mix) + y * mix * np.max(np.abs(x))


def loopify(x, fade=1.5):
    n = int(fade * SR)
    head = x[:n].copy()
    tail = x[-n:].copy()
    w = np.linspace(0, 1, n)
    x = x[:-n].copy()
    x[:n] = head * w + tail * (1 - w)
    return x


def norm(x, peak=0.8):
    return x / (np.max(np.abs(x)) + 1e-9) * peak


def tone(freq, sec, harmonics=(1.0,), phase=0.0):
    t = t_axis(sec)
    out = np.zeros_like(t)
    for i, a in enumerate(harmonics):
        out += a * np.sin(2 * np.pi * freq * (i + 1) * t + phase)
    return out


def write_ogg(x, rel, stereo=None):
    path = os.path.join(GAME, "audio", rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    x = np.clip(x, -1, 1)
    if stereo is not None:
        data = np.stack([x, np.clip(stereo, -1, 1)], axis=1)
        ch = 2
    else:
        data = x[:, None]
        ch = 1
    pcm = (data * 32767).astype(np.int16)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
        wav = tf.name
    with wave.open(wav, "wb") as wf:
        wf.setnchannels(ch)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libvorbis", "-q:a", "3", path], check=True)
    os.unlink(wav)
    print("  audio", rel)


def wind(sec, seed=1, lo=80, hi=900):
    a = bandnoise(sec, lo, hi, seed) * slowmod(sec, 0.25, 0.7, seed)
    b = bandnoise(sec, 300, 2400, seed + 7) * slowmod(sec, 0.6, 0.9, seed + 3) * 0.25
    return a + b


def crickets(sec, seed=2):
    r = np.random.default_rng(seed)
    t = t_axis(sec)
    out = np.zeros_like(t)
    for c in range(3):
        f = r.uniform(3800, 5200)
        rate = r.uniform(12, 18)
        chirp = (np.sin(2 * np.pi * rate * t + c) > 0.6).astype(float)
        chirp *= (np.sin(2 * np.pi * 0.35 * t + c * 2) > -0.2)
        out += np.sin(2 * np.pi * f * t) * lowpass(chirp, 60) * 0.15
    return out


def hum(sec, base=55, seed=4, rough=0.3):
    h = tone(base, sec, (1, 0.6, 0.35, 0.2, 0.1)) * slowmod(sec, 0.3, 0.25, seed)
    h += bandnoise(sec, 30, 200, seed) * rough
    return h


def machinery(sec, seed=6):
    x = hum(sec, 43, seed, 0.5) * 0.6 + bandnoise(sec, 100, 1200, seed) * 0.2 * slowmod(sec, 0.5, 0.6, seed)
    r = np.random.default_rng(seed)
    for _ in range(int(sec / 3)):
        p = int(r.uniform(0, sec - 1) * SR)
        k = metal_hit(r.uniform(0.3, 0.6), seed=int(r.integers(0, 999))) * r.uniform(0.15, 0.35)
        x[p:p + len(k)] += k[:len(x) - p]
    return x


def metal_hit(sec=0.6, seed=0, f0=None):
    r = np.random.default_rng(seed)
    n = int(sec * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    f0 = f0 or r.uniform(180, 420)
    for k, ratio in enumerate((1, 2.76, 5.4, 8.9, 13.3)):
        out += np.sin(2 * np.pi * f0 * ratio * t) * np.exp(-t * (6 + k * 5)) / (k + 1)
    out += r.normal(0, 1, n) * np.exp(-t * 60) * 0.5
    return out


def drag(sec=3.0, seed=8):
    x = bandnoise(sec, 120, 1800, seed) * slowmod(sec, 7, 0.9, seed) ** 2
    t = t_axis(sec)
    x *= np.sin(np.pi * t / sec) ** 0.7
    x += hum(sec, 38, seed, 0.2) * 0.3 * np.sin(np.pi * t / sec)
    return x


def heartbeat(sec=4.0, bpm=70):
    t = t_axis(sec)
    out = np.zeros_like(t)
    per = 60 / bpm
    for b in np.arange(0, sec, per):
        for off, amp in ((0, 1.0), (0.18, 0.7)):
            p = int((b + off) * SR)
            n = int(0.18 * SR)
            if p + n < len(out):
                tt = np.arange(n) / SR
                out[p:p + n] += np.sin(2 * np.pi * 52 * tt) * np.exp(-tt * 26) * amp
    return lowpass(out, 180)


def glitch(sec=0.8, seed=11):
    r = np.random.default_rng(seed)
    x = np.zeros(int(sec * SR))
    p = 0
    while p < len(x):
        n = int(r.uniform(0.01, 0.06) * SR)
        kind = r.integers(0, 3)
        if kind == 0:
            seg = r.normal(0, 1, n)
        elif kind == 1:
            seg = np.sign(np.sin(2 * np.pi * r.uniform(200, 2000) * np.arange(n) / SR))
        else:
            seg = np.zeros(n)
        x[p:p + n] = seg[:len(x) - p] * r.uniform(0.2, 0.8)
        p += n
    return x


def voice_like(sec=1.5, seed=12, f0=180):
    """Formantlı, anlaşılmayan 'insan sesi' gibi fısıltı."""
    t = t_axis(sec)
    src = bandnoise(sec, 100, 6000, seed) * 0.6 + np.sign(np.sin(2 * np.pi * f0 * t * (1 + 0.04 * np.sin(2 * np.pi * 3 * t)))) * 0.15
    f = np.fft.rfft(src)
    fr = np.fft.rfftfreq(len(src), 1 / SR)
    mask = np.zeros_like(fr)
    for fc, bw in ((700, 180), (1200, 220), (2600, 400)):
        mask += np.exp(-((fr - fc) / bw) ** 2)
    out = np.fft.irfft(f * mask, len(src))
    syll = (np.sin(2 * np.pi * 4.2 * t) * 0.5 + 0.5) ** 2
    return out * syll * np.sin(np.pi * t / sec)


def piano_note(freq, sec=3.0):
    t = t_axis(sec)
    x = np.zeros_like(t)
    for k, a in enumerate((1, 0.5, 0.25, 0.12, 0.06)):
        x += a * np.sin(2 * np.pi * freq * (k + 1) * t) * np.exp(-t * (1.2 + k * 0.9))
    return x * np.minimum(t / 0.005, 1)


def melody(notes, bpm=52, sec=None, pad=None, seed=1):
    beat = 60 / bpm
    total = sum(d for _, d in notes) * beat
    sec = sec or total + 4
    out = np.zeros(int(sec * SR))
    p = 0.0
    for f, d in notes:
        if f:
            n = piano_note(f, min(4.0, d * beat + 2.5))
            i = int(p * SR)
            out[i:i + len(n)] += n[:len(out) - i] * 0.5
        p += d * beat
    if pad:
        for f in pad:
            out += tone(f, sec, (1, 0.3)) * 0.05 * slowmod(sec, 0.1, 0.5, seed)
    return reverb(out, 2.5, 0.45)


NOTE = {n: 440 * 2 ** ((i - 9) / 12) for i, n in enumerate(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])}


def nf(name, octave):
    return NOTE[name] * 2 ** (octave - 4)


def gen_audio():
    if not shutil.which("ffmpeg"):
        print("! ffmpeg bulunamadı; sesler atlandı.")
        return
    # ---- Ambiyans (döngü) ----
    s = 34
    write_ogg(norm(loopify(wind(s, 1)), 0.5), "amb/wind.ogg", norm(loopify(wind(s, 2)), 0.5))
    write_ogg(norm(loopify(wind(s, 3) * 0.7 + crickets(s)), 0.45), "amb/forest_night.ogg", norm(loopify(wind(s, 4) * 0.7 + crickets(s, 5)), 0.45))
    x = wind(s, 6, 60, 400) * 0.5 + hum(s, 50, 6, 0.1) * 0.15
    r = np.random.default_rng(3)
    for _ in range(3):
        p = int(r.uniform(2, s - 3) * SR)
        bark = voice_like(0.35, int(r.integers(1, 99)), 300) * 0.25
        x[p:p + len(bark)] += reverb(bark, 1.2, 0.7)
    write_ogg(norm(loopify(x), 0.4), "amb/town_night.ogg")
    write_ogg(norm(loopify(hum(s, 55, 7, 0.2) + wind(s, 8) * 0.25), 0.5), "amb/tower_hum.ogg")
    write_ogg(norm(loopify(hum(s, 60, 9, 0.05) * 0.4 + bandnoise(s, 2000, 8000, 9) * 0.08 * slowmod(s, 3, 0.8, 9)), 0.4), "amb/relay.ogg")
    write_ogg(norm(loopify(machinery(s, 10)), 0.55), "amb/b3.ogg", norm(loopify(machinery(s, 11)), 0.55))
    write_ogg(norm(loopify(bandnoise(s, 400, 3000, 12) * 0.25 * slowmod(s, 0.2, 0.5, 12) + tone(1760, s) * 0.02 + hum(s, 70, 12, 0.05) * 0.2), 0.4), "amb/b2.ogg")
    t = t_axis(s)
    alarm = np.sin(2 * np.pi * 440 * t) * (np.sin(2 * np.pi * 0.5 * t) > 0.6) * 0.15
    write_ogg(norm(loopify(hum(s, 40, 13, 0.4) * 0.6 + lowpass(alarm, 900)), 0.5), "amb/quarantine.ogg")
    z = sum(tone(f, s, (1, 0.4)) * slowmod(s, 0.08, 0.6, 20 + i) for i, f in enumerate((36.7, 41.2, 49.0, 55.0, 61.7)))
    z += bandnoise(s, 20, 120, 14) * 0.6
    write_ogg(norm(loopify(z), 0.6), "amb/z0.ogg")
    birds = np.zeros(int(s * SR))
    r = np.random.default_rng(15)
    for _ in range(40):
        p = int(r.uniform(0, s - 1) * SR)
        n = int(r.uniform(0.08, 0.25) * SR)
        tt = np.arange(n) / SR
        f = r.uniform(2500, 4500)
        ch = np.sin(2 * np.pi * (f + 900 * np.sin(2 * np.pi * r.uniform(8, 20) * tt)) * tt) * np.sin(np.pi * tt / tt[-1])
        birds[p:p + n] += ch * r.uniform(0.05, 0.2)
    write_ogg(norm(loopify(birds + wind(s, 16, 60, 500) * 0.3), 0.45), "amb/dawn.ogg")
    tick = np.zeros(int(s * SR))
    for k in range(s):
        p = k * SR
        h_ = metal_hit(0.05, k, 2400) * 0.08
        tick[p:p + len(h_)] += h_
    write_ogg(norm(loopify(tick + bandnoise(s, 60, 400, 17) * 0.05), 0.3), "amb/kitchen.ogg")
    tens = hum(s, 32.7, 18, 0.2) + tone(65.4 * 1.06, s) * 0.2 * slowmod(s, 0.15, 0.8, 18)
    write_ogg(norm(loopify(tens), 0.5), "amb/tension.ogg")

    # ---- Efektler ----
    t = t_axis(0.5)
    write_ogg(norm(np.sin(2 * np.pi * 1000 * t) * (t < 0.35), 0.4), "sfx/phone_beep.ogg")
    cut = np.concatenate([glitch(0.5, 3) * 0.6, np.zeros(int(0.3 * SR)), np.sin(2 * np.pi * 425 * t_axis(0.25)) * 0.3, np.zeros(int(0.15 * SR)), np.sin(2 * np.pi * 425 * t_axis(0.25)) * 0.3])
    write_ogg(norm(cut, 0.6), "sfx/phone_cut.ogg")
    write_ogg(norm(bandnoise(1.2, 500, 6000, 4) * env_ad(int(1.2 * SR), 0.01, 0.5), 0.5), "sfx/static.ogg")
    write_ogg(norm(np.concatenate([bandnoise(0.15, 800, 5000, 5), np.sin(2 * np.pi * 1200 * t_axis(0.08))]) * 0.6, 0.5), "sfx/radio.ogg")
    write_ogg(norm(heartbeat(4.0, 72), 0.8), "sfx/heartbeat.ogg")
    write_ogg(norm(reverb(drag(3.0, 8), 1.5, 0.4), 0.7), "sfx/metal_drag.ogg")
    write_ogg(norm(reverb(np.concatenate([metal_hit(0.7, 1, 140), np.zeros(int(0.5 * SR)), metal_hit(0.7, 2, 140), np.zeros(int(0.6 * SR)), metal_hit(0.7, 3, 140)]), 1.8, 0.5), 0.7), "sfx/metal_knock.ogg")
    slam = metal_hit(1.2, 4, 70) + bandnoise(1.2, 30, 400, 4) * env_ad(int(1.2 * SR), 0.002, 0.15) * 2
    write_ogg(norm(reverb(slam, 2.0, 0.4), 0.9), "sfx/door_slam.ogg")
    hiss = bandnoise(1.6, 2000, 9000, 5) * env_ad(int(1.6 * SR), 0.05, 0.6) + hum(1.6, 80, 5, 0.1) * 0.3 * env_ad(int(1.6 * SR), 0.3, 0.8)
    write_ogg(norm(hiss, 0.5), "sfx/door_open.ogg")
    write_ogg(norm(np.concatenate([metal_hit(0.08, 6, 2200), np.zeros(int(0.06 * SR)), metal_hit(0.12, 7, 1600)]), 0.6), "sfx/lock_click.ogg")
    steps = np.zeros(int(2.4 * SR))
    for k in range(6):
        p = int(k * 0.4 * SR)
        st = bandnoise(0.12, 60, 900, 30 + k) * env_ad(int(0.12 * SR), 0.003, 0.03)
        steps[p:p + len(st)] += st
    write_ogg(norm(reverb(steps, 1.0, 0.3), 0.5), "sfx/footsteps.ogg")
    kc = np.zeros(int(1.6 * SR))
    r = np.random.default_rng(31)
    for _ in range(14):
        p = int(r.uniform(0, 1.5) * SR)
        c = metal_hit(0.04, int(r.integers(0, 99)), r.uniform(1800, 3200)) * r.uniform(0.3, 1)
        kc[p:p + len(c)] += c[:len(kc) - p]
    write_ogg(norm(reverb(kc, 0.8, 0.3), 0.6), "sfx/kirpinti.ogg")
    shot = bandnoise(1.5, 40, 6000, 32) * env_ad(int(1.5 * SR), 0.001, 0.08) * 2 + metal_hit(1.5, 33, 90) * 0.3
    write_ogg(norm(reverb(shot, 2.2, 0.45), 0.95), "sfx/gunshot.ogg")
    tt = t_axis(1.5)
    sweep = np.sin(2 * np.pi * (2000 * np.exp(-tt * 2.5) + 40) * tt) * np.exp(-tt * 1.2)
    write_ogg(norm(reverb(sweep + shot[:len(sweep)] * 0.6, 2.0, 0.4), 0.9), "sfx/resonance_shot.ogg")
    tt = t_axis(4.0)
    big = np.sin(2 * np.pi * (60 + 30 * tt) * tt) * env_ad(len(tt), 1.5, 1.2) + bandnoise(4.0, 30, 2000, 34) * env_ad(len(tt), 1.8, 0.6)
    write_ogg(norm(reverb(big, 2.5, 0.4), 0.9), "sfx/suppress.ogg")
    write_ogg(norm(glitch(0.9, 35), 0.6), "sfx/glitch.ogg")
    write_ogg(norm(reverb(voice_like(1.6, 36, 210), 2.0, 0.6), 0.6), "sfx/whisper.ogg")
    write_ogg(norm(reverb(voice_like(1.2, 37, 140), 2.5, 0.75), 0.6), "sfx/echo_voice.ogg")
    bs = np.zeros(int(4.0 * SR))
    r = np.random.default_rng(38)
    for _ in range(18):
        p = int(r.uniform(0, 2.4) * SR)
        n = int(r.uniform(0.08, 0.2) * SR)
        tq = np.arange(n) / SR
        f = r.uniform(2500, 4200)
        bs[p:p + n] += np.sin(2 * np.pi * (f + 700 * np.sin(2 * np.pi * 14 * tq)) * tq) * np.sin(np.pi * tq / tq[-1]) * 0.3
    bs[int(2.6 * SR):] = 0
    write_ogg(norm(bs + wind(4.0, 39) * 0.15 * (t_axis(4.0) < 2.6), 0.5), "sfx/birds_stop.ogg")
    tt = t_axis(2.5)
    write_ogg(norm(lowpass(np.sign(np.sin(2 * np.pi * 620 * tt)) * (np.sin(2 * np.pi * 2 * tt) > 0), 2000) * 0.5, 0.5), "sfx/alarm.ogg")
    write_ogg(norm(reverb(bandnoise(0.6, 30, 300, 40) * env_ad(int(0.6 * SR), 0.003, 0.1), 1.0, 0.3), 0.8), "sfx/thud.ogg")
    tt = t_axis(3.0)
    sting = sum(np.sin(2 * np.pi * f * tt) for f in (1046, 1108, 1174, 1244)) * env_ad(len(tt), 0.02, 0.9) + bandnoise(3.0, 50, 300, 41) * env_ad(len(tt), 0.01, 0.4)
    write_ogg(norm(reverb(sting, 2.5, 0.5), 0.75), "sfx/sting.ogg")
    tt = t_axis(0.08)
    write_ogg(norm(np.sin(2 * np.pi * 1800 * tt) * np.exp(-tt * 70), 0.15), "sfx/ui_hover.ogg")
    write_ogg(norm(metal_hit(0.3, 42, 600), 0.35), "sfx/ui_select.ogg")
    glass = bandnoise(1.0, 2000, 12000, 43) * env_ad(int(1.0 * SR), 0.001, 0.12)
    for k in range(6):
        o = int(k * 0.07 * SR)
        hit = metal_hit(1.0, 44 + k, 3000 + k * 500)[:len(glass) - o]
        glass[o:o + len(hit)] += hit * 0.2
    write_ogg(norm(reverb(glass, 1.4, 0.4), 0.7), "sfx/bottle.ogg")
    tt = t_axis(3.0)
    fan = np.sin(2 * np.pi * 110 * tt) * 0.3 + bandnoise(3.0, 200, 2000, 45) * (0.5 + 0.5 * np.sin(2 * np.pi * 18 * tt)) * 0.5
    write_ogg(norm(fan * np.minimum(tt / 0.8, 1), 0.6), "sfx/fan.ogg")
    tt = t_axis(5.0)
    plat = hum(5.0, 48, 46, 0.6) * np.minimum(tt / 0.5, 1) + metal_hit(5.0, 47, 120) * 0.6
    write_ogg(norm(reverb(plat, 2.0, 0.3), 0.7), "sfx/platform.ogg")
    tt = t_axis(2.5)
    growl = bandnoise(2.5, 40, 400, 48) * (0.5 + 0.5 * np.sin(2 * np.pi * 23 * tt)) * np.sin(np.pi * tt / 2.5) + tone(46, 2.5) * 0.4 * np.sin(np.pi * tt / 2.5)
    write_ogg(norm(reverb(growl, 2.5, 0.5), 0.85), "sfx/growl.ogg")
    sc = np.zeros(int(2.0 * SR))
    r = np.random.default_rng(49)
    for _ in range(40):
        p = int(r.uniform(0, 1.9) * SR)
        c = bandnoise(0.03, 800, 5000, int(r.integers(0, 999))) * env_ad(int(0.03 * SR), 0.001, 0.008)
        sc[p:p + len(c)] += c[:len(sc) - p] * r.uniform(0.3, 1)
    write_ogg(norm(reverb(sc, 1.0, 0.3), 0.6), "sfx/crawl.ogg")
    write_ogg(norm(reverb(np.concatenate([bandnoise(0.4, 100, 2000, 50) * env_ad(int(0.4 * SR), 0.01, 0.1), metal_hit(1.0, 51, 260)]), 1.5, 0.4), 0.7), "sfx/lever.ogg")
    tt = t_axis(0.25)
    write_ogg(norm(np.sin(2 * np.pi * 880 * tt) * np.exp(-tt * 12) + np.sin(2 * np.pi * 1320 * tt) * np.exp(-tt * 14) * 0.5, 0.5), "sfx/notify.ogg")
    tt = t_axis(1.0)
    write_ogg(norm(bandnoise(1.0, 200, 3000, 52) * env_ad(len(tt), 0.2, 0.3), 0.4), "sfx/flashlight.ogg")
    write_ogg(norm(np.concatenate([np.sin(2 * np.pi * 440 * t_axis(0.15)), np.zeros(int(0.1 * SR)), np.sin(2 * np.pi * 440 * t_axis(0.15))]) * 0.5, 0.4), "sfx/phone_ring.ogg")

    # ---- Müzik ----
    m = [("A", 3, 2), ("C", 4, 1), ("E", 4, 1), ("D", 4, 2), (None, 0, 1), ("C", 4, 1), ("B", 3, 2), ("G#", 3, 2),
         ("A", 3, 3), (None, 0, 1), ("E", 4, 1), ("F", 4, 1), ("E", 4, 1), ("D", 4, 1), ("C", 4, 2), ("B", 3, 2), ("A", 3, 4)]
    notes = [(nf(n, o) if n else None, d) for n, o, d in m]
    th = melody(notes, 50, sec=48, pad=(55, 82.4, 110))
    write_ogg(norm(loopify(th, 3.0), 0.55), "music/theme.ogg")
    m2 = [("C", 4, 2), ("E", 4, 1), ("G", 4, 1), ("A", 4, 2), ("G", 4, 2), ("F", 4, 1), ("E", 4, 1), ("D", 4, 2),
          ("C", 4, 2), ("E", 4, 1), ("G", 4, 1), ("C", 5, 3), ("B", 4, 1), ("A", 4, 2), ("G", 4, 4)]
    notes2 = [(nf(n, o), d) for n, o, d in m2]
    ep = melody(notes2, 60, sec=40, pad=(65.4, 98, 130.8))
    write_ogg(norm(loopify(ep, 3.0), 0.5), "music/epilogue.ogg")
    tt = t_axis(30)
    dread = tone(55, 30, (1, 0.5, 0.2)) * slowmod(30, 0.1, 0.6, 60) + tone(58.3, 30) * 0.4 + bandnoise(30, 2000, 6000, 61) * 0.03
    write_ogg(norm(loopify(reverb(dread, 3.0, 0.4)), 0.5), "music/dread.ogg")
    tt = t_axis(32)
    pulse = (np.sin(2 * np.pi * 2.2 * tt) > 0.7).astype(float)
    chase = lowpass(pulse, 80) * tone(41.2, 32) + bandnoise(32, 60, 500, 62) * 0.3 * slowmod(32, 2, 0.8, 62) + tone(82.4, 32) * 0.2
    write_ogg(norm(loopify(chase), 0.65), "music/chase.ogg")


def gen_extras():
    """Dedektör bipleri, telsiz paraziti, kâğıt dokusu, fener maskesi."""
    # Dedektör: yaklaştıkça hızlanan bip döngüleri
    for name, gap in (("tracker_slow", 1.6), ("tracker_med", 0.8), ("tracker_fast", 0.36)):
        sec = gap * 4
        x = np.zeros(int(sec * SR))
        for k in range(4):
            p = int(k * gap * SR)
            t = t_axis(0.09)
            b = np.sin(2 * np.pi * 1180 * t) * np.exp(-t * 30) + np.sin(2 * np.pi * 2360 * t) * np.exp(-t * 45) * 0.3
            x[p:p + len(b)] += b
        write_ogg(norm(x, 0.35), "sfx/%s.ogg" % name)
    # Telsiz paraziti (döngü) ve kilitlenme sesi
    s = 8
    st = bandnoise(s, 300, 7000, 70) * (0.7 + 0.3 * slowmod(s, 6, 0.8, 71))
    write_ogg(norm(loopify(st, 0.5), 0.45), "amb/static_loop.ogg")
    t = t_axis(0.6)
    lock = np.sin(2 * np.pi * 660 * t) * (t < 0.12) + np.sin(2 * np.pi * 990 * t) * ((t > 0.16) & (t < 0.3))
    write_ogg(norm(lock, 0.4), "sfx/radio_lock.ogg")
    # Korkutma vuruşu
    t = t_axis(1.6)
    hit = bandnoise(1.6, 40, 9000, 72) * env_ad(len(t), 0.002, 0.25) * 1.5
    hit += sum(np.sin(2 * np.pi * f * t) for f in (880, 932, 988, 1046)) * env_ad(len(t), 0.005, 0.6) * 0.4
    hit += np.sin(2 * np.pi * 45 * t) * env_ad(len(t), 0.003, 0.5)
    write_ogg(norm(reverb(hit, 1.8, 0.35), 0.95), "sfx/jumpscare.ogg")
    # Kâğıt
    pw, ph = 760, 900
    base = np.zeros((ph, pw, 3)) + np.array([206, 198, 178])
    n = fbm(pw, ph, base=90, octaves=4, seed=80)[..., None]
    base = base * (0.86 + 0.18 * n)
    yy, xx = np.mgrid[0:ph, 0:pw]
    dd = np.sqrt(((xx - pw / 2) / (pw / 2)) ** 2 + ((yy - ph / 2) / (ph / 2)) ** 2)
    base *= (1 - 0.28 * np.clip(dd - 0.5, 0, 1))[..., None]
    for _ in range(3):
        cx, cy, r = rng.uniform(80, pw - 80), rng.uniform(80, ph - 80), rng.uniform(30, 70)
        ring = np.exp(-((np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) - r) / 4) ** 2) * 18
        base -= ring[..., None] * np.array([0.6, 0.8, 1.0])
    Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB").save(os.path.join(GAME, "gui", "paper.png"))
    # Fener maskesi: siyah, ortasında yumuşak delik (fare ile hareket eder)
    mw, mh = 2560, 1440
    yy, xx = np.mgrid[0:mh, 0:mw]
    d = np.sqrt((xx - mw / 2) ** 2 + (yy - mh / 2) ** 2)
    a = np.clip((d - 120) / 140, 0, 1) ** 1.3 * 236
    z = np.zeros((mh, mw))
    Image.fromarray(np.dstack([z, z, z + 2, a]).astype(np.uint8), "RGBA").save(os.path.join(GAME, "gui", "flashlight_mask.png"))
    print("  extras: tracker, static, jumpscare, paper, flashlight_mask")


# =============================================================================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["bg", "char", "audio"])
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list:
        for sub in ("images/bg", "images/char", "audio/amb", "audio/sfx", "audio/music"):
            p = os.path.join(GAME, sub)
            if os.path.isdir(p):
                for f in sorted(os.listdir(p)):
                    print(os.path.join(sub, f))
        return
    if a.only in (None, "bg"):
        print("Arka planlar…")
        gen_backgrounds()
    if a.only in (None, "char"):
        print("Silüetler…")
        gen_chars()
        gen_overlays()
        gen_ui()
    if a.only in (None, "audio"):
        print("Sesler…")
        gen_audio()
        gen_extras()
    print("Tamam.")


if __name__ == "__main__":
    main()
