# donya.design: notes for Claude Code

Donya Yarahmadi's hand-coded portfolio (Product Designer). Plain HTML, CSS and JS, published with GitHub Pages from `main`.

## How the site is built
- `tools/build.py` holds **all the content** (home, case studies, testimonials, stats) as Python f-strings, and writes `index.html`.
  Edit content there, then run `python3 tools/build.py`. Don't hand-edit `index.html`; the next build overwrites it.
- Helpers in build.py: `h2`, `tldr`, `metrics`, `opts` (rejected/chosen), `figs` (`cls="one"` = full width), `proto` (prototype card), `process`, `iatree`, `sysflow`, `parts`, `case`.
- Hash routing in `main.js` (`views` map): `#education`, `#exam`, `#subjects`, `#books`, `#design-system`, `#connecta`, `#live-tv`.
- `style.css`: new rules are appended at the end and override earlier ones.
- Grid lines: only the outer left/right frame lines are always visible (`.gridlines`), with a "+" wherever two lines cross.
- Images live in `img/`. Case-study covers are dark/yellow (Aladia) or purple (Connecta) gradients with a laptop + phone mockup.

## Preview
`python3 -m http.server 8000` in this folder, then open http://localhost:8000.

## Working rules (from Donya)
- **Never push to `main` until Donya says "publish".** Work on a `draft` branch and show her the local preview first.
- Commit as Donya: `git -c user.name="Donya Yarahmadi" -c user.email="donyayarahmadi@outlook.com" commit ...`
- Aladia work is under NDA: no real Figma files, only the prepared screenshots and prototypes.
- Don't name the Connecta client contact on the site; say "the co-founders".
- Live TV Guide is a **concept project**. Never call it an interview test.
- Don't invent wireframes, research or numbers. Use only facts Donya gave. The Exam result is "42% faster exam creation with AI" (Maze, 6 → 3.5 min average).
- Don't claim she codes in HTML, CSS or React. She builds prototypes with AI tools (Claude Code, Cursor, Codex).
- Writing style: short, plain English sentences.

## Case study structure
Context → Problem → My role and goal → Process → Decisions (rejected vs chosen, with prototypes) → Result → What I learned.
