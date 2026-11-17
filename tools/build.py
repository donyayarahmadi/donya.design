#!/usr/bin/env python3
"""Builds site/index.html (home + 4 case studies, hash-routed) from the content below."""
from pathlib import Path
import re

OUT = Path(__file__).resolve().parent.parent / "index.html"

# ---------------------------------------------------------------- helpers
def opts(*items):
    rows = []
    for kind, title, text in items:
        tag = "Chosen" if kind == "yes" else "Rejected"
        rows.append(f'<div class="opt {kind}"><span class="tag">{tag}</span><div><b>{title}</b> {text}</div></div>')
    return '<div class="options">' + "".join(rows) + "</div>"

def figs(*items, cls=""):
    out = []
    for src, cap in items:
        alt = re.sub("<[^>]+>", "", cap).strip()
        out.append(f'<figure class="reveal"><div class="ph"><img src="img/{src}" alt="{alt}" loading="lazy"></div><figcaption>{cap}</figcaption></figure>')
    return f'<div class="figs {cls}">' + "".join(out) + "</div>"

def metrics(*items):
    out = []
    for num, text, note in items:
        n = f'<small>{note}</small>' if note else ""
        out.append(f'<div class="metric"><div class="num">{num}</div><p>{text}</p>{n}</div>')
    return '<div class="metrics reveal">' + "".join(out) + "</div>"


def flow(title, steps):
    """Auto-playing prototype walkthrough. steps: (img, caption, (x%, y%) of the next click or None)."""
    imgs = "".join(f'<img src="img/{im}" alt="{cap}" loading="lazy" class="{"on" if i == 0 else ""}">' for i, (im, cap, _) in enumerate(steps))
    data = "|".join(f'{cap}~{"" if hs is None else f"{hs[0]},{hs[1]}"}' for im, cap, hs in steps)
    segs = "".join("<i><b></b></i>" for _ in steps)
    return f'''<div class="flow reveal" data-steps="{data}">
  <div class="flow-head"><span class="flow-tag">PROTOTYPE</span><span class="flow-title">{title}</span><span class="flow-count">1 / {len(steps)}</span></div>
  <div class="flow-stage" role="img" aria-label="{title}">{imgs}<span class="tap"></span></div>
  <div class="flow-bar">{segs}</div>
  <div class="flow-foot"><p class="flow-cap"></p><div class="flow-ctl"><button class="fp" aria-label="Previous step">←</button><button class="fpp" aria-label="Pause">PAUSE</button><button class="fn" aria-label="Next step">→</button></div></div>
</div>'''


def proto(title, desc, thumb, url, tag="FIGMA PROTOTYPE"):
    return f'''<a class="proto reveal" href="{url}" target="_blank" rel="noopener">
  <div class="proto-thumb"><img src="img/{thumb}" alt="{title}" loading="lazy"><span class="proto-play">▶</span></div>
  <div class="proto-body"><span class="flow-tag">{tag}</span><h4>{title}</h4><p>{desc}</p><span class="proto-cta">Open the prototype ↗</span></div>
</a>'''


def process(*stages):
    """stages: (name, text) tuples."""
    items = "".join(f'<li><span class="pn">{i+1:02d}</span><b>{n}</b><p>{t}</p></li>' for i, (n, t) in enumerate(stages))
    return f'<div class="process reveal"><span class="kicker">How I worked</span><ol>{items}</ol></div>'

def chain(title, nodes, note=""):
    """Horizontal structure/flow diagram. nodes: (label, sub) tuples."""
    parts = []
    for i, (label, sub) in enumerate(nodes):
        if i: parts.append('<span class="ch-arrow">→</span>')
        parts.append(f'<div class="ch-node"><b>{label}</b>{f"<small>{sub}</small>" if sub else ""}</div>')
    n = f'<p class="ch-note">{note}</p>' if note else ""
    return f'<div class="diagram reveal"><span class="flow-tag">{title}</span><div class="chain">{"".join(parts)}</div>{n}</div>'

def hub(title, top, middle, bottom, note=""):
    """Tree diagram: one top node, a row of middle nodes, a chain of bottom nodes."""
    mid = "".join(f'<div class="ch-node"><b>{a}</b><small>{b}</small></div>' for a, b in middle)
    bot = '<span class="ch-arrow">→</span>'.join(f'<div class="ch-node"><b>{a}</b><small>{b}</small></div>' for a, b in bottom)
    n = f'<p class="ch-note">{note}</p>' if note else ""
    return f'''<div class="diagram reveal"><span class="flow-tag">{title}</span>
  <div class="tree"><div class="ch-node root"><b>{top[0]}</b><small>{top[1]}</small></div>
  <span class="ch-down">↓</span><div class="tier">{mid}</div>
  <span class="ch-down">↓ linked into</span><div class="chain">{bot}</div></div>{n}</div>'''

def research(method, rows, note=""):
    r = "".join(f'<tr><td>{a}</td><td>{b}</td><td class="after">{c}</td></tr>' for a, b, c in rows)
    n = f'<p class="ch-note">{note}</p>' if note else ""
    return f'<div class="research reveal"><span class="flow-tag">USABILITY TESTING</span><p class="rm">{method}</p><table><thead><tr><th>Measure</th><th>Before</th><th>After</th></tr></thead><tbody>{r}</tbody></table>{n}</div>'

def iatree(focus=None, note=None):
    def col(name, sub, groups, item, details):
        g = "".join(f"<li>{x}</li>" for x in groups)
        d = "".join(f"<li>{x}</li>" for x in details)
        cls = "" if not focus else (" focus" if name == focus else " dim")
        return f'''<div class="ia-col{cls}"><div class="ch-node lib"><b>{name}</b><small>{sub}</small></div>
<ul class="ia-groups">{g}</ul><div class="ch-node item"><b>{item[0]}</b><small>{item[1]}</small></div><ul class="ia-details">{d}</ul></div>'''
    cols = (col("Subject Areas", "one per organisation or teacher", ["My areas", "Shared areas"], ("Subject", "title, icon, colour"), ["Teachers assigned", "Study levels", "Linked books", "Linked exams"])
          + col("Book Libraries", "one per organisation or teacher", ["My libraries", "Shared libraries"], ("Book", "PDF, purchase link or written"), ["Details, filled by ISBN", "Cover from the first pages", "Subject and level", "Companion volumes"])
          + col("Exam Collections", "one per organisation or teacher", ["My collections", "Shared collections"], ("Exam", "one version, reused"), ["Questions, AI-assisted", "Written or oral", "Linked subject", "No date, no grading scale"]))
    return f'''<div class="diagram ia reveal"><span class="flow-tag">INFORMATION ARCHITECTURE{" · " + focus.upper() if focus else ""}</span>
<div class="ch-node root"><b>Education</b><small>one group in settings and navigation</small></div>
<span class="ch-down">↓</span>
<div class="ia-cols">{cols}</div>
<div class="ia-roles"><span>Same roles in all three</span><b>Owner</b><b>Curator</b><b>Editor</b><b>Viewer</b></div>
<span class="ch-down">↓ added to</span>
<div class="ia-use">
<div class="ch-node"><b>Course</b><small>subjects with a level · their teachers invited · books · exams with a date, rules and grading scale</small></div>
<span class="ch-arrow">→</span>
<div class="ch-node"><b>Lecture & live session</b><small>a subject · the book’s page range · an exam</small></div>
<span class="ch-arrow">→</span>
<div class="ch-node"><b>Student</b><small>sees only what’s assigned, already in the lecture</small></div>
</div>
<p class="ch-note">{note or "Content lives once, above the course. Courses and lectures only point to it, and decide how it is used."}{' <a class="ia-link" href="#education">See the full system in Education System →</a>' if focus else ""}</p></div>'''

