## Yalnızca ESIK_AUTOTEST ortam değişkeniyle etkin olan otomatik oynanış testi.
init 999 python:
    import os, sys
    if os.environ.get("ESIK_AUTOTEST"):
        config.auto_choice_delay = 0.02
        config.skip_delay = 1
        _seen_labels = []
        def _lc(name, abnormal):
            if not name.startswith("_"):
                sys.stdout.write("LABEL " + name + "\n"); sys.stdout.flush()
        config.label_callbacks.append(_lc)
        _shot_dir = os.environ.get("ESIK_SHOTS")
        _shot_n = [0]
        def _shot():
            _shot_n[0] += 1
            if _shot_dir and _shot_n[0] % int(os.environ.get("ESIK_SHOT_EVERY", "25")) == 0:
                renpy.screenshot(os.path.join(_shot_dir, "shot_%04d.png" % _shot_n[0]))
        config.start_interact_callbacks.append(_shot)

label autotest_run:
    python:
        import os
        if os.environ.get("ESIK_AUTOTEST"):
            preferences.skip_unseen = True
            preferences.skip_after_choices = True
            preferences.transitions = 0
            renpy.config.skipping = "fast" if os.environ.get("ESIK_FAST") == "1" else True
    if os.environ.get("ESIK_AUTOTEST"):
        $ suppress_overlay = False
        $ autotest_mode = True
        $ _game_menu_screen = "save"
        call start
        $ print("AUTOTEST_DONE notes=%d kanit=%d gerginlik=%d mermi=%d rezonans=%d final=%s" % (len(notes), len(kanit), gerginlik, mermi, rezonans, final_yontem))
        $ renpy.quit()
    return
