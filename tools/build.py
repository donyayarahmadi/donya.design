#!/usr/bin/env python3
"""Builds site/index.html (home + 4 case studies, hash-routed) from the content below."""
from pathlib import Path

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
        alt = cap.split(".")[0].replace("<b>", "").replace("</b>", "")
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
    items = "".join(f'<li><span>{i+1:02d}</span>{t}</li>' for i, t in enumerate(stages))
    return f'<div class="process reveal"><span class="kicker">Process</span><ol>{items}</ol></div>'

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
        <p class="reveal">{overview}</p>
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
{process("Framing the problem", "Exam structure", "Flows & UI", "Figma prototypes", "Maze testing", "Handoff")}
{h2("01 — The problem", "Exams didn’t exist yet")}
<p>Teachers on Aladia needed to create exams, run them with supervision and grade them, all inside the platform. None of that existed yet.</p>
<p>And Aladia serves very different institutions. An Italian liceo grades from 18 to 30, while a corporate course grades from 0 to 100. <strong>The same system had to work for both.</strong></p>
<h3>Who it affected</h3>
<ul>
<li><strong>Teachers</strong> often reuse the same exam in several courses, and may supervise <strong>forty students at once</strong> during a live exam.</li>
<li><strong>Students</strong> take exams from home, with camera, microphone and screen monitored, where a bad WiFi connection can look like cheating.</li>
</ul>
<h3>How I found the problem</h3>
<p>Most LMS platforms put exams inside courses. It’s the obvious structure, and it ships faster.</p>
<p>But Aladia had already hit this problem twice, with Books and with Subjects. When content lived inside a course, every course ended up with its own copy. Fix a typo in one, and the others still have it. Over time, the copies stopped being the same thing at all.</p>
<div class="callout">The hardest part wasn’t the exam itself. It was keeping <b>one exam consistent</b> across many courses, many grading rules and many students.</div>

{h2("02 — Decision 1", "The exam lives outside the course")}
{opts(("no", "Exams inside courses, like most LMS platforms.", "Simple and fast to build, but a teacher using the same final exam in five courses would end up with five copies to maintain."),
      ("yes", "Exam Collections at the profile level.", "An exam is created once and used anywhere."))}
<p>Each course adds its own <strong>schedule, proctoring rules and grading scale on top</strong>, without ever touching the exam itself. The exam only knows raw points. Each course decides how those points become a grade.</p>
<p><strong>Why it matters:</strong> the same exam can run in a course graded 18–30 and one graded 0–100 on the same afternoon. And a teacher with forty students across three courses maintains exactly one version of each exam.</p>
{chain("HOW AN EXAM MOVES THROUGH THE SYSTEM", [("Exam Collection", "shared, with roles"), ("Exam", "one version"), ("Course", "sets date & grading scale"), ("Student attempt", "on-demand, scheduled or live"), ("Grade", "AI suggests, teacher decides")], "The exam is written once. Each course that uses it brings its own date, rules and grading scale.")}
{proto("Creating an exam inside a collection", "Click through how a teacher opens a collection and creates an exam there, outside any course.", "proto-create-1.jpg", "https://www.figma.com/proto/V7itexfsk2WrTZHVXnbVie/Portflio-prototypes?node-id=3-62221&scaling=scale-down&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=3%3A62221&show-proto-sidebar=1")}

{h2("03 — Building the exam", "Questions, with AI as an assistant")}
<p>Teachers write exams in the Document Builder, the same block editor used for books. Each question can be one of eight types, from multiple choice and match-the-pairs to essays and file uploads, and saved questions can be reused in any exam.</p>
<p>AI sits on each question as an <strong>Ask AI</strong> action, and a teacher can ask it to draft an exam for a subject. The teacher stays the author: AI suggests, the teacher edits and decides.</p>
{proto("Building questions in the exam builder", "Click through the exam builder: adding a question, choosing its type and writing the options.", "proto-build-1.jpg", "https://www.figma.com/proto/V7itexfsk2WrTZHVXnbVie/Portflio-prototypes?node-id=11-7129&scaling=scale-down&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=11%3A7129&show-proto-sidebar=1")}

{h2("04 — Decision 2", "The course decides the grade, not the exam")}
<p>Every institution grades differently. An Italian liceo grades from 18 to 30, a school might use A+ to F, and a corporate course may only need pass or fail. And because exams live outside courses, the same exam can appear in all of them.</p>
{opts(("no", "Save the grading scale inside the exam.", "Every institution would need its own copy, which is the exact problem Decision 1 solved."),
      ("no", "One fixed scale for the whole platform.", "Simple, but wrong for most institutions."),
      ("yes", "The exam stays neutral and only knows raw points.", "Each course decides how points become a grade."))}
