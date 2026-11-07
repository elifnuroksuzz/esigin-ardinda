#!/usr/bin/env python3
"""
EŞİĞİN ARDINDA — Ren'Py gerektirmeyen statik hikâye kontrolü.

Kontrol edilenler:
  * jump / call hedeflerinin (yerel .label dahil) tanımlı olması
  * scene/show ile kullanılan "bg x" görsellerinin game/images/bg/ altında bulunması
  * sfx()/amb()/amb2()/bgm() ve doğrudan "audio/..." yollarının var olması
  * add_note()/add_evidence() kimliklerinin state.rpy'de tanımlı olması
  * Her bölüm dosyasının (ch01..ch18) "label chNN" içermesi

Kullanım:  python tools/check_story.py
Çıkış kodu 0 = sorun yok, 1 = hata var.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.join(ROOT, "game")

errors = []


def rpy_files():
    for d, _, fs in os.walk(GAME):
        for f in fs:
            if f.endswith(".rpy"):
                yield os.path.join(d, f)


def rel(p):
    return os.path.relpath(p, ROOT)


labels = set()
refs = []          # (file, line, target)
bg_refs = []
audio_refs = []
note_refs = []
ev_refs = []
image_defs = set()

label_re = re.compile(r"^\s*label\s+([\w\.]+)\s*(\(.*\))?\s*:")
jump_re = re.compile(r"^\s*(jump|call)\s+(?!expression|screen)([\w\.]+)")
bg_re = re.compile(r"^\s*(scene|show)\s+bg\s+(\w+)")
img_re = re.compile(r"^\s*image\s+([\w ]+?)\s*[=:]")
fn_re = {
    "sfx": (re.compile(r"sfx\(\"(\w+)\""), "audio/sfx/%s.ogg"),
    "amb": (re.compile(r"amb2?\(\"(\w+)\""), "audio/amb/%s.ogg"),
    "bgm": (re.compile(r"bgm\(\"(\w+)\""), "audio/music/%s.ogg"),
}
path_re = re.compile(r"\"(audio/[\w/]+\.ogg)\"")
note_re = re.compile(r"add_note\(\"(\w+)\"\)")
ev_re = re.compile(r"add_evidence\(\"(\w+)\"\)")

for path in rpy_files():
    current_global = None
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            code = line.split("#", 1)[0] if not line.strip().startswith(("\"", "narrator", "centered")) else line
            m = label_re.match(line)
            if m:
                name = m.group(1)
                if name.startswith("."):
                    labels.add((current_global or "") + name)
                else:
                    labels.add(name)
                    if "." not in name:
                        current_global = name
            m = jump_re.match(line)
            if m:
                t = m.group(2)
                if t.startswith("."):
                    t = (current_global or "") + t
                refs.append((path, n, t))
            m = bg_re.match(line)
            if m:
                bg_refs.append((path, n, m.group(2)))
            m = img_re.match(line)
            if m:
                image_defs.add(m.group(1).strip())
            for key, (rx, fmt) in fn_re.items():
                for a in rx.findall(line):
                    audio_refs.append((path, n, fmt % a))
            for a in path_re.findall(line):
                audio_refs.append((path, n, a))
            for a in note_re.findall(line):
                note_refs.append((path, n, a))
            for a in ev_re.findall(line):
                ev_refs.append((path, n, a))

for path, n, t in refs:
    if t not in labels:
        errors.append("%s:%d tanımsız label: %s" % (rel(path), n, t))

bg_dir = os.path.join(GAME, "images", "bg")
bgs = {os.path.splitext(f)[0] for f in os.listdir(bg_dir)} if os.path.isdir(bg_dir) else set()
for path, n, b in bg_refs:
    if b not in bgs:
        errors.append("%s:%d arka plan bulunamadı: bg %s" % (rel(path), n, b))

for path, n, a in audio_refs:
    if not os.path.exists(os.path.join(GAME, a)):
        errors.append("%s:%d ses dosyası bulunamadı: %s" % (rel(path), n, a))

state = open(os.path.join(GAME, "core", "state.rpy"), encoding="utf-8").read()
journal_ids = set(re.findall(r"^\s*\"(\w+)\":\s*\(", state, re.M))
for path, n, a in note_refs + ev_refs:
    if a not in journal_ids:
        errors.append("%s:%d defter/kanıt kimliği tanımsız: %s" % (rel(path), n, a))

for i in range(1, 19):
    if "ch%02d" % i not in labels:
        errors.append("Bölüm label'ı eksik: ch%02d" % i)

print("Label: %d  ·  Atlama/çağrı: %d  ·  Arka plan ref.: %d  ·  Ses ref.: %d  ·  Defter/kanıt ref.: %d"
      % (len(labels), len(refs), len(bg_refs), len(audio_refs), len(note_refs) + len(ev_refs)))
if errors:
    print("\n%d sorun bulundu:" % len(errors))
    for e in errors:
        print("  ✗", e)
    sys.exit(1)
print("✓ Sorun bulunamadı.")
