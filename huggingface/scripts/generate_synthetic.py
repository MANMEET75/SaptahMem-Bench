#!/usr/bin/env python3
"""Generate the deterministic, explicitly synthetic SaptahMem short-term-memory corpus."""

import argparse
from collections import Counter
import hashlib
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path


DEFAULT_SEED = 20261025
COUNTS = {"pilot": 50, "dev": 200, "test": 800}

DOMAINS = [
    ("travel_planning", "weekend trip"),
    ("home_organization", "storage-room reset"),
    ("learning", "photography class"),
    ("hobby_project", "balcony garden project"),
    ("community_event", "neighborhood book swap"),
    ("work_planning", "team workshop"),
    ("errand_planning", "bike-repair and supply run"),
    ("meal_planning", "friends' dinner plan"),
]

SPLIT_POOLS = {
    "pilot": {
        "names": ["Avery", "Morgan", "Riley", "Casey", "Jordan", "Taylor", "Quinn", "Cameron", "Drew", "Skyler", "Parker", "Reese", "Rowan", "Jamie", "Blair", "Emery", "Finley", "Sage", "Robin", "Kendall"],
        "venues": ["Cedar Hall", "Maple Studio", "North Pier Room", "Orchard House", "Juniper Library", "Willow Workshop", "Harbor Room", "Pine Commons", "Meadow Studio", "Birch Center"],
        "items": ["folding chairs", "supply box", "printed guide", "tool roll", "snack tray", "seed packets", "photo backdrop", "paper labels", "tea thermos", "display stand"],
        "tasks": ["setting up the sign-in table", "checking the projector", "bringing the spare notebook", "arranging the welcome table", "packing the extension cable", "printing the route sheet", "watering the seedlings", "collecting the name cards", "sorting the recipe notes", "returning the borrowed stand"],
    },
    "dev": {
        "names": ["Alex", "Bailey", "Charlie", "Dakota", "Elliot", "Frankie", "Gray", "Harper", "Indigo", "Jules", "Kai", "Logan", "Micah", "Nico", "Oakley", "Peyton", "Remy", "Shiloh", "Toby", "Winter"],
        "venues": ["Riverstone Room", "Linden Studio", "Eastgate Hall", "Clover Library", "Summit Workshop", "Bluebell Center", "Station Gallery", "Garden Annex", "Canal House", "Elm Commons"],
        "items": ["canvas tote", "route cards", "coffee urn", "repair kit", "reference sheets", "plant markers", "display boards", "folded map", "serving tray", "supply basket"],
        "tasks": ["laying out the route cards", "charging the speaker", "bringing the spare marker", "setting out the name tags", "packing the measuring tape", "printing the check-in list", "labeling the plant trays", "collecting the handouts", "arranging the serving plates", "returning the borrowed lamp"],
    },
    "test": {
        "names": ["Adrian", "Brooke", "Cleo", "Devon", "Ellis", "Farah", "Gale", "Hollis", "Imani", "Jo", "Keegan", "Lane", "Marlowe", "Nia", "Orion", "Priya", "Rory", "Sam", "Teagan", "Uma", "Val", "Wren", "Xander", "Yara", "Zuri"],
        "venues": ["Ashford Room", "Beacon Studio", "Copperfield Hall", "Dovetail Library", "Evergreen Annex", "Foxglove Center", "Granary Workshop", "Highland Gallery", "Inkstone House", "Kestrel Commons", "Lighthouse Room", "Millbrook Studio", "Nightingale Hall", "Overlook Library", "Pebble Workshop", "Queensway Center", "Redfern Room", "Stonebridge Hall", "Tidepool Studio", "Upfield Commons", "Valley Annex", "Westhaven Gallery", "Yellowbrick Room", "Zephyr House"],
        "items": ["linen banner", "checklist folder", "portable kettle", "patch set", "lesson notes", "watering can", "poster tubes", "ticket envelope", "serving platter", "parts case", "reference binder", "table runner", "clip-on light", "garden twine", "name-card stack"],
        "tasks": ["preparing the welcome sign", "testing the room microphone", "bringing the spare pencil case", "setting up the display corner", "packing the small toolkit", "printing the attendance sheet", "marking the seedling rows", "gathering the instruction cards", "arranging the table settings", "dropping off the borrowed easel", "checking the supply shelf", "folding the seating chart"],
    },
}

