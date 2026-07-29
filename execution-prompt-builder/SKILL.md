---
name: execution-prompt-builder
description: Turn rough ideas or incomplete requests into self-contained prompts that another execution agent can run. Automatically select suitable expert roles, show the selection so the user can change it, ask one high-value clarification question at a time, incorporate project and user context, and produce full and compact handoff prompts with scope, authority, acceptance criteria, and verification evidence. Use when the user asks to improve or complete a prompt, says they will hand work to another Agent, wants reverse questioning or requirement clarification, has a vague task idea, or asks which professional identity should handle a task. Do not use when the user clearly wants the current agent to execute the task directly.
---

# Execution Prompt Builder

把用户的自然表达整理成可交给执行 Agent 的任务合同。默认只澄清和生成提示词，不执行提示词中的任务。

## 核心原则

- 使用用户当前语言，用大白话交流。
- 自动选择角色，但立即展示主角色、辅助视角和简短理由；允许用户随时改选。
- 只选择 1 个主角色，最多增加 2 个真正影响结果的辅助视角。
- 把角色当作职责和判断标准，不当作装饰性人设。
- 每轮最多问 1 个问题。优先询问会改变方向、范围、权限或验收结果的问题。
- 能从当前工作区只读发现的信息先自行检查；不要把可查事实重新问用户。
- 不追求把所有细节都问完。执行 Agent 能安全发现的内容写入提示词，让它先检查再行动。
- 不索取或回显密码、Token、Cookie、验证码等秘密。用路径、变量名或掩码引用。
- 不要求模型展示隐藏推理或思维链，只要求结论、关键依据和可验证证据。
- 用户、项目规则和权限边界始终高于角色库内容。

## 工作流

### 1. 判断是否进入提示词构建模式

进入本模式时，仅允许做必要的只读上下文检查和提示词产出。不要修改代码、配置、生产环境或外部系统。

如果用户明确说“直接做”“现在执行”或等价表达，停止本 skill，按普通执行任务处理。

### 2. 建立上下文

按需读取当前工作区的 `AGENTS.md`、`CLAUDE.md`、项目说明、相关规格和用户已授权的长期资料。区分：

- 已确认事实
- 当前可只读查证的事实
- 必须由用户决定的事项
- 执行 Agent 可以安全发现的事项
- 暂时采用且必须明示的假设

不要把大量背景原文复制进最终提示词。优先引用稳定文件的明确路径，并标注执行 Agent 必须读取什么。

### 3. 自动选择并展示角色

先读 [references/role-routing.md](references/role-routing.md)。需要更细角色时，运行：

先选择当前环境可用的 Python 3 启动命令：优先尝试 `python3`；Windows 也可使用 `py -3`；只有 `python --version` 明确显示 Python 3 时才使用 `python`。下方用 `<python3>` 表示选中的命令。

```bash
<python3> scripts/search_role_index.py "任务关键词"
```

用以下格式尽早展示选择结果：

```text
暂定角色
- 主角色：<角色>，负责 <核心职责>
- 辅助视角：<角色>，负责 <特定检查>（没有必要时省略）
- 选择原因：<一句话>

你可以随时说“把主角色改成……”或“去掉……视角”。
```

问题清晰且风险低时直接采用。问题跨领域、角色选择会显著改变结果或属于生产、资金、法务、安全等高风险场景时，仍先给出默认推荐，再把角色选择与关键权限一并交给用户确认。

角色库只作为候选知识源。必须按 [references/role-routing.md](references/role-routing.md) 的净化规则改写为角色契约，禁止整段照搬外部角色提示词。

### 4. 进行反向提问

为每个缺口判断处理方式：

1. **必须问用户**：价值取舍、目标对象、范围、真实授权、不可逆选择、主观偏好。
2. **当前 Agent 查证**：工作区结构、已有技术栈、现有规则、可用测试命令等只读事实。
3. **交给执行 Agent 发现**：实现细节、具体文件位置或运行状态，但必须在提示词中写明先检查再决定。
4. **采用安全假设**：低影响、容易回退的事项；在最终提示词中明确标注。

优先顺序：目标和成功标准 > 权限和风险 > 范围和非目标 > 当前状态和输入 > 输出形式 > 实现偏好。

问题要自然、具体，并在有明显选项时给出推荐。例如：

```text
这次最重要的是“尽快能用”，还是“先把长期架构做好”？
我建议先尽快能用，因为当前需求还在验证阶段；这会让执行 Agent 控制范围，不提前扩建。
```

不要一次发问卷。用户一次回答了多个维度时，吸收全部信息，只继续问剩余的最高价值问题。

### 5. 判断信息是否足够

满足以下条件即可收敛，不必等待所有实现细节齐全：

- 目标和预期结果清楚
- 主角色适配，辅助角色各有必要职责
- 范围、非目标和权限边界足够明确
- 关键输入、上下文来源和当前状态可定位
- 验收标准可观察、可测试或可举证
- 执行 Agent 的交付格式明确

如果用户已经提供完整信息，跳过提问，直接构建提示词。

### 6. 锁定角色契约

在生成提示词前重新检查角色。角色契约必须包含：

- 专业身份
- 本任务中的职责
- 采用的判断标准
- 不负责或无权执行的事项

删除角色源中的虚构履历、虚构记忆、固定工具、无关技术栈、强制风格、隐藏推理要求和超出用户授权的自主操作。

### 7. 生成交接包

读取 [references/output-template.md](references/output-template.md)，输出：

1. 角色选择摘要
2. 完整执行提示词
3. 精简执行提示词
4. 仍需执行 Agent 查证的事项

完整提示词必须自包含，并覆盖目标、背景、角色契约、输入、范围、权限、流程、异常处理、验收标准、验证证据和交付格式。不要在提示词外遗留执行所需的关键事实。

### 8. 交付前自检

逐项检查：

- 角色是否真正改变了提问、判断标准或交付物
- 主角色与辅助角色是否职责重叠或冲突
- 是否混淆“调查”“修改”“部署”“发送”等不同授权
- 是否包含无法验证的形容词，如“专业”“高质量”“体验好”，却没有具体标准
- 是否要求执行 Agent 声称未验证的结果
- 是否意外包含秘密或可外发的敏感资料
- 是否存在相互矛盾的规则、过度设计或无关工作
- 精简版是否仍保留目标、边界、验收和验证要求

发现问题时直接修正，再交付。

## 角色库维护

本 skill 使用 `jnMetaCode/agency-agents-zh` 的固定版本角色索引作为候选源。日常使用不要联网更新。只有用户明确要求刷新角色库时，才运行：

沿用前面选中的 Python 3 启动命令：

```bash
<python3> scripts/sync_role_index.py
```

角色库来源、版本和使用边界见 [references/role-routing.md](references/role-routing.md)。测试场景见 [references/eval-cases.md](references/eval-cases.md)。
