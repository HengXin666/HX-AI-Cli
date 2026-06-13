# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "questionary>=2.0.1",
#   "rich>=13.7.0",
# ]
# ///
from __future__ import annotations

import argparse
import os
from pathlib import Path

from hx_ai_cli.core import configure_vscode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install HX-AI-Cli VS Code user terminal profile")
    parser.add_argument("--workspace", default=os.getcwd(), help="workspace passed to HX-AI-Cli when the terminal opens")
    parser.add_argument("--variant", choices=["code", "insiders", "codium"], default="code")
    parser.add_argument("--set-default", action="store_true", help="also make the profile the default terminal")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    configure_vscode(
        Path(args.workspace).expanduser(),
        set_default=True if args.set_default else None,
        scope="user",
        variant=args.variant,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
