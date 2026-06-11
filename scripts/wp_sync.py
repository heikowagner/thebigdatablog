#!/usr/bin/env python3
"""
WordPress ↔ Markdown bidirectional sync for thebigdatablog.com

Commands
--------
  pull    Download all posts from WordPress → Markdown files in articles/
  push    Upload Markdown files → WordPress (create or update posts)
  status  Show diff between local files and WordPress without making changes

Environment variables (in .env or GitHub Secrets)
--------------------------------------------------
  WP_URL          https://thebigdatablog.com
  WP_USER         WordPress username
  WP_APP_PASSWORD WordPress Application Password (spaces are stripped automatically)

LaTeX support
-------------
  Inline math : $...$
  Block math  : $$...$$  (rendered by a WordPress MathJax / KaTeX plugin)
  On pull the script converts WP-side delimiters (\\(…\\), \\[…\\], $latex …$,
  [latex]…[/latex]) to the standard $…$ / $$…$$ notation.
  On push the script converts them back to \\(…\\) / \\[…\\] for MathJax.
"""

import os
import re
import json
import sys
import argparse
import subprocess
import html as _html
from datetime import datetime, timezone
from pathlib import Path

import requests
import frontmatter
from markdownify import markdownify as _md
from markdown import markdown
from dotenv import load_dotenv

load_dotenv()

BASE_DIR   = Path(__file__).resolve().parent.parent
ARTICLES   = BASE_DIR / "articles"
STATE_FILE = ARTICLES / ".sync_state.json"


# ── Auth / low-level REST helpers ─────────────────────────────────────────────

def _creds() -> tuple[str, str, str]:
    url  = os.environ.get("WP_URL", "").rstrip("/")
    user = os.environ.get("WP_USER", "")
    pwd  = os.environ.get("WP_APP_PASSWORD", "").replace(" ", "")
    if not all([url, user, pwd]):
        sys.exit(
            "ERROR: set WP_URL, WP_USER and WP_APP_PASSWORD "
            "in a .env file or as environment variables."
        )
    return url, user, pwd


def _get(endpoint: str, **params):
    url, user, pwd = _creds()
    r = requests.get(
        f"{url}/wp-json/wp/v2/{endpoint}",
        auth=(user, pwd), params=params, timeout=30,
    )
    r.raise_for_status()
    return r


def _post(endpoint: str, data: dict) -> dict:
    url, user, pwd = _creds()
    r = requests.post(
        f"{url}/wp-json/wp/v2/{endpoint}",
        auth=(user, pwd), json=data, timeout=30,
    )
    r.raise_for_status()
    return r.json()


def _patch(endpoint: str, data: dict) -> dict:
    url, user, pwd = _creds()
    r = requests.patch(
        f"{url}/wp-json/wp/v2/{endpoint}",
        auth=(user, pwd), json=data, timeout=30,
    )
    r.raise_for_status()
    return r.json()


def fetch_all(resource: str, **params) -> list:
    """Paginate through a WP REST resource and return all items."""
    items, page = [], 1
    while True:
        resp  = _get(resource, per_page=100, page=page, **params)
        batch = resp.json()
        if not batch:
            break
        items.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return items


def term_id(taxonomy: str, name: str) -> int:
    """Return WP term ID for taxonomy entry; creates the term if it does not exist."""
    slug    = re.sub(r"[^\w-]", "-", name.lower()).strip("-")
    matches = fetch_all(taxonomy, slug=slug)
    if matches:
        return matches[0]["id"]
    return _post(taxonomy, {"name": name, "slug": slug})["id"]


# ── Math extraction / restoration ─────────────────────────────────────────────

# Patterns are tried in order; block patterns must come before inline ones.
_MATH_PATTERNS = [
    # Block: $$…$$
    (re.compile(r"\$\$(.*?)\$\$", re.DOTALL), True),
    # Block: \[…\]
    (re.compile(r"\\\[(.*?)\\\]",  re.DOTALL), True),
    # Block: [latex]…[/latex]
    (re.compile(r"\[latex\](.*?)\[/latex\]", re.DOTALL | re.IGNORECASE), True),
    # Inline: \(…\)
    (re.compile(r"\\\((.*?)\\\)"), False),
    # Inline: $latex …$  (WordPress.com shortcode)
    (re.compile(r"\$latex\s+(.*?)\$"), False),
    # Inline: $…$  (must be last to avoid false positives)
    (re.compile(r"(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)"), False),
]


def _extract_math(text: str) -> tuple[str, dict]:
    """Replace math expressions with opaque placeholders.

    Returns (modified_text, {placeholder: rendered_markdown}).
    """
    store: dict[str, str] = {}
    idx = 0

    def replace(m: re.Match, block: bool) -> str:
        nonlocal idx
        key   = f"WPMATHx{idx:04d}x"
        inner = m.group(1).strip()
        store[key] = f"$$\n{inner}\n$$" if block else f"${inner}$"
        idx += 1
        return key

    for pattern, is_block in _MATH_PATTERNS:
        text = pattern.sub(lambda m, b=is_block: replace(m, b), text)

    return text, store