def parts(*items):
    out = "".join(f'<a class="part reveal" href="#{slug}"><img src="img/{img}" alt="{t}" loading="lazy"><div><span class="pn">0{i+1}</span><b>{t}</b><p>{d}</p><span class="proto-cta">Read the case study →</span></div></a>' for i, (slug, t, d, img) in enumerate(items))
    return f'<div class="parts">{out}</div>'


def sysflow():
    def n(i, label, sub="", cls=""):
        return f'<div class="sf-n {cls}" data-n="{i}"><b>{label}</b>{f"<small>{sub}</small>" if sub else ""}</div>'
    def c(i, label):
        return f'<span class="sf-c" data-n="{i}">{label}</span>'
    def lib(lid, lname, mid, iid, iname, isub, chips):
        return f'''<div class="sf-col">{n(lid, lname, "", "lib")}{n(mid, "Members", "Owner · Curator · Editor · Viewer", "mem")}{n(iid, iname, isub)}<div class="sf-chips">{"".join(c(*x) for x in chips)}</div></div>'''
    diagram = f'''<div class="sf-map">
<div class="sf-row">{n("edu", "Education", "one place for teaching content", "root")}</div>
<div class="sf-ar">↓</div>
<div class="sf-cols">
{lib("sa", "Subject Area", "sam", "subj", "Subject", "created once", [("subj-b", "Books"), ("subj-f", "Files"), ("subj-l", "Study levels")])}
{lib("bl", "Book Library", "blm", "book", "Book", "created once", [("book-s", "Subject"), ("book-c", "Companion volumes")])}
{lib("ec", "Exam Collection", "ecm", "exam", "Exam template", "created once", [("exam-d", "Document editor"), ("exam-ai", "AI draft from subjects & books")])}
</div>
<div class="sf-ar">↓ added to</div>
<div class="sf-course">{n("course", "Course", "", "wide")}
<div class="sf-cols two">
<div class="sf-col">{n("live", "Live course")}<div class="sf-chips">{c("x-sch", "Scheduled exam")}{c("x-non", "Non-scheduled exam")}{c("x-oral", "Oral exam")}</div></div>
<div class="sf-col">{n("od", "On-demand course")}<div class="sf-chips">{c("x-non2", "Non-scheduled exam")}</div></div>
</div>
<div class="sf-chips center">{c("teach", "Teachers invited")}{c("link", "Linked subject comes along")}</div></div>
<div class="sf-ar">↓</div>
<div class="sf-cols three">{n("lecture", "Student · Lecture", "subject, books, files")}{n("room", "Student · Exam room", "in 100ms, camera on")}{n("proct", "Proctoring", "session recorded")}</div>
<div class="sf-ar">↓</div>
<div class="sf-row">{n("perf", "Performance", "results across courses and subjects", "root")}</div>
</div>'''
    steps = [
      ("Education", "One place, three libraries", "Under Education, an organisation creates a Subject Area, a Book Library and an Exam Collection. All teaching content starts here, outside any course.", "edu sa bl ec"),
      ("Education", "Invite members", "Each library has its own members, with the same four roles everywhere: Owner, Curator, Editor and Viewer.", "sa bl ec sam blm ecm"),
      ("Education", "Create a subject", "Inside a Subject Area, the subject is created once. Books, files and study levels are attached to it.", "sa subj subj-b subj-f subj-l"),
      ("Education", "Create a book", "Inside a Book Library, the book is created once. It gets a subject, and companion volumes can be added to it.", "bl book book-s book-c subj"),
      ("Education", "Create an exam template", "Inside an Exam Collection, the teacher writes the exam template in the document editor.", "ec exam exam-d"),
      ("Education", "Or let AI draft it", "The AI flow uses the subjects and books already on the platform to fetch the content and draft the exam. The teacher stays the author.", "exam exam-ai subj book"),
      ("Course", "Two kinds of course", "A course is either live or on demand. Both take subjects, books and exams from the libraries in the same way.", "course live od"),
      ("Course", "Add a subject", "Teachers aren’t invited in the Subject Area. When the subject is added to a course, its teachers are invited to that course.", "subj course teach"),
      ("Course", "Add a book", "If the book has a subject assigned, the subject is attached to the course along with it.", "book book-s course link"),
      ("Course", "Add an exam", "The same happens for exams: the exam brings its subject into the course.", "exam course link"),
      ("Course", "Exam types per course", "Live courses can have scheduled, non-scheduled and oral exams. On-demand courses have non-scheduled exams. All of them are added in the same way.", "course live od x-sch x-non x-oral x-non2"),
      ("Student", "In the lecture", "The student finds the subject, its books and files already in the lecture.", "lecture"),
      ("Student", "Scheduled exam", "Scheduled exams are held in 100ms with the camera on. If proctoring is on, the session is recorded.", "x-sch room proct"),
      ("Student", "Non-scheduled exam", "The student starts it from the course. Only when proctoring is on do they join a meeting room, where the session is recorded. Without proctoring, they simply take the exam.", "x-non x-non2 room proct"),
      ("Student", "Oral exam", "Oral exams run inside a live session.", "x-oral room"),
      ("Performance", "Performance", "After all of this, the performance module brings the results together for every student, course and subject.", "perf"),
    ]
    tabs, panels, phase = [], [], None
    for i, (ph, t, d, on) in enumerate(steps):
        if ph != phase:
            tabs.append(f'<span class="sf-ph">{ph}</span>'); phase = ph
        tabs.append(f'<button class="sf-dot{" on" if i == 0 else ""}" data-i="{i}" aria-label="Step {i+1}: {t}">{i+1:02d}</button>')
        panels.append(f'<div class="sf-step{" on" if i == 0 else ""}" data-on="{on}"><div class="ux-meta"><span class="ux-num">STEP {i+1:02d} / {len(steps)}</span><span class="ux-actor">{ph}</span></div><h4>{t}</h4><p>{d}</p></div>')
    return f'''<div class="sf reveal" tabindex="0" aria-label="Interactive system flow">
<div class="ux-head"><span class="flow-tag">SYSTEM FLOW · CLICK THROUGH</span></div>
<div class="sf-tabs">{"".join(tabs)}</div>
{diagram}
<div class="sf-foot"><div class="sf-steps">{"".join(panels)}</div>
<div class="ux-ctl"><button class="ux-prev" aria-label="Previous step">← Prev</button><span class="ux-count">1 / {len(steps)}</span><button class="ux-next" aria-label="Next step">Next →</button></div></div></div>'''

def tldr(summary, role, items):
    m = "".join(f'<div><b>{n}</b><span>{t}</span></div>' for n, t in items)
    return f'<div class="tldr reveal"><p class="tl-sum">{summary}</p><p class="tl-role">{role}</p><div class="tl-m">{m}</div></div>'

def arrow(a, b):
    return f'{a}<span class="arrow">→</span>{b}'

def h2(kicker, title):
    return f'<h2 class="reveal"><span class="kicker">{kicker}</span>{title}</h2>'

