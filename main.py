import argparse
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from scheduler import JobAutomation


def main():
    parser = argparse.ArgumentParser(description="AI Job Leads Automation")
    parser.add_argument("--once", action="store_true", help="Run once instead of scheduling")
    parser.add_argument("--schedule", action="store_true", help="Run on schedule (every 6 hours)")
    
    args = parser.parse_args()
    
    automation = JobAutomation()
    
    if args.once:
        print("Running job fetch once...")
        asyncio.run(automation.run_once())
    elif args.schedule:
        print("Starting scheduler (every 6 hours)...")
        automation.start()
    else:
        print("Running job fetch once (default)...")
        asyncio.run(automation.run_once())


if __name__ == "__main__":
    main()