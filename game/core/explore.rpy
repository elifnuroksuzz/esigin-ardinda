## KEŞİF MOTORU ###############################################################
##
## Tur tabanlı düğüm haritası. Oyuncu bir eylem yapar, sonra tehditler hareket eder.
## Esinlenilen: Alien: Isolation (gürültü), FNAF (kıt bilgi), Into the Breach
## (okunabilir düşman niyeti), Darkest Dungeon (kaynak), Duskers (oda oda keşif).
##
## Kullanım:  call explore("b3")
## Harita tanımları: core/maps.rpy

default sise = 0                 # fırlatılabilir şişe (dikkat dağıtır)
default kaydedici = 0            # ses kaydedici (uzaktan güçlü gürültü)
default saglik = 3               # keşif sırasındaki can
default ex = None                # aktif keşif durumu
default ex_done = False
default ex_result = None
default ex_hud_prev = False
default persistent.map_stars = {}

init -4 python:
    renpy.music.register_channel("tracker", mixer="sfx", loop=True)

init -1 python:

    import collections

    ACTION_NOISE = {"move": 1, "run": 3, "shoot": 5, "throw": 4, "decoy": 5}
    SEARCH_COST = 6
    MAX_HEALTH = 3

    THREAT_INFO = {
        "nobetci": dict(name="NÖBETÇİ", speed=2, hear=0, light=False, steps=1, dmg=2, vents=False, killable=False),
        "kirpinti": dict(name="KIRPINTI", speed=1, hear=1, light=False, steps=1, dmg=1, vents=True, killable=True),
        "surungen": dict(name="SÜRÜNGEN", speed=1, hear=0, light=True, steps=2, dmg=1, vents=False, killable=False),
    }

    LOOT_INFO = {
        "pil": ("Yedek pil", "Fener pili +35"),
        "sise": ("Boş şişe", "Fırlatıp dikkat dağıtmak için"),
        "ilkyardim": ("İlk yardım", "Bir can yeniler"),
        "mermi": ("Mermi", "+2 tabanca mermisi"),
        "kaydedici": ("Ses kaydedici", "Uzak bir odada güçlü gürültü"),
    }

    def link_key(a, b):
        return a + "|" + b if a < b else b + "|" + a

    def _adj(mid):
        M = MAPS[mid]
        if "_adj" not in M:
            adj = collections.defaultdict(list)
            for l in M["links"]:
                a, b = l[0], l[1]
                kind = l[2] if len(l) > 2 else ""
                adj[a].append((b, kind))
                adj[b].append((a, kind))
            M["_adj"] = dict(adj)
        return M["_adj"]

    def ex_map():
        return MAPS[ex["id"]]

    def ex_max_hp():
        return MAX_HEALTH + (1 if zorluk == "hikaye" else 0) - (1 if zorluk == "kabus" else 0)

    def ex_nearest():
        """En yakın canlı tehdidin oda uzaklığı (dedektör için)."""
        ds = [ex_dist(ex["room"], t["room"]) for t in ex["threats"] if t["alive"]]
        return min(ds) if ds else 99

    def ex_tracker():
        d = ex_nearest()
        f = {1: "tracker_fast", 2: "tracker_med", 3: "tracker_slow"}.get(d)
        if d == 0:
            f = "tracker_fast"
        if f:
            renpy.music.play("audio/sfx/%s.ogg" % f, channel="tracker", loop=True, if_changed=True)
        else:
            renpy.music.stop(channel="tracker", fadeout=0.5)

    def ex_pos(M, rid):
        """Harita koordinatını sağ panelin solundaki alana sığdırır."""
        x, y = M["rooms"][rid]["pos"]
        return (int(125 + (x - 150) * 0.93), int(y))

    def ex_neighbors(room, who=None):
        """who: None = oyuncu, aksi hâlde tehdit türü."""
        out = []
        for other, kind in _adj(ex["id"]).get(room, []):
            if link_key(room, other) in ex["blocked"]:
                continue
            if who is not None and kind == "vent" and not THREAT_INFO[who]["vents"]:
                continue
            out.append(other)
        return out

    def ex_bfs(start, who=None):
        dist = {start: 0}
        prev = {start: None}
        q = collections.deque([start])
        while q:
            r = q.popleft()
            for n in ex_neighbors(r, who):
                if n not in dist:
                    dist[n] = dist[r] + 1
                    prev[n] = r
                    q.append(n)
        return dist, prev

    def ex_dist(a, b, who=None):
        return ex_bfs(a, who)[0].get(b, 99)

    def ex_path(a, b, who=None):
        dist, prev = ex_bfs(a, who)
        if b not in dist:
            return []
        p = [b]
        while prev[p[-1]] is not None:
            p.append(prev[p[-1]])
        p.reverse()
        return p[1:]

    def ex_log(msg):
        ex["log"].append(msg)
        if len(ex["log"]) > 6:
            ex["log"].pop(0)

    def ex_snapshot():
        return dict(pil=pil, mermi=mermi, sise=sise, ilkyardim=ilkyardim, kaydedici=kaydedici,
                    rezonans=rezonans, gerginlik=gerginlik, yedek_pil=yedek_pil)

    def ex_restore(s):
        global pil, mermi, sise, ilkyardim, kaydedici, rezonans, gerginlik, yedek_pil
        pil, mermi, sise, ilkyardim = s["pil"], s["mermi"], s["sise"], s["ilkyardim"]
        kaydedici, rezonans, gerginlik, yedek_pil = s["kaydedici"], s["rezonans"], s["gerginlik"], s["yedek_pil"]

    def ex_begin(mid, retry=False):
        global ex, saglik
        M = MAPS[mid]
        fails = ex["fails"] if (retry and ex) else 0
        snap = ex["snap"] if (retry and ex) else ex_snapshot()
        if retry:
            ex_restore(snap)
        saglik = ex_max_hp()
        threats = []
        for t in M.get("threats", []):
            threats.append(dict(type=t["type"], room=t["start"], target=t.get("hunt"),
                                patrol=list(t.get("patrol", [])), pi=0, stun=0, alive=True,
                                seen=False, chase=t.get("chase", False)))
        ex = dict(id=mid, room=M["start"], prev=None, turn=0, noise_total=0, damage=0,
                  hidden=False, log=[], threats=threats, searched=[], flags=[], visited=[M["start"]],
                  blocked={}, lure={}, events_done=[], listen=False, pings=[], last_noise=None,
                  fails=fails, snap=snap, detected=False, run=False, hit=False, newdoc=None)
        ex_log(M.get("intro_log", "Keşif başladı."))

    def ex_machine_on(room):
        r = ex_map()["rooms"][room]
        m = r.get("mask")
        if m == "always":
            return True
        if m == "machine":
            return ex["turn"] % 2 == 0
        return False

    def ex_can_run():
        return not ex_map().get("no_run", False)

    def ex_run_targets():
        if not ex_can_run():
            return []
        dist = ex_bfs(ex["room"])[0]
        return [r for r, d in dist.items() if d == 2]

    def ex_throw_targets(maxd=2):
        dist = ex_bfs(ex["room"])[0]
        return [r for r, d in dist.items() if 1 <= d <= maxd]

    def ex_threats_here(room):
        return [t for t in ex["threats"] if t["alive"] and t["room"] == room]

    def ex_shoot_target():
        """Önce aynı odadaki, sonra komşu odadaki tehdit."""
        cands = []
        for t in ex["threats"]:
            if not t["alive"]:
                continue
            d = ex_dist(ex["room"], t["room"])
            if d <= 1:
                cands.append((d, 0 if THREAT_INFO[t["type"]]["killable"] else 1, t))
        if not cands:
            return None
        cands.sort(key=lambda c: (c[0], c[1]))
        return cands[0][2]

    def ex_room_use():
        r = ex_map()["rooms"][ex["room"]]
        return r.get("use")

    def ex_requirements_met():
        M = ex_map()
        req = M.get("require", [])
        need = M.get("require_count", len(req))
        return sum(1 for f in req if f in ex["flags"]) >= need

    def ex_unsearched_here():
        r = ex_map()["rooms"][ex["room"]]
        return ex["room"] not in ex["searched"] and (r.get("loot") or r.get("clue") or r.get("doc"))

    ## --- Tur ------------------------------------------------------------------

    def ex_act(action):
        global pil, mermi, sise, ilkyardim, kaydedici, saglik, rezonans, yedek_pil
        M = ex_map()
        kind = action[0]
        noises = []      # (oda, seviye, tür)
        ex["hidden"] = False
        ex["listen"] = False
        ex["hit"] = False
        ex["newdoc"] = None
        store.st_turns += 1
        here = ex["room"]

        def make_noise(room, lvl, t="sound"):
            if t == "sound" and ex_machine_on(room):
                if lvl <= 3:
                    ex_log("Makinenin gürültüsü sesini örtüyor.")
                    return
                lvl -= 2
            noises.append((room, lvl, t))
            ex["noise_total"] += lvl

        if kind == "move":
            dest = action[1]
            ex["prev"] = here
            ex["room"] = dest
            make_noise(dest, ACTION_NOISE["move"])
            sfx("footsteps")
        elif kind == "run":
            dest = action[1]
            path = ex_path(here, dest)
            ex["prev"] = path[-2] if len(path) > 1 else here
            for r in path:
                make_noise(r, ACTION_NOISE["run"])
                if r not in ex["visited"]:
                    ex["visited"].append(r)
            ex["room"] = dest
            stress(4)
            sfx("footsteps")
            ex_log("Koştun. Adımların koridorlarda yankılandı.")
        elif kind == "listen":
            ex["listen"] = True
            store.st_listens += 1
            ex_log("Nefesini tuttun ve dinledin.")
        elif kind == "search":
            pil = max(0, pil - SEARCH_COST)
            store.st_searches += 1
            noises.append((here, 3, "light"))
            sfx("flashlight")
            r = M["rooms"][here]
            if here not in ex["searched"]:
                ex["searched"].append(here)
            found = False
            if r.get("loot") and ("loot:" + here) not in ex["flags"]:
                ex["flags"].append("loot:" + here)
                ex_give(r["loot"])
                found = True
            if r.get("clue") and r["clue"][0] not in ex["flags"]:
                ex["flags"].append(r["clue"][0])
                ex_log(r["clue"][1])
                sfx("notify")
                found = True
            if r.get("doc") and ("doc:" + r["doc"]) not in ex["flags"]:
                ex["flags"].append("doc:" + r["doc"])
                isnew = find_doc(r["doc"])
                ex_log("Bir belge buldun: %s" % DOC_INFO[r["doc"]][1].capitalize() if isnew else "Bu belgeyi daha önce okumuştun.")
                if isnew:
                    ex["newdoc"] = r["doc"]
                found = True
            if not found:
                ex_log("Fener ışığında işe yarar bir şey yok.")
        elif kind == "throw":
            sise -= 1
            store.st_bottles += 1
            make_noise(action[1], ACTION_NOISE["throw"])
            sfx("bottle")
            ex_log("Şişe %s yönünde kırıldı." % M["rooms"][action[1]]["name"])
        elif kind == "decoy":
            kaydedici -= 1
            make_noise(action[1], ACTION_NOISE["decoy"])
            ex["lure"][action[1]] = 2
            sfx("whisper")
            ex_log("Kaydedici %s içinde çalıyor: senin sesin." % M["rooms"][action[1]]["name"])
        elif kind == "hide":
            ex["hidden"] = True
            ex_log("Saklandın. Kıpırdamadan bekliyorsun.")
        elif kind == "shoot":
            t = ex_shoot_target()
            if mermi > 0:
                mermi -= 1
                store.st_shots += 1
                sfx("gunshot")
                make_noise(here, ACTION_NOISE["shoot"])
                if t is None:
                    ex_log("Karanlığa ateş ettin. Hiçbir şey yok.")
                elif THREAT_INFO[t["type"]]["killable"]:
                    t["alive"] = False
                    store.kirpinti_vuruldu += 1
                    ex_log("Tek atış. %s yere yığıldı." % THREAT_INFO[t["type"]]["name"].capitalize())
                else:
                    ex_log("Mermi %s üzerinde hiçbir iz bırakmadı." % THREAT_INFO[t["type"]]["name"])
                    stress(8)
        elif kind == "resonance":
            t = ex_shoot_target()
            rezonans -= 1
            sfx("resonance_shot")
            if t is not None:
                t["stun"] = 4
                t["target"] = None
                ex_log("Rezonans Kesici! %s sarsıldı, birkaç tur hareket edemez." % THREAT_INFO[t["type"]]["name"])
        elif kind == "heal":
            ilkyardim -= 1
            saglik = min(ex_max_hp(), saglik + 1)
            ex_log("Yarayı sardın. Kendini biraz daha iyi hissediyorsun.")
        elif kind == "battery":
            yedek_pil -= 1
            pil = 100
            ex_log("Yedek pili taktın. Işık yeniden beyaz.")
        elif kind == "use":
            u = M["rooms"][here]["use"]
            if u["type"] == "lure":
                ex["lure"][here] = u.get("turns", 3)
                sfx("fan")
                ex_log(u.get("log", "Makine çalışmaya başladı."))
            elif u["type"] == "block":
                for a, b in u["links"]:
                    ex["blocked"][link_key(a, b)] = u.get("turns", 5)
                sfx("door_slam")
                ex_log(u.get("log", "Sürgüyü indirdin."))
                make_noise(here, 2)
        elif kind == "wait":
            ex_log("Bekledin.")

        if ex["room"] not in ex["visited"]:
            ex["visited"].append(ex["room"])
        ex["last_noise"] = noises[0] if noises else None

        ## Hedefe ulaşıldı mı?
        if ex["room"] == M["goal"] and ex_requirements_met():
            return "win"
        if ex["room"] == M["goal"] and not ex_requirements_met():
            ex_log(M.get("require_log", "Henüz gidemezsin; bir şey eksik."))

        ## Tur ilerler
        ex["turn"] += 1
        for k in list(ex["blocked"].keys()):
            ex["blocked"][k] -= 1
            if ex["blocked"][k] <= 0:
                del ex["blocked"][k]
                ex_log("Bir sürgü yeniden açıldı.")
        for r in list(ex["lure"].keys()):
            noises.append((r, 5, "sound"))
            ex["lure"][r] -= 1
            if ex["lure"][r] <= 0:
                del ex["lure"][r]

        if kind in ("move", "run"):
            res = ex_encounter()
            if res:
                return res
        res = ex_threats_move(noises)
        if res:
            return res

        ## Oda olayı
        ev = M["rooms"][ex["room"]].get("event")
        if ev and ev not in ex["events_done"]:
            ex["events_done"].append(ev)
            return ("event", ev)
        return None

    def ex_give(item):
        global pil, mermi, sise, ilkyardim, kaydedici, yedek_pil
        if item == "pil":
            yedek_pil += 1
        elif item == "sise":
            sise += 1
        elif item == "ilkyardim":
            ilkyardim += 1
        elif item == "mermi":
            mermi += 2
        elif item == "kaydedici":
            kaydedici += 1
        ex_log("Buldun: %s." % LOOT_INFO[item][0])
        sfx("notify")

    def ex_threats_move(noises):
        global saglik
        slow = 1 if zorluk == "hikaye" else 0
        ex["pings"] = []
        for t in ex["threats"]:
            if not t["alive"]:
                continue
            info = THREAT_INFO[t["type"]]
            ## Duyma
            best = None
            for room, lvl, kind in noises:
                if kind == "light" and not info["light"]:
                    continue
                eff = lvl + info["hear"] + (2 if kind == "light" else 0) + (1 if zorluk == "kabus" else 0)
                d = ex_dist(t["room"], room, t["type"])
                score = eff - d
                if score >= 1 and (best is None or score > best[0]):
                    best = (score, room)
            if t.get("chase") and ex_dist(t["room"], ex["room"], t["type"]) <= 4:
                best = (9, ex["room"])
            if best:
                if t["target"] != best[1]:
                    t["target"] = best[1]
                    if ex_dist(ex["room"], t["room"]) <= 2 and not t.get("chase"):
                        ex_log("Bir şey sese doğru döndü.")
            ## Hareket
            if t["stun"] > 0:
                t["stun"] -= 1
                continue
            speed = info["speed"] + slow
            if ex["turn"] % speed != 0:
                continue
            for _ in range(info["steps"]):
                if t["target"]:
                    if t["room"] == t["target"]:
                        t["target"] = None
                    else:
                        p = ex_path(t["room"], t["target"], t["type"])
                        if p:
                            t["room"] = p[0]
                        else:
                            t["target"] = None
                elif t["patrol"]:
                    nxt = t["patrol"][(t["pi"] + 1) % len(t["patrol"])]
                    p = ex_path(t["room"], nxt, t["type"])
                    if p:
                        t["room"] = p[0]
                    if t["room"] == nxt:
                        t["pi"] = (t["pi"] + 1) % len(t["patrol"])
                else:
                    ns = ex_neighbors(t["room"], t["type"])
                    if ns and renpy.random.random() < 0.5:
                        t["room"] = renpy.random.choice(ns)
                if t["room"] == ex["room"]:
                    break

        res = ex_encounter()
        if res:
            return res

        ## Duyulan sesler (görünmez tehditler için ses halkası)
        ex_update_pings()
        return None

    def ex_encounter():
        global saglik
        for t in ex["threats"]:
            if not t["alive"] or t["room"] != ex["room"] or t["stun"] > 0:
                continue
            if ex["hidden"]:
                ex_log("%s odaya girdi... ve seni görmeden geçti." % THREAT_INFO[t["type"]]["name"])
                stress(10)
                continue
            info = THREAT_INFO[t["type"]]
            saglik -= info["dmg"]
            ex["damage"] += info["dmg"]
            ex["detected"] = True
            stress(12)
            sfx("growl")
            ex["hit"] = t["type"]
            store.st_caught += 1
            if saglik <= 0:
                return "dead"
            ex_log("%s sana saldırdı! Geri kaçtın." % info["name"])
            t["stun"] = 1
            t["target"] = None
            if ex["prev"] and ex["prev"] != ex["room"]:
                ex["room"], ex["prev"] = ex["prev"], ex["room"]
        return None

    def ex_update_pings():
        ex["pings"] = []
        for t in ex["threats"]:
            if not t["alive"]:
                continue
            d = ex_dist(ex["room"], t["room"])
            loud = 2 if t["type"] == "nobetci" else 1
            if 1 <= d <= loud:
                ex["pings"].append(t["room"])
                if d == 1:
                    stress(2)
        ## Güvende geçen tur nabzı düşürür (gerilim eğrisi)
        if ex_nearest() >= 3 and not ex["hit"]:
            stress(-2)

    def ex_visible(t):
        """Tehdit oyuncuya görünür mü? Aynı oda, komşu oda + dinleme, ya da 2 oda + dinleme."""
        if not t["alive"]:
            return False
        d = ex_dist(ex["room"], t["room"])
        if d == 0:
            return True
        if ex["listen"] and d <= 2:
            return True
        return False

    def ex_stars():
        M = ex_map()
        s = 3
        if ex["damage"] > 0:
            s -= 1
        if ex["turn"] > M.get("par", 10):
            s -= 1
        if ex["detected"] and ex["damage"] == 0:
            s -= 0
        return max(1, s)

    def ex_finish():
        st = ex_stars()
        best = persistent.map_stars.get(ex["id"], 0)
        if st > best:
            persistent.map_stars[ex["id"]] = st
        if st == 3 and not ex["detected"]:
            unlock("golge")
        if len(persistent.map_stars) >= len(MAPS) and all(v >= 3 for v in persistent.map_stars.values()):
            unlock("stratejist")
        if ex_map().get("win_note"):
            add_note(ex_map()["win_note"])
        return st

    ## --- Otomatik test oyuncusu ----------------------------------------------

    def ex_auto_action():
        M = ex_map()
        here = ex["room"]
        if ex_unsearched_here() and pil >= SEARCH_COST:
            return ("search",)
        # bir tehdit komşudaysa ve şişe varsa uzağa at
        for t in ex["threats"]:
            if t["alive"] and ex_dist(here, t["room"]) == 1:
                if THREAT_INFO[t["type"]]["killable"] and mermi > 0:
                    return ("shoot",)
                if sise > 0:
                    far = ex_throw_targets()
                    far.sort(key=lambda r: -ex_dist(r, here))
                    if far:
                        return ("throw", far[0])
                if M["rooms"][here].get("hide"):
                    return ("hide",)
        near = any(t["alive"] and ex_dist(here, t["room"]) <= 2 for t in ex["threats"])
        if ex_room_use() and near:
            return ("use",)
        if renpy.random.random() < 0.1:
            return ("listen",)
        # hedef: eksik gereksinimler, sonra çıkış
        targets = []
        if not ex_requirements_met():
            for rid, r in M["rooms"].items():
                if r.get("clue") and r["clue"][0] in M.get("require", []) and r["clue"][0] not in ex["flags"]:
                    targets.append(rid)
                if r.get("event") and r.get("sets") in M.get("require", []) and r["event"] not in ex["events_done"]:
                    targets.append(rid)
        if not targets:
            targets = [M["goal"]]
        targets.sort(key=lambda r: ex_dist(here, r))
        p = ex_path(here, targets[0])
        if p:
            return ("move", p[0])
        return ("wait",)


