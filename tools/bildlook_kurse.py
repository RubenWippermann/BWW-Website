#!/usr/bin/env python3
"""Bild-Look: 11 neue Kurs-Illustrationen (Entwürfe aus Koordinator/bildlook-entwuerfe-08-11/bww) freistellen, als WebP unter neuem Dateinamen (-v2) ablegen und in den Seiten ersetzen. Idempotent."""
import glob, os, re
from PIL import Image, ImageDraw, ImageFilter, ImageChops
R = os.path.expanduser('~/Claude/bww-neu-wt'); os.chdir(R)
SRC = os.path.expanduser('~/Claude/Koordinator/bildlook-entwuerfe-08-11/bww')
MAP = {'01-course-lk2': ('course-lk2', 'Lehrkraft erklärt vor einer Gruppe an der Tafel und lässt eine Lehrprobe üben'),
       '02-course-bsf': ('course-bsf', 'Betriebssanitäterin übt die Beatmung mit dem Beatmungsbeutel an einer Übungspuppe'),
       '03-course-bsa': ('course-bsa', 'Zwei Betriebssanitäter arbeiten mit Absaugpumpe und Sauerstoffgerät an einer Übungspuppe'),
       '04-course-eh-ausbildung': ('course-eh-ausbildung', 'Gruppe übt im Kreis die stabile Seitenlage, daneben ein offener Verbandkasten'),
       '05-course-eh-fortbildung': ('course-eh-fortbildung', 'Zwei Kolleginnen üben im Wechsel die Herzdruckmassage an einer Übungspuppe'),
       '06-course-baby-kind': ('course-baby-kind', 'Eltern üben an einer Säuglingspuppe Rückenschläge und Herzdruckmassage'),
       '07-course-bibe': ('course-bibe', 'Erzieherin und Lehrkraft üben im Flur einer Kita einen Knieverband'),
       '08-course-lk-san': ('course-lk-san', 'Lehrkraft erklärt Schulsanitätern die Versorgungsstufen an der Tafel'),
       '09-course-nft': ('course-nft', 'Behandlungsteam übt einen Notfall im Behandlungszimmer mit Notfalltasche und Pulsoximeter'),
       '10-dguv-calculator': ('dguv-calculator', 'Person zeigt auf einem Tablet den Rechner für den Bedarf an Ersthelfern'),
       '11-dguv-billing': ('dguv-billing', 'Mitarbeiterin prüft Unterlagen zur Abrechnung, auf der Mappe ein Euro-Zeichen mit Haken')}
def freistellen(im):
    im = im.convert('RGB'); W, H = im.size; mark = im.copy()
    for pt in [(0, 0), (W-1, 0), (0, H-1), (W-1, H-1), (W//2, 0), (W//2, H-1), (0, H//2), (W-1, H//2)]:
        if sum(mark.getpixel(pt)) > 740: ImageDraw.floodfill(mark, pt, (255, 0, 255), thresh=22)
    bg = Image.new('L', (W, H), 0); px = mark.load(); b = bg.load()
    for y in range(H):
        for x in range(W):
            if px[x, y] == (255, 0, 255): b[x, y] = 255
    fig = ImageChops.invert(bg).filter(ImageFilter.MinFilter(3))
    out = im.convert('RGBA'); out.putalpha(fig.filter(ImageFilter.GaussianBlur(0.8)))
    halo = fig.filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.GaussianBlur(1.2))
    white = Image.new('RGBA', (W, H), (255, 255, 255, 255)); white.putalpha(halo)
    c = Image.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, 0)), white); c = Image.alpha_composite(c, out)
    bb = c.getbbox(); return c.crop((max(0, bb[0]-6), max(0, bb[1]-6), min(W, bb[2]+6), min(H, bb[3]+6)))
pages = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('tools/')]
html = {f: open(f, encoding='utf8').read() for f in pages}
n_pages = 0
for key, (alt_old, alt) in MAP.items():
    neu = f'{alt_old}-v2.webp'; dst = f'media/illustrations/bww/{neu}'
    if not os.path.exists(dst):
        im = freistellen(Image.open(f'{SRC}/{key}.png')); w = 720; im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(dst, quality=86, method=6)
    w, h = Image.open(dst).size
    pat = re.compile(r'(<img[^>]*?)src="/media/illustrations/bww/' + re.escape(alt_old) + r'\.webp"([^>]*>)')
    for f in pages:
        def rep(m):
            tag = m.group(1) + f'src="/media/illustrations/bww/{neu}"' + m.group(2)
            tag = re.sub(r'width="\d+"', f'width="{w}"', tag, count=1); tag = re.sub(r'height="\d+"', f'height="{h}"', tag, count=1)
            return tag
        new = pat.sub(rep, html[f])
        if new != html[f]: html[f] = new; n_pages += 1
for f in pages:
    open(f, 'w', encoding='utf8').write(html[f])
print('Ersetzungen auf Seiten (Summe je Motiv):', n_pages)
