# CLAUDE.md

Guidance for AI agents working in this repository. Read this before changing anything.

## What this repo is

A data-driven resume and CV for Reza Rajan. One set of YAML data renders two documents through Hugo:

- **CV** at `/` (site home): the full record, a scrollable document page.
- **Resume** at `/resume/`: a strict one-page A4 sheet.

Both deploy to GitHub Pages; CI also prints both to PDF (`/cv.pdf`, `/resume.pdf`) with headless Chrome and publishes them as workflow artifacts. **PDF renders are never tracked in git.**

## Structure

```
hugo/
  hugo.toml                  site config; resume section order lives in params.pages.features
  data/
    experience.yaml          roles; resume bullets in `details`, CV extras in `cv_details`,
                             one-line role descriptions in `context`, `cv_only: true` hides
                             an entry from the resume (historical roles)
    education.yaml           entries; `honors`, `cv_only` supported
    features.yaml            about (summary), skills groups, certificates
    courses.yaml             CV-only courses section
  layouts/
    home.html                CV page template
    _default/resume.html     resume page template
    partials/                header, section renderers, theme-slider, doc-actions,
                             pdf-modal, theme-script (scheme), nav-script (scroll-spy)
  assets/css/
    _tokens.scss             THE palette + dark-scheme/focus-ring mixins; all colors live here
    cv.scss                  CV page styles (screen + print)
    custom.scss              resume overrides (Harvard format, zoom, dark mode)
    _theme-slider.scss, _doc-actions.scss, _pdf-modal.scss   shared components
    _layout.scss, _section.scss, _redundant.scss   shadow theme files (resume paper)
  static/certificates/       certificate PDFs (tracked); favicon.svg
  themes/resume-a4/          git submodule; never edit, shadow files instead
scripts/generate-pdfs.sh     local PDF pre-render into hugo/static/ (gitignored)
scripts/qa/browser_qa.py     behavioral QA suite (CDP, stdlib-only); run it
.github/workflows/hugo.yaml  build, PDF generation, artifact upload, Pages deploy
```

## Commands

```bash
git submodule update --init          # once after cloning (theme)
cd hugo && hugo server               # dev server at :1313
cd hugo && hugo --gc --minify        # production build check (zero ERRORs expected)
./scripts/generate-pdfs.sh           # pre-render download PDFs locally (gitignored)
```

Versioning uses **jj** (colocated with git): `jj new -m "..."` to start work, `jj describe` to (re)word, `jj bookmark set main -r @ && jj git push --bookmark main` to publish. Never rewrite pushed commits; start a new change instead. Commit messages follow conventional style (`feat(site): ...`, `update(experience): ...`).

## Content rules

- **Experience bullets use the Google XYZ format**: accomplishment, then measurement, then method ("Cut rollouts from 3+ hours to <15 minutes with declarative Talos Linux IaC"). Every bullet carries a real measure unless explicitly agreed otherwise. 2-4 bullets per role on the resume.
- **No em-dashes in sentences.** No self-descriptive filler ("self-starter"). The summary is a single sentence.
- **The resume is one A4 page. Always.** Verify after any content change (see QA below).
- Resume bullets should render as one line each where possible (~100 characters); the flagship bullet per role may run two lines.
- Historical roles (Urban Shelter, BlueFire) and Naparima College are `cv_only` and must stay off the resume. The Ministry of Education role leads both documents.
- Certificate entries link into `static/certificates/`; template links use `absURL` so printed PDFs carry deployed URLs.

## Design rules

