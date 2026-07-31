#!/usr/bin/env python3
"""Regenerate the diagnostics table in README.md.

Discovers the repositories worth showing, gathers a row for each, and rewrites
the block between the DIAGNOSTICS markers. Standard library only, so the
workflow needs no dependencies beyond the runner's python3.

Cells come from three places. Some badges are ours to construct, because the
shape is fixed and shields serves them live — issues, pull requests, latest
release, last commit are at most ten minutes stale whenever anyone loads the
page, regardless of when this script last ran. Quality, coverage and downloads
are copied verbatim from each repository's own README, so a project decides for
itself what it publishes and under which package name. Branch and release
counts are plain numbers measured here, because no badge service exposes them,
and they are therefore only as fresh as the last run.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field

OWNERS = ("tschm", "jebel-quant")

# Repos worth showing that we do not own, so discovery by owner would either
# miss them or drag in the whole organisation alongside. Named individually and
# exempt from the release rule: asking for one by hand is deliberate enough.
INCLUDE = ("cvxgrp/cvxcla", "cvxgrp/cvxrisk")

# Scaffolding, teaching material and one-off talks. They satisfy the "has a
# release" rule but are not projects, so they would only pad the table. Add a
# name here to drop a row; this and OWNERS are the only hand-kept lists.
EXCLUDE = {
    "demopaper",
    "latex",
    "paper",
    "paper_template",
    "rhiza-go",
    "tschm",
}

# Badges we lift from a repository's own README, recognised by a fragment of
# their URL. Copying beats reconstructing: linalg publishes to PyPI as
# cvx-linalg, and its README already says so, so nothing has to infer it.
HARVEST = (
    ("quality", "codefactor.io"),
    ("coverage", "coverage-badge.svg"),
    ("downloads", "pepy.tech"),
)

# A badge, linked or bare. The linked form is tried first so its target is
# captured rather than left behind as stray text.
LINKED_BADGE = re.compile(r"\[!\[[^\]]*\]\(([^)]+)\)\]\(([^)]+)\)")
BARE_BADGE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")

# The percentage inside a coverage badge SVG. Its label is drawn into the image
# rather than passed as a parameter, so the only way to shed the word
# "coverage" is to read the number out and render it ourselves.
COVERAGE_VALUE = re.compile(r">(\d+(?:\.\d+)?)%<")

MARKER_START = "<!-- DIAGNOSTICS:START -->"
MARKER_END = "<!-- DIAGNOSTICS:END -->"

SHIELDS = "https://img.shields.io"
API = "https://api.github.com"

TOKEN = os.environ.get("GITHUB_TOKEN", "")


def get(url: str, headers: dict[str, str] | None = None) -> tuple[bytes, dict[str, str]]:
    request = urllib.request.Request(
        url, headers={"User-Agent": "tschm-diagnostics", **(headers or {})}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read(), dict(response.headers)


def api(path: str) -> tuple[object, dict[str, str]]:
    """GET a GitHub API path, returning the decoded body and response headers."""
    body, headers = get(
        path if path.startswith("http") else f"{API}{path}",
        {
            "Accept": "application/vnd.github+json",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
    )
    return json.loads(body), headers


def count_branches(owner: str, repo: str) -> int:
    """Number of branches, without walking the collection.

    Asking for one item per page makes the last page number the total, which
    turns an unbounded walk into a single request. A response with no Link
    header is either empty or a single item.
    """
    try:
        body, headers = api(f"/repos/{owner}/{repo}/branches?per_page=1")
    except urllib.error.HTTPError:
        return 0
    match = re.search(r'[?&]page=(\d+)>;\s*rel="last"', headers.get("Link", ""))
    if match:
        return int(match.group(1))
    return len(body) if isinstance(body, list) else 0


def published_releases(owner: str, repo: str) -> int:
    """Count releases a visitor can see, i.e. excluding drafts.

    Drafts are visible to whoever holds push access and to nobody else, so the
    collection size would make this script disagree with itself: run locally it
    saw a draft-only repository as released and inflated every other count by
    one or two, while CI — holding a token scoped to this repository — saw the
    public truth. The public truth is what a profile README should tell.
    """
    published, page = 0, 1
    while True:
        try:
            body, _ = api(f"/repos/{owner}/{repo}/releases?per_page=100&page={page}")
        except urllib.error.HTTPError:
            return published
        if not body:
            return published
        published += sum(1 for release in body if not release.get("draft"))
        page += 1


def coverage_percentage(url: str) -> str | None:
    """The number inside a coverage badge, e.g. "100%"."""
    try:
        body, _ = get(url)
    except (urllib.error.HTTPError, urllib.error.URLError):
        return None
    values = COVERAGE_VALUE.findall(body.decode("utf-8", "replace"))
    return f"{float(values[-1]):.0f}%" if values else None


def harvest(owner: str, repo: str) -> dict[str, str]:
    """What a repository advertises in its own README, reduced to values.

    The repo is asked where its coverage and downloads live, because only it
    knows — cvxcla publishes coverage to a custom domain and linalg ships to
    PyPI as cvx-linalg, neither of which is derivable from the slug. But its
    badges are relabelled here rather than reused verbatim, so a column says
    "A+" once in its header instead of "CodeFactor" in all seventeen rows.
    """
    try:
        body, _ = get(f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/README.md")
    except (urllib.error.HTTPError, urllib.error.URLError):
        return {}
    readme = body.decode("utf-8", "replace")

    linked = LINKED_BADGE.findall(readme)
    badges = [*linked, *((img, "") for img in BARE_BADGE.findall(readme) if img not in dict(linked))]

    sources: dict[str, tuple[str, str]] = {}
    for image, link in badges:
        for kind, signature in HARVEST:
            if kind not in sources and signature in image:
                sources[kind] = (image.strip(), link.strip())

    cells: dict[str, str] = {}

    if "quality" in sources:
        # Rebuilt through shields, which exposes the grade on its own; the
        # CodeFactor image itself has its name baked in.
        cells["quality"] = badge(
            "code quality",
            f"codefactor/grade/github/{owner}/{repo}?label=",
            sources["quality"][1] or f"https://www.codefactor.io/repository/github/{owner}/{repo}",
        )

    if "coverage" in sources:
        image, link = sources["coverage"]
        percentage = coverage_percentage(image)
        # Unparseable means an unfamiliar badge; keep theirs rather than drop
        # the column, even though it carries its own label.
        cells["coverage"] = f"[{percentage}]({link})" if percentage and link else f"[![coverage]({image})]({link})"

    if "downloads" in sources:
        image, link = sources["downloads"]
        # pepy takes its label as a parameter, so it can simply be emptied.
        cells["downloads"] = f"[![downloads]({re.sub(r'left_text=[^&]*', 'left_text=', image)})]({link})"

    # A pipe would end the table cell early. No URL here carries one today, but
    # other people's READMEs are not ours to police.
    return {kind: value.replace("|", "%7C") for kind, value in cells.items()}


@dataclass
class Repo:
    owner: str
    name: str
    pushed_at: str
    branches: int
    releases: int
    badges: dict[str, str] = field(default_factory=dict)

    @property
    def slug(self) -> str:
        return f"{self.owner}/{self.name}"


def candidates() -> list[tuple[str, str, str, bool]]:
    """What to consider, as (owner, name, pushed_at, named_by_hand)."""
    found: list[tuple[str, str, str, bool]] = []
    for owner in OWNERS:
        page = 1
        while True:
            body, _ = api(f"/users/{owner}/repos?per_page=100&type=owner&page={page}")
            if not body:
                break
            found.extend(
                (owner, repo["name"], repo["pushed_at"], False)
                for repo in body
                if not (repo["fork"] or repo["archived"] or repo["private"])
                and repo["name"] not in EXCLUDE
            )
            page += 1

    for slug in INCLUDE:
        owner, _, name = slug.partition("/")
        try:
            repo, _ = api(f"/repos/{slug}")
        except urllib.error.HTTPError:
            print(f"could not read {slug}; skipping", file=sys.stderr)
            continue
        found.append((owner, name, repo["pushed_at"], True))

    return found


def measure(candidate: tuple[str, str, str, bool]) -> Repo | None:
    """Gather one candidate's row, or None if it does not belong in the table.

    A published release is the cheapest available signal that something is a
    project rather than an experiment, and it means a new project joins the
    table on its first tag without anyone editing this file. Repos named by
    hand skip that test, so a deliberate request is never quietly dropped.
    """
    owner, name, pushed_at, named_by_hand = candidate
    releases = published_releases(owner, name)
    if releases == 0 and not named_by_hand:
        return None
    return Repo(
        owner=owner,
        name=name,
        pushed_at=pushed_at,
        branches=count_branches(owner, name),
        releases=releases,
        badges=harvest(owner, name),
    )


def discover() -> list[Repo]:
    """Every repo worth showing, gathered concurrently.

    Serially this is a few hundred round trips and several minutes, so they
    overlap; the work is entirely spent waiting.
    """
    with ThreadPoolExecutor(max_workers=8) as pool:
        measured = pool.map(measure, candidates())
    found = [repo for repo in measured if repo is not None]
    found.sort(key=lambda r: r.pushed_at, reverse=True)
    return found


def badge(alt: str, shield: str, link: str) -> str:
    return f"[![{alt}]({SHIELDS}/{shield})]({link})"


def row(repo: Repo) -> str:
    slug, home = repo.slug, f"https://github.com/{repo.slug}"
    return " | ".join(
        (
            f"| [{slug}]({home})",
            repo.badges.get("quality", "—"),
            repo.badges.get("coverage", "—"),
            repo.badges.get("downloads", "—"),
            badge("open issues", f"github/issues/{slug}?label=", f"{home}/issues"),
            badge("open pull requests", f"github/issues-pr/{slug}?label=", f"{home}/pulls"),
            str(repo.branches),
            str(repo.releases),
            badge("latest release", f"github/v/release/{slug}?label=&sort=semver", f"{home}/releases"),
            badge("last commit", f"github/last-commit/{slug}?label=", f"{home}/commits") + " |",
        )
    )


def render(repos: list[Repo]) -> str:
    header = (
        "| | quality | coverage | downloads | issues | pull requests | branches | releases | latest | last commit |",
        "|---|---|---|---|---|---|---|---|---|---|",
    )
    return "\n".join((MARKER_START, *header, *(row(r) for r in repos), MARKER_END))


def main() -> int:
    readme = "README.md"
    with open(readme, encoding="utf-8") as handle:
        text = handle.read()

    if MARKER_START not in text or MARKER_END not in text:
        print(f"{readme} is missing the DIAGNOSTICS markers", file=sys.stderr)
        return 1

    repos = discover()
    if not repos:
        print("discovered no repositories; refusing to write an empty table", file=sys.stderr)
        return 1

    start = text.index(MARKER_START)
    end = text.index(MARKER_END) + len(MARKER_END)
    updated = text[:start] + render(repos) + text[end:]

    if updated == text:
        print(f"table is current ({len(repos)} repositories)")
        return 0

    with open(readme, "w", encoding="utf-8") as handle:
        handle.write(updated)
    print(f"table rewritten ({len(repos)} repositories)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
