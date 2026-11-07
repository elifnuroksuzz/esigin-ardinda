## EŞİĞİN ARDINDA — ana akış ##################################################
##
## Her bölüm "chNN" adlı bir label'dır ve sonunda "return" eder.
## start, bölümleri sırayla çağırır. Bölüm Seç ekranı "sel_NN" label'ları
## üzerinden istenen bölümden başlatır.

label start:
    $ chapter_cursor = 1
    jump main_flow

label main_flow:
    while chapter_cursor <= len(CHAPTERS):
        call expression chapter_label(chapter_cursor)
        $ chapter_cursor += 1
    $ persistent.completed = True
    return

## Bölüm Seç girişleri
label sel_01:
    $ setup_for(1)
    jump main_flow
label sel_02:
    $ setup_for(2)
    jump main_flow
label sel_03:
    $ setup_for(3)
    jump main_flow
label sel_04:
    $ setup_for(4)
    jump main_flow
label sel_05:
    $ setup_for(5)
    jump main_flow
label sel_06:
    $ setup_for(6)
    jump main_flow
label sel_07:
    $ setup_for(7)
    jump main_flow
label sel_08:
    $ setup_for(8)
    jump main_flow
label sel_09:
    $ setup_for(9)
    jump main_flow
label sel_10:
    $ setup_for(10)
    jump main_flow
label sel_11:
    $ setup_for(11)
    jump main_flow
label sel_12:
    $ setup_for(12)
    jump main_flow
label sel_13:
    $ setup_for(13)
    jump main_flow
label sel_14:
    $ setup_for(14)
    jump main_flow
label sel_15:
    $ setup_for(15)
    jump main_flow
label sel_16:
    $ setup_for(16)
    jump main_flow
label sel_17:
    $ setup_for(17)
    jump main_flow
label sel_18:
    $ setup_for(18)
    jump main_flow