## Ekran öğeleri ##############################################################

init python:

    class MapCanvas(renpy.Displayable):
        """Izgara ve oda bağlantılarını çizer (mavi kopya görünümü)."""

        def __init__(self, mid, theme, blocked, visited, reach, **kw):
            super(MapCanvas, self).__init__(**kw)
            self.mid = mid
            self.theme = theme
            self.blocked = blocked
            self.visited = visited
            self.reach = reach

        def render(self, width, height, st, at):
            r = renpy.Render(1280, 720)
            c = r.canvas()
            grid = (22, 34, 44, 255)
            for x in range(0, 1280, 32):
                c.line(grid, (x, 0), (x, 720), 1)
            for y in range(0, 720, 32):
                c.line(grid, (0, y), (1280, y), 1)
            M = MAPS[self.mid]
            th = renpy.easy.color(self.theme)
            base = (int(th.rgb[0] * 255 * 0.45), int(th.rgb[1] * 255 * 0.45), int(th.rgb[2] * 255 * 0.45), 255)
            lit = (int(th.rgb[0] * 255), int(th.rgb[1] * 255), int(th.rgb[2] * 255), 255)
            for l in M["links"]:
                a, b = l[0], l[1]
                kind = l[2] if len(l) > 2 else ""
                pa = ex_pos(M, a)
                pb = ex_pos(M, b)
                key = link_key(a, b)
                if key in self.blocked:
                    col = (190, 50, 40, 255)
                elif (a in self.reach and b in self.reach):
                    col = lit
                else:
                    col = base
                if kind == "vent":
                    # kesikli çizgi: havalandırma
                    n = 14
                    for i in range(n):
                        if i % 2 == 0:
                            t0, t1 = i / float(n), (i + 1) / float(n)
                            c.line(col, (int(pa[0] + (pb[0] - pa[0]) * t0), int(pa[1] + (pb[1] - pa[1]) * t0)),
                                   (int(pa[0] + (pb[0] - pa[0]) * t1), int(pa[1] + (pb[1] - pa[1]) * t1)), 2)
                else:
                    c.line(col, (int(pa[0]), int(pa[1])), (int(pb[0]), int(pb[1])), 3)
            return r

        def visit(self):
            return []

