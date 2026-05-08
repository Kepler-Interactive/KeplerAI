# KeplerAI - Upstream Update Guide

This document provides instructions for updating the KeplerAI fork from the upstream [open-webui/open-webui](https://github.com/open-webui/open-webui) repository while preserving Kepler branding.

## Repository Setup

- **Origin:** `https://github.com/Kepler-Interactive/KeplerAI.git`
- **Upstream:** `https://github.com/open-webui/open-webui.git`

## Current Version

- **KeplerAI fork:** v0.9.2 (merged from upstream on 2026-05-08)
- **Based on:** open-webui v0.9.2

---

## Branding Files Reference

### Critical Branding Files (MUST preserve during every merge)

These are the files that control core user-visible branding. If upstream changes any of these, resolve conflicts in favor of KeplerAI values.

#### 1. Application Name Constants

| File | Line | Value |
|------|------|-------|
| `src/lib/constants.ts` | 4 | `export const APP_NAME = 'KeplerAI';` |
| `backend/open_webui/env.py` | ~90 | `WEBUI_NAME = os.environ.get("WEBUI_NAME", "KeplerAI")` |
| `package.json` | 2 | `"name": "KeplerAI"` |

#### 2. HTML Meta Tags & Title

**File:** `src/app.html`

| Line | Element |
|------|---------|
| 26 | `<meta name="apple-mobile-web-app-title" content="KeplerAI" />` |
| 34 | `<meta name="description" content="KeplerAI" />` |
| 38 | `title="KeplerAI"` (opensearch link) |
| 114 | `<title>KeplerAI</title>` |

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

| File | What | Value |
|------|------|-------|
| `backend/open_webui/main.py` | FastAPI title | `title="KeplerAI"` |
| `backend/open_webui/__init__.py` | CLI version output | `f"KeplerAI version: {VERSION}"` |
| `backend/open_webui/routers/openai.py` | X-Title header | `"X-Title": "KeplerAI"` |

#### 6. Notification Branding

**File:** `src/routes/+layout.svelte`

Two notification locations that show the app name to users:
- Chat completion notification: `` `${displayTitle} • KeplerAI` ``
- Channel message notification: `` `${title} • KeplerAI` ``

#### 7. Error Messages

These files contain user-visible error messages branded as "KeplerAI":
- `backend/open_webui/routers/ollama.py` - "KeplerAI: Server Connection Error"
- `backend/open_webui/routers/openai.py` - "KeplerAI: Server Connection Error"
- `backend/open_webui/routers/audio.py` - "KeplerAI: Server Connection Error"

### Branding Image Files (MUST preserve during every merge)

These are custom Kepler image assets. They should NEVER be overwritten by upstream defaults.

| File | Purpose |
|------|---------|
| `static/favicon.png` | Main favicon (128KB, Kepler-branded) |
| `static/keplerspin.gif` | Animated spinning blue Kepler logo (11MB) |
| `backend/open_webui/static/favicon.png` | Backend favicon |
| `backend/open_webui/static/favicon.svg` | Vector favicon |
| `backend/open_webui/static/favicon.ico` | ICO format favicon |
| `backend/open_webui/static/favicon-96x96.png` | High-res favicon |
| `backend/open_webui/static/favicon-dark.png` | Dark theme favicon |
| `backend/open_webui/static/apple-touch-icon.png` | iOS home screen icon |
| `backend/open_webui/static/logo.png` | PWA/manifest logo |
| `backend/open_webui/static/splash.png` | Light theme splash screen |
| `backend/open_webui/static/splash-dark.png` | Dark theme splash screen |
| `backend/open_webui/static/web-app-manifest-192x192.png` | Android PWA icon (small) |
| `backend/open_webui/static/web-app-manifest-512x512.png` | Android PWA icon (large) |

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
mkdir -p /tmp/kepler-branding-backup

# Frontend static
cp static/favicon.png static/keplerspin.gif /tmp/kepler-branding-backup/

# Backend static (main branding images)
cp backend/open_webui/static/favicon.png /tmp/kepler-branding-backup/backend-favicon.png
cp backend/open_webui/static/favicon.svg /tmp/kepler-branding-backup/
cp backend/open_webui/static/favicon.ico /tmp/kepler-branding-backup/
cp backend/open_webui/static/favicon-96x96.png /tmp/kepler-branding-backup/
cp backend/open_webui/static/favicon-dark.png /tmp/kepler-branding-backup/
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
- **`src/app.html`** - Keep all `KeplerAI` meta tags and title
- **`src/lib/constants.ts`** - Keep `APP_NAME = 'KeplerAI'`
- **`backend/open_webui/env.py`** - Keep `WEBUI_NAME` default as `"KeplerAI"`

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

If any branding was overwritten, restore from the values documented in the "Branding Files Reference" section above.

**Post-merge branding fixes to apply:**

1. **FastAPI title:** In `backend/open_webui/main.py`, change `title="Open WebUI"` to `title="KeplerAI"`
2. **CLI version:** In `backend/open_webui/__init__.py`, change `"Open WebUI version:"` to `"KeplerAI version:"`
3. **X-Title header:** In `backend/open_webui/routers/openai.py`, change `"X-Title": "Open WebUI"` to `"X-Title": "KeplerAI"`
4. **Error messages:** In `ollama.py`, `openai.py`, and `audio.py` routers, replace all `"Open WebUI: Server Connection Error"` with `"KeplerAI: Server Connection Error"`
5. **Notifications:** In `src/routes/+layout.svelte`, ensure notification strings use `KeplerAI` not `Open WebUI`

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

## Merge History

| Date | From Version | To Version | Commit |
|------|-------------|------------|--------|
| 2025-07-17 | - | v0.7.2 | Initial Kepler branding on upstream merge |
| 2025-09-26 | v0.7.2 | v0.7.2 | Branding refinements |
| 2026-02-16 | v0.7.2 | v0.8.1 | `4fef8b9fb` - 344 commits merged |
| 2026-02-16 | v0.8.1 | v0.8.3 | `8c714dd73` - 60 commits merged |
| 2026-03-02 | v0.8.3 | v0.8.7 | `c00045c1d` - 306 commits merged |
| 2026-03-09 | v0.8.7 | v0.8.9 | `4f02f60a4` - 142 commits merged |
| 2026-03-09 | v0.8.9 | v0.8.10 | `fa3bd41a0` - 33 commits merged |
| 2026-03-30 | v0.8.10 | v0.8.12 | `9ceeeb63a` - 244 commits merged |
| 2026-05-08 | v0.8.12 | v0.9.2 | `ec4fa6c91` - 410 commits merged |

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
- [ ] `src/routes/+layout.svelte` - Notifications say "KeplerAI"
- [ ] Error messages in `ollama.py`, `openai.py`, `audio.py` say "KeplerAI"
- [ ] All Kepler image files verified (favicon, logo, splash, PWA icons, keplerspin.gif)
- [ ] Committed and pushed
