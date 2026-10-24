#!/usr/bin/env python3
"""Flag exact cross-split text reuse; findings need human review."""

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path


def normalize(value):
    value = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.findall(r"\w+", value, flags=re.UNICODE))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path, nargs="+", help="one or more split JSONL files")
    parser.add_argument("--strict", action="store_true", help="exit non-zero if any exact overlap is flagged")
    args = parser.parse_args()
    episodes = []
    for data_path in args.data:
        with data_path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, 1):
                if not line.strip():
                    print("%s:%d: blank line" % (data_path, line_no), file=sys.stderr)
                    return 2
                try:
                    episodes.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    print("%s:%d: invalid JSON: %s" % (data_path, line_no, exc), file=sys.stderr)
                    return 2
    episode_splits = defaultdict(set)
    questions = defaultdict(list)
    messages = defaultdict(list)
    for ep in episodes:
        split = ep.get("split", "unknown")
        episode_splits[ep.get("episode_id")].add(split)
        for q in ep.get("questions", []):
            key = normalize(q.get("question", ""))
            if key:
                questions[key].append({"episode_id": ep.get("episode_id"), "split": split, "question_id": q.get("question_id")})
        for msg in ep.get("messages", []):
            text = normalize(msg.get("text", ""))
            if len(text.split()) >= 10:
                messages[text].append({"episode_id": ep.get("episode_id"), "split": split, "message_id": msg.get("message_id")})
    findings = []
    for eid, splits in episode_splits.items():
        if len(splits) > 1:
            findings.append({"kind": "episode_id_cross_split", "episode_id": eid, "splits": sorted(splits)})
    for key, rows in questions.items():
        if len(set(row["split"] for row in rows)) > 1:
            findings.append({"kind": "exact_question_cross_split", "normalized_text_sha256": hashlib.sha256(key.encode("utf-8")).hexdigest(), "items": rows})
    for key, rows in messages.items():
        if len(set(row["split"] for row in rows)) > 1:
            findings.append({"kind": "long_exact_message_cross_split", "normalized_text_sha256": hashlib.sha256(key.encode("utf-8")).hexdigest(), "items": rows})
    print(json.dumps({"episodes": len(episodes), "flagged_exact_overlaps": len(findings), "findings": findings, "limitations": "This scan finds exact normalized reuse only. A clean result does not establish semantic split independence or rule out paraphrase/template leakage; human review is required."}, ensure_ascii=False, indent=2))
    return 1 if args.strict and findings else 0


if __name__ == "__main__":
    sys.exit(main())
