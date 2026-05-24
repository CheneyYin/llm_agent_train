"""日志快速统计工具 — 配合 log-analyzer skill 使用"""
import sys
from collections import Counter


def analyze_log(filepath):
    with open(filepath) as f:
        lines = f.readlines()

    total = len(lines)
    levels = Counter()
    categories = Counter()

    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 3:
            level = parts[2]
            levels[level] += 1

    print(f"总行数: {total}")
    print(f"级别分布:")
    for level, count in levels.most_common():
        print(f"  {level}: {count}")
    print()

    if "ERROR" in levels:
        print(f"ERROR 行明细:")
        for i, line in enumerate(lines, 1):
            if "ERROR" in line:
                print(f"  [{i}] {line.strip()}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python parse_log.py <日志文件>")
        sys.exit(1)
    analyze_log(sys.argv[1])
