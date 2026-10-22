#!/usr/bin/env python3
"""Tiny, dependency-free, escaped HTML generator for Disu's portfolio."""
from __future__ import annotations

import html
import json
import os
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

BASE = Path(__file__).resolve().parent
SOURCE = BASE / 'content' / 'site.json'
ASSETS = BASE / 'public'
DIST = BASE / 'dist'


def e(value: object) -> str:
    return html.escape(str(value if value is not None else ''), quote=True)


def valid_url(url: str) -> bool:
    p = urlparse(url)
    return p.scheme in {'https', 'http'} and bool(p.netloc)


def safe_path(path: str) -> str:
    """Accept only existing files in public/ with a safe relative URL."""
    if not path or path.startswith('/') or '\\' in path or '..' in Path(path).parts:
        return ''
    target = (ASSETS / path).resolve()
    if not target.is_relative_to(ASSETS.resolve()) or not target.is_file():
        return ''
    return path


def attr_url(url: str) -> str:
    return e(url) if valid_url(url) else ''


def icon_arrow() -> str:
    return '<span class="arrow" aria-hidden="true">↗</span>'


def content_link(label: str, href: str, *, secondary=False, external=False) -> str:
    if not href:
        return ''
    target = ' target="_blank" rel="noopener noreferrer"' if external else ''
    klass = 'secondary' if secondary else ''
    return f'<a class="{klass}" href="{e(href)}"{target}>{e(label)} {icon_arrow()}</a>'


def header(home=True):
    prefix = '' if home else '/'
    return f'''<header class="site-header" id="top">
      <div class="site-shell header-inner">
        <a class="wordmark" href="{prefix}#top" aria-label="Disu Ibukunoluwa Raheemat — Home">
          <span class="monogram" aria-hidden="true">D.</span>
          <span class="brand-name">Disu Ibukunoluwa<span class="brand-role">Emerging Data Engineer</span></span>
        </a>
        <button class="nav-toggle" type="button" aria-label="Toggle navigation" aria-expanded="false" aria-controls="main-navigation" data-nav-toggle>
          <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
        </button>
        <nav id="main-navigation" class="nav-links" aria-label="Primary navigation" data-nav-menu>
          <a href="{prefix}#about">About</a><a href="{prefix}#education">Education</a>
          <a href="{prefix}#experience">Experience</a><a href="{prefix}#skills">Skills</a><a href="{prefix}#projects">Projects</a><a href="{prefix}#beyond">Leadership</a>
          <a class="nav-contact" href="{prefix}#contact">Get in touch ↗</a>
        </nav>
      </div>
    </header>'''


def section_index(number, name):
    return f'<aside class="section-index" aria-hidden="true"><span class="index-number">{e(number)}</span><span class="index-name">{e(name)}</span><span class="index-line"></span></aside>'


def head(data, title, description, *, path='/'):
    identity = data['identity']
    configured = identity.get('site_url', '').rstrip('/') or os.environ.get('CF_PAGES_URL', '').rstrip('/')
    canonical = f'<link rel="canonical" href="{e(configured + path)}">' if valid_url(configured) else ''
    og_image = e(configured + '/assets/og-cover.png') if valid_url(configured) else ''
    social_image = f'<meta property="og:image" content="{og_image}"><meta name="twitter:card" content="summary_large_image">' if og_image else ''
    return f'''<!doctype html><html lang="en"><head>
      <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
      <meta name="theme-color" content="#f8f8f4"><meta name="color-scheme" content="light">
      <title>{e(title)}</title><meta name="description" content="{e(description)}">
      <meta property="og:type" content="website"><meta property="og:title" content="{e(title)}">
      <meta property="og:description" content="{e(description)}">{social_image}
      <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
      <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link rel="stylesheet" href="/assets/style.css">
      {canonical}
    </head><body><a class="skip-link" href="#main">Skip to content</a>'''


def footer(data):
    return f'''<footer class="footer"><div class="site-shell footer-inner">
    <span><strong>{e(data['identity']['short_name'])}</strong> · {e(data['footer']['note'])}</span>
    <span>© <span data-year>2026</span> · <a href="#top">Back to top ↑</a></span></div></footer>
    <script src="/assets/main.js" defer></script></body></html>'''


