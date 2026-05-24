# 演示脚本 01：开场预告演示

> **运行环境**：Windows（CMD 或 PowerShell），命令已适配 Windows。Linux/macOS 用户将 `python` 换为 `python3`，`type` 换为 `cat`，`dir /s` 换为 `ls -R`。

## 场景准备

```bash
cd demo-project
pi
```

---

### 步骤：30 秒能力预览

**前情过渡**：—

**讲师话术**：
"我先花 30 秒给大家看一个东西——这是我们今天要讲的工具 pi agent。我把同一个任务给 AI 看，大家可以观察它做了什么。"

**命令**（在 pi 交互界面中输入）：
```
这个项目里有一个日志解析脚本 parse.py 和一个日志文件 sample.log。帮我快速看一下有什么问题。
```

**预期输出**：
- pi agent 自动读取 sample.log
- pi agent 自动读取 parse.py 源码
- pi agent 指出：正则只匹配了 ERROR，漏掉了 WARN 和 INFO 行
- 给出修改建议

**关键展示点**：
- 强调：Agent 自己决定先读哪个文件、后读哪个文件
- 强调：它不需要你告诉它每一步做什么

**备用方案**：
- 若 pi agent 不可用，用预先录制的终端截图或 asciicast 回放

**衔出过渡**：
"刚才看了 pi agent 能做到多厉害的事，但关键问题来了——不是随便打几个字就能得到这种结果。提示词写得好不好，结果天差地别。我们先从最基础的技巧开始，看看怎么让 AI 听懂你的话。"