def case(slug, title, sub, cover, overview_img, overview, meta, body, nxt):
    meta_html = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in meta)
    nslug, ntitle, ntags, ncover = nxt
    return f'''
<section class="view" id="view-{slug}">
  <div class="frame">
    <header class="cs-hero">
      <div><span class="eyebrow"><a href="#work">Case studies</a></span><h1>{title}</h1></div>
      <p>{sub}</p>
    </header>
    <div class="rule"></div>
    <div class="cs-cover"><div class="media"><img src="img/{cover}" alt="{title} cover"></div></div>
    <div class="rule"></div>
    <div class="cs-overview">
      <div class="shot reveal"><img src="img/{overview_img}" alt="{title} main screen"></div>
      <div class="side">
        <span class="eyebrow">Overview</span>
        <p class="reveal" data-words>{overview}</p>
        <dl class="meta reveal d1">{meta_html}</dl>
      </div>
    </div>
    <div class="rule"></div>
    <article class="cs-body"><div class="prose">{body}</div></article>
    <div class="next"><div class="rule"></div>
      <a href="#{nslug}">
        <div><small>NEXT PROJECT</small><h3>{ntitle}</h3><p class="count" style="margin-top:12px">{ntags}</p></div>
        <div class="media"><img src="img/{ncover}" alt="{ntitle} cover" loading="lazy"></div>
      </a>
    </div>
  </div>
</section>'''

# ---------------------------------------------------------------- EXAM
exam_body = f'''
{tldr("Aladia had no way to run exams. I designed the whole system, from writing questions with AI to live proctoring and grading, so one exam works across courses with completely different grading rules.",
      "UI/UX designer, course domain · Aladia · 2024–2026",
      [(arrow("6", "3.5"), "minutes to create an exam (Maze usability test)"), ("1", "version of each exam, reused across every course"), ("40", "students supervised by one teacher in one view")])}

{h2("01 — Context", "Schools, universities and companies on one platform")}
<p>Aladia is an e-learning platform used by very different institutions. An Italian liceo grades from 18 to 30, a corporate course from 0 to 100. Teachers needed to create exams, run them with supervision and grade them, all inside the platform.</p>

{h2("02 — The problem", "Exams didn’t exist, and the obvious design would break")}
<ul>
<li><strong>Teachers</strong> reuse the same exam in several courses, and may supervise <strong>forty students at once</strong> in a live exam.</li>
<li><strong>Students</strong> take exams from home, monitored, where a bad WiFi connection can look like cheating.</li>
<li>Most platforms put exams inside courses. Aladia had already hit that with Books and Subjects: every course got its own copy, and the copies drifted apart.</li>
</ul>
<div class="callout">The hard part wasn’t the exam. It was keeping <b>one exam consistent</b> across many courses, grading rules and students.</div>

{h2("03 — My role and goal", "From the structure to the last error state")}
<p>I was the UI/UX designer on the team responsible for the course domain. I designed the exam system end to end: the structure, the builder with AI, live proctoring, grading and the student side, for web and mobile, and prototyped every flow in Figma. I worked closely with the project manager, the backend and frontend developers and the other designers, from requirements to handoff, and built working prototypes of my designs in code with Claude Code.</p>
<p><strong>The goal:</strong> write an exam once, run it anywhere, and keep the teacher in control, of the questions, the grade and every flag.</p>

{h2("04 — Decision 1", "The exam lives outside the course")}
<p><strong>Solves:</strong> one exam turning into many drifting copies.</p>
{opts(("no", "Exams inside courses, like most platforms.", "Fast to build, but five courses would mean five copies to maintain."),
      ("yes", "Exam Collections, outside any course.", "An exam is written once, and each course adds its own date, rules and grading scale."))}
{iatree("Exam Collections", "The exam is written once in a collection, with no date or grading scale. Each course that uses it adds its own.")}
{proto("Creating an exam inside a collection", "Click through how a teacher opens a collection and creates an exam there, outside any course.", "proto-create-1.jpg", "https://www.figma.com/proto/V7itexfsk2WrTZHVXnbVie/Portflio-prototypes?node-id=3-62221&scaling=scale-down&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=3%3A62221&show-proto-sidebar=1")}
{proto("Creating an exam, with AI on mobile", "Start an exam, open Aladia AI, and generate questions from the platform’s books or write them yourself.", "proto-exam-mobile.jpg", "https://www.figma.com/proto/V7itexfsk2WrTZHVXnbVie/Portflio-prototypes?node-id=57-96937&scaling=scale-down&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=57%3A96937&show-proto-sidebar=1", tag="MOBILE PROTOTYPE")}

{h2("05 — Decision 2", "The course decides the grade, not the exam")}
<p><strong>Solves:</strong> the same exam running in courses graded 18–30, A+ to F or pass/fail.</p>
{opts(("no", "Save the grading scale inside the exam.", "Every institution would need its own copy again."),
      ("yes", "The exam only knows raw points.", "Each course sets its scale, pass mark, weights and which attempt counts."))}
{figs(("exam-09.jpg", "<b>Scheduling in a course.</b> The course adds date, time and proctoring on top of the shared exam."),
      ("exam-10.jpg", "<b>Course grading.</b> Change the scale once and every exam in the course rescales, without editing a question."))}

{h2("06 — Decision 3", "Supervising 40 students without watching 40 screens")}
<p><strong>Solves:</strong> one teacher, forty students at home, and no way to watch forty feeds.</p>
{opts(("no", "One shared room for everyone.", "Students would see each other, and the teacher would get one long recording."),
      ("yes", "One breakout room per student, in one grid,", "created automatically, with rooms that need attention lighting up."))}
{figs(("exam-13.jpg", "<b>Monitor Exam.</b> A teacher can’t scan forty rooms, but can react to the two or three that light up."),
      ("exam-17.jpg", "<b>Grading with AI.</b> AI suggests a score for open answers; the teacher accepts or changes it."))}
<p><strong>The system flags, the human decides.</strong> A lost camera, a WiFi drop or leaving fullscreen each gets its own calm message, and is logged for the teacher. Nothing ends an exam automatically.</p>

{h2("07 — The result", "A complete exam system, designed from nothing")}
{metrics((arrow("6", "3.5"), "minutes to create an exam", "Maze usability test"),
         ("1", "version of each exam, reused across every course", ""),
         ("40", "students supervised by one teacher in one view", ""))}
{proto("A live written exam, proctored and monitored", "The teacher starts the exam, students move into their own rooms, and every room is monitored.", "proto-proctor-1.jpg", "https://www.figma.com/proto/V7itexfsk2WrTZHVXnbVie/Portflio-prototypes?node-id=34-206021&scaling=scale-down&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=34%3A206172&show-proto-sidebar=1")}
{proto("Student: joining a scheduled exam", "How a student joins a scheduled exam at its set time, takes it and submits.", "proto-student-scheduled.jpg", "https://www.figma.com/proto/V7itexfsk2WrTZHVXnbVie/Portflio-prototypes?node-id=44-101499&scaling=scale-down&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=44%3A101499&show-proto-sidebar=1")}
<div class="learned reveal"><span class="kicker" style="color:#888">What I learned</span>
<p class="big" data-words>It all traces back to one early decision: keeping the exam separate from the course.</p></div>
'''