<p><strong>What I designed:</strong> three settings inside each course.</p>
<ul>
<li><strong>Grading scale:</strong> the course sets its maximum score (30, 10, 100…) and pass percentage, and exam points scale automatically. Advanced grading adds custom levels like A+ to F.</li>
<li><strong>Weights per exam type:</strong> a Final can count far more than a Quiz.</li>
<li><strong>Which attempt counts:</strong> Highest by default, because it rewards improvement without punishing a student for trying again. A stricter course can choose Latest or Average.</li>
</ul>
<p><strong>Why it works:</strong> none of these settings touch the exam. Changing a course’s scale rescales every exam in it instantly, without editing a single question.</p>
{proto("Adding an exam to a live course", "Click through how a teacher takes an exam from a collection and adds it to a running course, where the course sets its date and rules.", "proto-live-1.jpg", "https://www.figma.com/proto/V7itexfsk2WrTZHVXnbVie/Portflio-prototypes?node-id=24-27782&scaling=min-zoom&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=24%3A27782&show-proto-sidebar=1")}
{figs(("exam-07.jpg", "<b>Course content.</b> Exams sit in the course calendar next to lectures and schedule changes."),
      ("exam-08.jpg", "<b>Exam details inside a lecture.</b> Proctoring and eligibility are switched on per course."),
      ("exam-09.jpg", "<b>Scheduling an exam in a course.</b> The course adds date, time and proctoring on top of the shared exam."),
      ("exam-10.jpg", "<b>Course grading settings.</b> Which attempt counts, the course’s scale and pass mark, and weights per exam type."))}

{h2("05 — Decision 3", "Supervising 40 students without watching 40 screens")}
<p>On exam day, one teacher may supervise forty students at once, each at home with a camera and a shared screen. Nobody can watch forty video feeds continuously.</p>
{opts(("no", "One shared room for everyone.", "Students could see or hear each other, and the teacher would get one long recording to scroll through."),
      ("no", "A simple list of student names.", "The teacher would have to click into each student to check on them."),
      ("yes", "One breakout room per student, shown in a grid,", "with the rooms that need attention highlighted."))}
<ul>
<li>The rooms are <strong>created automatically</strong> from the participant list, so the teacher sets up nothing on the day.</li>
<li><strong>Monitor Exam</strong> shows one room per student: webcam and exam screen side by side.</li>
<li>Rooms are sorted into tabs: <strong>Open, Closed</strong> (students who submit move out of the way automatically) and <strong>Proctoring alerts</strong>.</li>
<li>A room <strong>lights up</strong> the moment something needs attention, like a raised hand or a flag.</li>
</ul>
<div class="callout">A teacher can’t scan forty rooms, but they can react to the <b>two or three that light up</b>. And each student’s session is recorded separately, so every attempt has its own file.</div>
{proto("A live written exam, proctored and monitored", "Click through a written exam during a live session: the teacher starts it, students move into their own rooms, and the teacher monitors every room with proctoring on.", "proto-proctor-1.jpg", "https://www.figma.com/proto/V7itexfsk2WrTZHVXnbVie/Portflio-prototypes?node-id=34-206021&scaling=scale-down&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=34%3A206172&show-proto-sidebar=1")}
{figs(("exam-11.jpg", "<b>Live session.</b> The teacher starts the exam and creates breakout rooms in one step."),
      ("exam-13.jpg", "<b>Monitor Exam.</b> Every room in one grid, with tabs for open and closed rooms."))}
<h3>Small decisions that remove work</h3>
<ul>
<li>If the exam is longer than its calendar slot, the end time <strong>extends automatically</strong>, instead of cutting the student’s time or showing an error.</li>
<li>The entry window (how long students have to start) <strong>grows with the exam’s length</strong>, so the teacher never has to set it.</li>
<li>When grading, <strong>AI suggests a score</strong> for open questions, and the teacher accepts or changes it.</li>
</ul>
{figs(("exam-17.jpg", "<b>Grading with AI.</b> AI evaluates open answers; the teacher sets the point or accepts the AI score."),
      ("exam-15.jpg", "<b>Exam overview.</b> Average score, pass rate and each student’s status, including regrade requests."))}

{h2("06 — Decision 4", "The system flags, the human decides")}
<p>Students take exams from home, with camera, microphone and screen monitored. In that situation, <strong>a technical problem can look like cheating</strong>. A student whose WiFi drops shouldn’t be treated as suspicious.</p>
{opts(("no", "End the exam automatically when a violation is detected.", "Too harsh, and often wrong."),
      ("no", "Show one generic error message.", "Confusing for the student, and it reads as suspicious behaviour."),
      ("yes", "Flag and notify, never end.", "The student is told in the moment, the incident is logged, and the teacher decides."))}
