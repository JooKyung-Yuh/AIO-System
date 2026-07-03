#!/usr/bin/env python3
"""validate.py — 스텁: data/records/*.json 파싱 + 필수 키 검사 (TODO)."""
import glob
import json
import sys


def main() -> int:
    bad = []
    for path in sorted(glob.glob("data/records/*.json")):
        try:
            json.load(open(path, encoding="utf-8"))
        except Exception as e:
            bad.append((path, e))
    for path, e in bad:
        print(f"FAIL {path}: {e}")
    # TODO: 필수 키 검사 (스키마 확정 후)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