def render_hero(data):
    i, h = data['identity'], data['hero']
    portrait = safe_path(i.get('portrait_file', ''))
    if portrait:
        picture = f'<img src="/{e(portrait)}" alt="Professional portrait of {e(i["full_name"])}" width="640" height="800" decoding="async" fetchpriority="high">'
        picture_class = ' has-photo'
    else:
        picture = '''<div class="photo-no-image" aria-label="Reserved space for a future professional photograph">
            <span class="placeholder-glyph" aria-hidden="true">D.</span>
            <span class="placeholder-text">Portrait to be added</span></div>'''
        picture_class = ''
    title = e(h['headline']).replace('Ibukunoluwa.', '<em>Ibukunoluwa.</em>', 1)
    return f'''<section class="hero site-shell" aria-labelledby="hero-title">
      <div class="topline"><span>Disu Ibukunoluwa Raheemat / Selected work &amp; experience</span><span class="time-stamp">Portfolio · 2026</span></div>
      <div class="hero-layout">
        <div class="hero-copy"><div class="eyebrow">{e(i['role'])}</div>
          <h1 class="hero-title" id="hero-title">{title}</h1>
          <p class="hero-lead">{e(h['lead'])}</p>
          <p class="hero-secondary">{e(h['secondary'])}</p>
          <div class="action-row"><a href="#projects" class="link-strong">Explore my work {icon_arrow()}</a>
          <a href="#about" class="link-plain">A little about me <span class="arrow" aria-hidden="true">↗</span></a></div>
        </div>
        <div class="hero-aside"><div class="photo-canvas{picture_class}">{picture}
          <div class="photo-caption"><span>01 / The person</span><span>{e(i['location'])}</span></div>
          </div><div class="hero-meta"><span>{e(i['availability'])}</span><i aria-hidden="true"></i></div>
        </div>
      </div>
      <div class="facts" aria-label="Professional highlights">
        <div class="fact"><span class="fact-no">01</span><p>Computer Science graduate<small>First Class Honours · 2026</small></p></div>
        <div class="fact"><span class="fact-no">02</span><p>Experience at Quidax<small>Data internship · Fintech</small></p></div>
        <div class="fact"><span class="fact-no">03</span><p>Beyond engineering<small>Leadership · Operations · Business</small></p></div>
      </div>
    </section>'''


def render_about(data):
    a = data['about']
    heading_parts = a['heading'].split('. ', 1)
    about_heading = (e(heading_parts[0]) + '. <em>' + e(heading_parts[1]) + '</em>' if len(heading_parts)==2 else e(a['heading']))
    ps = [f'<p>{e(p)}</p>' for p in a['paragraphs']]
    midpoint = (len(ps) + 1) // 2
    return f'''<section id="about" class="section section-divider"><div class="site-shell section-grid">
      {section_index('01', 'A little about me')}
      <div data-reveal><h2 class="section-heading">About me</h2>
        <div class="section-prose"><div class="left-column">{''.join(ps[:midpoint])}</div>
        <div class="right-column">{''.join(ps[midpoint:])}</div></div>
      </div>
    </div></section>'''


def render_experience(data):
    rows = []
    for w in data['experience']:
        url = w.get('company_url', '')
        company = (f'<a href="{attr_url(url)}" target="_blank" rel="noopener noreferrer">{e(w["company"])}</a>'
                   if valid_url(url) else e(w['company']))
        rows.append(f'''<article class="experience-row">
          <span class="work-dates">{e(w['dates'])}</span>
          <div><h3 class="work-title">{company}</h3><p class="experience-role">{e(w['role'])}</p>
          <p class="work-description">{e(w['description'])}</p></div>
        </article>''')
    return f'''<section class="section ink-panel" id="experience"><div class="site-shell section-grid">
      {section_index('03', 'Experience')}
      <div data-reveal><h2 class="section-heading">Experience</h2>
      <div class="experience-list">{''.join(rows)}</div></div>
    </div></section>'''


def render_skills(data):
    sk = data['skills']
    rows = []
    for group in sk['groups']:
        rows.append(f'''<div class="skill-row"><h3>{e(group['label'])}</h3>
          <ul>{''.join(f'<li>{e(item)}</li>' for item in group['items'])}</ul></div>''')
    return f'''<section id="skills" class="section section-divider"><div class="site-shell section-grid">
      {section_index('04', 'Skills')}
      <div data-reveal><h2 class="section-heading">{e(sk['heading'])}</h2>
      <p class="skills-intro">{e(sk['intro'])}</p>
      <div class="skills-list">{''.join(rows)}</div></div>
    </div></section>'''


def render_projects(data):
    cards = []
    for num, p in enumerate(data['projects'], 1):
        published = p.get('published', False)
        heading = (f'<a href="/projects/{e(p["slug"])}/">{e(p["title"])}</a>' if published else e(p['title']))
        side = (f'<a class="project-open" href="/projects/{e(p["slug"])}/">Read case study ↗</a>' if published
                else '<span class="status-inline">Case study in preparation</span>')
        cards.append(f'''<article class="project-card"><div class="project-num">{num:02d}</div>
          <div><h3 class="project-title">{heading}</h3><p>{e(p['summary'])}</p></div>
          <div class="project-side"><span class="project-category">{e(p['category'])}</span>{side}</div>
        </article>''')
    return f'''<section id="projects" class="section"><div class="site-shell section-grid">
      {section_index('05', 'Projects')}
      <div data-reveal><div class="eyebrow">Technical projects</div>
        <h2 class="section-heading">Projects</h2>
        <p class="projects-lead">{e(data['projects_intro'])}</p>
        <div class="projects-list">{''.join(cards)}</div>
      </div>
    </div></section>'''