<p><strong>What I designed:</strong> a specific, calm state for each failure.</p>
<ul>
<li>Camera or microphone disconnected → prompt to reconnect</li>
<li>WiFi drops → the exam pauses and shows that it’s reconnecting</li>
<li>Leaving fullscreen (Esc or F11) → prompt to return to the exam</li>
</ul>
<p>Naming exactly what happened <strong>protects the student as much as it protects the exam</strong>. The same thinking runs through the whole student experience:</p>
<ul>
<li><strong>Scoped rechecks:</strong> students select the specific questions they want reviewed and explain why, so a recheck doesn’t become a second full grading.</li>
<li><strong>Controlled chat:</strong> students can reach the teacher mid-exam, but only for clarification and support.</li>
<li><strong>Oral exams</strong> got their own one-to-one flow, instead of a video call attached to a written exam.</li>
</ul>
{proto("An oral exam, one to one", "Click through an oral exam: the teacher opens the exam from the calendar, joins the session and creates breakout rooms to examine students one by one.", "proto-oral-1.jpg", "https://www.figma.com/proto/V7itexfsk2WrTZHVXnbVie/Portflio-prototypes?node-id=38-91563&scaling=scale-down&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=38%3A91563&show-proto-sidebar=1")}
{proto("Student: taking an on-demand exam", "Click through how a student starts an on-demand exam from the course, answers the questions and submits.", "proto-student-ondemand.jpg", "https://www.figma.com/proto/V7itexfsk2WrTZHVXnbVie/Portflio-prototypes?node-id=44-100515&scaling=scale-down&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=44%3A100515&show-proto-sidebar=1")}
{proto("Student: joining a scheduled exam", "Click through how a student joins a scheduled exam at its set time, takes it and submits.", "proto-student-scheduled.jpg", "https://www.figma.com/proto/V7itexfsk2WrTZHVXnbVie/Portflio-prototypes?node-id=44-101499&scaling=scale-down&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=44%3A101499&show-proto-sidebar=1")}

{h2("07 — Performance", "One number teachers can trust")}
<p>A teacher with several courses may have <strong>a hundred students or more</strong>. Exam results alone don’t show who needs help, and neither does attendance. A student can attend every class and fail every exam; another can skip classes and still score well, until the material gets harder.</p>
<p><strong>What I designed:</strong> Performance, one number that combines both signals: <strong>Attendance 30% + Exams 70%</strong>.</p>
{opts(("no", "Let each course set its own formula, like grading.", "A “75” in one course would mean something different from a “75” in another, and nobody could compare."),
      ("yes", "One fixed formula everywhere,", "so the number always means the same thing."))}
<p>Exams carry the larger share on purpose: attendance shows engagement, exams show what a student can actually do, and engagement shouldn’t outweigh competence.</p>
{figs(("exam-24.jpg", "<b>Registry.</b> Attendance, score and performance for every student, with the trend over chapters."),
      ("exam-25.jpg", "<b>Subjects radar.</b> One student compared with the class average across subjects."))}

{h2("08 — The result", "A complete exam system, designed from nothing")}
{research("Unmoderated Maze tests on the Aladia platform · 50 participants across 4 flows", [("Time to create an exam", "6 min", "3.5 min")])}
{metrics((arrow("6", "3.5"), "minutes to create an exam", "Maze usability test"),
         ("1", "version of each exam, reused across every course", ""),
         ("40", "students supervised by one teacher in one view", ""))}
<p>A complete exam system, from creation to live proctoring, grading and rechecks, and the most structurally complex part of the platform.</p>
<div class="learned reveal"><span class="kicker" style="color:#888">What I learned</span>
<p class="big">It all traces back to one early decision: keeping the exam separate from the course.</p>
<p>That’s what lets the same exam run under completely different grading rules, and what keeps performance comparable everywhere. Almost every detail exists because a simpler version broke down against a real edge case during design. The happy path was never the hard part.</p></div>
'''

# ---------------------------------------------------------------- SUBJECTS
subjects_body = f'''
{process("Workflow mapping", "Structure & data model", "Permissions", "Flows & UI", "Edge cases", "Handoff")}
{h2("01 — The problem", "Built once, rebuilt everywhere")}
<p>Subjects lived inside courses. Every new course meant creating Mathematics, Italian and History again from scratch, and the Mathematics in one course had nothing to do with the Mathematics in the next. Books and exams couldn’t be linked to a subject at all.</p>
<p>Teachers were stuck in the same pattern. They could only be assigned to a subject inside a single course, so a teacher with Mathematics in eight courses had to be invited eight separate times. Once inside, they faced a calendar showing every lecture of a year-long course, while they taught roughly one lesson a week. <strong>Finding their own lectures was hard.</strong></p>
<h3>Who it affected</h3>
<p>The person who felt this most was the <strong>academic coordinator</strong>, managing 12 courses and more than 50 subjects. Every change had to be repeated course by course. When a teacher went on leave, replacing them meant redoing the same work in every course they taught.</p>
<div class="quote">“I have Mathematics in 8 different courses. When a teacher goes on leave and I need to replace him everywhere, I have to do it 8 times.”<cite>Academic coordinator</cite></div>
<h3>The insight</h3>
<p>A subject isn’t a course-level idea. Mathematics is Mathematics wherever it’s taught. The teacher is the same person, and the books and exams are the same resources.</p>
<div class="callout">So the subject should <b>live above the course</b>, and every course should simply use it.</div>
{figs(("subjects-03.jpg", "<b>One area, many subjects.</b> Members and subjects are managed in one place."), cls="one")}

{h2("02 — Decision 1", "Move subjects out of courses")}
{opts(("no", "Keep subjects inside courses, and make copying them faster.", "Every copy would still drift apart, and the coordinator’s problem would stay."),
      ("yes", "One shared Subject Area for each organisation or freelance teacher.", "Create a subject once, assign its teacher, link books and exams, then add it to any course, and everything comes with it."))}
