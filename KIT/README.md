# RESET — logo kit

Built by `pipeline/build_kit.py` from the 5316px master. Rerun it to rebuild
everything after a palette change. The drawing is never touched; the script
only colours it.

Treatment: bone lines, the iris lit from an amber core to an ember rim with a
two-stage glow, feathers running bone → sand → ember at the tips. Ground is
`#0B0A08` with a faint ember vignette on square formats.

| folder | what | use |
|---|---|---|
| `01_masters_transparent/` | full, eye+wordmark, eye, wordmark · 4096/2048/1024/512 · PNG alpha | drop onto anything |
| `02_on_ground/` | the same on the ground, square · 2048/1080/512 | posts, hero images |
| `03_avatars/` | eye only, circle-safe · 1080 → 180 | any profile picture |
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

Favicons use the eye with no glow so the strokes stay crisp at 16px.
