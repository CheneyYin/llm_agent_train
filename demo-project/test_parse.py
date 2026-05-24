"""验证 parse_log 的正确行为：应解析所有级别的日志行"""
import unittest
import tempfile
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse import parse_log


class TestParseLog(unittest.TestCase):

    def test_parses_all_log_levels(self):
        """parse_log 应该解析 ERROR、WARN、INFO 所有级别的行"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
            f.write('2026-05-24 10:23:15 ERROR DatabaseError: timeout\n')
            f.write('2026-05-24 10:23:17 WARN  Retry failed\n')
            f.write('2026-05-24 10:24:15 INFO  Pool restored\n')
            log_path = f.name

        try:
            result = parse_log(log_path)
            self.assertEqual(len(result), 3,
                             f"应解析3条日志，实际解析了{len(result)}条")
            self.assertEqual(result[0]['level'], 'ERROR')
            self.assertEqual(result[1]['level'], 'WARN')
            self.assertEqual(result[2]['level'], 'INFO')
        finally:
            os.unlink(log_path)

    def test_returns_empty_list_for_no_matches(self):
        """没有日志行时返回空列表"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
            f.write('just some random text\n')
            f.write('another line without log pattern\n')
            log_path = f.name

        try:
            result = parse_log(log_path)
            self.assertEqual(result, [])
        finally:
            os.unlink(log_path)

    def test_extracts_timestamp_level_and_message(self):
        """每条记录应正确提取时间戳、级别和消息"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
            f.write('2026-05-24 10:23:15 ERROR DatabaseError: timeout\n')
            log_path = f.name

        try:
            result = parse_log(log_path)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['time'], '2026-05-24 10:23:15')
            self.assertEqual(result[0]['level'], 'ERROR')
            self.assertEqual(result[0]['msg'], 'DatabaseError: timeout')
        finally:
            os.unlink(log_path)

    def test_handles_empty_file(self):
        """空文件返回空列表"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
            log_path = f.name

        try:
            result = parse_log(log_path)
            self.assertEqual(result, [])
        finally:
            os.unlink(log_path)

    def test_parses_sample_log_correctly(self):
        """使用 spec 中定义的 sample.log 验证：6行日志应全部解析"""
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'sample.log')
        result = parse_log(log_path)
        self.assertEqual(len(result), 6,
                         f"sample.log 有6行日志，应解析6条，实际解析了{len(result)}条")


if __name__ == '__main__':
    unittest.main()
