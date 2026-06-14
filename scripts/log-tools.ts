/**
 * log-tools — pi agent 自定义工具扩展示例
 *
 * 为 pi agent 注册一个 count_log_levels 工具，用于统计日志文件的级别分布。
 *
 * 安装方式：
 *   将此文件复制到 ~/.pi/agent/extensions/ 或项目 .pi/extensions/ 目录
 *   pi 启动时自动发现并加载
 *
 * 教学用途：
 *   此文件保存于 scripts/log-tools.ts，讲师在编辑器中直接打开展示
 *   在 pi 中输入 "用 count_log_levels 分析 sample.log" 演示效果
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "@earendil-works/pi-ai";

export default function (pi: ExtensionAPI) {

  // ── ① Schema：定义工具的参数格式 ──
  // LLM 据此判断"何时调用这个工具、传什么参数"
  pi.registerTool({
    name: "count_log_levels",
    label: "统计日志级别",
    description:
      "读取指定日志文件，统计 ERROR、WARN、INFO 各级别的数量。" +
      "当需要了解日志文件的错误分布时使用。",
    parameters: Type.Object({
      filepath: Type.String({ description: "日志文件的路径，如 sample.log" }),
    }),

    // ── ② Execute：实际的业务逻辑 ──
    execute: async (toolCallId, params, signal, onUpdate) => {
      // 流式推送进度——用户能看到工具正在运行
      onUpdate?.({
        content: [{ type: "text", text: "正在读取日志文件..." }],
        details: {},
      });

      if (!params || typeof params.filepath !== "string") {
        return {
          content: [{ type: "text", text: "错误：缺少 filepath 参数" }],
          details: {},
        };
      }

      const fs = await import("fs");
      const content = fs.readFileSync(params.filepath, "utf-8");
      const lines = content.split("\n").filter((l) => l.trim());

      // 用正则提取日志级别
      const counts: Record<string, number> = {};
      for (const line of lines) {
        const match = line.match(
          /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (\w+)/
        );
        if (match) {
          const level = match[1];
          counts[level] = (counts[level] || 0) + 1;
        }
      }

      // 返回结构化结果
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              tool: "count_log_levels",
              invoked_at: new Date().toISOString(),
              totalLines: lines.length,
              levelCounts: counts,
            }, null, 2),
          },
        ],
        details: { totalLines: lines.length, counts },
      };
    },
  });

  // ── ③ Hook：权限控制 ──
  // pi.on("tool_call") 在工具执行前触发，可返回 { block: true } 拦截
  pi.on("tool_call", async (event) => {
    if (event.toolName !== "count_log_levels") return;

    // pi 的 tool_call 事件中，参数在 input 字段
    const params = (event as any).input ?? {};
    const filepath = (params?.filepath ?? params?.filePath ?? "") as string;

    // 只允许读取 .log 文件，防止越权访问
    if (!filepath.endsWith(".log")) {
      return {
        block: true,
        reason: "count_log_levels 只允许分析 .log 文件",
      };
    }
    // 不阻止 → 工具正常执行
  });
}