<p><strong>Creating a subject is deliberately light:</strong> a title, a teacher, an icon and a colour. Subjects can also be organised by <strong>study level</strong>, like Mathematics for the first two years of a Liceo Scientifico, which matches how Italian schools actually teach.</p>
<p><strong>One permission model everywhere:</strong> Subject Areas use the same four roles as Book Libraries and Exam Collections (Owner, Curator, Editor, Viewer), so teachers learn it once. If someone can’t do something because of their role, the action simply isn’t there, instead of appearing disabled with an error.</p>
{figs(("subjects-04.jpg", "<b>Subject list.</b> Study levels, the courses using each subject and its teachers at a glance."),
      ("subjects-05.jpg", "<b>Creating a subject.</b> Title, colour, study levels, books and the teachers assigned."),
      ("subjects-06.jpg", "<b>Safe deletion.</b> Before a subject is removed, the courses that use it are listed."),
      ("subjects-08.jpg", "<b>Adding to a course.</b> Teachers pick subjects from the shared areas, with a level for each."))}

{h2("03 — Decision 2", "One decision about who teaches what")}
<p>A school may run dozens of courses, and the same teacher often teaches the same subject in many of them. The coordinator had to invite each teacher to each course by hand, and keep track of who was where.</p>
<p><strong>The new rule:</strong> the coordinator assigns a teacher to a subject once, and the platform works out which courses they need to be in.</p>
<ul>
<li><strong>A subject is added to a course:</strong> its teacher is invited automatically. I changed this from an optional invite to a mandatory one, because a course teaching Mathematics without its Mathematics teacher is broken.</li>
<li><strong>The subject has no teacher yet:</strong> it still joins the course, so the coordinator isn’t blocked while staffing is being decided.</li>
<li><strong>A teacher is assigned later:</strong> the system shows every course that uses the subject and offers to invite the teacher to all of them at once.</li>
</ul>
<p>This also solves the coordinator’s leave problem: assigning a new teacher to the subject reaches every course that uses it. <strong>One change instead of eight.</strong></p>
{figs(("subjects-09.jpg", "<b>Teachers follow the subject.</b> Adding a subject to a course invites its teachers in the same step."), cls="one")}

{h2("04 — Decision 3", "Books and exams follow the subject")}
<p>Once subjects lived outside courses, books and exams could be linked to them too. So adding a subject to a course could bring its content along.</p>
{opts(("no", "Add everything automatically.", "Fast, but teachers would lose control over their own course."),
      ("yes", "Ask one clear question at a time:", "“This subject has books. Do you want to add them to the course?” The same for exams. Nothing is added without the teacher’s say."))}
<p>The same logic reaches down to lectures: when a subject with books is assigned to a lecture, the teacher can add all of them, choose some, or skip. A fully built subject, with its teacher, books and exams, can now be added to a new course <strong>in one action</strong>.</p>
{figs(("subjects-10.jpg", "<b>One question at a time.</b> The course can inherit the subject’s books, or not."),
      ("subjects-07.jpg", "<b>Down to the lecture.</b> The subject’s book appears in the lecture with its page range."))}

{h2("05 — Decision 4", "One home for education content")}
<p>Subject Areas, Book Libraries and Exam Collections work exactly the same way: reusable, linked, with the same roles.</p>
{opts(("no", "Three separate places in the navigation, one for each.", ""),
      ("yes", "One Education tab,", "where teachers land once and branch into subjects, books or exams."))}
{hub("INFORMATION ARCHITECTURE", ("Education", "one tab in settings and navigation"), [("Subject Areas", "subjects, teachers, study levels"), ("Book Libraries", "books, details, page ranges"), ("Exam Collections", "exams, questions, templates")], [("Course", "uses subjects, books, exams"), ("Lecture", "subject + book pages + exam"), ("Student", "sees only what’s assigned")], "All three share the same four roles: Owner, Curator, Editor, Viewer.")}
<p>That’s what makes them feel like one system instead of three tools. And it made the other features possible: the Book Library’s subject links and the exams’ subject context both depend on subjects living outside courses.</p>

{h2("06 — The result", "Set up once, reused everywhere")}
{metrics((arrow("8", "1"), "changes to replace a teacher across 8 courses", ""),
         ("Auto", "teacher invitations, instead of course by course by hand", ""),
         ("3", "organisational edge cases handled by the system", "late assignment · leave · invite to all"))}
