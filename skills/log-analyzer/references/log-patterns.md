# 常见日志模式参考

## 数据库相关

| 模式 | 正则 | 可能原因 |
|------|------|---------|
| 连接超时 | `connection timeout after \d+s` | 连接池太小 / 网络延迟 / 数据库负载高 |
| 连接过多 | `too many connections.*current: (\d+), max: (\d+)` | 连接泄漏 / 未释放连接 / 并发过高 |
| 空值约束 | `null value in column "(\w+)"` | 插入前未校验 / 数据源问题 |
| 事务重试失败 | `Retry failed for transaction (\S+)` | 连接中断 / 死锁 / 超时 |

## 日志级别

| 级别 | 含义 | 关注点 |
|------|------|--------|
| ERROR | 需要立即关注的错误 | 数量、类型分布、时间集中度 |
| WARN | 潜在问题 | 是否和 ERROR 有时序关联 |
| INFO | 正常信息 | 不要忽略——INFO 可能包含恢复信息（如"pool restored"） |

## 分析技巧

1. **时间聚类**：同一秒出现大量 ERROR → 可能是瞬时故障（如网络闪断）
2. **级别关联**：WARN 后紧跟 ERROR → WARN 是前兆，ERROR 是结果
3. **恢复信息**：INFO 中的 "restored" / "recovered" → 确认故障已自愈
4. **代码对比**：日志有但代码没处理的级别 → 解析逻辑的 bug