transform ping_ring:
    subpixel True
    xanchor 0.5 yanchor 0.5
    zoom 0.25 alpha 0.9
    linear 1.3 zoom 1.1 alpha 0.0
    repeat

transform noise_ring(z):
    subpixel True
    xanchor 0.5 yanchor 0.5
    zoom 0.2 alpha 0.8
    linear 0.9 zoom z alpha 0.0

transform token_pulse:
    xanchor 0.5 yanchor 0.5
    zoom 1.0
    block:
        ease 0.8 zoom 1.18
        ease 0.8 zoom 1.0
        repeat

transform hit_flash:
    alpha 0.55
    linear 0.6 alpha 0.0

transform threat_shake:
    xanchor 0.5 yanchor 0.5
    block:
        linear 0.08 xoffset 2
        linear 0.08 xoffset -2
        repeat

style ex_text is default:
    font "DejaVuSans.ttf"
    size 15
    color "#cfc9bd"

style ex_head is default:
    font "fonts/Oswald-Medium.ttf"
    size 15
    color "#8a857c"
    kerning 2

style ex_btn is default:
    xfill True
    padding (10, 7, 10, 7)
    idle_background Solid("#121a21")
    hover_background Solid("#24323d")
    selected_background Solid("#3a2f18")
    insensitive_background Solid("#0c1014")
    hover_sound "audio/sfx/ui_hover.ogg"

