"""PostToolUse hook: format and lint a Python file right after Claude edits it.

Reads the hook payload from stdin. Remaining lint errors go to stderr with exit code 2,
which Claude Code shows to Claude so it fixes them in the same turn.
"""

import json
import subprocess
import sys


def ruff(*args: str) -> subprocess.CompletedProcess[str]:
    # Prefer the project's pinned ruff; fall back to uvx before Phase 1 adds it as a dev dependency.
    for prefix in (["uv", "run", "--quiet", "ruff"], ["uvx", "ruff"]):
        try:
            result = subprocess.run([*prefix, *args], capture_output=True, text=True)
        except FileNotFoundError:
            continue
        if "Failed to spawn" not in result.stderr and "not found" not in result.stderr:
            return result
    return subprocess.CompletedProcess(args, 0, "", "")


def main() -> int:
    payload = json.load(sys.stdin)
    path = payload.get("tool_input", {}).get("file_path", "")
    if not path.endswith(".py"):
        return 0

    ruff("format", path)
    check = ruff("check", "--fix", path)
    if check.returncode != 0:
        print(f"ruff found issues in {path}:\n{check.stdout.strip()}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
