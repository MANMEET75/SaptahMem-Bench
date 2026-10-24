#!/usr/bin/env python3
"""Score answer predictions against episode JSONL; standard-library only."""

import argparse
import json
import random
import string
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path


def norm(value):
    value = unicodedata.normalize("NFKC", value).casefold()
    value = " ".join(value.split())
    while value and (unicodedata.category(value[-1]).startswith("P") or value[-1] in string.punctuation):
        value = value[:-1]
    while value and (unicodedata.category(value[0]).startswith("P") or value[0] in string.punctuation):
        value = value[1:]
    return " ".join(value.split())


def load_predictions(path):
    result = {}
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                raise ValueError("%s:%d: blank prediction line" % (path, line_no))
            row = json.loads(line)
            for key in ("episode_id", "question_id", "answer", "abstained"):
                if key not in row:
                    raise ValueError("%s:%d: missing prediction field %s" % (path, line_no, key))
            if not isinstance(row["answer"], str) or not isinstance(row["abstained"], bool):
                raise ValueError("%s:%d: answer must be string and abstained must be Boolean" % (path, line_no))
            evidence = row.get("evidence_message_ids", [])
            if not isinstance(evidence, list) or any(not isinstance(x, str) for x in evidence):
                raise ValueError("%s:%d: evidence_message_ids must be an array of strings" % (path, line_no))
            key = (row["episode_id"], row["question_id"])
            if key in result:
                raise ValueError("%s:%d: duplicate prediction for %s/%s" % (path, line_no, key[0], key[1]))
            result[key] = row
    return result


def load_gold(path):
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                raise ValueError("%s:%d: blank gold line" % (path, line_no))
            ep = json.loads(line)
            for q in ep["questions"]:
                rows.append({"episode_id": ep["episode_id"], "question_id": q["question_id"], "category": q["primary_category"], "answerability": q["answerability"], "gold": q.get("gold_answer"), "acceptable": q.get("acceptable_answers", []), "evidence": q.get("source_message_ids", [])})
    return rows


def join_and_score(gold_rows, predictions, label):
    expected = set((r["episode_id"], r["question_id"]) for r in gold_rows)
    actual = set(predictions)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing or extra:
        raise ValueError("%s predictions mismatch gold: %d missing, %d extra; first missing=%r first extra=%r" % (label, len(missing), len(extra), missing[:1], extra[:1]))
    scored = []
    for g in gold_rows:
        p = predictions[(g["episode_id"], g["question_id"])]
        if g["answerability"] == "answerable":
            targets = [g["gold"]] + list(g["acceptable"])
            correct = (not p["abstained"] and norm(p["answer"]) in set(norm(x) for x in targets if isinstance(x, str)))
        else:
            correct = bool(p["abstained"])
        row = dict(g)
        row.update({"prediction": p["answer"], "abstained": p["abstained"], "correct": bool(correct), "predicted_evidence": p.get("evidence_message_ids", []), "system": label})
        if g["evidence"] and "evidence_message_ids" in p:
            pred_set = set(p["evidence_message_ids"])
            gold_set = set(g["evidence"])
            tp = len(pred_set & gold_set)
            precision = tp / len(pred_set) if pred_set else 0.0
            recall = tp / len(gold_set) if gold_set else 0.0
            row["evidence_precision"] = precision
            row["evidence_recall"] = recall
            row["evidence_f1"] = (2 * precision * recall / (precision + recall)) if precision + recall else 0.0
        scored.append(row)
    return scored


def summarize(rows):
    if not rows:
        return {"count": 0, "accuracy": None, "by_category": {}, "by_answerability": {}}
    categories = defaultdict(list)
    answerability = defaultdict(list)
    episodes = defaultdict(list)
    for row in rows:
        categories[row["category"]].append(row["correct"])
        answerability[row["answerability"]].append(row["correct"])
        episodes[row["episode_id"]].append(row)
    category_scores = {k: {"count": len(v), "accuracy": sum(v) / len(v)} for k, v in sorted(categories.items())}
    strata_scores = {k: {"count": len(v), "accuracy": sum(v) / len(v)} for k, v in sorted(answerability.items())}
    macro = sum(x["accuracy"] for x in category_scores.values()) / len(category_scores)
    abstain_targets = [r for r in rows if r["answerability"] in ("unanswerable", "ambiguous")]
    abstain_predictions = [r for r in rows if r["abstained"]]
    abstain_true_positives = [r for r in abstain_targets if r["abstained"]]
    abstain_precision = len(abstain_true_positives) / len(abstain_predictions) if abstain_predictions else 0.0
    abstain_recall = len(abstain_true_positives) / len(abstain_targets) if abstain_targets else None
    abstain_f1 = (2 * abstain_precision * abstain_recall / (abstain_precision + abstain_recall)) if abstain_recall is not None and abstain_precision + abstain_recall else 0.0
    answerable = [r for r in rows if r["answerability"] == "answerable"]
    false_abstentions = sum(1 for r in answerable if r["abstained"])
    false_assertions = sum(1 for r in abstain_targets if not r["abstained"])
    citations = [r for r in rows if "evidence_precision" in r]
    result = {"count": len(rows), "episode_count": len(episodes), "micro_accuracy": sum(r["correct"] for r in rows) / len(rows), "category_macro_accuracy": macro, "by_category": category_scores, "by_answerability": strata_scores, "abstention": {"precision": abstain_precision, "recall": abstain_recall, "f1": abstain_f1, "false_abstentions_on_answerable": false_abstentions, "missed_abstentions_false_assertions": false_assertions, "coverage": sum(1 for r in rows if not r["abstained"]) / len(rows)}}
    if citations:
        result["evidence"] = {"cited_answerable_count": len(citations), "precision": sum(r["evidence_precision"] for r in citations) / len(citations), "recall": sum(r["evidence_recall"] for r in citations) / len(citations), "f1": sum(r["evidence_f1"] for r in citations) / len(citations)}
    return result