style ex_btn_text is default:
    font "fonts/Oswald-Medium.ttf"
    size 16
    idle_color "#d8d2c6"
    hover_color "#ffffff"
    selected_color "#e8d08a"
    insensitive_color "#3a3f44"
    kerning 1


screen explore_map():
    modal True
    zorder 10
    default mode = "move"
    default hover = None

    $ M = ex_map()
    $ theme = M.get("theme", "#c8a24a")
    $ here = ex["room"]
    $ adj = ex_neighbors(here)
    $ runs = ex_run_targets() if mode == "run" else []
    $ throws = ex_throw_targets(2 if mode == "throw" else 3) if mode in ("throw", "decoy") else []
    $ reach = set(adj + [here])

    ## Arka plan
    add Solid("#05080b")
    add ("bg " + M["bg"]) alpha 0.16
    add MapCanvas(ex["id"], theme, ex["blocked"], ex["visited"], reach)
    add "fx_vignette" alpha 0.7

    ## Başlık şeridi
    frame:
        xpos 0 ypos 0 xsize 900 ysize 70
        background Solid("#05080bcc")
        padding (28, 12, 20, 8)
        vbox:
            spacing 0
            text M["title"] font "fonts/Oswald-SemiBold.ttf" size 30 color theme kerning 3
            text M["goal_text"] style "ex_text" size 15 color "#a9a295"

    ## Odalar
    for rid, r in M["rooms"].items():
        $ x, y = ex_pos(M, rid)
        $ is_here = (rid == here)
        $ can_move = (mode == "move" and rid in adj)
        $ can_run = (mode == "run" and rid in runs)
        $ can_throw = (mode in ("throw", "decoy") and rid in throws)
        $ active = can_move or can_run or can_throw
        $ known = rid in ex["visited"] or rid in adj
        $ searched = rid in ex["searched"]
        $ bcol = theme if is_here else ("#e8d08a" if active and mode == "move" else ("#d0d8e0" if can_run else ("#d06050" if can_throw else "#2c3a46")))
        button:
            pos (x, y)
            anchor (0.5, 0.5)
            xysize (150, 54)
            background Frame(Solid(bcol), 0, 0)
            padding (2, 2, 2, 2)
            if can_move:
                action Return(("move", rid))
            elif can_run:
                action Return(("run", rid))
            elif can_throw:
                action [SetScreenVariable("mode", "move"), Return((mode, rid))]
            else:
                action NullAction()
            hovered SetScreenVariable("hover", rid)
            unhovered SetScreenVariable("hover", None)
            frame:
                xfill True
                yfill True
                background Solid("#0c141b" if not is_here else "#1a1810")
                padding (8, 4, 6, 4)
                vbox:
                    yalign 0.5
                    spacing 0
                    text r["name"]:
                        font "fonts/Oswald-Medium.ttf"
                        size 15
                        color ("#f0e6c8" if is_here else ("#cfc9bd" if known else "#6a737b"))
                        kerning 1
                    hbox:
                        spacing 6
                        if rid == M["goal"]:
                            text "⚑ HEDEF" size 11 color "#e8d08a"
                        if r.get("hide"):
                            text "▣ saklan" size 11 color "#7aa0c0"
                        if r.get("mask"):
                            text "≋ gürültü" size 11 color "#a09070"
                        if r.get("use"):
                            text "⚙ " + r["use"]["label"] size 11 color "#9ec0a0"
                        if r.get("event") and r["event"] not in ex["events_done"]:
                            text "◆" size 11 color "#d58aa0"
                        if searched:
                            text "✓ arandı" size 11 color "#55605a"

    ## Ses halkaları (görünmeyen tehditler)
    for pr in ex["pings"]:
        $ px, py = ex_pos(M, pr)
        add Transform("gui/map/ring.png", matrixcolor=TintMatrix("#ff3a2a")) pos (px, py) at ping_ring
        text "?" pos (px + 62, py - 30) anchor (0.5, 0.5) size 20 color "#ff6a5a" font "fonts/Oswald-SemiBold.ttf"

    ## Görünen tehditler
    for t in ex["threats"]:
        if ex_visible(t):
            $ tx, ty = ex_pos(M, t["room"])
            add Transform("gui/map/dot.png", matrixcolor=TintMatrix("#ff2a1a")) pos (tx + 58, ty + 22) at token_pulse
            text THREAT_INFO[t["type"]]["name"] pos (tx + 58, ty + 46) anchor (0.5, 0.0) size 12 color "#ff7a6a" font "fonts/Oswald-Medium.ttf" kerning 2
            if ex["listen"] and t["target"] and t["target"] in M["rooms"]:
                $ gx, gy = ex_pos(M, t["target"])
                text "◎" pos (gx - 62, gy - 26) anchor (0.5, 0.5) size 22 color "#ff5a4a"

    ## Son gürültü dalgası
    if ex["last_noise"]:
        $ nr, nl, nk = ex["last_noise"]
        $ nx, ny = ex_pos(M, nr)
        add Transform("gui/map/ring.png", matrixcolor=TintMatrix("#e8d08a" if nk == "sound" else "#ffffff")) pos (nx, ny) at noise_ring(0.4 + nl * 0.35)

    ## Oyuncu
    $ hx, hy = ex_pos(M, here)
    add Transform("gui/map/dot.png", matrixcolor=TintMatrix(theme)) pos (hx - 58, hy + 22) at token_pulse
    if ex["hidden"]:
        text "SAKLANIYOR" pos (hx, hy + 34) anchor (0.5, 0.0) size 11 color "#7aa0c0" font "fonts/Oswald-Medium.ttf" kerning 2

    ## Oda bilgisi (üzerine gelince)
    if hover:
        $ hr = M["rooms"][hover]
        frame:
            xpos 24 ypos 650
            xmaximum 860
            background Solid("#05080bdd")
            padding (14, 8, 14, 8)
            hbox:
                spacing 12
                text hr["name"] font "fonts/Oswald-Medium.ttf" size 17 color "#e8d08a"
                text hr.get("desc", "") style "ex_text" size 15 yalign 0.5

    ## Saldırı anı: kırmızı parlama
    if ex.get("hit"):
        add Solid("#a00000") at hit_flash

    ## Sağ panel
    use explore_panel(mode)

    if autotest_mode:
        timer 0.03 action Return(ex_auto_action())


