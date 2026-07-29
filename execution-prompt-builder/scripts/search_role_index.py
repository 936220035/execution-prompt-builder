#!/usr/bin/env python3
"""Search the bundled role index without third-party dependencies."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROW_PATTERN = re.compile(
    r"^\|\s*`(?P<slug>[^`]+)`\s*\|\s*(?P<name>[^|]+?)\s*\|"
    r"\s*(?P<description>[^|]+?)\s*\|\s*(?P<origin>[^|]+?)\s*\|"
)


def parse_args() -> argparse.Namespace:
    default_index = Path(__file__).resolve().parent.parent / "references" / "role-index.md"
    parser = argparse.ArgumentParser(description="Search the execution prompt builder role index.")
    parser.add_argument("query", help="Space- or comma-separated search terms.")
    parser.add_argument("--limit", type=int, default=8, choices=range(1, 21))
    parser.add_argument("--index", type=Path, default=default_index)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    terms = list(dict.fromkeys(term.casefold() for term in re.split(r"[\s,，]+", args.query) if term))
    if not terms:
        raise SystemExit("Query must contain at least one search term.")

    index_path = args.index.expanduser().resolve()
    if not index_path.is_file():
        raise SystemExit(f"Role index not found: {index_path}. Run sync_role_index.py first.")

    matches: list[tuple[int, str, str, str, str]] = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        match = ROW_PATTERN.match(line)
        if not match:
            continue
        values = {key: value.strip() for key, value in match.groupdict().items()}
        haystack = " ".join(
            (values["slug"], values["name"], values["description"])
        ).casefold()
        score = sum(term in haystack for term in terms)
        if score:
            matches.append(
                (score, values["name"], values["slug"], values["description"], values["origin"])
            )

    matches.sort(key=lambda item: (-item[0], item[1].casefold()))
    if not matches:
        print(f"NO_ROLE_MATCH query={args.query}")
        return 0

    print("score\tname\tslug\tdescription\torigin")
    for match in matches[: args.limit]:
        print("\t".join((str(match[0]), *match[1:])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
