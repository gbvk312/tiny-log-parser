# Tiny Log Parser

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Tiny Log Parser is a fast, dependency-free Python developer utility for parsing large application server logs. It rapidly ingests log streams, filters by log levels, and extracts critical JSON summaries of error events to assist in live production debugging.

## 🌟 Features

- **Blazing Fast Parsing**: Processes streams line-by-line avoiding full memory loads.
- **Level Filtering**: Isolate metrics or extract explicitly `ERROR` or `WARN` logs.
- **Summary Generation**: Output a clean JSON aggregate grouped by log severity.
- **Date Extraction**: Automatically identifies common ISO 8601 or standard timestamps.

## 🚀 Installation

Ensure you have Python 3.8+ installed. You can install or run the utility locally:

```bash
# Clone the repository
git clone https://github.com/gbvk312/tiny-log-parser.git
cd tiny-log-parser

# Install the package locally
pip install .
```

## 🛠 Usage

Basic summary of a log file:

```bash
tiny-log parse server.log
```

Extract only errors to a JSON file:

```bash
tiny-log extract-errors server.log --output errors.json
```

Example Log Format Expected:
```
[INFO] 2026-03-28 10:00:00 Server started
[ERROR] 2026-03-28 10:05:00 Connection timeout
```

## 🗺 Roadmap

- [ ] Support custom RegEx patterns for unknown log formats
- [ ] Implement compressed log (`.gz`) support natively
- [ ] Add real-time stream `tail` tracking

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