screen explore_panel(mode):
    $ M = ex_map()
    $ theme = M.get("theme", "#c8a24a")
    $ here = ex["room"]
    $ room = M["rooms"][here]
    $ shoot_t = ex_shoot_target()

    frame:
        xpos 912 ypos 0 xsize 368 ysize 720
        background Solid("#080c10f2")
        padding (20, 18, 20, 14)

        vbox:
            spacing 8

            hbox:
                xfill True
                text ("TUR %d" % ex["turn"]) style "ex_head" size 18 color "#d8d2c6"
                $ hmax = ex_max_hp()
                hbox:
                    xalign 1.0
                    spacing 3
                    for i in range(hmax):
                        text ("♥" if i < saglik else "♡") size 22 color ("#d04a3a" if i < saglik else "#3a3030")

            ## Kaynaklar
            frame:
                xfill True
                background Solid("#0e141a")
                padding (12, 8, 12, 8)
                vbox:
                    spacing 4
                    hbox:
                        text "FENER" style "ex_head" min_width 92
                        bar value StaticValue(pil, 100) xsize 150 ysize 6 yalign 0.5 left_bar Solid("#e05040" if pil < 25 else theme) right_bar Solid("#1c2228")
                        text " [pil]%" style "ex_text" size 13
                    hbox:
                        $ dn = ex_nearest()
                        text "DEDEKTÖR" style "ex_head" min_width 92
                        hbox:
                            spacing 4
                            yalign 0.5
                            for i in range(3):
                                add Solid(("#ff4a3a" if dn <= 1 else ("#e8a040" if dn == 2 else "#c8b060")) if (4 - max(dn, 1)) > i else "#1c2228", xsize=40, ysize=6)
                        text ("  ÇOK YAKIN" if dn <= 1 else ("  YAKIN" if dn == 2 else ("  UZAKTA" if dn == 3 else "  SESSİZ"))) style "ex_text" size 12 color "#8a857c"
                    hbox:
                        text "NABIZ" style "ex_head" min_width 92
                        bar value StaticValue(gerginlik, 100) xsize 150 ysize 6 yalign 0.5 left_bar Solid("#c2302f") right_bar Solid("#1c2228")
                    null height 2
                    grid 3 2:
                        xfill True
                        spacing 4
                        text "● MERMİ [mermi]" style "ex_text" size 13
                        text "◍ ŞİŞE [sise]" style "ex_text" size 13
                        text "✚ YARDIM [ilkyardim]" style "ex_text" size 13
                        text "▮ PİL [yedek_pil]" style "ex_text" size 13
                        text "◉ KAYIT [kaydedici]" style "ex_text" size 13
                        if rezonans_alindi:
                            text "◆ REZ. [rezonans]" style "ex_text" size 13 color "#b0a8ff"
                        else:
                            null

            ## Bulunduğun oda
            text room["name"].upper() font "fonts/Oswald-SemiBold.ttf" size 20 color theme kerning 2
            text room.get("desc", "") style "ex_text" size 14 color "#a9a295"

            ## Hareket kipi
            hbox:
                spacing 6
                xfill True
                textbutton "YÜRÜ" style "ex_btn" text_style "ex_btn_text" xsize 106 action SetScreenVariable("mode", "move") selected (mode == "move")
                textbutton "KOŞ ×2" style "ex_btn" text_style "ex_btn_text" xsize 106 action SetScreenVariable("mode", "run") selected (mode == "run") sensitive ex_can_run()
                textbutton "İPTAL" style "ex_btn" text_style "ex_btn_text" xsize 106 action SetScreenVariable("mode", "move") sensitive (mode in ("throw", "decoy", "run"))

            if mode == "run":
                text "Beyaz çerçeveli odaya tıkla. Koşmak gürültülüdür (3)." style "ex_text" size 13 color "#d0d8e0"
            elif mode == "throw":
                text "Kırmızı çerçeveli odaya şişe at (gürültü 4)." style "ex_text" size 13 color "#d06050"
            elif mode == "decoy":
                text "Kaydediciyi bırakacağın odayı seç (2 tur, gürültü 5)." style "ex_text" size 13 color "#d06050"
            else:
                text "Sarı çerçeveli komşu odaya tıklayarak yürü (gürültü 1)." style "ex_text" size 13 color "#8a857c"

            ## Eylemler
            grid 2 5:
                xfill True
                spacing 6
                textbutton "DİNLE" style "ex_btn" text_style "ex_btn_text" action Return(("listen",))
                textbutton ("ARA  (-%d pil)" % SEARCH_COST) style "ex_btn" text_style "ex_btn_text" action Return(("search",)) sensitive (pil >= SEARCH_COST)
                textbutton "ŞİŞE AT" style "ex_btn" text_style "ex_btn_text" action SetScreenVariable("mode", "throw") sensitive (sise > 0) selected (mode == "throw")
                textbutton "KAYDEDİCİ" style "ex_btn" text_style "ex_btn_text" action SetScreenVariable("mode", "decoy") sensitive (kaydedici > 0) selected (mode == "decoy")
                textbutton "SAKLAN" style "ex_btn" text_style "ex_btn_text" action Return(("hide",)) sensitive bool(room.get("hide"))
                textbutton "ATEŞ ET" style "ex_btn" text_style "ex_btn_text" action Return(("shoot",)) sensitive (mermi > 0 and shoot_t is not None)
                textbutton "İLK YARDIM" style "ex_btn" text_style "ex_btn_text" action Return(("heal",)) sensitive (ilkyardim > 0 and saglik < ex_max_hp())
                textbutton "PİL TAK" style "ex_btn" text_style "ex_btn_text" action Return(("battery",)) sensitive (yedek_pil > 0 and pil < 70)
                if room.get("use"):
                    textbutton room["use"]["label"].upper() style "ex_btn" text_style "ex_btn_text" action Return(("use",))
                elif rezonans > 0 and shoot_t is not None and not THREAT_INFO[shoot_t["type"]]["killable"]:
                    textbutton "REZONANS" style "ex_btn" text_style "ex_btn_text" action Return(("resonance",))
                else:
                    textbutton "—" style "ex_btn" text_style "ex_btn_text" action NullAction() sensitive False
                textbutton "BEKLE" style "ex_btn" text_style "ex_btn_text" action Return(("wait",))

            ## Günlük
            frame:
                xfill True
                yfill True
                background Solid("#0b1015")
                padding (12, 8, 12, 8)
                vbox:
                    spacing 3
                    text "GÜNLÜK" style "ex_head" size 13
                    for i, line in enumerate(ex["log"]):
                        text line style "ex_text" size 13 color ("#e6e2da" if i == len(ex["log"]) - 1 else "#7c776f")


