#!/usr/bin/env python3
"""Deprecated wrapper for the retired final audit script.

This file used to be a one-off verification script tied to an old homepage
system-architecture canvas. That canvas has been archived, and the current
validation entry is `validate_kb.py`.
"""

from __future__ import annotations


def main() -> int:
    print(
        "[DEPRECATED] final_audit.py was retired on 2026-06-29.\n"
        "\n"
        "Why it was retired:\n"
        "- it depended on an archived homepage system-architecture canvas\n"
        "- it duplicated checks that now live in validate_kb.py\n"
        "- its old implementation was a one-off historical script, not a current workflow entry\n"
        "\n"
        "Use one of these instead:\n"
        "  python validate_kb.py --quick\n"
        "  python validate_kb.py --full\n"
        "  python validate_kb.py --dir <path>\n"
        "\n"
        "Current truth sources:\n"
        "- the homepage system-architecture note\n"
        "- the homepage status-summary note\n"
        "- scripts/validate_kb.py\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