# ---------------------------------------------------------------- SUBJECTS
subjects_body = f'''
{tldr("Subjects were rebuilt inside every course, and teachers were invited course by course. I moved subjects into one shared Subject Area, so a subject is created once and its teacher, books and exams follow it into every course.",
      "UI/UX designer, course domain · Aladia · 2024–2026",
      [(arrow("8", "1"), "changes to replace a teacher across 8 courses"), ("Auto", "teacher invitations, instead of by hand"), ("1", "subject, reused by every course")])}

{h2("01 — Context", "Schools run dozens of courses")}
<p>An Italian school on Aladia runs many courses at once, and the same subjects appear in all of them: Mathematics, Italian, History. Each subject has its teachers, books and exams.</p>

{h2("02 — The problem", "Built once, rebuilt everywhere")}
<ul>
<li><strong>Subjects lived inside courses,</strong> so every new course meant creating Mathematics again, unrelated to the Mathematics in the next.</li>
<li><strong>Teachers were invited per course.</strong> One teacher with Mathematics in eight courses was invited eight times.</li>
<li><strong>Books and exams</strong> couldn’t be linked to a subject at all.</li>
</ul>
<div class="quote">“I have Mathematics in 8 different courses. When a teacher goes on leave and I need to replace him everywhere, I have to do it 8 times.”<cite>Academic coordinator, 12 courses and 50+ subjects</cite></div>

{h2("03 — My role and goal", "Redesigning a feature everyone already used")}
<p>I was the UI/UX designer on the team responsible for the course domain. This was a redesign: I mapped the full workflow, from subject to teacher to book to exam to course, then redesigned the structure, permissions and flows. I worked closely with the project manager, the backend and frontend developers and the other designers, from requirements to handoff, and built working prototypes of my designs in code with Claude Code.</p>
<p><strong>The goal:</strong> a subject should live above the course, so one change reaches every course that uses it.</p>
{iatree("Subject Areas", "Subjects live in Subject Areas, and courses use them.")}

{h2("04 — Decision 1", "Move subjects out of courses")}
<p><strong>Solves:</strong> the same subject rebuilt, and drifting apart, in every course.</p>
{opts(("no", "Keep subjects in courses, and make copying faster.", "The copies would still drift apart."),
      ("yes", "One shared Subject Area per organisation,", "where a subject is created once and added to any course."))}
{figs(("subjects-04.jpg", "<b>Subject list.</b> Study levels, the courses using each subject and its teachers, in one place."),
      ("subjects-08.jpg", "<b>Adding to a course.</b> Teachers pick subjects from the shared areas, with a level for each."))}

{h2("05 — Decision 2", "The teacher follows the subject")}
<p><strong>Solves:</strong> inviting the same teacher course by course, and replacing them eight times.</p>
{opts(("no", "Keep inviting teachers per course.", "The coordinator’s repeated work would stay."),
      ("yes", "Assign the teacher to the subject once,", "and the platform invites them to every course that uses it."))}
{figs(("subjects-09.jpg", "<b>Teachers follow the subject.</b> Adding a subject to a course invites its teachers in the same step."),
      ("subjects-10.jpg", "<b>One question at a time.</b> The subject’s books can come along, or not; the teacher decides."))}
<p>Edge cases were part of the design: a subject with no teacher yet still joins the course, and assigning one later offers to invite them everywhere at once.</p>

{h2("06 — The result", "Set up once, reused everywhere")}
{metrics((arrow("8", "1"), "changes to replace a teacher across 8 courses", ""),
         ("Auto", "teacher invitations, instead of course by course by hand", ""),
         ("3", "organisational edge cases handled by the system", "late assignment · leave · invite to all"))}
{figs(("subjects-mobile.jpg", "<b>Subjects on mobile.</b> Subject Areas as a list or as cards, and editing a subject."), cls="one")}
<div class="learned reveal"><span class="kicker" style="color:#888">What I learned</span>
<p class="big" data-words>The most useful change a designer can make isn’t always on the screen. Sometimes it’s the structure underneath.</p></div>
'''

# ---------------------------------------------------------------- BOOKS
books_body = f'''
{tldr("A book on Aladia was just a file attached to one lecture. I designed a Book Library from scratch, so a book is uploaded once, linked to any course, and opens at the right pages inside the lecture.",
      "UI/UX designer, course domain · Aladia · 2024–2026",
      [(arrow("62", "81"), "usability score for book upload (Maze test)"), ("48%", "of books added through ISBN search"), (arrow("12", "1"), "copies of the same book a teacher maintains")])}

{h2("01 — Context", "Every lecture needs its reading")}
<p>Teachers on Aladia teach from textbooks, PDFs and their own material, often the same book in several courses. Students need to know exactly what to read for each lesson.</p>

{h2("02 — The problem", "Books were just attachments")}
<ul>
<li><strong>The same book was uploaded again in every course,</strong> with no link between the copies.</li>
<li><strong>Updates were missed:</strong> teachers had to remember every place a book lived.</li>
<li><strong>Students got a 300-page PDF</strong> and a separate message saying which chapter to read.</li>
</ul>
<div class="quote">“I have the same PDF uploaded 12 times across my courses. When I update it, I always forget at least one.”<cite>Department head with over 200 teaching PDFs</cite></div>

{h2("03 — My role and goal", "A new part of the platform")}
<p>I was the UI/UX designer on the team responsible for the course domain. I audited the existing workflow, mapped the data model with the PM, then designed the library, the upload flow and the reader from scratch. I worked closely with the project manager, the backend and frontend developers and the other designers through to handoff, and built working prototypes of my designs in code with Claude Code.</p>
<p><strong>The goal:</strong> make books real objects on the platform. Create once, link anywhere, and point each lecture to its own pages.</p>
{iatree("Book Libraries", "One book in the library, and every lecture points to a different part of it.")}

{h2("04 — Decision 1", "Three paths into one form")}
<p><strong>Solves:</strong> books arriving as PDFs, purchase links or teachers’ own material.</p>
{opts(("no", "A better upload button.", "Faster uploads, but teachers would still create copies."),
      ("yes", "Add New Book with three paths into one form,", "with ISBN search that fills in the details."))}
{figs(("books-05.jpg", "<b>Three kinds of book.</b> PDF, purchase link or written in the editor, each clearly labelled."),
      ("books-06.jpg", "<b>One form.</b> ISBN search fills in the details, the route used for 48% of books."))}

{h2("05 — Decision 2", "Each lecture points to its own pages")}
<p><strong>Solves:</strong> students getting the whole book instead of this week’s reading.</p>
{opts(("no", "Attach the book to the course.", "Students would still have to find the right chapter."),
      ("yes", "A page range per lecture,", "and the reader opens directly at those pages."))}
{figs(("books-09.jpg", "<b>Page ranges.</b> One book in the library; each lecture points to its own pages."),
      ("books-mobile.jpg", "<b>Book details on mobile.</b> Start Reading opens at the assigned pages, with the companion volume below."))}

{h2("06 — The result", "A new part of the platform")}
{metrics((arrow("62", "81"), "usability score for book upload", "Maze usability test"),
         ("48%", "of books added through ISBN search, the fastest route", ""),
         (arrow("12", "1"), "copies of the same book a teacher maintains", ""))}
<div class="learned reveal"><span class="kicker" style="color:#888">What I learned</span>
<p class="big" data-words>For something new, the concept has to come before the interface.</p></div>
'''