## Sonuç ekranları ############################################################

screen ex_caught():
    modal True
    zorder 120
    add Solid("#000000")
    add "fx_red"
    vbox:
        xalign 0.5
        yalign 0.45
        spacing 16
        text "YAKALANDIN" font "fonts/Oswald-SemiBold.ttf" size 72 color "#d04a3a" xalign 0.5 kerning 8
        text "Bu keşfi baştan dene. Kaynakların keşfin başındaki hâline döner." style "ex_text" size 18 xalign 0.5
        null height 20
        textbutton "TEKRAR DENE" style "ex_btn" text_style "ex_btn_text" xsize 360 xalign 0.5 action Return("retry")
        if (ex["fails"] >= 2 or zorluk == "hikaye") and zorluk != "kabus":
            textbutton "KEŞFİ ATLA (hikâyeye devam)" style "ex_btn" text_style "ex_btn_text" xsize 360 xalign 0.5 action Return("skip")
    if autotest_mode:
        timer 0.05 action Return("skip" if (ex["fails"] >= 2 and zorluk != "kabus") or ex["fails"] >= 5 else "retry")

screen ex_win(stars):
    modal True
    zorder 120
    add Solid("#05080b")
    $ M = ex_map()
    vbox:
        xalign 0.5
        yalign 0.42
        spacing 12
        text "KEŞİF TAMAMLANDI" font "fonts/Oswald-Medium.ttf" size 20 color "#8a857c" xalign 0.5 kerning 6
        text M["title"] font "fonts/Oswald-SemiBold.ttf" size 52 color M.get("theme", "#c8a24a") xalign 0.5 kerning 4
        null height 6
        hbox:
            xalign 0.5
            spacing 14
            for i in range(3):
                text ("★" if i < stars else "☆") size 56 color ("#e8d08a" if i < stars else "#333")
        null height 14
        grid 4 1:
            xalign 0.5
            spacing 46
            vbox:
                text str(ex["turn"]) size 34 color "#e6e2da" xalign 0.5
                text ("tur (hedef %d)" % M.get("par", 10)) style "ex_text" size 13 xalign 0.5 color "#8a857c"
            vbox:
                text str(ex["noise_total"]) size 34 color "#e6e2da" xalign 0.5
                text "toplam gürültü" style "ex_text" size 13 xalign 0.5 color "#8a857c"
            vbox:
                text str(min(ex["damage"], 9)) size 34 color ("#d04a3a" if ex["damage"] else "#e6e2da") xalign 0.5
                text "alınan hasar" style "ex_text" size 13 xalign 0.5 color "#8a857c"
            vbox:
                text ("Hayır" if not ex["detected"] else "Evet") size 34 color ("#9ec0a0" if not ex["detected"] else "#d06050") xalign 0.5
                text "fark edildin mi" style "ex_text" size 13 xalign 0.5 color "#8a857c"
        null height 30
        textbutton "DEVAM" style "ex_btn" text_style "ex_btn_text" xsize 240 xalign 0.5 action Return()
    if autotest_mode:
        timer 0.05 action Return()


