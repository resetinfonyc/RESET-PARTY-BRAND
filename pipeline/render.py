#!/usr/bin/env python3
"""Render the RESET flyer at story, feed and square sizes.

    python3 render.py ../work/1018 1018

Edit the copy in reset_flyer.html first (ids: room, date, act1, act2, live1, foot).
Only the date, room and lineup change week to week.
"""
import os, sys, datetime, pathlib
from playwright.sync_api import sync_playwright
here=pathlib.Path(__file__).parent.resolve()
out=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else here/'../work/deliver').resolve(); out.mkdir(parents=True,exist_ok=True)
tag=sys.argv[2] if len(sys.argv)>2 else datetime.date.today().strftime('%m%d')
SIZES={'story':('',1080,1920),'feed_4x5':('feed',1080,1350),'square':('square',1080,1080)}
exe=os.environ.get('CHROME')  # set if playwright's own chromium is not installed
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
    for name,(cls,w,h) in SIZES.items():
        pg=b.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
        pg.goto(f'file://{here}/reset_flyer.html')
        if cls: pg.evaluate(f"document.getElementById('canvas').classList.add('{cls}')")
        pg.wait_for_timeout(300)
        f=out/f'reset_{tag}_{name}_{w}x{h}.png'; pg.locator('#canvas').screenshot(path=str(f)); print(f)
    b.close()
