"""`refund-eval`: run the seven-metric evaluation of the refund agent."""

import argparse
import json
import logging
from pathlib import Path

from dotenv import load_dotenv

from refund_agent.config import get_settings


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="refund-eval",
        description=(
            "Run the refund agent over the evaluation dataset and score it with seven DeepEval "
            "metrics. Calls the OpenAI API: every case costs agent and judge tokens."
        ),
    )
    parser.add_argument("--limit", type=int, help="only evaluate the first N cases")
    parser.add_argument("--runs", type=int, default=1, help="repeat the evaluation N times")
    parser.add_argument("--model", help="agent model (default: from config)")
    parser.add_argument("--judge-model", help="judge model for the metrics (default: from config)")
    parser.add_argument("--out", type=Path, help="write a JSON record of the run(s) to this path")
    args = parser.parse_args(argv)
    if args.runs < 1:
        parser.error("--runs must be at least 1")
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be at least 1")
    return args


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    load_dotenv()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

    # Imported here so `--help` works without loading LangChain and DeepEval.
    from refund_eval.report import build_run_record
    from refund_eval.runner import run_once

    settings = get_settings()
    overrides = {"agent_model": args.model, "judge_model": args.judge_model}
    settings = settings.model_copy(update={k: v for k, v in overrides.items() if v})

    runs = [run_once(settings, args.limit) for _ in range(args.runs)]
    cases = len(runs[0][1].test_results)
    print(f"\nCompleted all 7 metrics for {cases} test cases x {args.runs} run(s).")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        record = build_run_record(settings, runs, args.limit)
        args.out.write_text(json.dumps(record, indent=2), encoding="utf-8")
        print(f"Saved run record to {args.out}")


if __name__ == "__main__":
    main()