## Ana döngü ##################################################################

label explore(mid):
    $ ex_begin(mid)
    $ ex_hud_prev = show_hud
    $ show_hud = False
    $ quick_menu = False
    $ ex_done = False
    window hide
    scene black
    if MAPS[mid].get("amb"):
        $ amb(MAPS[mid]["amb"])
    call tip("harita", "Keşif haritası", "Her eylem bir {b}tur{/b} harcar; sonra yaratıklar hareket eder. Sarı çerçeveli komşu odaya tıklayarak yürü.\n\n{b}Dinle{/b}: yakındaki yaratıkları ve nereye gittiklerini gösterir.  {b}Ara{/b}: fener pili harcayarak malzeme ve ipucu bulur.\n\nYaratıklar {b}sesle{/b} avlanır. Koşmak ve ateş etmek uzaktan duyulur; şişe atarak onları başka yöne çekebilirsin. Kırmızı {b}?{/b} halkası: bir şey duyuyorsun.")
    while not ex_done:
        $ ex_tracker()
        call screen explore_map
        $ renpy.block_rollback()
        $ ex_result = ex_act(_return)
        if ex.get("hit"):
            call jumpscare(ex["hit"])
        if ex.get("newdoc"):
            call screen doc_reader(ex["newdoc"], True)
        if ex_result == "win":
            $ ex_done = True
        elif ex_result == "dead":
            $ ex["fails"] += 1
            call screen ex_caught
            if _return == "retry":
                $ ex_begin(mid, retry=True)
            else:
                ## Atlanan keşifte zorunlu hikâye sahneleri yine de oynanır.
                $ ex_pending = [r["event"] for r in MAPS[mid]["rooms"].values() if r.get("event") and r.get("sets") in MAPS[mid].get("require", []) and r["event"] not in ex["events_done"]]
                while ex_pending:
                    $ ex_ev = ex_pending.pop(0)
                    $ ex["events_done"].append(ex_ev)
                    $ quick_menu = True
                    call expression ex_ev
                    $ quick_menu = False
                    scene black
                $ ex["room"] = MAPS[mid]["goal"]
                $ ex["damage"] = 9
                $ ex_done = True
        elif isinstance(ex_result, tuple) and ex_result[0] == "event":
            $ quick_menu = True
            call expression ex_result[1]
            $ quick_menu = False
            window hide
            scene black
            $ ev_flag = MAPS[mid]["rooms"][ex["room"]].get("sets")
            if ev_flag and ev_flag not in ex["flags"]:
                $ ex["flags"].append(ev_flag)
            if MAPS[mid].get("amb"):
                $ amb(MAPS[mid]["amb"])
    $ renpy.music.stop(channel="tracker", fadeout=0.5)
    $ stress(-15)
    $ ex_st = ex_finish() if ex["damage"] < 9 else 0
    call screen ex_win(ex_st)
    $ show_hud = ex_hud_prev
    $ quick_menu = True
    return

