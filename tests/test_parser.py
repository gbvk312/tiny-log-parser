import pytest
import os
import tempfile
import json
from tiny_log_parser.parser import LogParser

class TestLogParser:
    @pytest.fixture
    def parser(self):
        return LogParser()

    def test_parse_info_line(self, parser):
        line = "[INFO] 2026-03-28 10:00:00 Application started"
        data = parser.parse_line(line)
        assert data is not None
        assert data['level'] == 'INFO'
        assert data['timestamp'] == '2026-03-28 10:00:00'
        assert data['message'] == 'Application started'
        assert parser.stats['INFO'] == 1
        assert len(parser.errors) == 0

    def test_parse_error_line(self, parser):
        line = "[ERROR] 2026-03-28 10:05:00 Connection failed"
        data = parser.parse_line(line)
        assert data is not None
        assert data['level'] == 'ERROR'
        assert parser.stats['ERROR'] == 1
        assert len(parser.errors) == 1
        assert parser.errors[0]['message'] == 'Connection failed'

    def test_process_file(self, parser):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            f.write("[INFO] 2026-03-28 10:00:00 Start\n")
            f.write("[WARN] 2026-03-28 10:01:00 Slow\n")
            f.write("[ERROR] 2026-03-28 10:05:00 Fail\n")
            f.write("Invalid line format\n")
            name = f.name
            
        try:
            summary = parser.process_file(name)
            assert summary['summary']['INFO'] == 1
            assert summary['summary']['WARN'] == 1
            assert summary['summary']['ERROR'] == 1
            assert summary['total_errors'] == 1
        finally:
            os.unlink(name)

    def test_extract_errors(self, parser):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            f.write("[INFO] 2026-03-28 10:00:00 Start\n")
            f.write("[ERROR] 2026-03-28 10:05:00 Fail\n")
            log_name = f.name
            
        out_name = log_name + ".json"
            
        try:
            parser.extract_errors(log_name, out_name)
            with open(out_name, 'r') as out_f:
                data = json.load(out_f)
                assert len(data) == 1
                assert data[0]['level'] == 'ERROR'
        finally:
            os.unlink(log_name)
            if os.path.exists(out_name):
                os.unlink(out_name)