def _restore_math(text: str, store: dict) -> str:
    for key, math in store.items():
        text = text.replace(key, math)
    return text


# ── Content conversion ────────────────────────────────────────────────────────

def html_to_markdown(html: str) -> str:
    """Convert WordPress HTML (including LaTeX) → clean Markdown."""
    protected, store = _extract_math(html)
    md_text = _md(protected, heading_style="ATX", bullets="-", newline_style="backslash")
    return _restore_math(md_text, store).strip()


def markdown_to_html(text: str) -> str:
    """Convert Markdown → HTML for WordPress.

    - Math:  $…$  → \\(…\\),  $$…$$ → \\[…\\]   (WP QuickLaTeX)
    - Code:  ```lang…```  → [sourcecode language="lang"]…[/sourcecode]
             (SyntaxHighlighter Evolved plugin)
    - Strikethrough: ~~text~~ → <del>text</del>
    """
    store: dict[str, str] = {}
    idx = 0

    def protect_block(m: re.Match) -> str:
        nonlocal idx
        key        = f"WPMATHx{idx:04d}x"
        store[key] = f"\\[{m.group(1).strip()}\\]"
        idx += 1
        return key

    def protect_inline(m: re.Match) -> str:
        nonlocal idx
        key        = f"WPMATHx{idx:04d}x"
        store[key] = f"\\({m.group(1).strip()}\\)"
        idx += 1
        return key

    # Extract math before any other processing
    text = re.sub(r"\$\$(.*?)\$\$", protect_block,  text, flags=re.DOTALL)
    text = re.sub(r"(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)", protect_inline, text)

    # Strikethrough: ~~text~~ → <del>text</del>  (not in stdlib markdown)
    text = re.sub(r"~~(.+?)~~", r"<del>\1</del>", text)

    html = markdown(text, extensions=["tables", "fenced_code", "toc"])

    # Restore math placeholders
    for key, math in store.items():
        html = html.replace(key, math)

    # Convert <pre><code class="language-X">…</code></pre>
    # → [sourcecode language="X"]…[/sourcecode]  (SyntaxHighlighter Evolved)
    # The markdown library HTML-encodes code content; we unescape it so the
    # shortcode handler receives plain text (it does its own escaping for display).
    def _to_syntaxhighlighter(m: re.Match) -> str:
        lang    = m.group(1) or "text"
        content = _html.unescape(m.group(2)).rstrip("\n")
        return f'[sourcecode language="{lang}"]{content}[/sourcecode]'

    html = re.sub(
        r'<pre><code(?:\s+class="language-([\w-]+)")?>(.*?)</code></pre>',
        _to_syntaxhighlighter,
        html,
        flags=re.DOTALL,
    )

    return html


# ── File / state helpers ──────────────────────────────────────────────────────

def post_filename(post: dict) -> str:
    date = post["date"][:10]
    slug = re.sub(r"[^\w-]", "", post["slug"])[:60]
    return f"{date}-{slug}.md"


def article_dir(wp_status: str) -> Path:
    d = ARTICLES / ("published" if wp_status == "publish" else "drafts")
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_state() -> dict:
    return json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}


def save_state(state: dict) -> None:
    state["last_sync"] = datetime.now(timezone.utc).isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2))


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_pull(args) -> None:
    """WordPress → local Markdown."""
    print("Fetching posts from WordPress …")
    posts = fetch_all(
        "posts", status="any",
        _fields="id,slug,title,content,date,modified,status,categories,tags",
    )

    # Build ID → name maps for taxonomy terms
    cat_map = {c["id"]: c["name"] for c in fetch_all("categories")}
    tag_map = {t["id"]: t["name"] for t in fetch_all("tags")}

    print(f"Found {len(posts)} posts.")
    state   = load_state()
    written = skipped = 0

    for post in posts:
        folder   = article_dir(post["status"])
        filename = post_filename(post)
        filepath = folder / filename

        # Skip if the post hasn't changed since last pull
        if filepath.exists() and not args.force:
            existing = frontmatter.load(str(filepath))
            if existing.metadata.get("wp_modified") == post["modified"]:
                skipped += 1
                continue

        body = html_to_markdown(post["content"]["rendered"])
        meta = {
            "wp_id":       post["id"],
            "title":       post["title"]["rendered"],
            "date":        post["date"][:10],
            "wp_modified": post["modified"],
            "status":      post["status"],
            "slug":        post["slug"],
            "categories":  [cat_map.get(c, c) for c in post.get("categories", [])],
            "tags":        [tag_map.get(t, t) for t in post.get("tags", [])],
        }

        fm_post = frontmatter.Post(body, **meta)
        with open(filepath, "w", encoding="utf-8") as f:
            frontmatter.dump(fm_post, f)

        print(f"  ✓  {folder.name}/{filename}")
        written += 1

    save_state(state)
    print(f"\nDone — {written} written, {skipped} unchanged.")


