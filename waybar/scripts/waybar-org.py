#!/usr/bin/env python3
import orgparse
import datetime
import sys
import json
import os

JSON_MODE = True


def get_counts(org_file):
    # Expand ~ in file path
    org_file = os.path.expanduser(org_file)

    today = datetime.date.today()
    nodes = orgparse.load(org_file)[1:]

    today_count = stale_count = closed_count = 0

    for node in nodes:
        if (
            node.closed
            and hasattr(node.closed, "start")
            and node.closed.start.date() == today
        ):
            closed_count += 1

        if node.todo and node.todo != "DONE":
            if (
                node.scheduled
                and hasattr(node.scheduled, "start")
                and node.scheduled.start.date() == today
            ):
                today_count += 1
            elif node.deadline and hasattr(node.deadline, "start"):
                deadline = node.deadline.start.date()
                if deadline == today:
                    today_count += 1
                elif deadline < today:
                    stale_count += 1

    return today_count, stale_count, closed_count


def format_output(today, stale, closed, as_json=True):
    parts = []
    if today > 0:
        parts.append(
            f'<span color="#D08770">{today}</span>'
        )  # Nord Orange - today's tasks
    if stale > 0:
        parts.append(
            f'<span color="#BF616A">{stale}</span>'
        )  # Nord Red - overdue tasks
    if closed > 0:
        parts.append(
            f'<span color="#A3BE8C">{closed}</span>'
        )  # Nord Green - completed tasks

    text = " ".join(parts) or '<span color="#4C566A">0</span>'

    if as_json:
        return json.dumps(
            {
                "text": text,
                "tooltip": f"Today: {today} | Overdue: {stale} | Done: {closed}",
            }
        )
    return text


if __name__ == "__main__":
    org_file = sys.argv[1] if len(sys.argv) > 1 else "~/Org/tasks.org"

    try:
        counts = get_counts(org_file)
        print(format_output(*counts, as_json=JSON_MODE))
    except Exception:
        print(json.dumps({"text": "error", "class": "error"}) if JSON_MODE else "error")
