## Karakterler ################################################################
##
## Renk kodu: her karakterin silüetindeki kenar ışığı ile isim rengi aynıdır.
## YANKI taklitleri soluk, italik ve yankı efektiyle gösterilir.

init -5 python:

    def echo_callback(event, interact=True, **kwargs):
        """Sahte (YANKI) seslerde, satır başlarken boğuk bir yankı çalar."""
        if event == "show_done":
            sfx("echo_voice")

    def radio_callback(event, interact=True, **kwargs):
        """Telsiz / telefon konuşmalarında kısa parazit."""
        if event == "show_done":
            sfx("radio")

define narrator = Character(None, what_color="#cfc9bd")
define thought = Character(None, what_italic=True, what_color="#a9a295")

define m = Character("Mert", color="#c8a24a", image="mert")
define a = Character("Aras", color="#6fa8dc", image="aras")
define dz = Character("Deniz", color="#e8e8e8", image="deniz")
define k = Character("Kemal", color="#9ec0a0", image="kemal")
define h = Character("Hakan", color="#7aa0c0", image="hakan")
define adr = Character("Adrian Voss", color="#d04a3a", image="adrian")
define du = Character("Duru", color="#d58aa0", image="duru")
define idl = Character("İdil", color="#b0a0e0", image="idil")
define rz = Character("Rıza", color="#a09070", image="riza")
define bo = Character("Bora", color="#c09060", image="bora")
define ka = Character("Kaan", color="#80b080", image="kaan")
define el = Character("Elif", color="#e0a070", image="elif")
define em = Character("Emir", color="#a0a0d0", image="emir")

## Telefon / telsiz varyantları
define dz_tel = Character("Deniz (telefonda)", kind=dz, what_color="#b8c8d8", callback=radio_callback)
define dz_kayit = Character("Deniz (eski kayıt)", kind=dz, what_color="#b8c8d8", callback=radio_callback)
define m_tel = Character("Mert (telsiz)", kind=m, callback=radio_callback)
define m_mesaj = Character("Mert (sesli mesaj)", kind=m, what_color="#c8b890")
define a_tel = Character("Aras (telsiz)", kind=a, what_color="#9ab8d0", callback=radio_callback)
define a_kam = Character("Aras (kamerada)", kind=a, what_color="#9ab8d0", callback=radio_callback)
define bo_tel = Character("Bora (telsiz)", kind=bo, callback=radio_callback)
define bo_fon = Character("Bora (telefon)", kind=bo, callback=radio_callback)
define du_tel = Character("Duru (telsiz)", kind=du, callback=radio_callback)
define k_kayit = Character("Kemal (eski kayıt)", kind=k, what_color="#a8c0b0", callback=radio_callback)
define k_arsiv = Character("Kemal (arşiv)", kind=k, what_color="#a8c0b0", callback=radio_callback)
define adr_arsiv = Character("Adrian (arşiv)", kind=adr, what_color="#c08070", callback=radio_callback)
define gorevli = Character("Görevli telsizi", color="#888888", callback=radio_callback)

## YANKI taklitleri
define uzak = Character("Uzak ses", color="#6f7880", what_italic=True, what_color="#8a949c", callback=echo_callback)
define dz_fake = Character("Deniz'in sesi", color="#6f7880", what_italic=True, what_color="#8a949c", callback=echo_callback)
define m_fake = Character("Mert'in sesi", color="#6f7880", what_italic=True, what_color="#8a949c", callback=echo_callback)
define k_baba_fake = Character("Babasının sesi", color="#6f7880", what_italic=True, what_color="#8a949c", callback=echo_callback)
define k_fake1 = Character("Kemal'in sesi", color="#6f7880", what_italic=True, what_color="#8a949c", callback=echo_callback)
define k_fake2 = Character("İkinci Kemal sesi", color="#6f7880", what_italic=True, what_color="#8a949c", callback=echo_callback)
define takl = Character("Taklitçi", color="#5a6066", what_italic=True, what_color="#7a848c", callback=echo_callback)
define kirp = Character("Kırpıntı", color="#5a6066", what_italic=True, what_color="#7a848c")

## Silüet görselleri ##########################################################

image mert:
    "images/char/mert.png"
    matrixcolor BrightnessMatrix(-0.08) * SaturationMatrix(0.6)
    alpha 0.82
image mert speaking = "images/char/mert.png"
image aras:
    "images/char/aras.png"
    matrixcolor BrightnessMatrix(-0.08) * SaturationMatrix(0.6)
    alpha 0.82
image aras speaking = "images/char/aras.png"
image deniz:
    "images/char/deniz.png"
    matrixcolor BrightnessMatrix(-0.08) * SaturationMatrix(0.6)
    alpha 0.82
image deniz speaking = "images/char/deniz.png"
image kemal:
    "images/char/kemal.png"
    matrixcolor BrightnessMatrix(-0.08) * SaturationMatrix(0.6)
    alpha 0.82
image kemal speaking = "images/char/kemal.png"
image hakan:
    "images/char/hakan.png"
    matrixcolor BrightnessMatrix(-0.08) * SaturationMatrix(0.6)
    alpha 0.82
image hakan speaking = "images/char/hakan.png"
image adrian:
    "images/char/adrian.png"
    matrixcolor BrightnessMatrix(-0.08) * SaturationMatrix(0.6)
    alpha 0.82
image adrian speaking = "images/char/adrian.png"
image duru:
    "images/char/duru.png"
    matrixcolor BrightnessMatrix(-0.08) * SaturationMatrix(0.6)
    alpha 0.82
image duru speaking = "images/char/duru.png"
image idil:
    "images/char/idil.png"
    matrixcolor BrightnessMatrix(-0.08) * SaturationMatrix(0.6)
    alpha 0.82
image idil speaking = "images/char/idil.png"
image riza:
    "images/char/riza.png"
    matrixcolor BrightnessMatrix(-0.08) * SaturationMatrix(0.6)
    alpha 0.82
image riza speaking = "images/char/riza.png"
image bora:
    "images/char/bora.png"
    matrixcolor BrightnessMatrix(-0.08) * SaturationMatrix(0.6)
    alpha 0.82
image bora speaking = "images/char/bora.png"
image kaan:
    "images/char/kaan.png"
    matrixcolor BrightnessMatrix(-0.08) * SaturationMatrix(0.6)
    alpha 0.82
image kaan speaking = "images/char/kaan.png"
image elif:
    "images/char/elif.png"
    matrixcolor BrightnessMatrix(-0.08) * SaturationMatrix(0.6)
    alpha 0.82
image elif speaking = "images/char/elif.png"
image emir:
    "images/char/emir.png"
    matrixcolor BrightnessMatrix(-0.08) * SaturationMatrix(0.6)
    alpha 0.82
image emir speaking = "images/char/emir.png"

image nobetci = "images/char/nobetci.png"
image surungen = "images/char/surungen.png"
image kirpinti = "images/char/kirpinti.png"
image taklitci = "images/char/taklitci.png"
