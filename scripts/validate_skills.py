#!/usr/bin/env python3
"""Validate Agent Skills frontmatter, relative links, Makefiles, and SHA-pinned workflows."""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SHA_USES_RE = re.compile(
    r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_./-]+)?@([0-9a-f]{40})$"
)
UNSAFE_INTERP_RE = re.compile(r"\$\{\{\s*github\.event\.")


def load_yaml(path: pathlib.Path) -> object:
    try:
        import yaml  # type: ignore[import-not-found]

        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except ModuleNotFoundError:
        ruby_cmd = [
            "ruby",
            "-ryaml",
            "-rjson",
            "-e",
            "puts JSON.generate(YAML.safe_load(File.read(ARGV[0]), aliases: true))",
            str(path),
        ]
        out = subprocess.check_output(ruby_cmd, text=True)
        return json.loads(out)


def parse_frontmatter(text: str, path: pathlib.Path, errors: list[str]) -> dict[str, str]:
    if not text.startswith("---\n"):
        errors.append(f"{path}: missing YAML frontmatter block")
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        errors.append(f"{path}: unterminated YAML frontmatter block")
        return {}
    meta: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"{path}: invalid frontmatter line: {line!r}")
            continue
        key, val = line.split(":", 1)
        meta[key.strip()] = val.strip().strip("\"'")
    return meta


def check_markdown_links(md_path: pathlib.Path, text: str, errors: list[str]) -> None:
    # Strip fenced code blocks before scanning links so example snippets aren't treated as real links
    stripped = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    for match in MD_LINK_RE.finditer(stripped):
        target = match.group(1).strip()
        if (
            not target
            or target.startswith(("http://", "https://", "mailto:", "#"))
            or "{" in target
        ):
            continue
        rel = target.split("#", 1)[0]
        resolved = (md_path.parent / rel).resolve()
        if not resolved.exists():
            errors.append(f"{md_path.relative_to(ROOT)}: broken relative link -> {target}")


def validate_skills(errors: list[str]) -> int:
    skill_dirs = sorted(
        [p for p in ROOT.glob("*-updater") if p.is_dir()]
        + ([ROOT / "issue-triage"] if (ROOT / "issue-triage").is_dir() else [])
    )
    if not skill_dirs:
        errors.append("No skill directories found")
        return 0

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{skill_dir.name}: missing SKILL.md")
            continue

        text = skill_md.read_text(encoding="utf-8")
        lines = text.splitlines()
        if len(lines) > 500:
            errors.append(f"{skill_md.relative_to(ROOT)}: {len(lines)} lines exceeds 500-line recommendation")

        meta = parse_frontmatter(text, skill_md.relative_to(ROOT), errors)
        name = meta.get("name", "")
        desc = meta.get("description", "")

        if name != skill_dir.name:
            errors.append(
                f"{skill_md.relative_to(ROOT)}: frontmatter name {name!r} does not match directory {skill_dir.name!r}"
            )
        if not (1 <= len(name) <= 64 and SKILL_NAME_RE.match(name)):
            errors.append(f"{skill_md.relative_to(ROOT)}: invalid skill name {name!r}")
        if not (1 <= len(desc) <= 1024):
            errors.append(f"{skill_md.relative_to(ROOT)}: description must be 1..1024 chars")

        check_markdown_links(skill_md, text, errors)

    for root_doc in (ROOT / "README.md", ROOT / "AGENTS.md"):
        if root_doc.is_file():
            check_markdown_links(root_doc, root_doc.read_text(encoding="utf-8"), errors)

    return len(skill_dirs)


def validate_workflows(errors: list[str]) -> int:
    workflows = sorted(
        list((ROOT / ".github" / "workflows").glob("*.yml"))
        + list(ROOT.glob("*-updater/assets/workflows/*.yml"))
    )
    for wf in workflows:
        rel = wf.relative_to(ROOT)
        raw = wf.read_text(encoding="utf-8")
        try:
            data = load_yaml(wf)
        except Exception as exc:
            errors.append(f"{rel}: invalid YAML: {exc}")
            continue

        if not isinstance(data, dict):
            errors.append(f"{rel}: workflow root must be a mapping")
            continue

        perms = data.get("permissions")
        if perms != {"contents": "read"}:
            errors.append(f"{rel}: top-level permissions must be {{'contents': 'read'}}, got {perms!r}")

        # Verify raw `uses:` lines carry a 40-char SHA + trailing `# v...` version comment
        for lineno, line in enumerate(raw.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            m = re.match(r"^(?:-\s+)?uses:\s*(.+)$", stripped)
            if not m:
                continue
            rhs = m.group(1).strip()
            if rhs.startswith("./"):
                continue
            if "#" not in rhs:
                errors.append(f"{rel}:{lineno}: external action missing trailing '# vX.Y.Z' comment: {rhs}")
                continue
            ref_part, comment = [p.strip() for p in rhs.split("#", 1)]
            ref_part = ref_part.strip("\"'")
            if not SHA_USES_RE.match(ref_part):
                errors.append(f"{rel}:{lineno}: external action not pinned to 40-char SHA: {ref_part}")
            if not comment.startswith("v"):
                errors.append(f"{rel}:{lineno}: SHA comment should start with version tag 'v...': #{comment}")

        # Check jobs for unsafe `${{ github.event.* }}` interpolation in `run:` scripts
        jobs = data.get("jobs", {})
        if isinstance(jobs, dict):
            for job_name, job in jobs.items():
                if not isinstance(job, dict):
                    continue
                if "uses" not in job and "timeout-minutes" not in job:
                    errors.append(f"{rel}: job '{job_name}' missing timeout-minutes")
                for step in job.get("steps", []) or []:
                    if isinstance(step, dict) and isinstance(step.get("run"), str):
                        if UNSAFE_INTERP_RE.search(step["run"]):
                            errors.append(
                                f"{rel}: job '{job_name}' interpolates github.event.* directly inside run:"
                            )

    # Also validate dependabot YAML files
    for dep_yml in [ROOT / ".github" / "dependabot.yml", ROOT / "project-updater" / "assets" / "dependabot.yml"]:
        if dep_yml.is_file():
            try:
                load_yaml(dep_yml)
            except Exception as exc:
                errors.append(f"{dep_yml.relative_to(ROOT)}: invalid YAML: {exc}")

    return len(workflows)


def validate_makefiles(errors: list[str]) -> int:
    makefiles = sorted([ROOT / "Makefile"] + list(ROOT.glob("*-updater/assets/Makefile")))
    required_targets = {"all", "format", "format-check", "analyze", "test", "test-ci", "fix", "upgrade"}
    for mk in makefiles:
        if not mk.is_file():
            continue
        rel = mk.relative_to(ROOT)
        targets: set[str] = set()
        for lineno, line in enumerate(mk.read_text(encoding="utf-8").splitlines(), start=1):
            if line.startswith("  ") and not line.lstrip().startswith("#"):
                errors.append(f"{rel}:{lineno}: spaces used instead of TAB in Makefile recipe")
            m = re.match(r"^([a-zA-Z0-9_-]+)\s*:", line)
            if m:
                targets.add(m.group(1))
        missing = required_targets - targets
        if missing:
            errors.append(f"{rel}: missing standard Makefile targets: {sorted(missing)}")
    return len(makefiles)


def main() -> int:
    errors: list[str] = []
    n_skills = validate_skills(errors)
    n_workflows = validate_workflows(errors)
    n_makefiles = validate_makefiles(errors)

    if errors:
        print("Validation failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(
        f"OK: validated {n_skills} skills, {n_workflows} workflows, and {n_makefiles} Makefiles with 0 errors."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
