# Execution Prompt Builder

[中文](#中文) | [English](#english)

把一句还没想完整的需求，整理成另一个 Agent 可以直接执行、检查和验收的任务提示词。

## 中文

### 它是什么

Execution Prompt Builder 是一个面向 Codex 等 Agent 客户端的需求澄清 Skill。你只需要先说出大概想法，它会根据任务自动选择合适的专业角色，用每轮一个关键问题逐步补齐目标、范围、权限和验收标准，最后生成一份可以直接交给另一个执行 Agent 的完整提示词。

它的重点不是把句子写得更长，而是把容易导致执行偏差的信息提前说清楚：要做什么、不做什么、允许做到哪一步、遇到异常怎么办，以及最终拿什么证据证明任务真的完成了。

> 这个 Skill 只负责澄清需求和构建提示词，不会擅自执行提示词中的修改、部署、发送或其他实际操作。

### 它解决什么问题

很多 Agent 任务失败，并不是模型不会做，而是原始要求里缺少关键条件。例如：

- 只说“帮我优化一下”，但没有说明优化目标和判断标准；
- 把调查、修改、部署、发送混成一个授权，导致执行范围失控；
- 给了大量背景，却没有明确最终交付物；
- 要求“专业、稳定、体验好”，但没有可测试的验收标准；
- 把任务交给另一个 Agent 后，对方仍要重新追问全部背景；
- 执行 Agent 只汇报“已经完成”，却没有测试结果或运行证据。

Execution Prompt Builder 会把这些缺口转成少量高价值问题，并把答案整理成一份自包含的任务合同。

### 核心能力

- **自动选择专业角色**：根据任务选择 1 个主角色，必要时增加最多 2 个职责明确的辅助视角，并说明选择理由。
- **支持随时调整角色**：你可以直接要求更换主角色、增加某个检查视角，或删除不需要的角色。
- **逐轮反向提问**：每轮最多问 1 个真正影响方向、范围、权限或验收结果的问题，不发一整页问卷。
- **优先读取现有上下文**：能从工作区规则、项目说明和相关文件中只读查到的信息，会先自行检查，减少重复提问。
- **明确权限边界**：区分只读调查、本地修改、外部写入、部署、发送和不可逆操作，避免把“看看”误解成“直接改”。
- **生成可验收标准**：把“做得专业”“体验更好”等模糊表达，转换成可观察、可测试或可举证的结果。
- **提供完整与精简两版提示词**：完整版本适合复杂任务交接，精简版本适合直接粘贴到新会话。
- **要求验证证据**：提示执行 Agent 汇报测试、运行状态、差异或其他证据，不把未经验证的结果当成完成。
- **保护敏感信息**：不会要求回显密码、Token、Cookie 或验证码；提示词中只使用路径、变量名或掩码引用。

### 工作流程

1. **理解原始想法**：识别目标、已知背景、当前状态和明显缺口。
2. **选择任务角色**：展示主角色、辅助视角及选择原因，你可以立即修改。
3. **检查现有上下文**：按需读取项目规则、说明文档和可安全获取的只读信息。
4. **逐轮补齐关键条件**：优先确认成功标准、权限、范围和非目标；信息已经足够时不会为了提问而继续提问。
5. **锁定角色职责**：明确每个角色负责什么、采用什么判断标准，以及无权做什么。
6. **生成交接包**：输出角色摘要、完整执行提示词、精简执行提示词，以及仍需执行 Agent 查证的事项。
7. **交付前自检**：检查权限混淆、规则冲突、不可验证要求、敏感信息和无关工作。

### 最终会得到什么

默认交付包包含四部分：

1. **角色选择摘要**：主角色、辅助视角及各自职责。
2. **完整执行提示词**：覆盖目标、背景、输入、范围、非目标、权限、执行流程、异常处理、验收标准、验证证据和交付格式。
3. **精简执行提示词**：保留关键目标、边界、验收和证据要求，适合快速交给另一个 Agent。
4. **待查证事项**：列出不需要现在追问用户、但执行 Agent 开工前必须确认的信息。

### 前后对比示例

原始想法：

```text
帮我把网站登录功能优化一下，然后交给另一个 Agent 做。
```

Skill 不会立刻编造一份笼统的长提示词。它会先自动推荐角色，例如“认证流程工程师”为主角色、“安全审查”为辅助视角，然后只询问当前最影响结果的问题：

```text
这次最重要的是减少登录失败、提升登录速度，还是增加新的登录方式？
我建议先选一个首要目标，因为三种方向对应的改动范围和验收方法不同。
```

经过必要的澄清后，生成的执行提示词会明确：

- 要解决的具体登录问题和用户范围；
- 哪些仓库、页面或接口在范围内；
- 当前只授权调查、本地修改，还是也允许部署；
- 必须保留的安全机制和明确的非目标；
- 需要运行哪些测试、采集哪些前后对比数据；
- 遇到无法复现、依赖缺失或生产权限不足时如何停止并汇报；
- 最终应提交哪些文件、测试结果和验证证据。

这样，接手的执行 Agent 不需要猜测你的真实意图，也不能用一句“已经优化完成”代替验收。

### 适用场景

- 只有一个大概想法，还不知道怎样写成完整提示词；
- 准备把开发、排错、研究、内容、设计或运营任务交给另一个 Agent；
- 任务跨多个专业领域，不确定应该采用什么角色和检查视角；
- 需要明确只读、修改、部署、发送等权限边界；
- 希望任务带有可复现的验收标准和证据要求；
- 已经有项目规则和背景资料，希望交接时自动纳入上下文。

不适合的场景：你已经明确要求当前 Agent 立即执行任务。此时应直接进入执行流程，而不是调用这个 Skill。

### 安装到 Codex

要求：已安装 Git 和 Python 3。角色搜索与更新脚本只使用 Python 3 标准库，不需要额外安装 Python 包。

克隆仓库后，把仓库内层的完整 `execution-prompt-builder` 文件夹复制到 Codex Skill 目录。不要只复制 `SKILL.md`，因为运行时还需要 `references`、`scripts` 和 `agents`。

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

安装后重新打开 Codex 任务，让客户端重新发现 Skill。

### 使用方法

直接点名调用：

```text
使用 $execution-prompt-builder 帮我完善这个需求，并生成交给执行 Agent 的提示词：
我想做一个自动整理客户反馈的工具。
```

也可以自然描述：

```text
我准备把这个排错任务交给另一个 Agent。先帮我反向提问，把范围、权限和验收标准补完整，再生成提示词。
```

调整角色：

```text
把主角色改成产品经理，再增加一个隐私合规视角。
```

当你不想继续提问时，可以要求它基于当前信息生成，并明确保留的假设：

```text
先按目前的信息生成，不能确定的地方采用安全假设并单独列出。
```

Python 3 启动命令可以使用 `python3`、Windows 的 `py -3`，或明确指向 Python 3 的 `python`。

### 权限与安全边界

- Skill 默认只做必要的只读上下文检查和提示词构建。
- 不会因为提示词里写了“部署”“发送”或“删除”，就替你执行这些操作。
- 用户授权、项目规则和系统安全限制始终高于角色库内容。
- 外部角色资料只作为候选知识源，会先净化，再转换成有限职责的角色契约。
- 日常使用不会联网更新角色库；只有用户明确要求刷新时才运行同步脚本。
- 密码、Token、Cookie、验证码等秘密不应写入生成的提示词或公开仓库。

### 兼容性

- **操作系统**：Windows、macOS、Linux。
- **Agent 客户端**：按 Codex Skill 目录结构打包；生成的提示词也可交给 Claude Code、OpenClaw 或其他执行 Agent 使用。
- **Python**：Python 3，仅使用标准库。
- **联网要求**：日常选角和提示词构建使用仓库内置的固定角色索引，无需联网；克隆仓库或明确刷新角色库时需要联网。

### 角色索引与安全模型

仓库内置角色索引来自 [`jnMetaCode/agency-agents-zh`](https://github.com/jnMetaCode/agency-agents-zh) 的固定提交 `77f3f4c1477702e66ab56b1bf54e9b922c9d46db`。固定版本让角色选择结果可复现，避免日常运行时静默引入上游变化。

外部角色描述会被视为不可信参考数据。Skill 只保留与任务有关的职责、方法、质量标准和交付物，并移除虚构履历、虚构记忆、固定无关工具、隐藏推理要求以及超出用户授权的操作指令。

## English

Execution Prompt Builder is a reusable Agent Skill that turns rough ideas into self-contained, execution-ready prompts for a separate agent. It selects task-relevant expert roles, asks one high-value clarification question at a time, captures scope and authority boundaries, and defines observable acceptance criteria and verification evidence.

It is designed to prevent a common failure mode in agent handoffs: the request sounds clear to its author, but the receiving agent has to guess the actual goal, permission level, non-goals, or definition of done.

### How it works

1. Understands the initial request and available context.
2. Selects one primary role and up to two useful supporting perspectives.
3. Shows the role selection so the user can change it.
4. Reads safe, relevant project context before asking for facts that are already available.
5. Asks at most one high-impact question per turn.
6. Produces a full prompt, a compact prompt, and a list of facts the execution agent must still verify.
7. Checks the handoff for permission ambiguity, unverifiable claims, conflicting instructions, and exposed secrets.

The Skill builds prompts only. It does not execute the requested code changes, deployments, messages, deletions, or other external actions.

### Install for Codex

Requirements: Git and Python 3. The bundled role search and refresh tools use only the Python 3 standard library.

Clone this repository and copy the inner `execution-prompt-builder` directory to `~/.codex/skills/execution-prompt-builder`. Copy the complete directory, not only `SKILL.md`, then restart your Codex task so the Skill can be discovered.

Invoke it directly:

```text
Use $execution-prompt-builder to clarify this idea and create a handoff prompt for another agent: ...
```

The generated prompts can also be handed to Claude Code, OpenClaw, or another execution agent. Use `python3`, Windows `py -3`, or `python` when it explicitly points to Python 3.

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

## Community / 社区与网站

- QQ 2群：`227075481`
- Telegram 交流群：[点击加入](https://t.me/+SmQkUl6XiBNiMTVk)
- 官网：[https://www.aiaiai001.com/](https://www.aiaiai001.com/)
- 中转站官网：[https://api.aiaiai001.com/](https://api.aiaiai001.com/)

## License

MIT. See [LICENSE](LICENSE), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), and the bundled upstream license in [THIRD_PARTY_LICENSES](THIRD_PARTY_LICENSES/agency-agents-zh-LICENSE).