# ---------------------------------------------------------------- CONNECTA
connecta_body = f'''
{tldr("A no-code integration platform for Odoo made people feel they needed a developer. I separated simple tasks from advanced ones, by role and by task, without removing any power.",
      "Sole product designer · May–Sep 2026",
      [(arrow("4", "2"), "separate dashboards merged into two role-based views"), ("4", "steps to a first connection, instead of the full flow builder"), ("50+", "screens across 20 flows, designed alone")])}

{h2("01 — Context", "Connecting Odoo to everything else")}
<p>Connecta links Odoo with apps like Shopify, Bol.com, Exact Online and Magento, so businesses can sync orders, products and stock without writing code.</p>
<p>Two kinds of people use it. <strong>Business owners</strong> just want to know that everything is working. <strong>Developers and admins</strong> need enough detail to fix what breaks, fast.</p>

{h2("02 — The problem", "A time-saving tool that felt like it needed a developer")}
<p>Behind every connection are mappings, schedules, retries and conditions. The product showed all of it to everyone, all the time. I audited the whole product and found three symptoms:</p>
<ul>
<li><strong>Four separate dashboards in separate tabs</strong> (historical, technical, one for business owners and one for partners) showing overlapping data. Nobody got one clear answer.</li>
<li><strong>Connecting Shopify needed the flow builder,</strong> the most advanced tool. A customer’s very first task was the hardest one.</li>
<li><strong>The setup form was so long it broke its own layout.</strong></li>
</ul>
<div class="callout">The problem wasn’t too many features. <b>Simple and advanced tasks were mixed together</b>, and everyone saw everything.</div>

{h2("03 — My role and goal", "One designer, the whole product")}
<p>I was the only designer, working directly with the co-founders. I audited the product, framed the problem, designed 50+ screens across 20 flows, and rebuilt the final UI as a responsive coded prototype. The setup wizard had a hard deadline: it had to ship before a trade fair.</p>
<p><strong>The goal:</strong> keep all the power, but show the simple path by default. Each person sees what their role needs, and simple tasks never need the advanced tools.</p>

{h2("04 — Decision 1", "Two views of the same data")}
<p><strong>Solves:</strong> four overlapping dashboards that worked for no one.</p>
{opts(("no", "One dashboard, with explanations for owners.", "Owners would still dig through errors and settings they don’t need."),
      ("yes", "One dashboard with a role switcher,", "and two views over the same data: business owners and partners merged into Management, historical and technical merged into Development."))}
{figs(("connecta-02.jpg", "<b>Management view.</b> Read-only: is everything working, and what changed since my last visit?"),
      ("connecta-03.jpg", "<b>Development view.</b> Repeating errors grouped, with retry and a shortcut to the record in Odoo."))}
<p><strong>A constraint:</strong> ideally the view would follow the user’s role automatically, from the backend. The client couldn’t support that yet, so I designed a simple switcher at the top, which still turned four tabs into one place.</p>
<p>When an app can’t retry, the button is <strong>disabled, not hidden</strong>, so the limit is visible. My rule: hide what your role can’t do, disable what the system can’t do.</p>

{h2("05 — Decision 2", "Taking setup out of the flow builder")}
<p><strong>Solves:</strong> a first connection that required the most advanced tool.</p>
{opts(("no", "Keep setup in the flow builder.", "New users would have to learn the whole platform before one connection."),
      ("yes", "A separate four-step wizard", "that starts from the app library."))}
{chain("SETUP FLOW", [("Ensure app", "existing or new"), ("Connect", "search the library"), ("Authenticate", "6 methods"), ("Details", "essentials only"), ("Test & save", "ready to sync")], "")}
{figs(("connecta-05.jpg", "<b>Library first.</b> Known apps are prefilled and tested for you, so most people never type a URL."),
      ("connecta-07.jpg", "<b>Essentials only.</b> The extra fields that broke the layout now sit in collapsed Advanced settings."))}

{h2("06 — Decision 3", "A canvas you can still read months later")}
<p><strong>Solves:</strong> crowded flows that people had to relearn every time they reopened them.</p>
{opts(("no", "Studio as a full page.", "People would lose their place every time they edited a flow."),
      ("yes", "Studio as a slide-in overlay,", "with a start page for recent work and clearer canvas blocks."))}
{figs(("connecta-09.jpg", "<b>The canvas.</b> Clearer blocks and structure, so a flow reads the same months later."),
      ("connecta-ai-2.jpg", "<b>AI drafts a flow.</b> Describe it in plain words; every step is listed and stays editable."))}

{h2("07 — The result", "Simple by default, powerful one click away")}
{metrics((arrow("4", "2"), "separate dashboards merged into two role-based views", ""),
         ("4", "steps to a first working connection, shipped before the trade fair", ""),
         ("50+", "screens across 20 user flows, as the sole designer", ""))}
{proto("The redesigned Connecta, working in code", "Switch between desktop and mobile to see the same product on both.", "proto-connecta.jpg", "https://claude.ai/artifact/H5VD7nLN5CXi5Qm6ckoTqT", tag="CODED PROTOTYPE")}
<div class="learned reveal"><span class="kicker" style="color:#888">What I learned</span>
<p class="big" data-words>Making a technical product simple doesn’t mean removing its power. It means deciding who needs that power, and when.</p></div>
'''

# ---------------------------------------------------------------- EDUCATION (system overview)
education_body = f'''
{tldr("Subjects, books and exams were each built inside courses, and copied into every new one. Before designing any of them, I designed one structure for all three: shared libraries above the course, with the same rules.",
      "UI/UX designer, course domain · Aladia · 2024–2026",
      [("3", "libraries under one Education group, with the same structure"), ("4", "roles shared by all three, learned once"), ("1", "version of each subject, book and exam, reused everywhere")])}
{process(("Discover", "Saw the same pattern three times: subjects, books and exams were all built inside courses, and copied into every new one."),
         ("Define", "The problem wasn’t one feature. It was where content lived. It had to move above the course."),
         ("Structure", "Designed one model for all three: a shared library, an item inside it, and links into courses and lectures."),
         ("Rules", "Gave the three the same four roles and the same behaviour, so teachers learn the system once."),
         ("Design", "Designed each part end to end: Subject Areas, Book Libraries and Exam Collections."),
         ("Connect", "Linked them together, so adding a subject to a course can bring its teacher, books and exams with it."))}
{h2("01 — Context and problem", "Everything lived inside the course")}
<p>On Aladia, a course was a container for everything: its subjects, its books and later its exams were all created inside it. That works for one course. It breaks for a school running dozens.</p>
<ul>
<li><strong>Subjects</strong> were rebuilt in every course. Mathematics in one course had nothing to do with Mathematics in the next, and a teacher with the same subject in 8 courses was invited 8 times.</li>
<li><strong>Books</strong> were files attached to single lectures. One textbook used in 12 places meant 12 uploads, and 12 places to update.</li>
<li><strong>Exams</strong> didn’t exist yet. Built the same way, every course would have had its own copy of the same exam.</li>
</ul>
<div class="callout">Three features, <b>one structural problem</b>: content that should be shared was trapped inside courses.</div>

{h2("02 — My role and goal", "Structure first, screens second")}
<p>I was the UI/UX designer on the team responsible for the course domain, briefed to improve the learning flow and materials for students and teachers. I designed the overall structure first, then each part in depth: I redesigned Subjects, and designed Books and Exams from scratch. I worked closely with the project manager, the backend and frontend developers and the other designers, from requirements to handoff, and built working prototypes of my designs in code with Claude Code.</p>
<p><strong>The goal:</strong> every piece of teaching content lives once, and every course uses it.</p>

{h2("03 — Decision", "Content lives once, courses point to it")}
{opts(("no", "Fix each feature on its own,", "with faster copying or bulk editing. The copies would still drift apart."),
      ("yes", "Lift all teaching content above the course,", "into shared libraries. A course doesn’t own its subjects, books and exams anymore; it uses them."))}
<p>That gave every piece of content the same shape: a <strong>library</strong> owned by an organisation or a freelance teacher, <strong>items</strong> inside it, and <strong>links</strong> from courses and lectures that decide how each item is used there: a level, a page range, a date, a grading scale.</p>

{h2("04 — Information architecture", "One tree for the whole system")}
<p>All three libraries sit together under <strong>Education</strong>, in settings and in the navigation, and follow the same structure. This is the map I designed before any screen.</p>
{iatree()}

{h2("05 — The flow", "How it all connects, step by step")}
<p>The tree shows the structure. This walks through it: from the libraries in Education, into live and on-demand courses, to the student’s lectures and exams, and finally performance. Click any step, or use the arrows.</p>
{sysflow()}

{h2("06 — The three parts", "Each one in depth")}
<p>Each part had its own users, edge cases and decisions. These case studies go through them in detail.</p>
{parts(("subjects", "Subject Areas", "The decision that connected the platform: one shared subject, with its teacher, books and exams following it into every course.", "cover-subjects.jpg"),
       ("books", "Book Libraries", "Books as real objects in a library, linked to lectures with a page range and opened in the built-in reader.", "cover-books.jpg"),
       ("exam", "Exam Module", "A complete exam system, from the first question to live proctoring and a grade every course can trust.", "cover-exam.jpg"))}

{h2("07 — The result", "Three tools that feel like one system")}
{metrics((arrow("8", "1"), "changes to replace a teacher across 8 courses", ""),
         (arrow("12", "1"), "copies of the same book a teacher maintains", ""),
         ("1", "version of each exam, reused across every course", ""))}
<div class="learned reveal"><span class="kicker" style="color:#888">What I learned</span>
<p class="big" data-words>The best design work on this project happened before any screen: deciding where content lives.</p></div>
'''

