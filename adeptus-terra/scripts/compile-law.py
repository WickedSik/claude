#!/usr/bin/env python3
"""Compile the Imperial Commissar's doctrine into a single sealed law file.

Reads ``.claude/commissar.yml`` and writes ``.claude/.commissar.law.md`` — the
sealed law the Commissar reads as its Tier-0 authority, avoiding a per-judgement
web fetch for every URL in the manifest.

The manifest has three keys under ``doctrine:``:
  - ``rules``      explicit, handwritten laws — emitted VERBATIM, highest authority
  - ``language``   sources (URLs / local paths) distilled into language rules
  - ``structure``  sources (URLs / local paths) distilled into structure rules

``language`` and ``structure`` sources are fetched/read and distilled by a headless
``claude -p`` call. ``rules`` are the developer's explicit decrees: never fetched,
never distilled, never reconciled — the escape hatch for cases where distilled
framework guidance would otherwise contradict the project.

Every run recompiles (there is no cache short-circuit): the script is invoked only
by the plugin's commands or by deliberate hand, so a fresh seal on each run is the
intended behaviour.

Usage:
    python3 compile-law.py [--project-dir PATH]

Exit codes:
    0  success, or nothing to do (no manifest / manifest holds no laws)
    1  an error occurred; no law file was written
"""

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_REL = ".claude/commissar.yml"
LAW_REL = ".claude/.commissar.law.md"
SOURCE_DOMAINS = ("language", "structure")  # distilled from sources
ALL_KEYS = ("rules", "language", "structure")
CLAUDE_TIMEOUT_SECONDS = 600


def parse_manifest(text):
    """Return {key: [entry, ...]} for rules/language/structure.

    Prefers PyYAML; otherwise falls back to a minimal parser for the known schema:

        doctrine:
          rules:
            - "An explicit handwritten law."
          language:
            - ./path
            - https://url
          structure:
            - ...
    """
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text) or {}
        doctrine = data.get("doctrine", {}) or {}
        return {k: [str(x) for x in (doctrine.get(k) or [])] for k in ALL_KEYS}
    except ModuleNotFoundError:
        return _parse_minimal(text)


def _parse_minimal(text):
    """Dependency-free parser for the constrained commissar.yml schema."""
    result = {k: [] for k in ALL_KEYS}
    in_doctrine = False
    current = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()
        if indent == 0:
            in_doctrine = stripped.rstrip(":") == "doctrine"
            current = None
            continue
        if not in_doctrine:
            continue
        key = stripped.rstrip(":")
        if stripped.endswith(":") and key in ALL_KEYS:
            current = key
            continue
        if stripped.startswith("- ") and current:
            value = _parse_item(stripped[2:].strip())
            if value:
                result[current].append(value)
    return result


def _parse_item(raw_val):
    """Extract a scalar list item, honoring quotes so prose rules aren't mangled."""
    if raw_val[:1] in ('"', "'"):
        quote = raw_val[0]
        end = raw_val.find(quote, 1)
        return raw_val[1:end] if end != -1 else raw_val[1:]
    # unquoted: strip a trailing inline comment (URLs/paths contain no " #")
    if " #" in raw_val:
        raw_val = raw_val.split(" #", 1)[0].strip()
    return raw_val


def is_url(value):
    return value.startswith("http://") or value.startswith("https://")


