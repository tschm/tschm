#!/usr/bin/env python3
"""Regenerate the diagnostics table in README.md.

Discovers the repositories worth showing, measures each one, and rewrites the
block between the DIAGNOSTICS markers. Standard library only, so the workflow
needs no dependencies beyond the runner's python3.

Columns fall into two kinds. Badges are live: the README ships a URL and the
value is fetched when someone loads the page, so it is at most ten minutes
stale regardless of when this script last ran. Plain numbers are what this
script measured, and are only as fresh as the last run, because no badge
service exposes a branch or release count.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

OWNERS = ("tschm", "jebel-quant")

# Scaffolding, teaching material and one-off talks. They satisfy the "has a
# release" rule but are not projects, so they would only pad the table.
EXCLUDE = {
    "demopaper",
    "latex",
    "paper",
    "paper_template",
    "tschm",
}

MARKER_START = "<!-- DIAGNOSTICS:START -->"
MARKER_END = "<!-- DIAGNOSTICS:END -->"

SHIELDS = "https://img.shields.io"
API = "https://api.github.com"

TOKEN = os.environ.get("GITHUB_TOKEN", "")


def api(path: str) -> tuple[object, dict[str, str]]:
    """GET a GitHub API path, returning the decoded body and response headers."""
    request = urllib.request.Request(
        path if path.startswith("http") else f"{API}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "tschm-diagnostics",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response), dict(response.headers)


def count(owner: str, repo: str, collection: str) -> int:
    """Total size of a paginated collection, without walking it.

    Asking for one item per page makes the last page number the total, which
    turns an unbounded walk into a single request. A response with no Link
    header is either empty or a single item.
    """
    try:
        body, headers = api(f"/repos/{owner}/{repo}/{collection}?per_page=1")
    except urllib.error.HTTPError:
        return 0
    match = re.search(r'[?&]page=(\d+)>;\s*rel="last"', headers.get("Link", ""))
    if match:
        return int(match.group(1))
    return len(body) if isinstance(body, list) else 0


def codefactor_grade(owner: str, repo: str) -> str | None:
    """The repo's CodeFactor grade, or None when it is not registered there."""
    url = f"{SHIELDS}/codefactor/grade/github/{owner}/{repo}.json"
    try:
        body, _ = api(url)
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
        return None
    message = body.get("message", "") if isinstance(body, dict) else ""
    return None if "not found" in message.lower() else message


def coverage_url(owner: str, repo: str) -> str | None:
    """The coverage badge rhiza publishes to Pages, when the repo publishes one."""
    url = f"https://{owner.lower()}.github.io/{repo}/coverage-badge.svg"
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "tschm-diagnostics"})
    try:
        with urllib.request.urlopen(request, timeout=30):
            return url
    except (urllib.error.HTTPError, urllib.error.URLError):
        return None


def pypi_package(owner: str, repo: str) -> str | None:
    """The PyPI project this repo publishes, if it demonstrably owns it.

    Both halves matter. The name is read from the repo's own pyproject rather
    than guessed from the repo name, because the two often differ — linalg
    publishes as cvx-linalg. And PyPI must link back to this repo, because a
    declared name is only an intention: jebel-quant/greeks declares "greeks",
    but PyPI's greeks belongs to someone else entirely. Guessing, or trusting
    the declaration alone, would advertise a stranger's download count as ours.
    """
    try:
        with urllib.request.urlopen(
            f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/pyproject.toml", timeout=30
        ) as response:
            pyproject = response.read().decode("utf-8", "replace")
    except (urllib.error.HTTPError, urllib.error.URLError):
        return None

    match = re.search(r'(?m)^\s*name\s*=\s*["\']([^"\']+)["\']', pyproject)
    if not match:
        return None
    package = match.group(1)

    try:
        body, _ = api(f"https://pypi.org/pypi/{package}/json")
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
        return None

    info = body.get("info", {}) if isinstance(body, dict) else {}
    urls = [info.get("home_page") or "", *(info.get("project_urls") or {}).values()]
    return package if any(f"github.com/{owner}/{repo}".lower() in u.lower() for u in urls) else None


@dataclass
class Repo:
    owner: str
    name: str
    pushed_at: str
    branches: int
    releases: int
    grade: str | None
    coverage: str | None
    package: str | None

    @property
    def slug(self) -> str:
        return f"{self.owner}/{self.name}"


def candidates() -> list[tuple[str, str, str]]:
    """Non-fork, unarchived, public repos of ours, as (owner, name, pushed_at)."""
    found: list[tuple[str, str, str]] = []
    for owner in OWNERS:
        page = 1
        while True:
            body, _ = api(f"/users/{owner}/repos?per_page=100&type=owner&page={page}")
            if not body:
                break
            found.extend(
                (owner, repo["name"], repo["pushed_at"])
                for repo in body
                if not (repo["fork"] or repo["archived"] or repo["private"])
                and repo["name"] not in EXCLUDE
            )
            page += 1
    return found


def measure(candidate: tuple[str, str, str]) -> Repo | None:
    """Measure one candidate, or None if it has never cut a release.

    A release is the cheapest available signal that something is a project
    rather than an experiment, and it means a new project joins the table on
    its first tag without anyone editing this file.
    """
    owner, name, pushed_at = candidate
    releases = count(owner, name, "releases")
    if releases == 0:
        return None
    return Repo(
        owner=owner,
        name=name,
        pushed_at=pushed_at,
        branches=count(owner, name, "branches"),
        releases=releases,
        grade=codefactor_grade(owner, name),
        coverage=coverage_url(owner, name),
        package=pypi_package(owner, name),
    )


def discover() -> list[Repo]:
    """Every repo worth showing, measured concurrently.

    Serially this is some seventy-five round trips and several minutes, most of
    it spent waiting on cold CodeFactor lookups, so the requests overlap.
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

    grade = (
        badge(
            "code quality",
            f"codefactor/grade/github/{slug}?label=",
            f"https://www.codefactor.io/repository/github/{slug}",
        )
        if repo.grade
        else "—"
    )
    coverage = (
        f"[![coverage]({repo.coverage})](https://{repo.owner.lower()}.github.io/{repo.name}/)"
        if repo.coverage
        else "—"
    )
    downloads = (
        badge("downloads", f"pypi/dm/{repo.package}?label=", f"https://pypi.org/project/{repo.package}/")
        if repo.package
        else "—"
    )

    return " | ".join(
        (
            f"| [{repo.name}]({home})",
            grade,
            coverage,
            downloads,
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
