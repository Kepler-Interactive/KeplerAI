# KeplerAI - Upstream Update Guide

This document provides instructions for updating the KeplerAI fork from the upstream [open-webui/open-webui](https://github.com/open-webui/open-webui) repository while preserving Kepler branding.

## Repository Setup

- **Origin:** `https://github.com/Kepler-Interactive/KeplerAI.git`
- **Upstream:** `https://github.com/open-webui/open-webui.git`

## Current Version

- **KeplerAI fork:** v0.11.1 (merged from upstream on 2026-08-31)
- **Based on:** open-webui v0.11.1

---

## Branding Files Reference

### Critical Branding Files (MUST preserve during every merge)

These are the files that control core user-visible branding. If upstream changes any of these, resolve conflicts in favor of KeplerAI values.

#### 1. Application Name Constants

| File                        | Line | Value                                              |
| --------------------------- | ---- | -------------------------------------------------- |
| `src/lib/constants.ts`      | 4    | `export const APP_NAME = 'KeplerAI';`              |
| `backend/open_webui/env.py` | ~932 | `WEBUI_NAME = os.getenv('WEBUI_NAME', 'KeplerAI')` |
| `package.json`              | 2    | `"name": "KeplerAI"`                               |

> Note: as of v0.11.0 upstream reformatted the backend to single-quoted strings and
> `os.getenv`. Grep for the symbol (`WEBUI_NAME`), not the old quoting style.

#### 2. HTML Meta Tags & Title

**File:** `src/app.html`

| Line | Element                                                         |
| ---- | --------------------------------------------------------------- |
| 26   | `<meta name="apple-mobile-web-app-title" content="KeplerAI" />` |
| 34   | `<meta name="description" content="KeplerAI" />`                |
| 38   | `title="KeplerAI"` (opensearch link)                            |
| 126  | `<title>KeplerAI</title>`                                       |

#### 3. PWA Manifest

**File:** `backend/open_webui/static/site.webmanifest`

```json
{
	"name": "KeplerAI",
	"short_name": "KeplerAI",
	"description": "KeplerAI - AI Assistant Platform",
	"theme_color": "#0066cc",
	"background_color": "#0066cc"
}
```

#### 4. OpenSearch XML

**File:** `static/opensearch.xml`

```xml
<ShortName>KeplerAI</ShortName>
<Description>Search KeplerAI</Description>
```

#### 5. Backend API & CLI

| File                                          | What                      | Value                                                  |
| --------------------------------------------- | ------------------------- | ------------------------------------------------------ |
| `backend/open_webui/main.py`                  | FastAPI title             | `title="KeplerAI"`                                     |
| `backend/open_webui/__init__.py`              | CLI version output        | `f"KeplerAI version: {VERSION}"`                       |
| `backend/open_webui/routers/openai.py`        | X-Title header            | `'X-Title': 'KeplerAI'`                                |
| `backend/open_webui/routers/notifications.py` | Push-target test fallback | `getattr(request.app.state, 'WEBUI_NAME', 'KeplerAI')` |

#### 6. Notification & Tab-Title Branding

Upstream switched the app-name separator from `•` to `/` in v0.11.0. KeplerAI follows
upstream's separator — keep the code change, swap only the name.

**File:** `src/routes/+layout.svelte` — three notification sites:

- Chat completion: `` `${data.title} / KeplerAI` ``
- Channel message (displayTitle): `` `${displayTitle} / KeplerAI` ``
- Channel message (title): `` `${title} / KeplerAI` ``

**File:** `src/lib/components/channel/Channel.svelte` — two `<title>` sites in `<svelte:head>`:

- DM title: `` `}, '')} / KeplerAI</title` ``
- Named channel: `#{channel?.name ?? 'Channel'} / KeplerAI`

#### 7. Auth Page Branding

**File:** `src/routes/auth/+page.svelte`

- Kepler purple background: `<div class="w-full h-full absolute top-0 left-0" style="background-color: #3924f6;">`
  (upstream ships `bg-white dark:bg-black` here)
- Spinning Kepler logo above the login card: `<img src="/keplerspin.gif" alt="KeplerAI" class="h-48 w-48 mb-4" />`
- Sign-in heading is the literal `KeplerAI` rather than upstream's
  `{$i18n.t('Sign in to {{WEBUI_NAME}}', ...)}` (signin mode only; ldap/signup keep the i18n string)

Keep upstream's `id="auth-login-card"` on the card div — it was added in v0.11.0.

> **This orphans an i18n key.** Because the signin heading no longer calls
> `$i18n.t('Sign in to {{WEBUI_NAME}}')`, that key becomes unused and `npm run i18n:parse`
> strips it from all 63 locale files. Upstream still uses the key, so every merge brings it
> back and CI's "Ensure working tree is clean" step fails until it is stripped again.
>
> **After every merge, run `npm run i18n:parse` and commit the result** (at most one deletion
> per locale file — verify with `git diff --numstat`; how many locales are affected varies,
> the v0.11.1 merge touched only `fo-FO` because the rest kept the stripped state). The alternative is to
> restore upstream's i18n heading, which renders "Sign in to KeplerAI" and ends the churn
> permanently, at the cost of the bare-wordmark heading under the spinning logo.

#### 8. About Page Fork Attribution

**File:** `src/lib/components/chat/Settings/About.svelte`

Inside the `Community` `UserSettingSection`, between the Twemoji credit and the copyright
notice, Kepler adds:

> This project is a customized fork of Open WebUI, the community-driven open-source AI
> platform. This release is not affiliated with or maintained by the official Open WebUI team.

Upstream restructures this footer area fairly often — re-insert the paragraph as a sibling
`<div class="text-xs text-gray-400 dark:text-gray-500">` matching upstream's current markup.

#### 9. Error Messages

These files contain user-visible error messages branded as "KeplerAI":

- `backend/open_webui/constants.py` — `SERVER_CONNECTION_ERROR` (the canonical constant, added
  in v0.11.1 when upstream consolidated the string)
- `backend/open_webui/routers/openai.py` - "KeplerAI: Server Connection Error"
- `backend/open_webui/routers/audio.py` - "KeplerAI: Server Connection Error"

> As of v0.11.1 upstream moved this string into `constants.py` but still has inline copies in
> `openai.py` and `audio.py`. Brand all of them — grep for `Server Connection Error` rather
> than assuming a single site.
>
> `ollama.py` no longer carries these strings — upstream refactored its error handling in
> v0.11.0 to generic `HTTP Error` / `External Error` details. Nothing to brand there now.

#### 10. Upstream LICENSE Branding Notices (added v0.11.1)

Upstream v0.11.1 added ~148 in-code notices of the form:

```
# LICENSE covers this Open WebUI branding surface, ...
# Do not alter, remove, obscure, or replace it except as LICENSE permits:
# https://docs.openwebui.com/license.
```

They sit immediately above every branded string, so **they turn nearly every branding site
into a merge conflict**. Where KeplerAI rebrands the string, drop the accompanying notice
with it (a "do not alter" comment above altered text is just noise). Keep the notice where
the branded content is itself preserved — e.g. the Open WebUI copyright attribution in
`About.svelte`.

**`env.py` also gained active enforcement** — delete these two lines on every merge:

```python
if WEBUI_NAME != 'Open WebUI':
    WEBUI_NAME += ' (Open WebUI)'
```

Left in place, the app renders "KeplerAI (Open WebUI)" everywhere `WEBUI_NAME` appears.

> **Licensing note.** LICENSE clause 4 (unchanged since before the fork started) prohibits
> altering Open WebUI branding _except_ where: (i) total end users do not exceed fifty (50)
> in any rolling 30-day period, (ii) written permission has been obtained, or (iii) an
> enterprise license is in force. Every merge to date has rebranded on the basis that Kepler
> falls within one of these. Re-confirm this still holds — v0.11.1 also added an admin-panel
> banner in `src/lib/components/admin/Users/UserList.svelte` that appears once a workspace
> exceeds 50 users.

### Branding Image Files (MUST preserve during every merge)

These are custom Kepler image assets. They should NEVER be overwritten by upstream defaults.

| File                                                     | Purpose                                   |
| -------------------------------------------------------- | ----------------------------------------- |
| `static/favicon.png`                                     | Main favicon (128KB, Kepler-branded)      |
| `static/keplerspin.gif`                                  | Animated spinning blue Kepler logo (11MB) |
| `backend/open_webui/static/favicon.png`                  | Backend favicon                           |
| `backend/open_webui/static/favicon.svg`                  | Vector favicon                            |
| `backend/open_webui/static/favicon.ico`                  | ICO format favicon                        |
| `backend/open_webui/static/favicon-96x96.png`            | High-res favicon                          |
| `backend/open_webui/static/apple-touch-icon.png`         | iOS home screen icon                      |
| `backend/open_webui/static/logo.png`                     | PWA/manifest logo                         |
| `backend/open_webui/static/splash.png`                   | Light theme splash screen                 |
| `backend/open_webui/static/splash-dark.png`              | Dark theme splash screen                  |
| `backend/open_webui/static/web-app-manifest-192x192.png` | Android PWA icon (small)                  |
| `backend/open_webui/static/web-app-manifest-512x512.png` | Android PWA icon (large)                  |

> **Removed in v0.11.0:** `favicon-dark.png` (both the `backend/open_webui/static/` and
> `static/static/` copies). Upstream deleted it in an asset refactor and no code in `src/`
> or `backend/` ever referenced it, so KeplerAI accepted the deletion rather than carry a
> conflict forward every merge. Nothing renders differently.

---

## Step-by-Step Update Procedure

### 1. Prepare

```bash
# Ensure you're on main with a clean working tree
git checkout main
git status  # should be clean

# Create a backup branch
git checkout -b backup-before-merge-$(date +%Y%m%d)
git checkout main

# Fetch latest upstream
git fetch upstream
```

### 2. Backup Branding Files

```bash
# Create temp backup of all branding image files
# (on Windows use a scratch dir, e.g. $env:TEMP\kepler-branding-backup)
mkdir -p /tmp/kepler-branding-backup

# Frontend static
cp static/favicon.png static/keplerspin.gif /tmp/kepler-branding-backup/

# Backend static (main branding images)
cp backend/open_webui/static/favicon.png /tmp/kepler-branding-backup/backend-favicon.png
cp backend/open_webui/static/favicon.svg /tmp/kepler-branding-backup/
cp backend/open_webui/static/favicon.ico /tmp/kepler-branding-backup/
cp backend/open_webui/static/favicon-96x96.png /tmp/kepler-branding-backup/
cp backend/open_webui/static/apple-touch-icon.png /tmp/kepler-branding-backup/
cp backend/open_webui/static/logo.png /tmp/kepler-branding-backup/
cp backend/open_webui/static/splash.png /tmp/kepler-branding-backup/
cp backend/open_webui/static/splash-dark.png /tmp/kepler-branding-backup/
cp backend/open_webui/static/web-app-manifest-192x192.png /tmp/kepler-branding-backup/
cp backend/open_webui/static/web-app-manifest-512x512.png /tmp/kepler-branding-backup/
cp backend/open_webui/static/site.webmanifest /tmp/kepler-branding-backup/
cp static/opensearch.xml /tmp/kepler-branding-backup/
```

### 3. Merge Upstream

```bash
git merge upstream/main --no-edit
```

### 4. Resolve Conflicts

Common conflict locations (resolve in favor of KeplerAI branding):

- **`package.json`** - Keep `"name": "KeplerAI"`, take upstream version number
- **`src/routes/+layout.svelte`** - Keep `KeplerAI` in notification strings, take upstream code changes
- **`src/lib/components/channel/Channel.svelte`** - Keep `KeplerAI` in the two `<title>` tags
- **`src/routes/auth/+page.svelte`** - Keep the keplerspin logo, purple background, and `KeplerAI` heading; take upstream's markup/attribute changes
- **`src/lib/components/chat/Settings/About.svelte`** - Re-insert the fork-attribution paragraph into upstream's restructured footer
- **`src/app.html`** - Keep all `KeplerAI` meta tags and title
- **`src/lib/constants.ts`** - Keep `APP_NAME = 'KeplerAI'`
- **`backend/open_webui/env.py`** - Keep `WEBUI_NAME` default as `KeplerAI`
- **`backend/open_webui/main.py`** - Usually an _additive_ collision: upstream adds a new
  top-level function right where the Kepler `_cache_control_for` / `CachedStaticFiles` block
  lives. Keep both sides.

**Guiding rule:** take upstream's code, substitute only the name. When upstream changes
formatting or structure around a branded string (quoting style, separators, wrapper markup),
adopt the change — carrying a cosmetic divergence forward means re-resolving it every merge.

### 5. Restore Branding After Merge

After resolving conflicts, verify and fix these items:

```bash
# Check core branding constants are intact
grep "APP_NAME = 'KeplerAI'" src/lib/constants.ts
grep 'WEBUI_NAME.*KeplerAI' backend/open_webui/env.py
grep '"name": "KeplerAI"' package.json

# Check HTML meta tags
grep 'KeplerAI' src/app.html

# Check manifests
grep 'KeplerAI' backend/open_webui/static/site.webmanifest
grep 'KeplerAI' static/opensearch.xml
```

**Sweep for newly-introduced upstream branding.** A large merge adds new files that hardcode
"Open WebUI". Review anything user-visible; leave i18n keys and genuine references to the
upstream project/community alone (see "Known References" below).

```bash
# Backend: new hardcoded names outside comments/docstrings
grep -rn "Open WebUI" backend/open_webui/routers/ backend/open_webui/main.py

# Frontend: new strings outside the locale files
grep -rn "Open WebUI" src/ --include=*.svelte --include=*.ts --include=*.html \
  | grep -v "i18n/locales"
```

**Diff against upstream to see the complete Kepler delta.** This is the fastest way to
confirm every customization survived and nothing extra crept in:

```bash
git diff upstream/main -- src/ backend/open_webui/
```

If any branding was overwritten, restore from the values documented in the "Branding Files Reference" section above.

**Post-merge branding fixes to apply:**

1. **FastAPI title:** In `backend/open_webui/main.py`, change `title="Open WebUI"` to `title="KeplerAI"`
2. **CLI version:** In `backend/open_webui/__init__.py`, change `"Open WebUI version:"` to `"KeplerAI version:"`
3. **X-Title header:** In `backend/open_webui/routers/openai.py`, change `'X-Title': 'Open WebUI'` to `'X-Title': 'KeplerAI'`
4. **Error messages:** In `openai.py` and `audio.py` routers, replace all `'Open WebUI: Server Connection Error'` with `'KeplerAI: Server Connection Error'`
5. **Notifications:** In `src/routes/+layout.svelte`, ensure the three notification strings use `KeplerAI`
6. **Channel tab titles:** In `src/lib/components/channel/Channel.svelte`, ensure both `<title>` tags use `KeplerAI`
7. **Push-target fallback:** In `backend/open_webui/routers/notifications.py`, the `getattr(request.app.state, 'WEBUI_NAME', ...)` default should be `'KeplerAI'`
8. **Auth page:** In `src/routes/auth/+page.svelte`, confirm the keplerspin logo, `#3924f6` background, and `KeplerAI` signin heading are present
9. **About page:** In `src/lib/components/chat/Settings/About.svelte`, confirm the fork-attribution paragraph is present

**Then verify it actually compiles** — a large merge can leave a syntactically valid but
broken resolution:

```bash
python -m py_compile backend/open_webui/main.py backend/open_webui/routers/*.py

npm install
# The v0.11.0 frontend needs more than Node's default heap; without this the build dies
# with "Ineffective mark-compacts near heap limit" while rendering chunks.
NODE_OPTIONS=--max-old-space-size=8192 npm run build   # PowerShell: $env:NODE_OPTIONS="--max-old-space-size=8192"
```

`npm install` rewrites the two `name` fields in `package-lock.json` to match
`package.json` (`open-webui` → `KeplerAI`). That is expected — commit it, or the tree
re-dirties on every install.

> **The Railway build needs the same heap bump — and it must be set in the `Dockerfile`.**
> The frontend build OOMs on Node's default heap (~4GB); v0.11.1 was the merge where it
> tipped over, failing with `Ineffective mark-compacts near heap limit` and
> `npm error signal SIGABRT` during `vite build`.
>
> Upstream ships the fix commented out in the frontend build stage of `Dockerfile`:
>
> ```dockerfile
> # ENV NODE_OPTIONS="--max-old-space-size=4096"
> ```
>
> Kepler uncomments it and raises it to `8192`. **Keep this through every merge** — it sits
> in a stanza upstream still edits, so expect it to come back commented out.
>
> Setting `NODE_OPTIONS` as a Railway _service variable_ does **not** work: this service
> builds from a Dockerfile, and Railway service variables are not injected into Docker
> build stages. The symptom is a build that still caps at ~4000 MB despite the variable
> being set.

### 6. Verify Image Files

```bash
# Compare image files with backup to ensure they weren't overwritten
md5sum /tmp/kepler-branding-backup/favicon.png
md5sum static/favicon.png
# If they differ, restore:
# cp /tmp/kepler-branding-backup/favicon.png static/favicon.png

# Repeat for all image files...
```

### 7. Commit

```bash
# Check for stray untracked files first -- `git add -A` will sweep them into the merge
# commit. The repo tends to accumulate artifacts like `nul` (from a Windows redirect) and
# `.claude/scheduled_tasks.lock`.
git status --short

git add -A
git commit -m "Merge upstream/main vX.Y.Z while preserving KeplerAI branding"
```

### 8. Push

```bash
git push origin main
```

---

## Known "Open WebUI" References (Intentionally Kept)

These references to "Open WebUI" are **intentionally preserved** as proper attribution to the upstream project:

- **`src/lib/components/chat/Settings/About.svelte`** - Attribution text: "This project is a customized fork of Open WebUI" and copyright notice linking to Open WebUI Inc.
- **Translation files** (`src/lib/i18n/locales/*/translation.json`) - Contains some "Open WebUI" strings in help text. These are used as i18n translation keys and changing them would require updating all 59+ locale files.
- **`src/lib/components/admin/Settings/General.svelte`** - Help text: "Discover how to use Open WebUI and seek support from the community" (i18n string)
- **Comments/docstrings** in backend Python files referencing "Open WebUI" as the upstream project name
- **External URLs** pointing to `openwebui.com`, Discord, Twitter, and GitHub for the upstream project

---

## KeplerAI-Specific Customizations (MUST preserve during every merge)

These are functional changes Kepler has made on top of upstream that are not branding-related. Resolve conflicts in favor of these.

### Frontend build heap limit (`Dockerfile`)

The frontend build stage sets `ENV NODE_OPTIONS="--max-old-space-size=8192"`. Upstream ships
that line commented out at 4096; without it the Railway build fails with a JS heap OOM. See
the build note in step 5. Re-apply it if a merge reverts the stanza.

### Static asset Cache-Control headers (for Railway CDN)

**File:** `backend/open_webui/main.py`

To make Railway's opt-in CDN actually cache static assets, we set explicit `Cache-Control` headers on the `/static/*` and SPA frontend mounts. Without these headers Railway's edge passes everything through to the origin.

Look for:

- A `_cache_control_for(path, is_html=False)` helper just before the `SPAStaticFiles` class
- A `CachedStaticFiles(StaticFiles)` class that wraps `get_response` to set `Cache-Control`
- `SPAStaticFiles.get_response` also calls `_cache_control_for` on both the normal and `index.html` fallback paths
- `/static` mount uses `CachedStaticFiles(...)` rather than bare `StaticFiles(...)`

Cache policy:

- `*/immutable/*` (SvelteKit fingerprinted chunks) → `public, max-age=31536000, immutable`
- `version.json` → `no-cache, must-revalidate`
- HTML / SPA fallback → `no-cache`
- Everything else → `public, max-age=3600, must-revalidate`

If upstream refactors the static mounts and removes these, restore from this guide. Do not use the `CACHE_CONTROL` env var as a substitute — it applies one global value to every response (including API/auth) and would either break auth caching or fail to cache static assets.

---

## Merge History

| Date       | From Version | To Version | Commit                                                                                                                        |
| ---------- | ------------ | ---------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 2025-07-17 | -            | v0.7.2     | Initial Kepler branding on upstream merge                                                                                     |
| 2025-09-26 | v0.7.2       | v0.7.2     | Branding refinements                                                                                                          |
| 2026-02-16 | v0.7.2       | v0.8.1     | `4fef8b9fb` - 344 commits merged                                                                                              |
| 2026-02-16 | v0.8.1       | v0.8.3     | `8c714dd73` - 60 commits merged                                                                                               |
| 2026-03-02 | v0.8.3       | v0.8.7     | `c00045c1d` - 306 commits merged                                                                                              |
| 2026-03-09 | v0.8.7       | v0.8.9     | `4f02f60a4` - 142 commits merged                                                                                              |
| 2026-03-09 | v0.8.9       | v0.8.10    | `fa3bd41a0` - 33 commits merged                                                                                               |
| 2026-03-30 | v0.8.10      | v0.8.12    | `9ceeeb63a` - 244 commits merged                                                                                              |
| 2026-05-08 | v0.8.12      | v0.9.2     | `ec4fa6c91` - 410 commits merged                                                                                              |
| 2026-05-14 | v0.9.2       | v0.9.5     | `5ed5a9be1` - 147 commits merged                                                                                              |
| 2026-06-08 | v0.9.5       | v0.9.6     | `2d5a3c70d` - 248 commits merged                                                                                              |
| 2026-07-28 | v0.9.6       | v0.11.0    | `4f7484e42` - 1009 commits merged; 7 conflicts; separator `•`→`/`; dropped `favicon-dark.png`                                 |
| 2026-08-31 | v0.11.0      | v0.11.1    | `ca3397ad6` - 460 commits merged; 12 conflicts; upstream added 148 LICENSE branding notices + `WEBUI_NAME` suffix enforcement |

---

## Quick Checklist for Future Merges

- [ ] Backup branch created
- [ ] Branding image files backed up to temp directory
- [ ] `git fetch upstream && git merge upstream/main` completed
- [ ] Merge conflicts resolved (KeplerAI branding preserved)
- [ ] `src/lib/constants.ts` - `APP_NAME = 'KeplerAI'`
- [ ] `backend/open_webui/env.py` - `WEBUI_NAME` default is `"KeplerAI"`
- [ ] `package.json` - `"name": "KeplerAI"` (version updated to upstream)
- [ ] `src/app.html` - All meta tags say "KeplerAI"
- [ ] `backend/open_webui/static/site.webmanifest` - KeplerAI branding
- [ ] `static/opensearch.xml` - KeplerAI branding
- [ ] `backend/open_webui/main.py` - FastAPI `title="KeplerAI"`
- [ ] `backend/open_webui/__init__.py` - CLI says "KeplerAI version"
- [ ] `backend/open_webui/routers/openai.py` - `X-Title: KeplerAI`
- [ ] `backend/open_webui/routers/notifications.py` - `WEBUI_NAME` fallback is "KeplerAI"
- [ ] `src/routes/+layout.svelte` - All three notifications say "KeplerAI"
- [ ] `src/lib/components/channel/Channel.svelte` - Both `<title>` tags say "KeplerAI"
- [ ] `src/routes/auth/+page.svelte` - keplerspin logo, `#3924f6` background, "KeplerAI" heading
- [ ] `src/lib/components/chat/Settings/About.svelte` - Fork-attribution paragraph present
- [ ] Error messages in `openai.py`, `audio.py` say "KeplerAI"
- [ ] `backend/open_webui/constants.py` - `SERVER_CONNECTION_ERROR` says "KeplerAI"
- [ ] `backend/open_webui/env.py` - upstream's `WEBUI_NAME += ' (Open WebUI)'` suffix lines removed
- [ ] `Dockerfile` - `ENV NODE_OPTIONS="--max-old-space-size=8192"` is uncommented in the frontend build stage
- [ ] Railway cache-control block intact in `main.py` (`_cache_control_for`, `CachedStaticFiles`, `/static` mount)
- [ ] All Kepler image files verified (favicon, logo, splash, PWA icons, keplerspin.gif)
- [ ] `grep -rn "Open WebUI"` sweep for newly-introduced upstream strings
- [ ] `git diff upstream/main -- src/ backend/open_webui/` reviewed
- [ ] `python -m py_compile` + `npm run build` both pass
- [ ] New DB migrations reviewed for deploy risk (see below)
- [ ] Committed and pushed

---

## Deploy Notes

Check for new Alembic migrations each merge:

```bash
git diff ORIG_HEAD --name-only --diff-filter=A -- backend/open_webui/migrations/versions/
```

Migrations run automatically at startup, so a failing one takes the app down rather than
degrading it. Read any new migration's `upgrade()` for pre-flight checks that `raise`.

**v0.11.1 added 3 migrations**, all low-risk — no `raise` guards, no unique constraints:
`1ce6ade7d93b` (group_member index), `6d09d1bf1f23` (repairs double-encoded `user.oauth`;
fully guarded, but `downgrade()` is a no-op so it is not reversible), and `d4c1a8e37b62`
(adds `chat.timer_at` plus five indexes on `chat`/`chat_message` — the index builds are the
only meaningful cost, and they scale with table size).

<details>
<summary>v0.11.0 migration notes (historical)</summary>

**v0.11.0 added 11 migrations.** Two warranted attention before deploying:

- `f0bd01a18a3d_add_unique_normalized_user_email_index.py` — adds a UNIQUE index on
  `lower(email)` and **raises `RuntimeError`, aborting startup, if any two users share a
  case-insensitively identical email**. Check before deploying:

  ```sql
  SELECT lower(email), count(*) FROM "user"
  WHERE email IS NOT NULL GROUP BY lower(email) HAVING count(*) > 1;
  ```

  If that returns rows, merge or remove the duplicate users first.

- `3ff2c63645b8_reshape_config_to_per_key_rows.py` — restructures the `config` table from a
  single blob into per-key rows. Back up the database before running it.

</details>