<ul>
<li><strong>Subject setup:</strong> from once in every course to once in total, reused everywhere.</li>
<li><strong>Teacher calendar:</strong> from every lecture of the course to only their own lessons.</li>
</ul>
<div class="learned reveal"><span class="kicker" style="color:#888">What I learned</span>
<p class="big">The most useful change a designer can make isn’t always on the screen. Sometimes it’s the structure underneath.</p>
<p>Teachers asked for one thing: to find their own lectures. Everything else was friction I uncovered by mapping the full workflow, from subject to teacher to book to exam to course, and designing the system to absorb it.</p></div>
'''

# ---------------------------------------------------------------- BOOKS
books_body = f'''
{process("Workflow audit", "Data model with the PM", "Flows & UI", "Maze testing", "Shipped")}
{h2("01 — The problem", "Books were just attachments")}
<p>Before the Book Library, a “book” on Aladia was just a file attached to a lecture. If a teacher needed the same textbook in three courses, they uploaded it three times. The copies had no link to each other, no details, and no connection to their subject. When the book was updated, the teacher had to remember every place it lived, and they always missed at least one.</p>
<div class="quote">“I have the same PDF uploaded 12 times across my courses. When I update it, I always forget at least one.”<cite>Department head with over 200 teaching PDFs</cite></div>
<h3>How I found the problem</h3>
<p>I audited the existing workflow, mapped with the PM how books relate to subjects, teachers and courses, and watched teachers try to share one book across three courses. Every time, they uploaded a new copy.</p>
{opts(("no", "A better upload button.", "It would make uploading faster, but teachers would still create copies."),
      ("yes", "Make books real objects on the platform,", "living in a central library with their own details, subjects and team roles. Create once, link to any course."))}
<p>This meant designing a <strong>new data model before any screen</strong>, following the same structure as Subject Areas and Exam Collections: library → book → course → lecture → page range.</p>
{chain("DATA MODEL", [("Book Library", "shared, with roles"), ("Book", "PDF, link or written"), ("Course", "links the book"), ("Lecture", "picks a page range"), ("Reader", "opens at those pages")], "One book in the library; every lecture points to a different part of it.")}

{h2("02 — Decision 1", "One place, one set of rules")}
<p>Books, subjects and exams all work in a similar way and connect to each other. If each had its own place and its own rules, teachers would have to learn three systems.</p>
{opts(("no", "A separate section for books, with its own permissions.", ""),
      ("yes", "Book Libraries in the Education tab,", "next to Subject Areas and Exam Collections, with the same four roles: Owner, Curator, Editor and Viewer."))}
<p><strong>Why:</strong> a teacher who understands one understands the others. And when someone can’t do something because of their role, the action simply isn’t there, which makes the role system feel natural instead of bureaucratic.</p>
{figs(("books-03.jpg", "<b>Education group.</b> Subjects, books and exams sit together in settings and navigation."), cls="one")}

{h2("03 — Decision 2", "Three paths, one form")}
<p>Teachers don’t all have books in the same form. Some have a PDF, some can only point to a book for sale, and some write their own material. <strong>Add New Book</strong> opens with three paths that all lead to the same form:</p>
<ul>
<li><strong>Upload a PDF:</strong> the most common case.</li>
<li><strong>Attach a purchase link:</strong> for copyrighted books that can’t be shared as files. The teacher adds the ISBN and a link, and students see exactly which book to buy instead of nothing.</li>
<li><strong>Create it manually:</strong> for teachers writing their own material.</li>
</ul>
<h3>Three small decisions that removed friction</h3>
<ul>
<li><strong>Cover images:</strong> asking teachers to make a cover for every book would stall the flow. The system shows the first five pages of the PDF, and the teacher picks one as the cover with a single tap.</li>
<li><strong>Writing a book:</strong> instead of a new editor just for books, I reused the Document Builder, the same editor used for exams. AI sits inline on each block, like in Notion, not in a separate mode, so the teacher stays the author.</li>
<li><strong>Book details:</strong> teachers can type them in, or search by ISBN and have everything fill in automatically. Most teachers already know the ISBN of their books, so this became the most used route: <strong>48% of books</strong> were added this way.</li>
</ul>
{figs(("books-05.jpg", "<b>Three kinds of book.</b> PDF, purchase link, AI-generated and manually added books, each labelled."),
      ("books-06.jpg", "<b>One form.</b> ISBN search fills in the details; books link to a subject and level."),
      ("books-07.jpg", "<b>Writing a book.</b> The Document Builder with AI inline, the same editor teachers know from exams."), cls="three")}

{h2("04 — Decision 3", "Let the connections come to the teacher")}
<p>A book belongs to a subject, and a subject can have its own teacher. When adding a book to a course, teachers had to remember all these connections, and they usually didn’t.</p>
{opts(("no", "Leave it to the teacher", "to add the related subject and invite the right people by hand."),
      ("yes", "Ask at the right moment,", "with one question at a time the teacher can accept or skip."))}
<ul>
<li>“This book belongs to a subject. Should that subject be added to the course too?”</li>
<li>“That subject has a teacher. Should they be invited?”</li>
</ul>
<p><strong>Page ranges per lecture:</strong> a textbook covers a whole year, but one lecture covers a few pages. So the teacher sets a page range for each lecture: chapter three this week, chapter four next. The book lives in the library once, and each lecture points to a different part of it.</p>
{figs(("books-08.jpg", "<b>Connections on request.</b> Adding a book offers to add its subjects and invite their teachers."),
      ("books-09.jpg", "<b>Page ranges.</b> Each lecture points to its own pages of the same book."),
      ("books-10.jpg", "<b>In the lecture.</b> The book and its companion volume, with the assigned pages."),
      ("books-11.jpg", "<b>Recurring events too.</b> Books can be attached to a whole series of live sessions."))}

