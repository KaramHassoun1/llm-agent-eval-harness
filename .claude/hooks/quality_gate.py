"""Stop hook: Claude can't end a turn with failing lint or fast tests.

Runs only when Python files changed and only the cheap checks (no LLM calls).
Exit code 2 sends the failure back to Claude and keeps it working; Claude Code caps
consecutive blocks, and `stop_hook_active` stops us re-blocking on the same failure.
"""

import json
import os
import subprocess
import sys

TAIL_LINES = 40


def run(cmd: list[str]) -> subprocess.CompletedProcess[str] | None:
    """Run a command; None when the tool isn't installed yet (e.g. before Phase 1 adds dev deps)."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        return None
    if "Failed to spawn" in result.stderr:
        return None
    return result


def changed_python_files() -> bool:
    status = run(["git", "status", "--porcelain"])
    if status is None:
        return False
    return any(line.rstrip().endswith(".py") for line in status.stdout.splitlines())


def main() -> int:
    payload = json.load(sys.stdin)
    if payload.get("stop_hook_active") or not changed_python_files():
        return 0

    checks = [["uv", "run", "--quiet", "ruff", "check", "."]]
    if os.path.isdir("tests"):
        checks.append(["uv", "run", "--quiet", "pytest", "-m", "not llm", "-q", "-x"])

    for cmd in checks:
        result = run(cmd)
        if result is None:
            continue
        if result.returncode not in (0, 5):  # pytest exit 5 = no tests collected
            output = (result.stdout + result.stderr).strip().splitlines()[-TAIL_LINES:]
            print(f"Quality gate failed: {' '.join(cmd)}\n" + "\n".join(output), file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