default ev_flag = None
default ex_pending = []
default ex_ev = None
default ex_st = 0


## TEÇHİZAT EKRANI (Bölüm 7) ##################################################
## Darkest Dungeon tarzı erzak seçimi: 4 yuvalık çanta.

init python:
    LOADOUT_ITEMS = [
        ("pil", "Yedek pil", "Feneri bir kez tamamen doldurur. ARA eylemi pil harcar.", "▮"),
        ("sise", "İki şişe", "Fırlatınca gürültü yapar; yaratıkları başka odaya çeker.", "◍"),
        ("ilkyardim", "İlk yardım", "Keşifte bir can yeniler.", "✚"),
        ("mermi", "Mermi kutusu", "+3 mermi. Yalnızca Kırpıntı'ya işler.", "●"),
        ("kaydedici", "Ses kaydedici", "Uzak bir odada 2 tur boyunca senin sesini çalar.", "◉"),
    ]
    LOADOUT_SLOTS = 4

    def loadout_apply(bag):
        global yedek_pil, sise, ilkyardim, mermi, kaydedici
        for it in bag:
            if it == "pil":
                yedek_pil += 1
            elif it == "sise":
                sise += 2
            elif it == "ilkyardim":
                ilkyardim += 1
            elif it == "mermi":
                mermi += 3
            elif it == "kaydedici":
                kaydedici += 1

    def loadout_auto():
        return [renpy.random.choice([i[0] for i in LOADOUT_ITEMS]) for _ in range(LOADOUT_SLOTS)]

screen loadout():
    modal True
    default bag = []
    add Solid("#06080a")
    add "bg town_morning" alpha 0.18
    add "fx_vignette"

    vbox:
        xpos 70 ypos 50
        spacing 4
        text "TEÇHİZAT" font "fonts/Oswald-SemiBold.ttf" size 44 color "#e6e2da" kerning 6
        text "Çantada yalnızca [LOADOUT_SLOTS] yer var. Aşağıda her şeyi alamazsın; ne alırsan ECHO'da onunla yaşayacaksın." style "ex_text" size 17 color "#a9a295"
        text "Sabit teçhizat: fener, telsiz, Bora'nın tabancası (6 mermi), 1 ilk yardım." style "ex_text" size 15 color "#77736b"

    ## Raf
    vbox:
        xpos 70 ypos 190
        spacing 10
        for iid, iname, idesc, icon in LOADOUT_ITEMS:
            $ cnt = bag.count(iid)
            button:
                xsize 640
                padding (18, 12, 18, 12)
                idle_background Solid("#10151a")
                hover_background Solid("#1e2830")
                insensitive_background Solid("#0a0d10")
                hover_sound "audio/sfx/ui_hover.ogg"
                activate_sound "audio/sfx/ui_select.ogg"
                sensitive (len(bag) < LOADOUT_SLOTS and cnt < 2)
                action SetScreenVariable("bag", bag + [iid])
                hbox:
                    spacing 18
                    text icon size 34 color "#c8a24a" yalign 0.5 min_width 40
                    vbox:
                        text iname font "fonts/Oswald-Medium.ttf" size 22 color "#e6e2da"
                        text idesc style "ex_text" size 15 color "#a9a295"
                    if cnt:
                        text "×[cnt]" font "fonts/Oswald-Medium.ttf" size 22 color "#e8d08a" yalign 0.5

    ## Çanta
    frame:
        xpos 780 ypos 190 xsize 430 ysize 420
        background Solid("#0c1014")
        padding (24, 20, 24, 20)
        vbox:
            spacing 12
            text "ÇANTA" style "ex_head" size 20
            for i in range(LOADOUT_SLOTS):
                if i < len(bag):
                    $ it = [x for x in LOADOUT_ITEMS if x[0] == bag[i]][0]
                    button:
                        xfill True
                        padding (14, 10, 14, 10)
                        idle_background Solid("#1a1810")
                        hover_background Solid("#3a1a14")
                        action SetScreenVariable("bag", bag[:i] + bag[i + 1:])
                        hbox:
                            spacing 12
                            text it[3] size 24 color "#c8a24a"
                            text it[1] font "fonts/Oswald-Medium.ttf" size 20 color "#e6e2da" yalign 0.5
                            text "çıkar ✕" style "ex_text" size 12 color "#77736b" yalign 0.5
                else:
                    frame:
                        xfill True
                        padding (14, 14, 14, 14)
                        background Solid("#0a0d10")
                        text "boş yuva" style "ex_text" size 14 color "#3a3f44"

    textbutton "HAZIRIM":
        xpos 780 ypos 630 xsize 430
        style "ex_btn" text_style "ex_btn_text"
        text_size 24
        text_xalign 0.5
        sensitive (len(bag) == LOADOUT_SLOTS)
        action Return(bag)

    if autotest_mode:
        timer 0.05 action Return(loadout_auto())