COLORS = ["amber", "blue", "coral", "green", "indigo", "silver", "teal", "violet", "white", "yellow"]
LAYOUTS = ["large-print", "two-column", "plain-text", "diagram-first", "high-contrast", "compact", "step-by-step", "landscape", "numbered", "minimal"]
TIMES = ["8:15 am", "9:40 am", "10:20 am", "11:35 am", "12:10 pm", "1:25 pm", "2:45 pm", "3:30 pm", "4:50 pm", "6:05 pm", "7:20 pm", "8:40 pm"]
OTHER_EVENTS = ["a pottery sale", "a concert poster", "a farmers' market notice", "a film screening", "a repair cafe listing", "a garden tour advert", "a lecture flyer", "a bookshop notice"]


def iso_time(start, hours):
    return (start + timedelta(hours=hours)).isoformat(timespec="seconds").replace("+00:00", "Z")


def question(qid, query_time, text, category, answerability, gold, acceptable, evidence, rubric, difficulty):
    return {
        "question_id": qid,
        "query_time": query_time,
        "question": text,
        "primary_category": category,
        "secondary_categories": [],
        "answerability": answerability,
        "gold_answer": gold,
        "acceptable_answers": acceptable,
        "source_message_ids": evidence,
        "rubric": rubric,
        "difficulty": difficulty,
    }