def _git_dirty_articles() -> set[Path]:
    """Return absolute paths of article files that are new or locally modified.

    A file is considered dirty when:
    - it is untracked (new article without wp_id), OR
    - it has uncommitted changes vs. HEAD.
    """
    dirty: set[Path] = set()
    try:
        # Modified / staged files relative to HEAD
        modified = subprocess.check_output(
            ["git", "diff", "--name-only", "HEAD", "--", "articles/"],
            cwd=BASE_DIR, text=True,
        ).splitlines()
        # Untracked new files
        untracked = subprocess.check_output(
            ["git", "ls-files", "--others", "--exclude-standard", "articles/"],
            cwd=BASE_DIR, text=True,
        ).splitlines()
        for rel in modified + untracked:
            dirty.add(BASE_DIR / rel)
    except subprocess.CalledProcessError:
        pass  # Not a git repo or git not available — fall through (push all)
    return dirty


def cmd_push(args) -> None:
    """Local Markdown → WordPress.

    By default only pushes files that are new (no wp_id) or locally modified
    (git-dirty).  Pass --all to push every file regardless.
    """
    state   = load_state()
    pushed  = created = skipped = conflicts = 0

    dirty = None if args.all else _git_dirty_articles()

    for subdir in ("published", "drafts"):
        dirpath = ARTICLES / subdir
        if not dirpath.exists():
            continue

        for filepath in sorted(dirpath.glob("*.md")):
            post    = frontmatter.load(str(filepath))
            meta    = post.metadata
            wp_id   = meta.get("wp_id")
            wp_stat = "publish" if subdir == "published" else "draft"

            # Skip unmodified files unless --all was requested
            if dirty is not None and wp_id and filepath not in dirty:
                skipped += 1
                continue

            payload: dict = {
                "title":   meta.get("title", filepath.stem),
                "content": markdown_to_html(post.content),
                "slug":    meta.get("slug", filepath.stem),
                "status":  wp_stat,
            }

            if meta.get("categories"):
                payload["categories"] = [term_id("categories", c) for c in meta["categories"]]
            if meta.get("tags"):
                payload["tags"] = [term_id("tags", t) for t in meta["tags"]]

            if wp_id:
                # Conflict check: skip if WordPress was modified after our last pull
                wp_info = _get(f"posts/{wp_id}", _fields="modified").json()
                if (
                    not args.force
                    and meta.get("wp_modified")
                    and wp_info.get("modified") != meta["wp_modified"]
                ):
                    print(
                        f"  ! CONFLICT {filepath.name} "
                        f"(WP modified={wp_info['modified']}) — "
                        "skipping. Run with --force to override."
                    )
                    conflicts += 1
                    continue

                result = _patch(f"posts/{wp_id}", payload)
                print(f"  ↑  updated  {subdir}/{filepath.name}  (id={wp_id})")
                pushed += 1
            else:
                result = _post("posts", payload)
                print(f"  +  created  {subdir}/{filepath.name}  (id={result['id']})")
                created += 1

            # Persist new wp_id / wp_modified back into the file's frontmatter
            meta["wp_id"]       = result["id"]
            meta["wp_modified"] = result["modified"]
            updated = frontmatter.Post(post.content, **meta)
            with open(filepath, "w", encoding="utf-8") as f:
                frontmatter.dump(updated, f)

    save_state(state)
    print(f"\nDone — {pushed} updated, {created} created, {skipped} skipped (unchanged), {conflicts} conflicts.")


def cmd_status(args) -> None:
    """Show sync status without making changes."""
    posts = {
        p["id"]: p
        for p in fetch_all(
            "posts", status="any",
            _fields="id,slug,title,modified,status,date",
        )
    }

    local_ids: set[int] = set()

    for subdir in ("published", "drafts"):
        dirpath = ARTICLES / subdir
        if not dirpath.exists():
            continue
        for filepath in sorted(dirpath.glob("*.md")):
            meta  = frontmatter.load(str(filepath)).metadata
            wp_id = meta.get("wp_id")
            if wp_id:
                local_ids.add(wp_id)
                wp = posts.get(wp_id)
                if wp and wp["modified"] != meta.get("wp_modified"):
                    print(f"  ~  diverged   {subdir}/{filepath.name}  (WP modified={wp['modified']})")
                else:
                    print(f"  ✓  in-sync    {subdir}/{filepath.name}")
            else:
                print(f"  +  local-only {subdir}/{filepath.name}")

    for pid, p in posts.items():
        if pid not in local_ids:
            print(f"  ↓  wp-only    {p['date'][:10]}-{p['slug']}.md  (id={pid})")


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync WordPress ↔ Markdown articles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_pull = sub.add_parser("pull",   help="WordPress → local Markdown")
    p_pull.add_argument("--force", action="store_true",
                        help="Overwrite local files even if wp_modified matches")

    p_push = sub.add_parser("push",   help="Local Markdown → WordPress")
    p_push.add_argument("--force", action="store_true",
                        help="Push even when WordPress has newer changes (overwrite)")
    p_push.add_argument("--all", action="store_true",
                        help="Push ALL files, not just git-dirty ones")

    sub.add_parser("status", help="Show sync status without changes")

    args = parser.parse_args()
    {"pull": cmd_pull, "push": cmd_push, "status": cmd_status}[args.cmd](args)


if __name__ == "__main__":
    main()
