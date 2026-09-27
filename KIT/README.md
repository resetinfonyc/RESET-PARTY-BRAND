# RESET — logo kit

Built by `pipeline/build_kit.py` from the 5316px master. Rerun it to rebuild
everything after a palette change. The drawing is never touched; the script
only colours it.

**The logo is the full lockup: the word RESET, the eye, the feathers. It is
never cropped.** Every file in this kit carries all three, down to the 16px
favicon. (Andre, 2026-09-26.)

Treatment: bone lines, the iris lit from an amber core to an ember rim with a
two-stage glow, feathers running bone → sand → ember at the tips. Ground is
`#0B0A08` with a faint ember vignette on square formats.

| folder | what | use |
|---|---|---|
| `01_masters_transparent/` | the logo · 4096/2048/1024/512/256 · PNG alpha | drop onto anything |
| `02_on_ground/` | the same on the ground, square · 2048/1080/512 | posts, hero images |
| `03_avatars/` | the logo sized to sit inside the circle crop · 1080 → 180 | any profile picture |
| `04_platforms/` | one file per platform slot, already at the right size | see below |
| `05_print_one_colour/` | black and white one-colour, 4096, plus the vector SVG | print, embroidery, stamps, laser |

## Platform slots

| platform | file | goes in |
|---|---|---|
| Instagram | `instagram/profile_1080` | profile picture |
| | `instagram/post_1080x1080`, `portrait_1080x1350`, `story_1080x1920` | the relaunch grid post / story |
| Facebook | `facebook/profile_720`, `cover_1640x624`, `event_cover_1920x1005` | page + events |
| X | `x/profile_400`, `header_1500x500` (mark right of centre, clear of the avatar) | |
| YouTube | `youtube/avatar_800`, `banner_2560x1440` (mark inside the TV-safe area) | |
| TikTok | `tiktok/profile_400` | |
| SoundCloud | `soundcloud/avatar_1000`, `banner_2480x520` (right of centre) | |
| Spotify | `spotify/profile_750`, `header_2660x1140` | artist / playlist |
| LinkedIn | `linkedin/profile_400`, `cover_1128x191` | |
| Partiful | `partiful/host_avatar_512`, `event_cover_1200x1200` | host account + standing cover |
| Web | `web/favicon.ico` (16/32/48), `favicon_*.png`, `apple_touch_180`, `icon_192`, `icon_512`, `og_image_1200x630` | link page |

Covers and banners sit on a New York skyline at night; posts, stories and
event covers sit on a crowd dancing under warm light. Both photos are pulled
to the palette (shadows to ground, lights to ember and amber), softened and
darkened behind the mark, with film grain. `04_platforms/_alternates/` has
the same slots on mirror balls, a backlit saxophone and the crowd, if a
platform wants a different mood. Photo credits in
`pipeline/assets/backgrounds/CREDITS.md`.

Profile pictures carry a thin ember ring at the edge of the circle crop and
a second pass of glow, so the mark reads lit even at 150px. Profile pictures and favicons stay
clean so the mark reads at small size.

`instagram/highlights/` has a cover for every existing highlight plus NEXT.

Favicons carry the full logo with no glow so the strokes stay as crisp as
16px allows. `web/icon_192` and `icon_512` are the ones browsers show most.
