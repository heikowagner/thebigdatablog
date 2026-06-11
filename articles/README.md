# Blog Articles

This folder is the **source of truth** for all posts on [thebigdatablog.com](https://thebigdatablog.com).  
Articles are written in Markdown (with `$…$` / `$$…$$` math) and synced to/from WordPress via `scripts/wp_sync.py`.

```
articles/
  published/    ← live posts  (wp status = publish)
  drafts/       ← drafts      (wp status = draft)
  .sync_state.json  ← last-sync timestamps (auto-generated, do not edit)
```

Each file follows the naming convention `YYYY-MM-DD-slug.md` and starts with YAML frontmatter:

```markdown
---
wp_id: 42
title: "Mein Artikel über Stochastik"
date: 2024-03-01
wp_modified: "2024-03-01T10:00:00"
status: publish
slug: mein-artikel-ueber-stochastik
categories:
  - Data Science
tags:
  - python
  - stochastik
---

Einleitung …

Inline-Formel: $E = mc^2$

Block-Formel:

$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
```

---

## Einmaliges Setup

### 1 — WordPress Application Password anlegen

1. Im WordPress-Backend: **Benutzer → Profil → Anwendungspasswörter**
2. Namen vergeben (z. B. `GitHub Sync`) → **Neues Anwendungspasswort hinzufügen**
3. Das generierte Passwort kopieren (nur einmalig sichtbar)

### 2 — Math-Plugin in WordPress aktivieren

Damit `\(…\)` / `\[…\]` im Browser gerendert wird, installiere ein MathJax- oder KaTeX-Plugin, z. B.:
- **Simple MathJax** (kostenlos, empfohlen)
- **MathJax-LaTeX**

### 3 — Lokales `.env` anlegen

```bash
cp .env.example .env
# .env befüllen:
# WP_URL=https://thebigdatablog.com
# WP_USER=dein_benutzername
# WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```

### 4 — Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 5 — Ersten Pull durchführen (alle bestehenden Artikel importieren)

```bash
python scripts/wp_sync.py pull
```

LaTeX-Notation im Blog wird dabei automatisch nach `$…$` / `$$…$$` konvertiert.

---

## Täglicher Workflow

| Aktion | Befehl |
|---|---|
| Alle WP-Posts herunterladen | `python scripts/wp_sync.py pull` |
| Lokale Änderungen hochladen | `python scripts/wp_sync.py push` |
| Diff ohne Änderungen anzeigen | `python scripts/wp_sync.py status` |
| Konflikte ignorieren / überschreiben | `… pull --force` / `… push --force` |

Neuen Artikel erstellen → Datei in `articles/drafts/` anlegen (ohne `wp_id` in der Frontmatter) → `push` ausführen → WordPress erstellt den Post und schreibt die `wp_id` zurück.

---

## GitHub Actions (automatischer Sync)

| Trigger | Richtung |
|---|---|
| `git push` mit Änderungen in `articles/**` | push → WordPress |
| Montags 05:00 UTC (Schedule) | pull ← WordPress → Commit |
| Manuell via **Actions → Run workflow** | wählbar |

### GitHub Secrets konfigurieren

Im GitHub-Repo: **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Wert |
|---|---|
| `WP_URL` | `https://thebigdatablog.com` |
| `WP_USER` | WordPress-Benutzername |
| `WP_APP_PASSWORD` | Generiertes Application Password |