{h2("05 — What the student sees", "The right reading, already in the lecture")}
<p>All of this structure leads to one simple result for the student: the lecture page. Every book assigned to the lecture appears there, and opening it launches the built-in reader <strong>directly at the assigned pages</strong>.</p>
{opts(("no", "Before:", "a 300-page PDF and a separate message saying which chapter to read."),
      ("yes", "Now:", "the teacher’s decision arrives already applied."))}
{figs(("books-12.jpg", "<b>Books in the lecture.</b> Each book shows the page ranges assigned for this lesson."),
      ("books-13.jpg", "<b>Book details.</b> Description, language, length and its companion volumes."),
      ("books-14.jpg", "<b>The reader.</b> Opens at the assigned pages, with a banner saying who assigned them."), cls="three")}

{h2("06 — The result", "A new part of the platform")}
{research("Unmoderated Maze tests on the Aladia platform · 50 participants across 4 flows", [("Book upload usability score", "62", "81")])}
{metrics((arrow("62", "81"), "usability score for book upload", "Maze usability test"),
         ("48%", "of books added through ISBN search, the fastest route", ""),
         (arrow("12", "1"), "copies of the same book a teacher maintains", ""))}
<p>The Book Library shipped as a completely new part of the platform, connected to courses, lectures, subjects, calendar events and live sessions.</p>
<div class="learned reveal"><span class="kicker" style="color:#888">What I learned</span>
<p class="big">For something new, the concept has to come before the interface.</p>
<p>I had to create the mental model, the navigation and the permissions at the same time. Once the structure was clear, every screen could follow from it. And a good default does more than a good form: one optional ISBN field saved more effort than any layout change could have.</p></div>
'''

# ---------------------------------------------------------------- CONNECTA
connecta_body = f'''
{process("Product-wide audit", "Role-based views", "Setup wizard", "Studio & AI flows", "Website & portal", "Coded prototype")}
{h2("01 — The problem", "“No-code” doesn’t mean simple")}
<p>Behind every connection there is data mapping, sync schedules, retries and conditions between systems that don’t naturally agree. The product showed all of this to everyone, all the time. <strong>A tool built to save people time made them feel they needed a developer.</strong></p>
<h3>Who it affected</h3>
<ul>
<li><strong>Business owners</strong> want a quick answer: is everything working?</li>
<li><strong>Developers and admins</strong> need enough detail to fix what’s broken, fast.</li>
</ul>
<p>And for both of them, simply connecting a new app meant going through the full flow builder, the most complex part of the product.</p>
<h3>How I found the problem</h3>
<p>As the only designer, I worked across the whole product instead of one feature, so I could see the same pattern everywhere:</p>
<ul>
<li>the same data appeared in three overlapping views, and none of them worked well for either user;</li>
<li>a simple task (connecting Shopify) required the most advanced tool in the product;</li>
<li>the setup form had so many fields that it broke the layout it lived in.</li>
</ul>
<div class="callout">The problem wasn’t too many features. It was that <b>simple and advanced tasks were mixed together</b>, and everyone saw everything.</div>
{proto("The redesigned Connecta, working in code", "A clickable prototype of the final UI from Figma, built in code and responsive: switch between desktop and mobile to see the same product on both.", "proto-connecta.jpg", "https://claude.ai/artifact/H5VD7nLN5CXi5Qm6ckoTqT", tag="CODED PROTOTYPE")}

{h2("02 — Decision 1", "Two views of the same data")}
{opts(("no", "One dashboard for everyone.", "It would do both jobs badly: too technical for owners, not detailed enough for developers."),
      ("no", "Keep the technical dashboard and add explanations for owners.", "Owners would still have to dig through errors and settings they don’t need."),
      ("yes", "Two views over the same data,", "each built for one kind of user."))}
<ul>
<li><strong>Management view</strong> is calm and read-only. It shows whether everything is connected and healthy, with nothing to configure.</li>
<li><strong>Development view</strong> is built for the people doing the work. Repeating errors are grouped instead of flooding the list, records can be filtered, and every issue has retry, retry all and retry selected, plus a shortcut to the source record in Odoo.</li>
</ul>
<p>When an app doesn’t support retries, the button appears <strong>disabled</strong> instead of hidden, so the limitation is visible instead of mysterious. My rule across products: <strong>hide what your role can’t do, disable what the system can’t do.</strong></p>
{figs(("connecta-02.jpg", "<b>Management view.</b> Is everything working? Today’s syncs, failures and what changed since the last visit."),
      ("connecta-03.jpg", "<b>Development view.</b> Errors by app, top error types and active errors to fix."))}

{h2("03 — Decision 2", "Taking setup out of the flow builder")}
<p>Connecting a new app meant going through the full flow builder. It’s powerful, but far too much for someone who just wants to link Shopify and move on.</p>
{opts(("no", "Keep setup inside the flow builder.", "New users would have to understand the whole platform before creating a single connection."),
      ("yes", "A separate four-step wizard", "that starts with searching the app library."))}
