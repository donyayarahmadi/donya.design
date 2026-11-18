# donya.design — hand-coded portfolio

Plain HTML, CSS and JavaScript. No framework and no build step needed to run it.

- `index.html` — the whole site: home and the case studies (#education, #exam, #subjects, #books, #design-system, #connecta, #live-tv)
- `style.css` — all styling
- `main.js` — scroll effects, testimonials carousel, image lightbox, page switching
- `img/` — images
- `tools/build.py` — all the content; regenerates index.html (`python3 tools/build.py`)
- `CLAUDE.md` — how to work on this site with Claude Code

## Publish it
Drag this folder into Netlify Drop (app.netlify.com/drop), or push it to GitHub and connect Vercel or Netlify, then point donya.design at it.

## Sharper images
Screenshots were captured from the live site at about 1x. For crisp images, export each screen from Figma at 2x as JPG and replace the file with the same name in `img/`.
