import argparse
import sys
import json
from tiny_log_parser.parser import LogParser

def main():
    parser = argparse.ArgumentParser(description="Tiny Log Parser")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Parse command
    parse_parser = subparsers.add_parser('parse', help='Parse and summarize a log file')
    parse_parser.add_argument('file', type=str, help='Path to log file')

    # Extract command
    extract_parser = subparsers.add_parser('extract-errors', help='Extract errors to JSON')
    extract_parser.add_argument('file', type=str, help='Path to log file')
    extract_parser.add_argument('--output', type=str, required=True, help='Output JSON file path')

    args = parser.parse_args()
    log_parser = LogParser()

    try:
        if args.command == 'parse':
            summary = log_parser.process_file(args.file)
            print(json.dumps(summary, indent=2))
        elif args.command == 'extract-errors':
            log_parser.extract_errors(args.file, args.output)
            print(f"Extracted {log_parser.stats.get('ERROR', 0)} errors to {args.output}")
            
    except FileNotFoundError:
        print(f"Error: Log file '{args.file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