# ---------------------------------------------------------------- DESIGN SYSTEM
ds_body = f'''
{tldr("Aladia’s design kit had drifted away from the product, and teams weren’t aligned. I built a design system from scratch in Figma, variables first, so a value changed in one place updates the whole product.",
      "Product designer · Aladia · 2024–2026",
      [("735", "design tokens across three tiers"), ("450+", "components built on the tokens"), ("3 + 2", "breakpoint modes and Light/Dark themes")])}
{h2("01 — The problem", "One kit, many domains, no single truth")}
<p>Aladia already had a design kit. But the platform was big, with many domains, and over time the Figma files and the live product drifted apart. <strong>Teams were not aligned</strong> on which version was right.</p>
<div class="callout">The goal: <b>one source of truth</b>, so we could design faster and stay consistent.</div>
<ul>
<li><strong>Decisions made once, reused everywhere.</strong> Change a value in one place, and the whole product follows.</li>
<li><strong>Built from scratch in Figma,</strong> variables first, then components built on top of them.</li>
</ul>

{h2("02 — Structure", "Four layers, each built on the one before")}
{chain("STRUCTURE", [("Core", "Tier 1 · raw values, no meaning yet"), ("Themes", "Tier 2 · names by purpose, Light and Dark"), ("Breakpoints", "Desktop, Tablet and Mobile modes"), ("Components", "atoms, molecules, organisms")], "Each layer only uses the one before it, so a change at the bottom flows all the way up.")}

{h2("03 — Tier 1 · Core", "The raw palette")}
<p>Over 400 variables for colour, typography, radius, spacing, shadows and more. None of them has a meaning yet: they are just the values the rest of the system is allowed to use.</p>
{figs(("ds-core.jpg", "<b>Core Tier 1.</b> Primitives for radius, colour and typography, and the variable collections in Figma."), cls="one")}

{h2("04 — Tier 2 · Themes", "Names by purpose")}
<p>Themes give each value a job, like a primary background or a hover state. The same token points to a different core value in Light and in Dark, so components never need to know which theme they are in.</p>
{figs(("ds-themes.jpg", "<b>Themes Tier 2.</b> Radius and content colours named by purpose, with Light and Dark values side by side."), cls="one")}

{h2("05 — Breakpoints", "One component, three screen sizes")}
<p>Breakpoint modes for Desktop, Tablet and Mobile change values like spacing, sizes and visibility. A component adapts by switching mode, without being redrawn for each screen. This is what made every screen on the platform responsive, with mobile versions designed too.</p>
{figs(("ds-breakpoints.jpg", "<b>Core Breakpoints.</b> Responsive values per mode: Desktop, Tablet and Mobile."), cls="one")}

{h2("06 — Components", "Built in atomic levels, with variants and states")}
<ul>
<li><strong>Atoms:</strong> foundation pieces with one job each, like dividers, logos, icons and images.</li>
<li><strong>Molecules:</strong> small interactive parts, like buttons, dropdowns, input fields and chips.</li>
<li><strong>Organisms:</strong> complex, complete sections, like tables, breadcrumbs, cards and pop-ups.</li>
</ul>
{figs(("ds-atomic.jpg", "<b>Atomic levels.</b> Atoms, molecules and organisms, in Aladia’s own style."), cls="one")}
{figs(("ds-components.jpg", "<b>Variants and states.</b> Icons, buttons, input fields and lists, each with their variants."), cls="one")}

{h2("07 — Workflow", "How the team worked with it")}
{chain("WORKFLOW", [("Domain files", "one Figma file per domain, with a local Components page"), ("Branch per task", "a Figma branch named after the task, then design"), ("Approve and merge", "after approval the branch is merged")], "The system stays clean, because nothing reaches it without review.")}

{h2("08 — The result", "One source of truth for the whole platform")}
{metrics(("735", "design tokens across three tiers", ""),
         ("450+", "components built on the tokens", ""),
         ("3", "breakpoint modes, plus Light and Dark themes", ""))}
<p>Every web screen on Aladia was responsive and had a mobile version, built from the same tokens and components.</p>
'''

# ---------------------------------------------------------------- LIVE TV (concept)
tv_body = f'''
{tldr("A self-initiated concept: a live TV guide for 500+ channels on Android TV, where every choice is made with a remote. I designed it from the logic flow to the hi-fi screen, tokens and developer handover.",
      "Concept project · Product designer, UX, UI & design system",
      [("500+", "channels, navigable with a D-Pad only"), ("3", "entitlement states, never shown by colour alone"), ("1", "hi-fi screen at 1920×1080, with full handover")])}
<div class="callout"><b>Concept project.</b> A self-initiated exercise, designed from brief to developer handover. No real client or users, so there are no results to report.</div>
{h2("01 — The brief", "500 channels, one remote")}
<p>The brief described a live TV platform for Android TV with more than 500 channels, some free, some premium and some locked. The existing programme guide (EPG) was a wall of data: no hierarchy, no recommendations and no clear way to tell what the viewer could actually watch.</p>
<ul>
<li><strong>Choice paralysis:</strong> scrolling hundreds of channels before choosing anything.</li>
<li><strong>Entitlement:</strong> showing what is free, premium or locked without cluttering the screen.</li>
<li><strong>Input:</strong> everything had to work with a D-Pad remote only, at 1920×1080, read from a sofa.</li>
</ul>

{h2("02 — The approach", "Broadcast guide meets streaming app")}
{opts(("no", "A classic EPG grid only.", "Familiar, but it is exactly the wall of data that causes the problem."),
      ("no", "A streaming-style home with rails only.", "Easy to browse, but it hides what is on now across 500 channels."),
      ("yes", "A hybrid layout,", "with a full-bleed hero panel, a curated “Recommended Live Now” rail and a smart EPG grid on the same screen."))}
<p><strong>The hero panel updates on every D-Pad move.</strong> Focusing a programme anywhere shows its full title, time and actions at the top. This solves long titles on TV without tooltips or hover states, which a remote doesn’t have.</p>
{figs(("tv-hero.jpg", "<b>Main screen, 1920×1080.</b> Hero panel, recommendation rail and EPG grid, all reachable with the D-Pad."), cls="one")}

{h2("03 — Entitlement", "Never colour alone")}
<p>Every programme is <strong>Free</strong>, <strong>Premium</strong> or <strong>Locked</strong>. Each state is shown three ways at once (colour, opacity and a text label), so it still reads for colour-blind viewers and from across the room. Pressing OK on a free or premium programme plays it; on a locked one it opens the upgrade modal instead.</p>
<div class="tv-states reveal"><span class="st free">✓ Free</span><span class="st prem">★ Premium</span><span class="st lock">🔒 Locked</span></div>
<p>Every interactive element also has a visible focused state, because on TV the focus <em>is</em> the cursor.</p>

{h2("04 — Logic flow", "Every path, not just the happy one")}
<p>Before any screen, I mapped the whole flow: loading with a skeleton, data errors with retry, the hero actions (Watch Live, Info, Restart), the restart sheet for programmes that started earlier, and locked channels leading to the upgrade modal or back to the guide.</p>
{figs(("tv-flow.jpg", "<b>Logic flow.</b> Happy and unhappy paths, plus edge cases like long titles and missing thumbnails."), cls="one")}

{h2("05 — Design system", "Same structure, different screen")}
<p>The design system uses the same two first tiers as my Aladia work: <strong>Core Tier 1</strong> primitives and <strong>Themes Tier 2</strong> semantic tokens, sized for TV with minimum font sizes and spacing for 10-foot viewing. <a class="ia-link" href="#design-system">See how I build design systems →</a></p>

{h2("06 — Handover", "Written for developers")}
<p>The handover covers how each behaviour should work: how the hero updates on focus, how the rail and grid scroll, where the “now” line sits, when long titles start to scroll, which way BACK goes, and how often data refreshes.</p>
{figs(("tv-dev.jpg", "<b>Developer notes.</b> Key behaviours to implement, with timings and rules."), cls="one")}
'''

