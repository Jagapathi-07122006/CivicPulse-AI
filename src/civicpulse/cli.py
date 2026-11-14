import argparse
import asyncio
from pathlib import Path
from .agent import CivicPulseAgent

def main():
    parser = argparse.ArgumentParser(prog="civicpulse")
    sub = parser.add_subparsers(dest="command", required=True)
    analyze = sub.add_parser("analyze", help="Run a live public-data analysis")
    analyze.add_argument("place")
    analyze.add_argument("--radius", type=int, default=5000)
    analyze.add_argument("--forecast-days", type=int, default=2)
    analyze.add_argument("--output")
    export = sub.add_parser("export-system-prompt", help="Create a local system-prompt artifact")
    export.add_argument("--output", default="exports/civicpulse-system-prompt.md")
    args = parser.parse_args()

    if args.command == "analyze":
        result, report = asyncio.run(CivicPulseAgent().analyze_report(
            args.place, radius_m=args.radius, forecast_days=args.forecast_days))
        if args.output:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            Path(args.output).write_text(report, encoding="utf-8")
            print(f"Report written to {args.output}")
        else:
            print(report)
    elif args.command == "export-system-prompt":
        root = Path(__file__).resolve().parents[2]
        sections = []
        for filename in ("SOUL.md", "RULES.md", "EXPLAINABILITY.md"):
            path = root / filename
            if not path.exists():
                raise SystemExit(f"Required source file missing: {path}")
            sections.append(path.read_text(encoding="utf-8"))
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n\n---\n\n".join(sections), encoding="utf-8")
        print(f"System-prompt artifact written to {target}")

if __name__ == "__main__":
    main()
