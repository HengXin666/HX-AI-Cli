# HX-AI-Cli

`HX-AI-Cli` 是一个跨平台的交互式 AI CLI 启动器，用来统一启动 `codex`、`claude`、`cc`、`gemini`、`aider`、`opencode` 等命令行工具。

它是一个单文件 uv 脚本：

```sh
uv run --script aiw.py launch
```

脚本使用 PEP 723 元数据声明依赖，uv 会自动创建隔离环境并安装 `questionary` 和 `rich`。

## git w 是什么

这里的 `git w` 按 Git 内置的 `git worktree` 工作流处理。`git worktree` 可以让同一个仓库同时拥有多个工作目录。对 AI 任务来说，它适合把每个独立任务放进单独目录和分支，避免多个 agent 或多个任务互相改乱同一个工作区。

新建独立任务时，脚本会按这个模式创建工作树：

```sh
git worktree add -b ai/<任务名> .ai-worktrees/<任务名> HEAD
```

如果当前目录还不是 Git 仓库，交互流程会询问是否执行 `git init`。如果仓库还没有任何提交，Git 不能创建 worktree，脚本会提示改为直接在当前工作区启动。

## tmux

这里明确使用 `tmux` 作为任务续跑的终端复用器。脚本会用 `tmux has-session`、`tmux attach-session` 和 `tmux new-session` 管理任务会话。

如果本机没有 `tmux`，任务仍会被记录，但命令会直接启动。后续安装 `tmux` 后可以继续使用保存的任务会话。

## 功能

- 单文件 uv 脚本：`uv run --script aiw.py`。
- 交互界面支持中文和英文。首次进入会选择语言，之后可在配置菜单里修改。
- 交互界面使用彩色文本，高亮当前选择、成功状态和错误状态。
- 自动识别常见 AI CLI：`codex`、`claude`、`cc`、`gemini`、`aider`、`opencode`。
- `cc` 和 `claude` 视为同一个 Claude Code 工具；优先使用 `claude`，没有时再使用真正的 AI CLI 版 `cc`。
- 避免把 Linux 上常见的 C 编译器 `/usr/bin/cc` 误识别为 Claude Code。
- 支持可配置启动命令、默认参数和自动驾驶参数。
- 默认以自动驾驶模式启动：Codex 跳过确认和沙箱，Claude Code 跳过权限确认。
- 支持基于 `tmux` 的任务续跑。
- 支持基于 `git worktree` 的独立任务工作区。
- 支持一键写入 VS Code 自定义集成终端 profile。
- 支持配置导入和导出。
- 配置目录符合平台习惯：
  - Linux：`$XDG_CONFIG_HOME/hx-ai-cli` 或 `~/.config/hx-ai-cli`
  - macOS：`~/Library/Application Support/hx-ai-cli`
  - Windows：`%APPDATA%\hx-ai-cli`

## 常用命令

```sh
uv run --script aiw.py launch
uv run --script aiw.py configure
uv run --script aiw.py doctor
uv run --script aiw.py doctor --json
uv run --script aiw.py vscode
uv run --script aiw.py export ./aiw-config.json
uv run --script aiw.py import ./aiw-config.json
uv run --script aiw.py where
```

## VS Code 一键自定义终端

默认写入 VS Code 用户级 `settings.json`，让任意工作区都可以使用这个终端 profile，并和其它用户级 profile 显示在同一组：

```sh
uv run --script aiw.py vscode
```

也可以显式指定用户级：

```sh
uv run --script aiw.py vscode --scope user
```

如果写入当前工作区的 `.vscode/settings.json`，VS Code 会把它作为工作区级 profile 显示，通常会出现在终端 profile 菜单分隔线下方：

```sh
uv run --script aiw.py vscode --scope workspace
```

支持 VS Code Insiders 和 VSCodium：

```sh
uv run --script aiw.py vscode --scope user --variant insiders
uv run --script aiw.py vscode --scope user --variant codium
```

写入后，VS Code 会出现名为 `HX-AI-Cli` 的集成终端 profile。需要让它出现在默认终端入口时，可以加 `--set-default`：

```sh
uv run --script aiw.py vscode --set-default
```

打开该终端会执行：

```sh
uv run --script <aiw.py> launch --workspace ${workspaceFolder}
```

工作区级配置会同时生成或刷新 `.ai-cli/ai-task.py`，VS Code profile 会指向这个工作区内脚本。用户级配置会指向当前这个 `aiw.py` 文件。

终端 profile 名称为 `HX-AI-Cli`。VS Code 的动态终端标题由全局 `terminal.integrated.tabs.title` 控制；为了不影响普通 zsh，本工具不会改这个全局设置。

## 交互流程

启动：

```sh
uv run --script aiw.py launch
```

首次进入会先选择界面语言：

- 中文
- English

进入后可以选择：

- 继续一个保存过的任务。
- 新建独立任务。
- 选择使用哪个 AI CLI。
- 是否为新任务创建 Git worktree。
- 配置 AI CLI、启动命令、tmux、worktree 默认值。
- 修改界面语言。
- 写入 VS Code 自定义终端配置。

## 自动驾驶模式

默认启动参数：

```sh
codex --dangerously-bypass-approvals-and-sandbox
claude --dangerously-skip-permissions
```

这些参数会让对应 AI CLI 尽量不再弹出人工确认。该模式适合你已经信任当前工作区，并且希望 agent 自动执行任务的场景。

可以在交互配置里进入“修改启动命令”，为每个 AI CLI 修改：

- 可执行命令
- 默认启动参数
- 自动驾驶参数
- 是否启用自动驾驶模式

## 环境检查

```sh
uv run --script aiw.py doctor
```

`doctor` 会检查 `uv`、`git`、`tmux` 和常见 AI CLI。支持 JSON 输出：

```sh
uv run --script aiw.py doctor --json
```

在支持的系统上，交互模式会提示是否安装缺失的基础工具，例如 `git` 或 `tmux`。