def bootstrap(rows, replicates, seed):
    by_episode = defaultdict(list)
    for row in rows:
        by_episode[row["episode_id"]].append(row)
    ids = sorted(by_episode)
    if len(ids) < 2 or replicates <= 0:
        return None
    rng = random.Random(seed)
    values = []
    for unused in range(replicates):
        sample = []
        for i in range(len(ids)):
            sample.extend(by_episode[ids[rng.randrange(len(ids))]])
        values.append(summarize(sample)["category_macro_accuracy"])
    values.sort()
    lo = values[int(0.025 * (len(values) - 1))]
    hi = values[int(0.975 * (len(values) - 1))]
    return {"level": 0.95, "unit": "episode_cluster", "replicates": replicates, "seed": seed, "lower": lo, "upper": hi}


def paired_delta(rows_a, rows_b, replicates, seed):
    other = {(r["episode_id"], r["question_id"]): r for r in rows_b}
    if set(other) != set((r["episode_id"], r["question_id"]) for r in rows_a):
        raise ValueError("Cannot compare systems: prediction item sets differ")
    grouped = defaultdict(list)
    for row in rows_a:
        r2 = other[(row["episode_id"], row["question_id"])]
        grouped[row["episode_id"]].append((row["category"], int(row["correct"]) - int(r2["correct"])))

    def metric(items):
        cats = defaultdict(list)
        for group in items:
            for cat, delta in group:
                cats[cat].append(delta)
        return sum(sum(v) / len(v) for v in cats.values()) / len(cats) if cats else 0.0

    groups = [grouped[eid] for eid in sorted(grouped)]
    point = metric(groups)
    if len(groups) < 2 or replicates <= 0:
        return {"macro_accuracy_delta_a_minus_b": point, "level": 0.95, "unit": "paired_episode_cluster", "replicates": 0, "seed": seed, "lower": None, "upper": None}
    rng = random.Random(seed)
    samples = [metric([groups[rng.randrange(len(groups))] for i in range(len(groups))]) for _ in range(replicates)]
    samples.sort()
    return {"macro_accuracy_delta_a_minus_b": point, "level": 0.95, "unit": "paired_episode_cluster", "replicates": replicates, "seed": seed, "lower": samples[int(0.025 * (len(samples) - 1))], "upper": samples[int(0.975 * (len(samples) - 1))]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gold", required=True, type=Path, help="episode JSONL with labels; only use public dev locally")
    parser.add_argument("--predictions", required=True, type=Path)
    parser.add_argument("--compare", type=Path, help="optional reference-system predictions on the same items")
    parser.add_argument("--name", default="system_a")
    parser.add_argument("--compare-name", default="system_b")
    parser.add_argument("--per-item-out", type=Path)
    parser.add_argument("--bootstrap", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20261025)
    args = parser.parse_args()
    if args.bootstrap < 0:
        parser.error("--bootstrap must be non-negative")
    try:
        gold = load_gold(args.gold)
        rows_a = join_and_score(gold, load_predictions(args.predictions), args.name)
        summary_a = summarize(rows_a)
        summary_a["category_macro_accuracy_ci"] = bootstrap(rows_a, args.bootstrap, args.seed)
        report = {"system": args.name, "summary": summary_a}
        all_rows = rows_a
        if args.compare:
            rows_b = join_and_score(gold, load_predictions(args.compare), args.compare_name)
            summary_b = summarize(rows_b)
            summary_b["category_macro_accuracy_ci"] = bootstrap(rows_b, args.bootstrap, args.seed)
            report["comparison_system"] = args.compare_name
            report["comparison_summary"] = summary_b
            report["paired_comparison"] = paired_delta(rows_a, rows_b, args.bootstrap, args.seed)
            all_rows = rows_a + rows_b
        if args.per_item_out:
            with args.per_item_out.open("w", encoding="utf-8", newline="\n") as handle:
                for row in all_rows:
                    handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print("Scoring failed: %s" % exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
