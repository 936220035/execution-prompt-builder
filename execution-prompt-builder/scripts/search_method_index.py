#!/usr/bin/env python3
"""Route a request to original, local work methods without dependencies."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


BLOCKED_PATTERNS = (
    r"\bbug\b", r"异常", r"报错", r"排错", r"故障", r"修复",
    r"部署", r"发布", r"上线", r"production", r"incident", r"rollback",
    r"数据库", r"\bdatabase\b", r"迁移", r"账号", r"权限", r"account", r"credential",
)


def parse_args() -> argparse.Namespace:
    default_index = Path(__file__).resolve().parent.parent / "references" / "method-index.json"
    parser = argparse.ArgumentParser(description="Route a request to execution prompt builder methods.")
    parser.add_argument("query", help="Natural-language task description.")
    parser.add_argument("--limit", type=int, default=3, choices=range(1, 4))
    parser.add_argument("--index", type=Path, default=default_index)
    return parser.parse_args()


def load_methods(index_path: Path) -> list[dict[str, object]]:
    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read method index: {index_path}") from exc
    methods = data.get("methods")
    if not isinstance(methods, list) or not methods:
        raise ValueError("Method index must contain a non-empty methods list.")
    identifiers: set[str] = set()
    for method in methods:
        if not isinstance(method, dict):
            raise ValueError("Each method must be an object.")
        identifier = method.get("id")
        keywords = method.get("keywords")
        if not isinstance(identifier, str) or not re.fullmatch(r"[a-z0-9-]+", identifier):
            raise ValueError("Each method id must use lowercase letters, digits, and hyphens.")
        if identifier in identifiers:
            raise ValueError(f"Duplicate method id: {identifier}")
        if not isinstance(keywords, list) or not all(isinstance(item, str) and item for item in keywords):
            raise ValueError(f"Method {identifier} must contain non-empty keywords.")
        identifiers.add(identifier)
    return methods


def is_blocked(query: str) -> bool:
    return any(re.search(pattern, query, flags=re.IGNORECASE) for pattern in BLOCKED_PATTERNS)


def route(query: str, methods: list[dict[str, object]], limit: int = 3) -> list[tuple[int, dict[str, object]]]:
    normalized = query.casefold()
    ranked: list[tuple[int, dict[str, object]]] = []
    for method in methods:
        keywords = method["keywords"]
        score = sum(str(keyword).casefold() in normalized for keyword in keywords)
        if score:
            ranked.append((score, method))
    return sorted(ranked, key=lambda item: (-item[0], str(item[1]["id"])))[:limit]


def main() -> int:
    args = parse_args()
    query = args.query.strip()
    if not query:
        raise SystemExit("Query must not be empty.")
    try:
        methods = load_methods(args.index.expanduser().resolve())
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    if is_blocked(query):
        print("METHOD_GATE category=non_product reason=operational_or_incident_task")
        return 0
    matches = route(query, methods, args.limit)
    if not matches:
        print(f"NO_METHOD_MATCH query={query}")
        return 0
    print("score\tid\tname_zh\tname_en\tfamily\tcontract")
    for score, method in matches:
        print("\t".join((
            str(score), str(method["id"]), str(method["name_zh"]), str(method["name_en"]),
            str(method["family"]), str(method["contract"]),
        )))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