- **All colors come from `hugo/assets/css/_tokens.scss`.** Never hardcode palette values elsewhere. Current palette: neutral paper light (near-white #fafaf9, no yellow/cream cast), classic gruvbox dark (#282828), pine/sage green accent. The user rejected crimson, blue, and ivory/cream light schemes; do not reintroduce them.
- **Print output is monotone black-on-white**, both documents, regardless of screen palette. CV print must match the resume's structure (margins, type scale, inline skills, inside square markers).
- Both pages share the Harvard visual system: Times New Roman, centered name/contact header, ruled uppercase section headings, bold organization + right-aligned gray date + italic role. Content type sizes must stay identical between the pages.
- Desktop CV nav rail marks the active section with text color and the sliding indicator only (no pill background); the pill background belongs to the narrow sticky bar layout.
- Mobile: flush-left header stack, dates on their own line beneath entry titles, hanging-indent bullets. The theme slider and doc-actions pills float with safe-area offsets.
- Certificate links open the in-page PDF preview modal (`data-pdf-preview`), never a full navigation.
- Respect `prefers-reduced-motion` for any animation or smooth scrolling; keep `focus-visible` outlines; keep `aria-current` on the active nav link.

## Quality assurance

Before finishing any change that touches content, layout, styles, or scripts:

1. `cd hugo && hugo --gc --minify -d /tmp/whoami-check` completes with zero `ERROR` lines.
2. **Run the behavioral suite**: start `hugo server`, then `python3 scripts/qa/browser_qa.py <port>`. It asserts the interaction invariants below across desktop, portrait-mobile, and landscape-mobile viewports and exits non-zero on failure. Extend it when adding interactive behavior; a bug fixed without a new check tends to come back.
3. Print both pages with headless Chrome (`--virtual-time-budget=8000 --no-pdf-header-footer`):
   - resume prints to **exactly 1 page**; CV prints to its expected count (currently 2);
   - output is monotone; no localhost URLs in PDF link annotations.
   - A one-page check that works: render the printed PDF at 100dpi; the content bottom must stay above ~1125px of the 1170px page.
4. Screenshot sanity at desktop (1600px), portrait mobile (390px), **and landscape mobile (844x390)** — landscape sits between the mobile and desktop breakpoints and catches overlap bugs neither of the others shows. Check light and dark (force the scheme via CDP `Emulation.setEmulatedMedia`; headless defaults are environment-dependent).
5. If data or styles changed, run `./scripts/generate-pdfs.sh` so local downloads match.

## Interaction invariants (hard-won; keep them true)

- **Scroll-spy**: the active nav section is the last one whose anchor sits above a fixed line 25% down the viewport; only at true page bottom (within 2px of max scroll) does the last section take over. Do NOT reintroduce an interpolated/progress-based reading line: it activates sections that are merely visible lower in the viewport and fights nav clicks near the page bottom.
- **Nav clicks pin**: a click activates its section immediately and suppresses the spy until the scroll settles (`scrollend` where supported, timeout fallback), so bottom-clustered sections don't steal the highlight mid-flight.
- **One animator per gesture**: JS `scrollIntoView`/`scrollTo` do the smooth scrolling; CSS `scroll-behavior: smooth` must stay unset or the two animations compound into jank. Dedupe state changes before animating (the pill bar centers only when the active id actually changes; per-frame smooth scrolls queue and stutter).
- **Touch hover**: every `:hover` affordance (color, underline, background) must live inside `@media (hover: hover)`. On touch devices, a tap otherwise applies hover styles that stick until the next tap — the "still highlighted after scrolling away" bug class.
- **Breakpoints are coupled**: the CV nav becomes a sticky top bar below 88rem, and the floating controls move to the bottom corner at the same 88rem. If these ever diverge, landscape phones (between ~40rem and 88rem) get overlapping chrome.
- **Reduced motion**: every animation and smooth scroll checks `prefers-reduced-motion`.

## Testing gotchas

- Headless screenshots taken after fragment/anchor navigation can silently drop fixed-position layers or paint blank; drive real scrolls and reads over CDP instead (see `scripts/qa/browser_qa.py` for the stdlib WebSocket client pattern).
- CDP checks must **act, wait (~400ms), then read**: spy and hide/show handlers are rAF-throttled, so reading state in the same evaluate call as the action returns stale values.
- Launch test Chrome with `--force-prefers-reduced-motion` so scrolls are instant and deterministic.
- SCSS: CSS `min()`/`max()` with mixed units must be escaped from SCSS builtins (`#{"min(860px, 94vw)"}`); `env()` inside `max()` likewise.
- `pkill -f "hugo server"` kills the invoking shell (pattern matches its own command line); use `pkill -f "hugo serve[r]"` standalone.

## CI notes

- The workflow pins its own Hugo version; templates must stay compatible with it (avoid newly-renamed Hugo APIs; `.Site.Data` deprecation warnings are expected and harmless locally).
- PDF generation serves the built site under its base path via a symlink, prints with the runner's preinstalled `google-chrome`, filters benign dbus log noise, and fails if either PDF is missing or empty.