<p><strong>A problem I found along the way:</strong> the connection-details step had so many fields that it broke the wizard’s sidebar layout. I kept only the essential fields and moved the rest into a collapsed <strong>Advanced settings</strong> section. The main path stays short, and the depth is still there for anyone who needs it.</p>
{chain("SETUP FLOW", [("Ensure app", "existing or new"), ("Connect", "search the library"), ("Authenticate", "6 methods"), ("Details", "essentials only"), ("Test & save", "ready to sync")], "Advanced settings stay collapsed in step 4, so the main path stays short.")}
{figs(("connecta-04.jpg", "<b>Step 1 — Ensure app.</b> Pick an app you already have, or create one."),
      ("connecta-05.jpg", "<b>Step 2 — Connect.</b> Search the library first; we prefill and test it for you."),
      ("connecta-06.jpg", "<b>Step 3 — Authentication.</b> Six methods described in plain language."),
      ("connecta-07.jpg", "<b>Step 4 — Details.</b> Only the essential fields, then test and save."))}

{h2("04 — Decision 3", "A canvas you can still read months later")}
<p>Connecta Studio is where the real logic gets built: a canvas where people connect blocks to define how data moves between systems, how fields map and what conditions apply. As flows grew, the screen became crowded, and people had to find a flow, open it and understand it again, often weeks later.</p>
{opts(("no", "Open Studio as a full page,", "taking over the whole product. Users would lose their place every time they edited a flow."),
      ("yes", "Open Studio as a slide-in overlay", "from a quieter button in the top bar, so people can edit a flow and return to where they were."))}
<ul>
<li>A <strong>Studio start page</strong> with Quick Create, recently closed tabs and a browse panel, so people get back to their work in one click.</li>
<li><strong>Redesigned canvas blocks</strong> and navigation, so a flow stays readable as it grows.</li>
<li>In the mapping tool, a <strong>field picker</strong> with drill-down navigation, a back button and required-field markers, and <strong>more than 70 functions</strong> organised into categories instead of one long list.</li>
</ul>
{figs(("connecta-08.jpg", "<b>Studio start page.</b> Start from a connection, mapping, endpoint or flow, with recent work one click away."),
      ("connecta-09.jpg", "<b>The canvas.</b> Clear blocks and structure, so a flow is readable months later."))}
<h3>Describe a flow, and AI drafts it</h3>
<p>From the same start page, people can describe what they need in plain words. Connecta AI builds a draft flow, lists every step it created, and saves it in Studio, where it stays fully editable. The person can open it on the canvas or ask for a change.</p>
{figs(("connecta-ai-1.jpg", "<b>Describe it.</b> Plain-language input with suggested starting points."),
      ("connecta-ai-2.jpg", "<b>Review the draft.</b> Each step the AI created is listed before opening the flow."))}

{h2("05 — Also designed", "The website, app store and customer portal")}
<p>Alongside the product, I designed Connecta’s public website. Instead of a standard SaaS landing page, I built the sections around <strong>puzzle pieces fitting together</strong>, a visual language for what the platform actually does: connecting separate systems into one.</p>
<p>The website also sells the product: an <strong>app store</strong> where each connector has its own details page, clear <strong>pricing</strong>, and a <strong>customer portal</strong> where customers and the Connecta team see the status of every installation.</p>
{figs(("connecta-10.jpg", "<b>App marketplace.</b> Featured and popular connectors with clear pricing."),
      ("connecta-11.jpg", "<b>App details.</b> What the app syncs in each direction, its pricing and what it needs to install."),
      ("connecta-13.jpg", "<b>Pricing.</b> Apps only, or the full platform configured to your plan."),
      ("connecta-14.jpg", "<b>Customer portal.</b> Every customer project with its environments, versions, health and backups."))}

{h2("06 — The result", "Simple by default, powerful one click away")}
{metrics((arrow("3", "2"), "overlapping views became two role-based views", ""),
         ("4", "steps to a first working connection, shipped before a trade-fair deadline", ""),
         ("50+", "screens across 20 user flows, as the sole designer", ""))}
