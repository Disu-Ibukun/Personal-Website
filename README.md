# Disu Ibukunluwa Raheemat — Personal Portfolio

A minimalist, editorial portfolio for an emerging Data Engineer. **This is a functioning static site**, not a mockup. It's deliberately built with HTML, CSS, a few lines of vanilla JavaScript, and a Python standard-library generator; there are **no npm packages, databases, paid services, or API keys**.

## What is ready

- Responsive single-page portfolio: introduction, About, Quidax experience, projects, student leadership, entrepreneurship, education, contact.
- Mobile navigation, skip link, keyboard focus styling, motion preferences, fast static assets, favicon, 404 page, share-preview image, metadata.
- A reusable, static, search-engine-friendly project case-study generator that creates a dedicated URL **only when a real project has been documented and published**.
- One central editable content file: `content/site.json`.
- Cloudflare Pages-compatible build script: `python3 build.py` → `dist/`.

## What's deliberately not published yet

No fake links or achievements were added. This first version needs your **actual professional email, LinkedIn, GitHub, CV PDF, headshot, internship responsibilities, tools, and project architecture/results**. When those are supplied, the site automatically enables the relevant links and project pages. Until then, the contact section gives an honest note and the project has a 'case study in preparation' label.

**Important:** The supplied brief spells the name `Disu Ibukunluwa Raheemat` and lists the Quidax internship as **March–September 2026**. Review these and other details before publishing. No CV or portrait was supplied.

## Folders

| Path | Purpose |
|---|---|
| `content/site.json` | **Your one-stop edit file** for text, dates, links, experiences, projects, education. |
| `build.py` | Generates the public site from your content, with automatic checks. |
| `public/assets/style.css` | Design system: fonts, colours, sections, responsive styles. |
| `public/assets/main.js` | Mobile menu, subtle scroll reveal, year. |
| `public/assets/favicon.svg` | Browser tab icon. |
| `public/assets/og-cover.png` | Social-share preview. |
| `dist/` | **Output to publish**. Rebuilt automatically on Cloudflare Pages. |
| `content/CASE_STUDY_GUIDE.md` | Exactly how to add/publish a detailed project. |
| `tests/test_site.py` | Built-in quality checks. |

## Try it on your Windows computer

