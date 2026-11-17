"""Génère ics/<date>-<titre>.ics pour chaque événement à venir de index.html.
Usage : python3 tools/build_ics.py   (depuis la racine du dépôt ; nécessite playwright)"""
import os, pathlib, shutil
from playwright.sync_api import sync_playwright
root = pathlib.Path(__file__).resolve().parent.parent
out = root / 'ics'
shutil.rmtree(out, ignore_errors=True); out.mkdir()
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto((root / 'index.html').as_uri()); pg.wait_for_timeout(500)
    files = pg.evaluate("""() => EVENTS.filter(e=>(e.end?parse(e.end):parse(e.date))>=today)
        .map(e=>[icsKey(e), icsBody([e])])""")
    b.close()
for k, body in files:
    (out / f'{k}.ics').write_text(body, encoding='utf-8', newline='')
print(len(files), 'fichiers .ics')