def build_episode(split, local_index, global_index, seed):
    rng = random.Random(seed + global_index * 1009)
    pool = SPLIT_POOLS[split]
    names = rng.sample(pool["names"], 4)
    domain, project_label = DOMAINS[global_index % len(DOMAINS)]
    start = datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc) + timedelta(days=global_index)
    project_date = (start + timedelta(days=5)).strftime("%d %B %Y")
    project = "the %s scheduled for %s" % (project_label, project_date)
    venue = pool["venues"][local_index % len(pool["venues"])]
    item = pool["items"][(local_index * 3 + global_index) % len(pool["items"])]
    task_a = pool["tasks"][(local_index * 2 + global_index) % len(pool["tasks"])]
    task_b = pool["tasks"][(local_index * 2 + global_index + 3) % len(pool["tasks"])]
    extra_item = pool["items"][(local_index * 5 + global_index + 2) % len(pool["items"])]
    if extra_item == item:
        extra_item = pool["items"][(pool["items"].index(extra_item) + 1) % len(pool["items"])]
    old_time = rng.choice(TIMES)
    new_time = rng.choice([value for value in TIMES if value != old_time])
    weekday = (start + timedelta(days=5)).strftime("%A")
    deadline = start + timedelta(days=4)
    deadline_label = deadline.strftime("%A, %d %B %Y")
    deadline_time = rng.choice(["9:00 am", "11:30 am", "1:00 pm", "4:15 pm", "6:30 pm"])
    layout = rng.choice(LAYOUTS)
    color = rng.choice(COLORS)
    distraction_event = rng.choice(OTHER_EVENTS)
    distraction_venue = "the " + rng.choice(["west", "upper", "lower", "garden", "market", "studio", "central", "riverside"]) + " room"
    distraction_time = rng.choice([value for value in TIMES if value not in (old_time, new_time)])
    person_a, person_b, person_c, person_d = names

    # Each split has a distinct surface realization family. The underlying task
    # and evidence structure stays fixed so results are comparable by capability.
    if split == "pilot":
        opening = "I'm sorting out %s. I pencilled in %s on %s at %s." % (project, venue, weekday, old_time)
        preference = "For this plan, could you use a %s layout? That's just for %s, not a general preference." % (layout, project)
        offer = "%s offered to bring the %s. I'll handle %s; %s might handle %s, but I haven't checked with them." % (person_a, item, task_a, person_b, task_b)
        update = "Change of plan: %s won't work. Move %s to %s on %s; %s is still the venue." % (old_time, project, new_time, weekday, venue)
        distraction = "Unrelated: I saw %s advertised in %s at %s. I'm only browsing." % (distraction_event, distraction_venue, distraction_time)
        ambiguity = "For %s, I could ask %s or %s to pick up the %s. I haven't chosen anyone yet." % (project, person_c, person_d, extra_item)
        confirmation = "%s confirmed the %s, and %s agreed to %s for %s." % (person_a, item, person_b, task_b, project)
        commitment = "I'll send the final notes to %s by %s at %s." % (person_a, deadline_label, deadline_time)
        boundary = "One last detail for %s: the backup tag is %s." % (project, color)
        phrasing = [
            "Where had %s first been pencilled in?" % project,
            "What time was originally pencilled in for %s?" % project,
            "Who offered the %s for %s?" % (item, project),
            "What will %s do for %s?" % (person_b, project),
            "What is the current start time for %s?" % project,
            "Which time was replaced when the plan changed?",
            "By when will the final notes go to %s?" % person_a,
            "Which layout did the user request just for this plan?",
            "Which task did %s agree to handle?" % person_b,
            "Which venue is still booked for %s, ignoring the unrelated advert?" % project,
            "What color was the backup tag mentioned near the end of the week?",
            "Summarize the current venue and time for %s." % project,
        ]
    elif split == "dev":
        opening = "I'm organizing %s. The first idea was %s on %s at %s." % (project, venue, weekday, old_time)
        preference = "For %s only, please make the handout %s. I don't mean that as my usual format." % (project, layout)
        offer = "My friend %s said they could bring the %s. I'll handle %s, and %s may cover %s, though I haven't heard back." % (person_a, item, task_a, person_b, task_b)
        update = "Update for %s: replace %s with %s on %s. The location remains %s." % (project, old_time, new_time, weekday, venue)
        distraction = "Separate from that, I noticed %s at %s at %s; it was just something I saw." % (distraction_event, distraction_venue, distraction_time)
        ambiguity = "For %s, I could ask either %s or %s to pick up the %s, but I haven't decided." % (project, person_c, person_d, extra_item)
        confirmation = "Good news: %s confirmed the %s, and %s will handle %s for %s." % (person_a, item, person_b, task_b, project)
        commitment = "I need to send the final notes to %s by %s, no later than %s." % (person_a, deadline_label, deadline_time)
        boundary = "Near the end of the week, one detail: %s's backup tag is %s." % (project, color)
        phrasing = [
            "Which location was the first plan for %s?" % project,
            "Before the update, what start time had been chosen for %s?" % project,
            "For %s, which friend is bringing the %s?" % (project, item),
            "What job did %s agree to do for %s?" % (person_b, project),
            "At what time is %s now planned to start?" % project,
            "What changed between the first and revised schedule for %s?" % project,
            "What is the deadline for sending the notes to %s?" % person_a,
            "What handout format was requested for %s specifically?" % project,
            "Which responsibility belongs to %s for %s?" % (person_b, project),
            "Which venue is part of %s, not the separate listing?" % project,
            "What is the backup-tag color for %s at the late-week cutoff?" % project,
            "Give the current venue and revised start time for %s." % project,
        ]
    else:
        opening = "I've got %s coming up. My initial notes say %s, %s, at %s." % (project, venue, weekday, old_time)
        preference = "For %s specifically, use a %s handout. That's a one-time request, not my standing preference." % (project, layout)
        offer = "%s volunteered to bring our %s. I can handle %s; %s might handle %s, but they haven't confirmed yet." % (person_a, item, task_a, person_b, task_b)
        update = "Schedule correction for %s: the time is now %s instead of %s on %s. Keep the venue at %s." % (project, new_time, old_time, weekday, venue)
        distraction = "On another topic, there's %s listed for %s at %s. That isn't part of my plan." % (distraction_event, distraction_venue, distraction_time)
        ambiguity = "For %s, either %s or %s could collect the %s; I haven't settled on one." % (project, person_c, person_d, extra_item)
        confirmation = "That's settled: %s is bringing the %s, and %s has confirmed they will handle %s for %s." % (person_a, item, person_b, task_b, project)
        commitment = "I'll get the final notes to %s by %s, before %s." % (person_a, deadline_label, deadline_time)
        boundary = "Final note before the week closes: the backup label for %s is %s." % (project, color)
        phrasing = [
            "What place appeared in the first notes for %s?" % project,
            "Which start time was listed before it changed for %s?" % project,
            "Who is confirmed to bring the %s for %s?" % (item, project),
            "For %s, which task has %s taken on?" % (project, person_b),
            "At what time should %s happen now?" % project,
            "How was the original time revised for %s?" % project,
            "When are the final notes due to %s?" % person_a,
            "Which format applies only to %s?" % project,
            "What has %s agreed to do for %s?" % (person_b, project),
            "Which venue should be used for %s rather than the unrelated listing?" % project,
            "Near the 168-hour boundary, what color was the backup label for %s?" % project,
            "What are the venue and current time for %s?" % project,
        ]

    messages = []
    def add(mid, hour, session, speaker, text):
        messages.append({"message_id": mid, "timestamp": iso_time(start, hour), "session_id": session, "speaker": speaker, "text": text})

    add("m01", 0.2, "s0", "user", opening)
    add("m02", 0.25, "s0", "assistant", "I have that first plan noted for %s." % project)
    add("m03", 0.35, "s0", "user", preference)
    add("m04", 0.4, "s0", "assistant", "Understood; I'll keep that format scoped to %s." % project)
    add("m05", 24.2, "s1", "user", offer)
    add("m06", 24.3, "s1", "assistant", "I'll treat %s as tentative for %s until they confirm." % (person_b, project))
    add("m07", 48.2, "s2", "user", update)
    add("m08", 48.3, "s2", "assistant", "Got it: %s at %s, with %s unchanged." % (new_time, venue, weekday))
    add("m09", 72.2, "s3", "user", distraction + " It is unrelated to " + project + ".")
    add("m10", 72.3, "s3", "assistant", "That separate listing sounds interesting, but it is unrelated to %s." % project)
    add("m11", 72.7, "s3", "user", ambiguity)
    add("m12", 72.8, "s3", "assistant", "I'll leave that pickup unassigned for %s until you choose." % project)
    add("m13", 96.1, "s4", "user", confirmation)
    add("m14", 96.2, "s4", "assistant", "Thanks; %s and %s are now confirmed for %s." % (person_a, person_b, project))
    add("m15", 96.4, "s4", "user", commitment + " This is for " + project + ".")
    add("m16", 96.5, "s4", "assistant", "I have the final-notes deadline as %s at %s for %s." % (deadline_label, deadline_time, project))
    add("m17", 167.0, "s5", "user", boundary)
    add("m18", 167.1, "s5", "assistant", "Noted: the backup tag is %s for %s." % (color, project))

    def qtime(hours):
        return iso_time(start, hours)

    qs = [
        question("q01", qtime(30), phrasing[0], "episodic_recall", "answerable", venue, ["at " + venue, venue + " was the venue"], ["m01"], "Must name the original venue for this project.", "easy"),
        question("q02", qtime(40), phrasing[1], "episodic_recall", "answerable", old_time, ["It was " + old_time, old_time + " was the original time"], ["m01"], "Must give the initially stated time.", "medium"),
        question("q03", qtime(110), phrasing[2], "cross_session_binding", "answerable", person_a, [person_a + " is bringing the " + item], ["m05", "m13"], "Must identify the person confirmed to bring the named item for this project.", "medium"),
        question("q04", qtime(110), phrasing[3], "cross_session_binding", "answerable", task_b, [person_b + " will handle " + task_b], ["m05", "m13"], "Must bind the confirmed task to the correct person.", "medium"),
        question("q05", qtime(112), phrasing[4], "temporal_recency", "answerable", new_time, ["The current time is " + new_time], ["m07"], "Must report the current time after the explicit correction.", "easy"),
        question("q06", qtime(113), phrasing[5], "state_update", "answerable", "The time changed from %s to %s." % (old_time, new_time), ["From %s to %s" % (old_time, new_time), "%s replaced by %s" % (old_time, new_time)], ["m01", "m07"], "Must distinguish the old and current values in the correct direction.", "hard"),
        question("q07", qtime(120), phrasing[6], "ephemeral_intent", "answerable", "%s at %s" % (deadline_label, deadline_time), ["By %s at %s" % (deadline_label, deadline_time), "%s, %s" % (deadline_time, deadline_label)], ["m15", "m16"], "Must give the stated deadline for sending the final notes; do not treat it as a permanent preference.", "medium"),
        question("q08", qtime(90), phrasing[7], "preference_scope", "answerable", layout, ["%s layout" % layout, "%s format" % layout], ["m03"], "Must name the requested format and retain its one-project scope; do not generalize it as a standing preference.", "medium"),
        question("q09", qtime(121), phrasing[8], "entity_binding", "answerable", task_b, [person_b + " will handle " + task_b], ["m13"], "Must assign the confirmed responsibility to the correct person.", "medium"),
        question("q10", qtime(115), phrasing[9], "distraction_resistance", "answerable", venue, ["the venue is " + venue], ["m07", "m09"], "Must use the venue for the named project and ignore the unrelated listing's venue and time.", "hard"),
        question("q11", qtime(167.5), phrasing[10], "window_boundary", "answerable", color, ["The color is " + color, color + " backup label"], ["m17"], "Must retrieve the detail stated near the end of the 168-hour window.", "medium"),
        question("q12", qtime(122), phrasing[11], "temporal_recency", "answerable", "%s at %s on %s" % (venue, new_time, weekday), ["%s, %s, %s" % (venue, new_time, weekday), "%s at %s" % (venue, new_time)], ["m01", "m07"], "Must report the current venue and revised time; include weekday if the answer gives it.", "hard"),
        question("q13", qtime(70), "What total budget was set for %s?" % project, "abstention", "unanswerable", None, [], [], "The conversation states no budget. Do not invent one.", "easy"),
        question("q14", qtime(80), "What room number is reserved for %s at %s?" % (project, venue), "abstention", "unanswerable", None, [], [], "The venue is named but no room number is provided.", "medium"),
        question("q15", qtime(110), "Which payment method did the user choose for %s?" % project, "abstention", "unanswerable", None, [], [], "No payment method is mentioned in the visible prefix.", "medium"),
        question("q16", qtime(111), "Who will definitely collect the %s for %s?" % (extra_item, project), "abstention", "ambiguous", None, [], ["m11", "m12"], "The user explicitly has not chosen between two possible people. A definite answer is unsupported; abstain or state the uncertainty.", "hard"),
    ]
    return {
        "episode_id": "synthetic_%s_%04d" % (split, local_index + 1),
        "split": split,
        "data_origin": "programmatic_synthetic",
        "start_time": start.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "duration_hours": 168,
        "scenario_domain": domain,
        "language": "en",
        "messages": messages,
        "questions": qs,
    }


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=Path("data/synthetic"))
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--pilot", type=int, default=COUNTS["pilot"])
    parser.add_argument("--dev", type=int, default=COUNTS["dev"])
    parser.add_argument("--test", type=int, default=COUNTS["test"])
    args = parser.parse_args()
    if min(args.pilot, args.dev, args.test) < 1:
        parser.error("pilot, dev, and test counts must each be at least 1")
    manifest = {
        "name": "SaptahMem-Bench Synthetic Track",
        "version": "0.3.0-synthetic-prep",
        "data_origin": "programmatic_synthetic",
        "seed": args.seed,
        "episodes_per_split": {},
        "questions_per_episode": 16,
        "question_counts_per_split": {},
        "domain_counts_per_split": {},
        "category_counts_per_split": {},
        "answerability_counts_per_split": {},
        "difficulty_counts_per_split": {},
        "contains_real_participant_data": False,
        "generation_note": "Deterministic template-driven fictional conversations. Useful for controlled tooling and system comparisons only; not evidence of real-user performance.",
        "files": {},
    }
    total = 0
    for split, count in (("pilot", args.pilot), ("dev", args.dev), ("test", args.test)):
        rows = [build_episode(split, i, total + i, args.seed) for i in range(count)]
        total += count
        path = args.output_root / split / "episodes.jsonl"
        write_jsonl(path, rows)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        manifest["episodes_per_split"][split] = count
        manifest["question_counts_per_split"][split] = sum(len(row["questions"]) for row in rows)
        manifest["domain_counts_per_split"][split] = dict(sorted(Counter(row["scenario_domain"] for row in rows).items()))
        manifest["category_counts_per_split"][split] = dict(sorted(Counter(q["primary_category"] for row in rows for q in row["questions"]).items()))
        manifest["answerability_counts_per_split"][split] = dict(sorted(Counter(q["answerability"] for row in rows for q in row["questions"]).items()))
        manifest["difficulty_counts_per_split"][split] = dict(sorted(Counter(q["difficulty"] for row in rows for q in row["questions"]).items()))
        manifest["files"][str(path).replace("\\", "/")] = {"sha256": digest, "bytes": path.stat().st_size}
        print("%s: %d episodes, %d questions, %d bytes, sha256=%s" % (split, count, manifest["question_counts_per_split"][split], path.stat().st_size, digest))
    manifest["total_episodes"] = total
    manifest["total_questions"] = sum(manifest["question_counts_per_split"].values())
    manifest_path = args.output_root / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("manifest: %s" % manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