def render_leadership(data):
    rows=[]
    for item in data['leadership']:
        link = item.get('organisation_url', '')
        title = (f'<a href="{attr_url(link)}" target="_blank" rel="noopener noreferrer">{e(item["organisation"])}</a>'
                 if valid_url(link) else e(item['organisation']))
        rows.append(f'''<article class="leadership-item"><div><h3>{title}</h3>
          <p class="role-tag">{e(item['roles'])}</p></div><p>{e(item['description'])}</p></article>''')
    return f'''<section id="beyond" class="section section-divider"><div class="site-shell section-grid">
      {section_index('07', 'Community')}
      <div data-reveal><div class="eyebrow">Leadership & community</div>
        <h2 class="section-heading">Leadership &amp; Community</h2>
        <p class="projects-lead">Organising people, making decisions, and explaining ideas well have been important parts of my experience, too.</p>
        <div class="leadership-list">{''.join(rows)}</div>
      </div></div></section>'''


def render_business(data):
    cards=[]
    for idx, item in enumerate(data['businesses'], 1):
        note = f'<p class="business-note">{e(item["footnote"])}</p>' if item.get('footnote') else ''
        cards.append(f'''<article class="business"><span class="mini-index">{idx:02d}.</span>
          <h3>{e(item['name'])}</h3><p class="sub">{e(item['subtitle'])}</p>
          <p class="description">{e(item['description'])}</p>
          <div class="business-role">{e(item['role'])}</div></article>''')
    return f'''<section class="section section-divider" id="entrepreneurship"><div class="site-shell section-grid">
      {section_index('06', 'Entrepreneurship')}
      <div data-reveal><div class="eyebrow">A perspective shaped by practice</div>
        <h2 class="section-heading">Entrepreneurship</h2>
        <p class="projects-lead">Running and supporting online businesses has taught me to think about operations, customers, inventory, and how dependable information supports decisions.</p>
        <div class="split-feature">{''.join(cards)}</div>
        
      </div>
    </div></section>'''


def render_education(data):
    cards=[]
    for idx, item in enumerate(data['education'], 1):
        cards.append(f'''<article class="education-card"><span class="overline">Learning / {idx:02d}</span>
          <h3>{e(item['institution'])}</h3><p class="qualification">{e(item['qualification'])}</p>
          <p class="status">{e(item['status'])}</p><p class="education-description">{e(item['description'])}</p></article>''')
    return f'''<section id="education" class="section education-wrap"><div class="site-shell section-grid">
      {section_index('02', 'Education')}
      <div data-reveal><div class="eyebrow">Education & development</div>
        <h2 class="section-heading">Education &amp; Development</h2>
        <div class="education-list">{''.join(cards)}</div>
      </div>
    </div></section>'''


def render_contact(data):
    i = data['identity']; links=[]
    if i.get('email') and re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', i['email']):
        links.append(content_link('Email me', 'mailto:' + i['email']))
    if valid_url(i.get('linkedin', '')):
        links.append(content_link('LinkedIn', i['linkedin'], secondary=True, external=True))
    if valid_url(i.get('github', '')):
        links.append(content_link('GitHub', i['github'], secondary=True, external=True))
    cv = safe_path(i.get('cv_file', ''))
    if cv and cv.lower().endswith('.pdf'):
        links.append(content_link('Download CV', '/' + cv, secondary=True))
    links_markup = '<div class="contact-links">' + ''.join(links) + '</div>' if links else ''
    pending_markup = ('<div class="contact-pending">Contact details will be added here once they are ready to share.</div>'
                      if not links else '')
    return f'''<section id="contact" class="contact"><div class="site-shell">
      <div class="contact-topline"><span>08 / Let’s connect</span><span>New conversations welcome</span></div>
      <h2 class="contact-title">Get in <em>touch.</em></h2>
      <p>I'm interested in early-career Data Engineering opportunities, thoughtful products, and conversations with people who care about building reliable systems.</p>
      {links_markup}{pending_markup}
    </div></section>'''


def render_home(data):
    i = data['identity']
    desc = ('Portfolio of ' + i['full_name'] + ', an emerging Data Engineer and First Class Computer Science graduate '
            'with experience across fintech, leadership, and entrepreneurship.')
    return (head(data, i['full_name'] + ' | Data Engineering & Beyond', desc)
            + header() + '<main id="main">'
            + render_hero(data) + render_about(data) + render_education(data)
            + render_experience(data) + render_skills(data) + render_projects(data)
            + render_business(data) + render_leadership(data) + render_contact(data) + '</main>' + footer(data))


