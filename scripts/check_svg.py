#!/usr/bin/env python3
"""Perform deterministic structural checks on self-contained SVG files."""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
REFERENCE_RE = re.compile(r"url\(#([^)]+)\)")
REMOTE_RE = re.compile(r"^(?:https?:)?//", re.IGNORECASE)


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    message: str


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_viewbox(value: str | None) -> tuple[float, float, float, float] | None:
    if not value:
        return None
    parts = re.split(r"[\s,]+", value.strip())
    if len(parts) != 4:
        return None
    try:
        parsed = tuple(float(part) for part in parts)
    except ValueError:
        return None
    if parsed[2] <= 0 or parsed[3] <= 0:
        return None
    return parsed  # type: ignore[return-value]


def iter_attributes(root: ET.Element) -> Iterable[tuple[ET.Element, str, str]]:
    for element in root.iter():
        for name, value in element.attrib.items():
            yield element, name, value


def check_svg(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        tree = ET.parse(path)
    except (ET.ParseError, OSError) as exc:
        return [Finding("error", "xml-parse", f"Cannot parse SVG: {exc}")]

    root = tree.getroot()
    if local_name(root.tag) != "svg":
        return [Finding("error", "root-element", "Root element is not <svg>.")]

    if parse_viewbox(root.get("viewBox")) is None:
        findings.append(Finding("error", "viewbox", "A valid positive viewBox is required."))

    direct_children = list(root)
    title = next((child for child in direct_children if local_name(child.tag) == "title"), None)
    desc = next((child for child in direct_children if local_name(child.tag) == "desc"), None)
    if title is None or not "".join(title.itertext()).strip():
        findings.append(Finding("error", "title", "Add a non-empty root-level <title>."))
    if desc is None or not "".join(desc.itertext()).strip():
        findings.append(Finding("warning", "description", "Add a non-empty root-level <desc>."))

    if root.get("role") != "img":
        findings.append(Finding("warning", "role", 'Set role="img" on the root SVG.'))
    if not root.get("aria-labelledby"):
        findings.append(Finding("warning", "aria-labelledby", "Connect the root to title and description IDs."))

    ids: dict[str, int] = {}
    references: set[str] = set()
    for element, name, value in iter_attributes(root):
        if name == "id":
            ids[value] = ids.get(value, 0) + 1
        references.update(REFERENCE_RE.findall(value))

        attribute_name = local_name(name)
        if attribute_name in {"href", "src"} and REMOTE_RE.match(value.strip()):
            findings.append(
                Finding("error", "remote-resource", f"Remote resource is not self-contained: {value}")
            )

        if local_name(element.tag) == "text" and attribute_name == "font-size":
            match = re.match(r"^([0-9.]+)", value.strip())
            if match and float(match.group(1)) < 12:
                findings.append(
                    Finding("warning", "small-text", f"Text smaller than 12 px found: {value}")
                )

    for duplicated_id, count in sorted(ids.items()):
        if count > 1:
            findings.append(
                Finding("error", "duplicate-id", f'ID "{duplicated_id}" appears {count} times.')
            )

    for missing_id in sorted(references.difference(ids)):
        findings.append(
            Finding("error", "broken-reference", f'Reference points to missing ID "{missing_id}".')
        )

    for element in root.iter():
        name = local_name(element.tag)
        if name == "script":
            findings.append(Finding("error", "script", "Static SVG must not contain scripts."))
        elif name == "foreignObject":
            findings.append(
                Finding("warning", "foreign-object", "foreignObject may reduce SVG portability.")
            )

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="SVG files to check")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    report: dict[str, list[dict[str, str]]] = {}
    has_error = False
    for path in args.paths:
        findings = check_svg(path)
        report[str(path)] = [asdict(finding) for finding in findings]
        has_error = has_error or any(finding.level == "error" for finding in findings)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        for path, findings in report.items():
            print(f"{path}: {len(findings)} finding(s)")
            for finding in findings:
                print(f"  {finding['level'].upper():7} {finding['code']}: {finding['message']}")
            if not findings:
                print("  OK")

    return 1 if has_error else 0


if __name__ == "__main__":
    sys.exit(main())
