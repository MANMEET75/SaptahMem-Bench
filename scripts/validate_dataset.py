#!/usr/bin/env python3
"""Validate SaptahMem-Bench JSONL records using only the Python standard library."""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path


def parse_utc(value, where, errors):
    if not isinstance(value, str) or not value.endswith("Z"):
        errors.append("%s: timestamp must be an ISO-8601 UTC string ending in Z" % where)
        return None
    try:
        return datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        errors.append("%s: invalid ISO-8601 timestamp %r" % (where, value))
        return None


def validate_episode(ep, line_no):
    errors = []
    where = "line %s" % line_no
    if not isinstance(ep, dict):
        return [where + ": record must be a JSON object"]
    required = ["episode_id", "split", "data_origin", "start_time", "duration_hours", "scenario_domain", "language", "messages", "questions"]
    for key in required:
        if key not in ep:
            errors.append("%s: missing required field %s" % (where, key))
    if errors:
        return errors
    top_allowed = set(required)
    unknown = set(ep) - top_allowed
    if unknown:
        errors.append("%s: unknown episode fields %s" % (where, sorted(unknown)))
    if ep["split"] not in ("dev", "pilot", "test"):
        errors.append(where + ": split must be dev, pilot, or test")
    if ep["data_origin"] not in ("hand_authored_fictional", "programmatic_synthetic", "consented_prospective"):
        errors.append(where + ": data_origin must identify fictional, synthetic, or consented prospective source")
    if not isinstance(ep.get("episode_id"), str) or not re.match(r"^[a-z0-9][a-z0-9_-]+$", ep.get("episode_id", "")):
        errors.append(where + ": episode_id must match ^[a-z0-9][a-z0-9_-]+$")
    if not isinstance(ep.get("scenario_domain"), str) or len(ep.get("scenario_domain", "")) < 2:
        errors.append(where + ": scenario_domain must be a string of at least two characters")
    if not isinstance(ep.get("language"), str) or len(ep.get("language", "")) < 2:
        errors.append(where + ": language must be a string of at least two characters")
    if ep["duration_hours"] != 168:
        errors.append(where + ": duration_hours must be 168")
    start = parse_utc(ep["start_time"], where + ".start_time", errors)
    end = start + timedelta(hours=168) if start else None
    if not isinstance(ep["messages"], list) or not ep["messages"]:
        errors.append(where + ": messages must be a non-empty list")
        messages = []
    else:
        messages = ep["messages"]
        if len(messages) < 4:
            errors.append(where + ": messages must contain at least four items")
    message_ids = set()
    message_times = {}
    previous = None
    for i, msg in enumerate(messages):
        loc = "%s.messages[%d]" % (where, i)
        if not isinstance(msg, dict):
            errors.append(loc + ": message must be an object")
            continue
        unknown = set(msg) - {"message_id", "timestamp", "session_id", "speaker", "text"}
        if unknown:
            errors.append(loc + ": unknown message fields %s" % sorted(unknown))
        for key in ("message_id", "timestamp", "session_id", "speaker", "text"):
            if key not in msg:
                errors.append(loc + ": missing %s" % key)
        mid = msg.get("message_id")
        if not isinstance(mid, str) or not mid:
            errors.append(loc + ": message_id must be a non-empty string")
        elif mid in message_ids:
            errors.append(loc + ": duplicate message_id %r" % mid)
        else:
            message_ids.add(mid)
        if msg.get("speaker") not in ("user", "assistant"):
            errors.append(loc + ": speaker must be user or assistant")
        for key in ("message_id", "session_id"):
            if not isinstance(msg.get(key), str) or not msg.get(key):
                errors.append(loc + ": %s must be a non-empty string" % key)
        if not isinstance(msg.get("text"), str) or not msg.get("text", "").strip():
            errors.append(loc + ": text must be a non-empty string")
        moment = parse_utc(msg.get("timestamp"), loc + ".timestamp", errors)
        if moment:
            message_times[mid] = moment
            if previous and moment < previous:
                errors.append(loc + ": messages are not chronological")
            previous = moment
            if start and (moment < start or (end and moment >= end)):
                errors.append(loc + ": message is outside the 168-hour episode window")
    questions = ep["questions"]
    if not isinstance(questions, list) or not questions:
        errors.append(where + ": questions must be a non-empty list")
        questions = []
    qids = set()
    for i, q in enumerate(questions):
        loc = "%s.questions[%d]" % (where, i)
        if not isinstance(q, dict):
            errors.append(loc + ": question must be an object")
            continue
        q_allowed = {"question_id", "query_time", "question", "primary_category", "secondary_categories", "answerability", "gold_answer", "acceptable_answers", "source_message_ids", "rubric", "difficulty"}
        unknown = set(q) - q_allowed
        if unknown:
            errors.append(loc + ": unknown question fields %s" % sorted(unknown))
        for key in ("question_id", "query_time", "question", "primary_category", "secondary_categories", "answerability", "gold_answer", "acceptable_answers", "source_message_ids", "rubric", "difficulty"):
            if key not in q:
                errors.append(loc + ": missing %s" % key)
        qid = q.get("question_id")
        if not isinstance(qid, str) or not qid:
            errors.append(loc + ": question_id must be a non-empty string")
        elif qid in qids:
            errors.append(loc + ": duplicate question_id %r" % qid)
        else:
            qids.add(qid)
        cutoff = parse_utc(q.get("query_time"), loc + ".query_time", errors)
        if cutoff and start and (cutoff < start or (end and cutoff > end)):
            errors.append(loc + ": query_time is outside the episode boundary")
        answerability = q.get("answerability")
        if answerability not in ("answerable", "unanswerable", "ambiguous"):
            errors.append(loc + ": invalid answerability label")
        categories = ("episodic_recall", "cross_session_binding", "temporal_recency", "state_update", "ephemeral_intent", "preference_scope", "entity_binding", "distraction_resistance", "abstention", "window_boundary")
        if q.get("primary_category") not in categories:
            errors.append(loc + ": invalid primary_category")
        secondary = q.get("secondary_categories")
        if not isinstance(secondary, list) or any(not isinstance(x, str) for x in secondary) or len(set(secondary)) != len(secondary):
            errors.append(loc + ": secondary_categories must be a unique list of strings")
        if q.get("difficulty") not in ("easy", "medium", "hard"):
            errors.append(loc + ": invalid difficulty")
        if not isinstance(q.get("question"), str) or not q.get("question", "").strip():
            errors.append(loc + ": question must be a non-empty string")
        if not isinstance(q.get("rubric"), str) or not q.get("rubric", "").strip():
            errors.append(loc + ": rubric must be a non-empty string")
        acceptable = q.get("acceptable_answers")
        if not isinstance(acceptable, list) or any(not isinstance(x, str) for x in acceptable):
            errors.append(loc + ": acceptable_answers must be a list of strings")
        evidence = q.get("source_message_ids")
        if not isinstance(evidence, list):
            errors.append(loc + ": source_message_ids must be a list")
            evidence = []
        elif any(not isinstance(x, str) for x in evidence) or len(set(evidence)) != len(evidence):
            errors.append(loc + ": source_message_ids must contain unique strings")
        if answerability == "answerable" and not evidence:
            errors.append(loc + ": answerable question requires evidence")
        if answerability in ("unanswerable", "ambiguous") and q.get("gold_answer") not in (None, ""):
            errors.append(loc + ": unanswerable/ambiguous question must not have a canonical gold answer")
        if answerability == "answerable" and (not isinstance(q.get("gold_answer"), str) or not q.get("gold_answer", "").strip()):
            errors.append(loc + ": answerable question requires a non-empty gold answer")
        for mid in evidence:
            if mid not in message_ids:
                errors.append(loc + ": evidence message_id %r does not exist" % mid)
            elif cutoff and message_times.get(mid) and message_times[mid] >= cutoff:
                errors.append(loc + ": evidence %r is not strictly before query cutoff" % mid)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path, nargs="+", help="one or more UTF-8 JSONL files; one episode per line")
    parser.add_argument("--expect-main-release", action="store_true", help="require exactly 200 dev and 800 test episodes, with 16 questions per episode")
    parser.add_argument("--expect-synthetic-release", action="store_true", help="require exactly 50 pilot, 200 dev, and 800 test synthetic episodes, with 16 questions each")
    args = parser.parse_args()
    all_errors = []
    counts = {"dev": 0, "pilot": 0, "test": 0}
    seen_episode_ids = set()
    for data_path in args.data:
        with data_path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, 1):
                location = "%s:%d" % (data_path, line_no)
                if not line.strip():
                    all_errors.append(location + ": blank JSONL line")
                    continue
                try:
                    episode = json.loads(line)
                except json.JSONDecodeError as exc:
                    all_errors.append(location + ": invalid JSON: %s" % exc)
                    continue
                all_errors.extend(validate_episode(episode, location))
                if isinstance(episode, dict):
                    split = episode.get("split")
                    if split in counts:
                        counts[split] += 1
                    eid = episode.get("episode_id")
                    if eid in seen_episode_ids:
                        all_errors.append(location + ": duplicate episode_id %r" % eid)
                    seen_episode_ids.add(eid)
                    if (args.expect_main_release or args.expect_synthetic_release) and len(episode.get("questions", [])) != 16:
                        all_errors.append(location + ": release target requires 16 questions per episode")
                    if args.expect_synthetic_release and episode.get("data_origin") != "programmatic_synthetic":
                        all_errors.append(location + ": synthetic release records must be marked programmatic_synthetic")
    if args.expect_main_release and (counts["dev"] != 200 or counts["test"] != 800 or counts["pilot"] != 0):
        all_errors.append("main release counts must be dev=200, test=800, pilot=0; found %s" % counts)
    if args.expect_synthetic_release and (counts["pilot"] != 50 or counts["dev"] != 200 or counts["test"] != 800):
        all_errors.append("synthetic release counts must be pilot=50, dev=200, test=800; found %s" % counts)
    if all_errors:
        print("Dataset validation failed (%d issue(s)):" % len(all_errors), file=sys.stderr)
        for item in all_errors:
            print("- " + item, file=sys.stderr)
        return 1
    print("Valid JSONL records: %d (dev=%d, pilot=%d, test=%d)" % (sum(counts.values()), counts["dev"], counts["pilot"], counts["test"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
