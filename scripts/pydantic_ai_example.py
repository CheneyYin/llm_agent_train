"""
Pydantic AI 结构化输出示例
演示：用代码定义数据结构，让库自动校验和重试 LLM 的输出

安装依赖：pip install pydantic-ai pydantic
运行需要设置 OPENAI_API_KEY 或 ANTHROPIC_API_KEY 环境变量
"""

from pydantic import BaseModel
from pydantic_ai import Agent


# ── 第1步：定义你期望的数据结构（这就是"表单"）──

class LogEntry(BaseModel):
    """单条日志记录"""
    time: str
    level: str
    message: str


class LogAnalysisResult(BaseModel):
    """日志分析结果"""
    entries: list[LogEntry]
    total_errors: int
    summary: str


# ── 第2步：创建 Agent，绑定返回类型 ──

agent = Agent(
    "openai:gpt-4o",              # 使用的模型
    result_type=LogAnalysisResult  # 告诉 Agent："你必须按这个结构返回"
)


# ── 第3步：一句话调用 ──

result = agent.run_sync("""
读取 sample.log 的所有行，提取时间、级别、消息。
统计 ERROR 级别的数量作为 total_errors。
summary 用中文写一句总结。
""")


# ── 第4步：类型安全地使用结果 ──

# result 是 LogAnalysisResult 类型，IDE 有自动补全
print(f"共 {result.total_errors} 条错误")
print(f"总结：{result.summary}")
print()

for entry in result.entries:
    print(f"[{entry.time}] {entry.level}: {entry.message}")


# ── 背后发生了什么 ──
#
#  定义 Pydantic Model        库转成 JSON Schema       LLM 生成响应        Pydantic 校验
#  ──────────────────    →    ─────────────────    →    ───────────    →    ────────────
#  class LogEntry(BaseModel):  {                        LLM 按 Schema   类型不匹配？→ 自动重试
#      time: str                "type": "object",       返回结构化数据   字段缺失？  → 自动重试
#      level: str               "properties": {                        校验通过    → 返回 Python 对象
#      message: str               "time": {"type": "string"},
#  }                              "level": {"type": "string"},
#                                 "message": {"type": "string"}
#                              }
#                              }