def case_section(heading, body_html):
    return f'<section class="case-section"><h2>{e(heading)}</h2><div>{body_html}</div></section>' if body_html else ''


def render_case(data, project):
    i = data['identity']
    sections = [case_section('The challenge', f'<p>{e(project["challenge"])}</p>')]
    sections.append(case_section('Approach', ''.join(f'<p>{e(x)}</p>' for x in project['approach'])))
    if project.get('architecture'):
        sections.append(case_section('Architecture', f'<p>{e(project["architecture"])}</p>'))
    if project.get('decisions'):
        sections.append(case_section('Decisions & trade-offs', ''.join(
            f'<h3>{e(x["title"])}</h3><p>{e(x["body"])}</p>' for x in project['decisions'])))
    if project.get('quality'):
        sections.append(case_section('Reliability & quality', f'<p>{e(project["quality"])}</p>'))
    sections.append(case_section('Outcomes', f'<p>{e(project["outcomes"])}</p>'))
    sections.append(case_section('What I learned', f'<p>{e(project["lessons"])}</p>'))
    photo = safe_path(project.get('image_file', ''))
    photo_html = f'<img class="case-architecture" alt="Architecture or project illustration for {e(project["title"])}" src="/{e(photo)}" loading="lazy">' if photo else ''
    github_link = content_link('View repository', project.get('github_url', ''), external=True) if valid_url(project.get('github_url', '')) else ''
    return (head(data, project['title'] + ' | ' + i['short_name'], project['summary'], path='/projects/'+project['slug']+'/')
            + header(home=False)
            + f'''<main class="site-shell" id="main"><article class="case-main">
                <a class="breadcrumb" href="/#projects">← Back to projects</a>
                <div class="case-label">{e(project['category'])}</div>
                <h1 class="case-title">{e(project['title'])}</h1>
                <p class="case-intro">{e(project['summary'])}</p>
                <div class="case-stack">{''.join(f'<span>{e(s)}</span>' for s in project.get('stack', []))}</div>
                {photo_html}{''.join(sections)}
                <div class="case-back">{github_link}<p><a class="link-plain" href="/#projects">← Back to all projects</a></p></div>
              </article></main>''' + footer(data))


def validate(data):
    assert data['identity']['full_name'].strip(), 'Missing full name'
    seen=set()
    for p in data['projects']:
        slug=p.get('slug', '')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
            raise ValueError('Project slug must be lowercase hyphenated: '+repr(slug))
        if slug in seen:
            raise ValueError('Duplicate project slug: '+slug)
        seen.add(slug)
        if p.get('published'):
            required=['title','summary','challenge','outcomes','lessons']
            blank=[f for f in required if not p.get(f)]
            if not p.get('approach') or not p.get('decisions'):
                blank.extend(['approach / decisions'])
            if blank:
                raise ValueError(f'Cannot publish {slug}; provide real data for: {", ".join(blank)}')
    return True


def build():
    data=json.loads(SOURCE.read_text(encoding='utf-8'))
    validate(data)
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ASSETS, DIST)
    (DIST/'index.html').write_text(render_home(data), encoding='utf-8')
    (DIST/'404.html').write_text(head(data, 'Page not found | '+data['identity']['short_name'], 'Page not found') + header(home=False)
          + '<main id="main" class="site-shell not-found"><h1>404.</h1><p>That page seems to have taken a different route.</p><a class="link-strong" href="/">Back to the homepage ↗</a></main>' + footer(data), encoding='utf-8')
    for p in data['projects']:
        if p.get('published'):
            route=DIST/'projects'/p['slug']
            route.mkdir(parents=True, exist_ok=True)
            (route/'index.html').write_text(render_case(data, p), encoding='utf-8')
    configured = data['identity'].get('site_url', '').rstrip('/') or os.environ.get('CF_PAGES_URL', '').rstrip('/')
    pages=['/']+[f'/projects/{p["slug"]}/' for p in data['projects'] if p.get('published')]
    if valid_url(configured):
        xml='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        xml+=''.join(f'<url><loc>{e(configured + path)}</loc></url>' for path in pages)+'</urlset>'
        (DIST/'sitemap.xml').write_text(xml, encoding='utf-8')
        (DIST/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+configured+'/sitemap.xml\n', encoding='utf-8')
    else:
        (DIST/'robots.txt').write_text('User-agent: *\nAllow: /\n', encoding='utf-8')
    print('Built', len(pages), 'public page(s) to', DIST)
    if not data['identity'].get('email'):
        print('Note: Contact links intentionally hidden until your email / profiles are provided.')
    if not data['identity'].get('site_url') and not os.environ.get('CF_PAGES_URL'):
        print('Note: Configure site_url after deployment for canonical / Open Graph image URLs.')


if __name__=='__main__':
    build()
