#!/usr/bin/env python3
"""Stub: data/records JSON 파싱 검사."""
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
    # TODO: schema/factor.v0.1.schema.json 기반 필수 키 검사
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