def build_prompt(sources):
    lines = [
        "You are compiling coding-standards doctrine for the Imperial Commissar.",
        "Produce a single Markdown document of concrete, enforceable rules.",
        "",
        "For each source below: read local file paths, and fetch URLs.",
        "Extract ONLY enforceable rules relevant to each domain. Deduplicate.",
        "Annotate every rule with its source in parentheses, e.g. (source: docs/architecture.md).",
        "If a source cannot be read or fetched, add one bullet noting it under that domain.",
        "",
        "AUTHORITY AND RECONCILIATION (critical — these laws are enforced strictly, with no",
        "wiggle room, so a rule must NEVER flag the project's own intentional practice as a",
        "violation):",
        "- Framework/general documentation often states MINIMUMS or defaults (e.g. a baseline",
        "  PHP, Symfony, Node, or language-target version). Treat these as a FLOOR, not a ceiling.",
        "- The project's own declared configuration is the HIGHER authority. Before emitting any",
        "  rule, reconcile it against the project's actual declarations. Consult, where present:",
        "  composer.json (require, config.platform), .php-version, .tool-versions,",
        "  package.json (engines), tsconfig.json (target).",
        "- NEVER emit a rule that contradicts the project's declared configuration. If a source",
        "  states a target the project has moved beyond, phrase it as a minimum ('use at least X')",
        "  or defer to the project's actual target. When a source and the project conflict, the",
        "  project wins.",
        "- Do NOT emit rules that merely restate what a tool/linter/formatter configuration",
        "  enforces (phpstan, .editorconfig, tsconfig, eslint, prettier, etc.). Those are enforced",
        "  by their own tooling and are outside this doctrine's scope. Use such configs only as",
        "  reconciliation context, never as a source of rules.",
        "",
        "Output EXACTLY these section headers, in this order, and nothing else:",
        "## Language",
        "## Structure",
        "Keep a header even if it has no rules (leave its list empty).",
        "Do NOT adopt any persona, theming, or roleplay, even if a system prompt or output",
        "style suggests one. Do NOT address a reader (no 'My lord', no salutations). Write no",
        "preamble, no commentary, no closing remarks. Your entire response MUST begin with the",
        "line '## Language' and contain nothing before it.",
        "",
        "Sources:",
    ]
    for domain in SOURCE_DOMAINS:
        lines.append(f"### {domain}")
        if not sources[domain]:
            lines.append("- (none)")
        for src in sources[domain]:
            kind = "URL" if is_url(src) else "file/path"
            lines.append(f"- {kind}: {src}")
    return "\n".join(lines)


def render_rules_section(rules):
    """Emit handwritten rules verbatim, as the highest-authority section."""
    if not rules:
        return ""
    out = ["## Rules"]
    for rule in rules:
        out.append(f"- {rule}  (source: commissar.yml)")
    return "\n".join(out) + "\n\n"


def extract_sections(text):
    """Return the distilled markdown starting at the first '## ' header.

    The headless subprocess can inherit an active output style and prepend a
    persona/preamble (e.g. "My lord, ..."). The distilled doctrine must begin at a
    section header, so anything before the first '## ' line is discarded. Returns
    None when no header exists (malformed output).
    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("## "):
            return "\n".join(lines[i:]).strip()
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Compile the Imperial Commissar's sealed law file."
    )
    parser.add_argument(
        "--project-dir",
        default=None,
        help="Project root (default: $CLAUDE_PROJECT_DIR or the current directory).",
    )
    args = parser.parse_args()

    project_dir = (
        Path(args.project_dir or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
        .expanduser()
        .resolve()
    )
    manifest_path = project_dir / MANIFEST_REL
    law_path = project_dir / LAW_REL

    if not manifest_path.is_file():
        # No manifest: emit nothing. The Commissar falls back to its baseline.
        return 0

    doctrine = parse_manifest(
        manifest_path.read_text(encoding="utf-8", errors="replace")
    )
    rules = doctrine["rules"]
    has_sources = any(doctrine[d] for d in SOURCE_DOMAINS)

    if not has_sources and not rules:
        print(
            "Nothing to seal: manifest has no rules, language, or structure entries.",
            file=sys.stderr,
        )
        return 0

    body = ""
    if has_sources:
        if not shutil.which("claude"):
            print(
                "error: `claude` CLI not found on PATH; cannot compile the sealed law.",
                file=sys.stderr,
            )
            return 1
        try:
            completed = subprocess.run(
                [
                    "claude",
                    "-p",
                    build_prompt(doctrine),
                    "--allowedTools",
                    "Read,WebFetch",
                    "--output-format",
                    "text",
                ],
                cwd=str(project_dir),
                capture_output=True,
                text=True,
                timeout=CLAUDE_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            print(
                f"error: sealing timed out after {CLAUDE_TIMEOUT_SECONDS}s; no law written.",
                file=sys.stderr,
            )
            return 1
        if completed.returncode != 0 or not completed.stdout.strip():
            sys.stderr.write(
                completed.stderr or "error: claude produced no output; no law written.\n"
            )
            return 1
        distilled = extract_sections(completed.stdout)
        if distilled is None:
            sys.stderr.write(
                "error: compiler output contained no '## ' section header; no law written.\n"
            )
            return 1
        body = distilled + "\n"

    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    header = (
        "<!-- commissar-law: compiled from .claude/commissar.yml\n"
        f"     compiled-at: {timestamp}\n"
        "     Generated file - do not edit by hand. Refresh with /seal-law. -->\n\n"
    )
    content = (header + render_rules_section(rules) + body).rstrip() + "\n"
    law_path.parent.mkdir(parents=True, exist_ok=True)
    law_path.write_text(content, encoding="utf-8")
    print(f"Sealed law written: {law_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