CASES = [
    ("education", "Education System", "How subjects, books and exams became one connected system on Aladia.",
     "cover-education.jpg", "education-tabs.jpg",
     "Before I designed subjects, books or exams one by one, I had to solve the problem they shared: all teaching content was trapped inside courses. I designed one structure for all three, shared libraries under Education, with the same rules, linked into courses and lectures.",
     [("Role", "Product Designer, end to end"), ("Company", "Aladia"), ("Industry", "EdTech · B2B & B2C SaaS"), ("Platform", "Web, responsive + mobile"), ("Focus", "Information architecture<br>System design")],
     education_body, ("exam", "Exam Module", "Live proctoring UX · Grading system design", "cover-exam.jpg")),
    ("exam", "Exam Module", "Designing a complete exam system, from the first question to the final grade.",
     "cover-exam.jpg", "exam-01.jpg",
     "Aladia had no exam system: no builder, no proctoring, no grading. I designed the whole thing from a blank canvas: three exam formats, AI-assisted question creation, live proctored exams, and a grading model that works across courses with completely different scoring scales.",
     [("Role", "Product Designer, end to end"), ("Company", "Aladia"), ("Industry", "EdTech · B2B & B2C SaaS"), ("Platform", "Web, responsive + mobile"), ("Focus", "Live proctoring UX<br>Grading system design")],
     exam_body, ("subjects", "Subject Areas", "Data model design · Permission systems", "cover-subjects.jpg")),
    ("subjects", "Subject Areas", "The decision that connected the platform: one shared subject, with its teacher, books and exams following it into every course.",
     "cover-subjects.jpg", "subjects-01.jpg",
     "Subjects on Aladia were rebuilt inside every course, and teachers had to be invited to each course by hand. I moved subjects into one shared Subject Area, so a subject is created once and reused everywhere, and its teacher, books and exams follow it into every course automatically.",
     [("Role", "Product Designer, end to end"), ("Company", "Aladia"), ("Industry", "EdTech · B2B & B2C SaaS"), ("Platform", "Web, responsive + mobile"), ("Focus", "Data model design<br>Permission systems")],
     subjects_body, ("books", "Book Libraries", "Content library design · In-lecture book reader", "cover-books.jpg")),
    ("books", "Book Libraries", "A book library built from scratch, so teachers upload a book once and use it everywhere.",
     "cover-books.jpg", "books-01.jpg",
     "Aladia had no concept of a book. Teachers could only attach files to individual lectures, one at a time. I designed a Book Library from zero: one place to upload, organise and reuse books across courses, lectures, subjects and live sessions.",
     [("Role", "Product Designer, end to end"), ("Company", "Aladia"), ("Industry", "EdTech · B2B & B2C SaaS"), ("Platform", "Web, responsive + mobile"), ("Focus", "Content library design<br>In-lecture book reader")],
     books_body, ("design-system", "Design System", "Design tokens · Component library", "cover-design-system.jpg")),
    ("design-system", "Design System", "Structure, modes and workflow of the design system I built from scratch.",
     "cover-design-system.jpg", "ds-atomic.jpg",
     "Aladia had a design kit, but the platform had many domains, and Figma files and the product had drifted apart. I built a design system from scratch in Figma, variables first: a core palette, themes, breakpoint modes and components on top, plus a branching workflow so the team could use it without breaking it.",
     [("Role", "Product Designer"), ("Company", "Aladia"), ("Industry", "EdTech · B2B & B2C SaaS"), ("Tool", "Figma variables & components"), ("Focus", "Design tokens<br>Component library")],
     ds_body, ("connecta", "Connecta", "Role-based dashboards · Setup wizard design", "cover-connecta.jpg")),
    ("connecta", "Connecta", "Making complex data integrations simple for people who don’t write code.",
     "cover-connecta.jpg", "connecta-01.jpg",
     "Connecta is a no-code integration platform built inside Odoo. It connects apps like Shopify, Bol.com, Exact Online and Magento, so businesses can sync their data without writing code. I designed the whole product: dashboards, setup flow, flow builder and marketing site.",
     [("Role", "Sole Product Designer"), ("Timeline", "May – Sep 2026"), ("Platform", "Web, responsive"), ("Focus", "Dashboard consolidation<br>Setup wizard design")],
     connecta_body, ("live-tv", "Live TV Guide", "Concept · Android TV", "cover-tv.jpg")),
    ("live-tv", "Live TV Guide", "A concept for choosing from 500 live channels on Android TV, using only a remote.",
     "cover-tv.jpg", "tv-hero.jpg",
     "A self-initiated concept: redesigning the live programme guide of a 500-channel Android TV platform with free, premium and locked content. I designed it from the logic flow to the hi-fi screen, design tokens and a full developer handover, all for D-Pad navigation.",
     [("Type", "Concept project"), ("Role", "Product Designer, UX, UI & design system"), ("Platform", "Android TV, 1920×1080"), ("Input", "D-Pad remote only"), ("Focus", "EPG layout<br>Entitlement states"), ("Deliverables", "Flow, hi-fi, tokens, handover")],
     tv_body, ("education", "Education System", "Information architecture · System design", "cover-education.jpg")),
]

WORKS = [
    ("education", "Education System", ["Information architecture", "System design"], "cover-education.jpg", ""),
    ("exam", "Exam Module", ["Live proctoring UX", "Grading system design"], "cover-exam.jpg", "right"),
    ("subjects", "Subject Areas", ["Data model design", "Permission systems"], "cover-subjects.jpg", ""),
    ("books", "Book Libraries", ["Content library design", "In-lecture book reader"], "cover-books.jpg", "right"),
    ("design-system", "Design System", ["Design tokens", "Component library"], "cover-design-system.jpg", ""),
    ("connecta", "Connecta", ["Role-based dashboards", "Setup wizard design"], "cover-connecta.jpg", "right"),
    ("live-tv", "Live TV Guide", ["Concept project", "Android TV · D-Pad UX"], "cover-tv.jpg", ""),
]

TESTIMONIALS = [
    ("Donya consistently demonstrated a high level of professionalism and reliability. Her work was of excellent quality, and she maintained a positive and collaborative attitude.", "Aladia", "E-learning platform, via Upwork", "A"),
    ("Donya brings a uniquely structured perspective to digital experiences, translating her background in architecture into interfaces that feel natural and intuitive.", "Rambod Rahmani", "Senior Software, AI &amp; Data Engineer", "RR"),
    ("A highly dedicated professional who consistently delivers top-tier UI/UX design — deep expertise paired with a strong, confident vision.", "Daniele Cosentino", "Visual Designer UX/UI", "DC"),
    ("Donya combines real design talent with an incredibly generous spirit. She approached every task thoughtfully and shared her process and knowledge freely.", "Lilit Gharagyozyan", "Product Designer", "LG"),
]

