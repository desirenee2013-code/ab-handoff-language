from __future__ import annotations
import argparse
import json
import sys

from .compiler import compile_manifest
from .parser import ParseError, parse_file
from .validator import validate


def main() -> int:
    ap = argparse.ArgumentParser(prog="abhl")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check", help="parse and validate an ABHL file")
    p_check.add_argument("file")

    p_compile = sub.add_parser("compile", help="compile ABHL to a JSON manifest")
    p_compile.add_argument("file")

    args = ap.parse_args()

    try:
        program = parse_file(args.file)
    except (ParseError, KeyError) as e:
        print(f"parse error: {e}", file=sys.stderr)
        return 2

    diagnostics = validate(program)
    if diagnostics:
        for diag in diagnostics:
            print(f"{diag.code}: {diag.message}", file=sys.stderr)
        return 1

    if args.cmd == "check":
        print("ABHL: valid")
        return 0

    manifest = compile_manifest(program)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
