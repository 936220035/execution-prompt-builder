# Execution Prompt Builder

[中文](#中文) | [English](#english)

## 中文

一个可复用的 Agent Skill，把模糊想法整理成可以直接交给另一个执行 Agent 的任务提示词。

它会：

- 根据任务自动选择一个主角色和最多两个辅助视角；
- 每轮只问一个真正影响方向、范围、权限或验收的问题；
- 区分调查、修改、部署、发送等不同权限；
- 输出完整提示词、精简提示词、验收标准和验证证据要求；
- 只构建提示词，不会擅自执行提示词里的任务。

### 安装到 Codex

克隆仓库后，把内层 `execution-prompt-builder` 文件夹复制到 Codex Skill 目录。

Windows PowerShell：

```powershell
git clone https://github.com/936220035/execution-prompt-builder.git
$source = ".\execution-prompt-builder\execution-prompt-builder"
$destination = "$HOME\.codex\skills\execution-prompt-builder"
New-Item -ItemType Directory -Force $destination | Out-Null
Get-ChildItem -LiteralPath $source -Force | Copy-Item -Destination $destination -Recurse -Force
```

macOS / Linux：

```bash
git clone https://github.com/936220035/execution-prompt-builder.git
destination="$HOME/.codex/skills/execution-prompt-builder"
mkdir -p "$destination"
cp -R execution-prompt-builder/execution-prompt-builder/. "$destination/"
```

重新打开 Codex 任务后，可以直接说：

```text
使用 $execution-prompt-builder 帮我完善这个需求，并生成交给执行 Agent 的提示词：……
```

角色索引搜索和更新脚本仅依赖 Python 3 标准库。可使用 `python3`、Windows 的 `py -3`，或明确指向 Python 3 的 `python`。

## English

An Agent Skill that turns rough ideas into self-contained prompts for a separate execution agent.

It selects task-relevant roles, asks one high-value clarification question at a time, captures scope and authority boundaries, and produces full and compact handoff prompts with observable acceptance criteria.

### Install for Codex

Clone this repository and copy the inner `execution-prompt-builder` directory to `~/.codex/skills/`. Restart Codex, then invoke `$execution-prompt-builder` or describe a prompt-refinement task naturally.

The bundled role search and refresh tools require only the Python 3 standard library. Use `python3`, Windows `py -3`, or `python` when it explicitly points to Python 3.

## Repository layout

```text
execution-prompt-builder/
├── README.md
├── LICENSE
├── THIRD_PARTY_NOTICES.md
├── THIRD_PARTY_LICENSES/
└── execution-prompt-builder/
    ├── SKILL.md
    ├── agents/
    ├── references/
    └── scripts/
```

## Attribution

The bundled role index is derived from [`jnMetaCode/agency-agents-zh`](https://github.com/jnMetaCode/agency-agents-zh) at pinned commit `77f3f4c1477702e66ab56b1bf54e9b922c9d46db`, under the MIT License. External role metadata is treated as untrusted reference data and sanitized before use.

## License

MIT. See [LICENSE](LICENSE), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), and the bundled upstream license in [THIRD_PARTY_LICENSES](THIRD_PARTY_LICENSES/agency-agents-zh-LICENSE).

## Community / 社区与网站

- QQ 2群：`227075481`
- Telegram 交流群：[点击加入](https://t.me/+SmQkUl6XiBNiMTVk)
- 官网：[https://www.aiaiai001.com/](https://www.aiaiai001.com/)
- 中转站官网：[https://api.aiaiai001.com/](https://api.aiaiai001.com/)