STATS = [
    ("100", "+", "Screens designed", "Across four major features on one B2B &amp; B2C platform."),
    ("3", "+", "Years experience", "Designing and shipping SaaS products."),
    ("450", "+", "Components", "In a three-tier design system built from scratch."),
    ("5", "", "User roles", "Served by one platform, each with its own needs."),
]

STEPS = [
    ("01/", "Understand the constraints", "Who uses it, what can break, and which rules the system has to respect."),
    ("02/", "Define the structure", "Data models, permissions, and how features connect, before any screen."),
    ("03/", "Design every state", "Empty, loading, error, disabled, recovery. Not just the happy path."),
    ("04/", "Ship with engineering", "I stay involved during the build and adjust as real constraints come up."),
]

ICON_IG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>'
ICON_IN = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.5h4V21H3zM9.5 9.5h3.8v1.6h.06c.53-1 1.83-2.06 3.77-2.06 4.03 0 4.77 2.65 4.77 6.1V21h-4v-5.2c0-1.24-.02-2.84-1.73-2.84-1.73 0-2 1.35-2 2.75V21h-4z"/></svg>'
ICON_MAIL = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>'


def dots(n=4):
    return '<div class="dots">' + "<i></i>" * n + "</div>"


def home():
    stats = "".join(
        f'<div class="stat"><i class="pt"></i><i class="pt r"></i>{dots()}<div class="stat-num" data-count="{n}" data-suffix="{s}">0{s}</div><h3>{t}</h3><p>{d}</p></div>'
        for n, s, t, d in STATS)
    steps = "".join(
        f'<div class="step"><div class="step-top"><span>{k}</span>{dots()}</div><div><h3>{t}</h3><p>{d}</p></div></div>'
        for k, t, d in STEPS)
    works_fill = '<div class="work work-fill" aria-hidden="true"></div>' if len(WORKS) % 2 else ""
    works = "".join(
        f'''<div class="work {side}"><a href="#{slug}">
      <div class="work-media"><img src="img/{img}" alt="{title} case study" loading="lazy"></div>
      <div class="work-meta"><div><div class="work-num">0{i+1} / 07</div><h3>{title}</h3><span class="view-case">VIEW CASE STUDY →</span></div><div class="tags">{"<br>".join(tags)}</div></div>
    </a></div>''' for i, (slug, title, tags, img, side) in enumerate(WORKS))
    slides = "".join(
        f'<div class="slide"><blockquote>“{q}”</blockquote><div class="avatar">{ini}</div><div class="who">{who}</div><div class="role">{role}</div></div>'
        for q, who, role, ini in TESTIMONIALS)
    return f'''
<section class="view" id="view-home">
  <div class="frame">
    <div class="hero">
      <div class="hero-sticky">
        <h1 class="hero-title"><span class="line"><span>Product</span></span><span class="line"><span>Designer</span></span></h1>
        <div class="portrait-stage"><div class="portrait">
          <img class="front" src="img/portrait-color.jpg" alt="Donya Yarahmadi">
        </div></div>
        <div class="hero-hint">SCROLL</div>
      </div>
    </div>
    <div class="rule"></div>
    <div class="facts"><div class="cols">
      <div><small>Location</small><strong>Milan, Italy · open to relocate</strong></div>
      <div><small>Field</small><strong>Product and UX Design</strong></div>
      <div><small>Approach</small><strong>System before screens</strong></div>
      <div><small>Clients</small><strong>SaaS &amp; B2B platforms</strong></div>
    </div></div>
    <div class="about">
      <span class="eyebrow">About</span>
      <p class="about-text" data-words>I’m a Product Designer in Milan. For 3+ years I’ve designed B2B and B2C SaaS, shaping the structure behind complex products so they feel simple, even when many types of users share the same system.</p>
    </div>
    <div class="stats"><div class="cols">{stats}</div></div>
  </div>

  <section class="approach dark">
    <div class="gl"><span></span><span></span><span></span><span></span></div>
    <div class="frame">
      <div class="rule"></div>
      <div class="approach-head"><span class="eyebrow">Approach <span class="count">(04)</span></span><h2 class="approach-title">How I work</h2></div>
      <div class="rule"></div>
      <div class="approach-grid">
        <div class="approach-img"><img src="img/approach.jpg" alt="Illustration of my process as four stacked layers: constraints, structure, every state, shipped" loading="lazy"></div>
        {steps}
      </div>
      <div class="approach-foot"></div>
    </div>
  </section>

  <div class="frame">
    <div class="cs-split"><div class="sticky"><span class="word l">Case</span><span class="word r">studies</span></div></div>
    <div class="works-head" id="work">
      <div><span class="eyebrow">Selected works <span class="count">(07)</span></span><h2>Complex products, made simple to use</h2></div>
      <p>Every project here started with the same question: <b>how do you make something complex feel simple?</b></p>
    </div>
    <div class="works">{works}{works_fill}</div>

    <div class="rule"></div>
    <div class="testi">
      <div class="testi-head"><span class="eyebrow">Feedback <span class="count">(04)</span></span><h2>What people I’ve<br>worked with say</h2></div>
      <div class="carousel">
        <div class="slides">{slides}</div>
        {dots()}
        <div class="carousel-nav"><button class="prev" aria-label="Previous testimonial">Prev</button><button class="next-t" aria-label="Next testimonial">Next</button></div>
      </div>
    </div>
  </div>
</section>'''


def footer():
    return f'''
<footer class="footer frame">
  <div class="rule"></div>
  <div class="footer-top">
    <div>
      <h2>Let’s talk.</h2>
      <p class="lead">I’m looking for a product design role, in Milan or remote, and I’m open to relocating. I’d love to hear about your team.</p>
      <div class="socials">
        <a href="https://www.instagram.com/donya.design/" aria-label="Instagram" target="_blank" rel="noopener">{ICON_IG}</a>
        <a href="https://www.linkedin.com/in/donya-yarahmadi-a0b804235/" aria-label="LinkedIn" target="_blank" rel="noopener">{ICON_IN}</a>
        <a href="mailto:donyayarahmadi@outlook.com" aria-label="Email">{ICON_MAIL}</a>
      </div>
    </div>
  </div>
  <div class="legal"><span>© 2026 Donya Yarahmadi</span><span>Product &amp; UX Design</span></div>
</footer>'''


def page():
    cases = "".join(case(*c) for c in CASES)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Donya Yarahmadi — Product Designer</title>
<meta name="description" content="Product &amp; UX Designer in Milan. I help SaaS teams design complex products that feel simple, even when many types of users share the same system.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Host+Grotesk:wght@300..800&family=IBM+Plex+Mono:wght@400;500&family=Inter+Tight:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="gridlines" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
<header class="header">
  <div class="frame">
    <a class="logo" href="#">Donya<br>Design</a>
    <nav class="nav"><a href="#" data-nav="home" data-roll>HOME</a><a href="#work" data-nav="work" data-roll>WORKS</a></nav>
    <a class="cta-call" href="https://calendly.com/donyarahmadi/30min" target="_blank" rel="noopener"><span>Book a Call</span><span class="arrow">→</span></a>
  </div>
</header>
<main>
{home()}
{cases}
</main>
{footer()}
<div class="lightbox" role="dialog" aria-label="Enlarged screenshot"><button>CLOSE ✕</button><img alt=""><p></p></div>
<script src="main.js"></script>
</body>
</html>'''


OUT.write_text(page(), encoding="utf-8")
print("wrote", OUT, len(page()) // 1024, "KB")