1. Download this ZIP and extract it. Open the resulting `disu-portfolio` folder in VS Code or File Explorer.
2. Install Python from [python.org/downloads](https://www.python.org/downloads/) if you don't have it. On Windows, during installation, select **Add Python to PATH**.
3. Open PowerShell in this folder (in File Explorer, click the address bar, type `powershell`, then press Enter).
4. Run these commands one at a time:

```powershell
py build.py
py -m http.server 8000 --directory dist
```

5. Open **http://localhost:8000/** in a browser. Edit content, run `py build.py` again, and refresh the browser. Press `Ctrl+C` in PowerShell when you're finished.

Mac/Linux alternative: replace `py` with `python3`.

### No Python on your computer?

That's fine if you only want to publish or update text via GitHub: Cloudflare can run the build for you on every push. You only need Python locally for a local preview.

## Publish for free with GitHub + Cloudflare Pages

No purchase or credit card is needed for a basic static Pages site. The URL will look like `https://your-chosen-name.pages.dev`.

### Faster one-time option (without GitHub)

If you only want to preview a live version quickly, use the separate `disu-portfolio-direct-upload.zip` deliverable. In Cloudflare **Workers & Pages → Create application → Pages → Drag and drop your files**, select that ZIP and deploy. The site goes live on a free `*.pages.dev` subdomain. **Important limitation:** Cloudflare cannot later convert that specific Direct Upload project to Git integration. For effortless automatic updates, prefer the GitHub-connected method below and create that project directly. The Direct Upload ZIP is already built; it does not need Python or build commands.

**Recommended ongoing workflow: GitHub integration**

**Part A — Put the project on GitHub**

1. Create a free [GitHub](https://github.com/) account if necessary.
2. Install [GitHub Desktop](https://desktop.github.com/) and sign in.
3. Choose **File → Add local repository** and select the extracted `disu-portfolio` folder. If it says the folder is not a Git repository, choose **create a repository here**.
4. Give the repository a name like `disu-portfolio`.
5. Click **Publish repository**. You may choose **Private** while preparing, but confirm your Cloudflare account can access the repository. Avoid uploading personal or secret material.

**Part B — Connect Cloudflare Pages**

1. Create or sign into your free [Cloudflare account](https://dash.cloudflare.com/).
2. In the dashboard, open **Workers & Pages**, select **Create**, choose **Pages**, then **Connect to Git** / **Import an existing Git repository**.
3. Authorise GitHub and select your `disu-portfolio` repository.
4. Under **Build settings**, enter exactly:

   - **Framework preset:** None
   - **Build command:** `python3 build.py`
   - **Build output directory:** `dist`
   - **Root directory:** leave as repository root
   - **Production branch:** `main`

5. Choose a project/subdomain name. Press **Save and Deploy**.
6. When Cloudflare says the deployment succeeded, open the assigned `*.pages.dev` URL and check it on your phone as well.

These settings are based on Cloudflare Pages' supported Python build environment. If its dashboard wording changes, look for the equivalent *Pages → Connect to Git* workflow.

**Part C — Add your real URL for sharing/search engines**

When the site has a real `https://...pages.dev` URL, paste it into the `identity.site_url` field in `content/site.json`. Save, commit, and push using GitHub Desktop. The next deployment will include an absolute canonical URL, OG image URL and `sitemap.xml`.

**Part D — Update the site later**

Open `content/site.json`, make an edit, save it, then open GitHub Desktop → enter a short summary like `Update education` → **Commit to main** → **Push origin**. Cloudflare automatically rebuilds the website. You can also edit `site.json` directly on GitHub; every saved commit to `main` triggers a redeploy.

## Your most common changes

| I want to… | Edit this field or file |
|---|---|
| Add my professional email | `identity.email` — it creates a working Email me button |
| Add LinkedIn / GitHub | `identity.linkedin` and `identity.github` — include `https://` |
| Add my CV | Put the PDF at `public/assets/cv.pdf`, set `identity.cv_file` to `assets/cv.pdf` |
| Add my headshot | Put JPG/PNG/WebP at `public/assets/portrait.jpg`, set `identity.portrait_file` to `assets/portrait.jpg` |
| Change the internship details | `work.description`, `work.dates`, `work.role` |
| Update leadership roles | Entries in `leadership` |
| Update business descriptions | Entries in `businesses` |
| Add a course/certification | Add an object to `education` (do not mark incomplete training 'certified') |
| Change your introduction | `hero` and `about` |
| Add a real project case study | `projects` array plus `content/CASE_STUDY_GUIDE.md` |
| Change colours | First 12 lines of `public/assets/style.css` |
| Change site address | `identity.site_url` |

**Image tip:** Use a real cropped 4:5 portrait, ideally at least 800×1000 px, compressed to WebP or JPEG under ~350 KB. Keep it professional and never commit an unlicensed photo.

## Publishing a project

Your project object stays with `"published": false` until the write-up is accurate. To publish, supply a factual `summary`, `challenge`, `approach` paragraphs, `decisions` objects, `outcomes`, and `lessons`, then set `"published": true`. Running `build.py` makes `/projects/project-slug/` and a clickable link on the homepage. The generator stops with a clear error if required facts are missing. Optional sections: `architecture`, `quality`, `stack`, `github_url`, and `image_file`.

## Quick checks / troubleshooting

Run:

```powershell
py -m unittest discover -s tests -v
py build.py
```

- **My edits don't appear:** did you save `site.json`, commit/push to GitHub, and wait for the new deployment to finish? Locally, rerun `py build.py` then refresh.
- **A link is missing:** empty links and missing files are intentionally hidden. Fill the field and upload the actual file.
- **A project doesn't open:** its `published` flag is probably `false`, or validation stopped the build. Complete real data first.
- **The site shows a 404 or CSS is missing:** confirm Cloudflare's **Build output directory** is exactly `dist` (without a slash), then redeploy.
- **JSON syntax error:** string values need double quotes and each field needs a comma except the last one. VS Code highlights errors in JSON.
- **Fonts aren't loading:** the site still works using system fallbacks; check network access to Google Fonts. The chosen free fonts are Instrument Serif and DM Sans.
- **Open Graph / social image missing:** set `identity.site_url` to your real https URL, then redeploy. Social platforms may cache older preview versions.
- **Want to customise more:** You can ask an AI coding assistant to change layout or add sections, but keep `site.json` as the single source of truth and run the tests again.

## Design rationale

The site prioritises recruiter scanning over decorative complexity. Single-page navigation provides immediate access to Quidax, technical work, and contact; deeper case-study pages appear only when there is evidence to read. Serif display typography adds warmth; small sans-serif text ensures legibility. Sage and navy are used for hierarchy and restraint, not as decoration. No fabricated metrics, placeholder social accounts, or fake contact form are included.

## Source verification

The **organisation-level context** was checked against official sites, but none of their general claims is presented as your own achievement:

- Quidax: https://www.quidax.io/c/about-us/
- Millennium Fellowship: https://www.millenniumfellows.org/impact
- Cloudflare Pages Python build documentation: https://developers.cloudflare.com/pages/configuration/build-image/
- Cloudflare Pages static hosting: https://developers.cloudflare.com/pages/framework-guides/deploy-anything/

The portfolio's personal claims are taken from the supplied brief only and should be reviewed before public launch.