<p><strong>Constraints:</strong> I was the only designer on the product, and the setup wizard had to ship before a trade-fair deadline, so I prioritised the paths new customers would hit first.</p>
<p>Studio became easier to navigate and easier to read, even for flows built months earlier.</p>
<div class="learned reveal"><span class="kicker" style="color:#888">What I learned</span>
<p class="big">Making a technical product simple doesn’t mean removing its power. It means deciding who needs that power, and when.</p>
<p>Across every part of this project, the same principle held: show the simple path by default, and keep the complexity one click away.</p></div>
'''

CASES = [
    ("exam", "Exam Module", "Designing a complete exam system, from the first question to the final grade.",
     "cover-exam.jpg", "exam-01.jpg",
     "Aladia had no exam system: no builder, no proctoring, no grading. I designed the whole thing from a blank canvas: three exam formats, AI-assisted question creation, live proctored exams, and a grading model that works across courses with completely different scoring scales.",
     [("Role", "Product Designer, end to end"), ("Client", "Aladia"), ("Industry", "EdTech · B2B & B2C SaaS"), ("Platform", "Web, responsive + mobile"), ("Focus", "Live proctoring UX<br>Grading system design"), ("Outcome", "Exam creation 6 → 3.5 min")],
     exam_body, ("subjects", "Subject Areas", "Data model design · Permission systems", "cover-subjects.jpg")),
    ("subjects", "Subject Areas", "The decision that connected the platform: one shared subject, with its teacher, books and exams following it into every course.",
     "cover-subjects.jpg", "subjects-01.jpg",
     "Subjects on Aladia were rebuilt inside every course, and teachers had to be invited to each course by hand. I moved subjects into one shared Subject Area, so a subject is created once and reused everywhere, and its teacher, books and exams follow it into every course automatically.",
     [("Role", "Product Designer, end to end"), ("Client", "Aladia"), ("Industry", "EdTech · B2B & B2C SaaS"), ("Platform", "Web, responsive + mobile"), ("Focus", "Data model design<br>Permission systems"), ("Outcome", "Teacher changes 8 → 1")],
     subjects_body, ("books", "Book Libraries", "Content library design · In-lecture book reader", "cover-books.jpg")),
    ("books", "Book Libraries", "A book library built from scratch, so teachers upload a book once and use it everywhere.",
     "cover-books.jpg", "books-01.jpg",
     "Aladia had no concept of a book. Teachers could only attach files to individual lectures, one at a time. I designed a Book Library from zero: one place to upload, organise and reuse books across courses, lectures, subjects and live sessions.",
     [("Role", "Product Designer, end to end"), ("Client", "Aladia"), ("Industry", "EdTech · B2B & B2C SaaS"), ("Platform", "Web, responsive + mobile"), ("Focus", "Content library design<br>In-lecture book reader"), ("Outcome", "Upload usability 62 → 81")],
     books_body, ("connecta", "Connecta", "Role-based dashboards · Setup wizard design", "cover-connecta.jpg")),
    ("connecta", "Connecta", "Making complex data integrations simple for people who don’t write code.",
     "cover-connecta.jpg", "connecta-01.jpg",
     "Connecta is a no-code integration platform built inside Odoo. It connects apps like Shopify, Bol.com, Exact Online and Magento, so businesses can sync their data without writing code. I designed the whole product: dashboards, setup flow, flow builder and marketing site.",
     [("Role", "Sole Product Designer"), ("Client", "Connecta Software"), ("Industry", "No-code integration · B2B SaaS"), ("Year", "2026"), ("Focus", "Role-based dashboards<br>Setup wizard design"), ("Outcome", "50+ screens, 20 flows")],
     connecta_body, ("exam", "Exam Module", "Live proctoring UX · Grading system design", "cover-exam.jpg")),
]

WORKS = [
    ("exam", "Exam Module", ["Live proctoring UX", "Grading system design"], "cover-exam.jpg", ""),
    ("subjects", "Subject Areas", ["Data model design", "Permission systems"], "cover-subjects.jpg", "right"),
    ("books", "Book Libraries", ["Content library design", "In-lecture book reader"], "cover-books.jpg", ""),
    ("connecta", "Connecta", ["Role-based dashboards", "Setup wizard design"], "cover-connecta.jpg", "right"),
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
        f'<div class="stat">{dots()}<div class="stat-num" data-count="{n}" data-suffix="{s}">0{s}</div><h3>{t}</h3><p>{d}</p></div>'
        for n, s, t, d in STATS)
    steps = "".join(
        f'<div class="step"><div class="step-top"><span>{k}</span>{dots()}</div><div><h3>{t}</h3><p>{d}</p></div></div>'
        for k, t, d in STEPS)
    works = "".join(
        f'''<div class="work {side}"><a href="#{slug}">
      <div class="work-media"><img src="img/{img}" alt="{title} case study" loading="lazy"></div>
      <div class="work-meta"><div><div class="work-num">0{i+1} / 04</div><h3>{title}</h3><span class="view-case">VIEW CASE STUDY →</span></div><div class="tags">{"<br>".join(tags)}</div></div>
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
        <div class="portrait-stage"><div class="portrait" style="transform:rotateY(180deg)">
          <img class="front" src="img/portrait-color.jpg" alt="Donya Yarahmadi">
          <img class="back" src="img/portrait-bw.jpg" alt="">
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
        <div class="approach-img"><img src="img/approach.jpg" alt="Sketching a user flow on paper" loading="lazy"></div>
        {steps}
      </div>
      <div class="approach-foot"></div>
    </div>
  </section>

  <div class="frame">
    <div class="cs-split"><div class="sticky"><span class="word l">Case</span><span class="word r">studies</span></div></div>
    <div class="works-head" id="work">
      <div><span class="eyebrow">Selected works <span class="count">(04)</span></span><h2>Complex products, made simple to use</h2></div>
      <p>Every project here started with the same question: <b>how do you make something complex feel simple?</b></p>
    </div>
    <div class="works">{works}</div>

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
    <div class="footer-links"><small>EMAIL</small>donyayarahmadi@outlook.com</div>
    <div class="footer-links"><small>ELSEWHERE</small><a href="https://www.linkedin.com/in/donya-yarahmadi-a0b804235/" target="_blank" rel="noopener">LinkedIn ↗</a><br><a href="https://calendly.com/donyarahmadi/30min" target="_blank" rel="noopener">Book a call ↗</a></div>
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
