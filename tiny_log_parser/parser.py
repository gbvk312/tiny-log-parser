import re
import json
from collections import defaultdict
from typing import Dict, List, Optional, Any

# Matches formats like: [INFO] 2026-03-28 10:00:00 Some message
LOG_PATTERN = re.compile(r'^\[(?P<level>[A-Z]+)\]\s+(?P<timestamp>\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)\s+(?P<message>.*)$')

class LogParser:
    def __init__(self):
        self.stats = defaultdict(int)
        self.errors = []

    def parse_line(self, line: str) -> Optional[Dict[str, str]]:
        """Parses a single log line."""
        match = LOG_PATTERN.match(line.strip())
        if match:
            data = match.groupdict()
            level = data['level']
            self.stats[level] += 1
            if level in ('ERROR', 'FATAL', 'CRITICAL'):
                self.errors.append(data)
            return data
        return None

    def process_file(self, filepath: str) -> Dict[str, Any]:
        """Processes a log file and returns summary stats."""
        self.stats.clear()
        self.errors.clear()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                self.parse_line(line)
                
        return {
            "summary": dict(self.stats),
            "total_errors": len(self.errors)
        }

    def extract_errors(self, filepath: str, output_path: str):
        """Extracts errors and writes them to a JSON file."""
        self.process_file(filepath)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.errors, f, indent=2)
