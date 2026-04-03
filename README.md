# `re:prompt`

**Grammarly for Prompts** -- research-backed scoring, rule-based rewriting, and cross-tool analytics for your AI conversations. No LLM needed, <50ms per prompt.

[![PyPI version](https://img.shields.io/pypi/v/reprompt-cli)](https://pypi.org/project/reprompt-cli/)
[![Python 3.10+](https://img.shields.io/pypi/pyversions/reprompt-cli)](https://pypi.org/project/reprompt-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-1892_passing-brightgreen)](https://github.com/reprompt-dev/reprompt/actions)
[![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)](https://github.com/reprompt-dev/reprompt)

---

## See it in action

### `reprompt check` -- full diagnostic in one command

<img src="docs/screenshots/check-good.svg" alt="reprompt check — good prompt" width="800">

### `reprompt rewrite` -- rule-based prompt improvement

<img src="docs/screenshots/rewrite.svg" alt="reprompt rewrite — before/after" width="800">

### `reprompt build` -- assemble prompts from components

<img src="docs/screenshots/build.svg" alt="reprompt build — structured prompt assembly" width="800">

<details>
<summary>What a bad prompt looks like</summary>

<img src="docs/screenshots/check-bad.svg" alt="reprompt check — weak prompt" width="800">
</details>

## What it does

### Analyze

| Command | Description |
|---------|-------------|
| `reprompt` | Instant dashboard -- prompts, sessions, avg score, top categories |
| `reprompt scan` | Auto-discover prompts from 9 AI tools |
| `reprompt check "prompt"` | **Full diagnostic** -- score + lint + rewrite preview in one command |
| `reprompt score "prompt"` | Research-backed 0-100 scoring with 30+ features |
| `reprompt compare "a" "b"` | Side-by-side prompt analysis (or `--best-worst` for auto-selection) |
| `reprompt insights` | Personal patterns vs research-optimal benchmarks |
| `reprompt style` | Prompting fingerprint with `--trends` for evolution tracking |
| `reprompt agent` | Agent workflow analysis -- error loops, tool patterns, session efficiency |
| `reprompt sessions` | Session quality scores with frustration signal detection |
| `reprompt repetition` | Cross-session repetition detection -- spot recurring prompts |
| `reprompt patterns` | **Personal prompt weaknesses** -- recurring gaps by task type |
| `reprompt projects` | Per-project quality breakdown -- sessions, scores, frustration signals |

### Optimize

| Command | Description |
|---------|-------------|
| `reprompt build "task"` | **Build prompts from components** -- task, context, files, errors, constraints. Model-aware (Claude/GPT/Gemini) |
| `reprompt rewrite "prompt"` | **Rewrite prompts to score higher** -- filler removal, restructuring, hedging cleanup |
| `reprompt compress "prompt"` | 4-layer prompt compression (40-60% token savings typical) |
| `reprompt distill` | Extract important turns from conversations with 6-signal scoring |
| `reprompt distill --export` | Recover context when a session runs out -- paste into new session |
| `reprompt lint` | Configurable prompt quality linter with CI/GitHub Action support |
| `reprompt init` | Generate `.reprompt.toml` config for your project |

### Manage

| Command | Description |
|---------|-------------|
| `reprompt privacy` | See what data you sent where -- file paths, errors, PII exposure |
| `reprompt privacy --deep` | Scan for sensitive content: API keys, tokens, passwords, PII |
| `reprompt report` | Full analytics: hot phrases, clusters, patterns (`--html` for dashboard) |
| `reprompt digest` | Weekly summary comparing current vs previous period |
| `reprompt wrapped` | Prompt DNA report -- persona, scores, shareable card |
| `reprompt template save\|list\|use` | Save and reuse your best prompts |

## Prompt Science

Scoring is calibrated against 10 peer-reviewed papers covering 30+ features across 5 dimensions:

| Dimension | What it measures | Key papers |
|-----------|-----------------|------------|
| **Structure** | Markdown, code blocks, explicit constraints | Prompt Report ([2406.06608](https://arxiv.org/abs/2406.06608)) |
| **Context** | File paths, error messages, I/O specs, edge cases | Zi+ ([2508.03678](https://arxiv.org/abs/2508.03678)), Google ([2512.14982](https://arxiv.org/abs/2512.14982)) |
| **Position** | Instruction placement relative to context | Stanford ([2307.03172](https://arxiv.org/abs/2307.03172)), Veseli+ ([2508.07479](https://arxiv.org/abs/2508.07479)), Chowdhury ([2603.10123](https://arxiv.org/abs/2603.10123)) |
| **Repetition** | Redundancy that degrades model attention | Google ([2512.14982](https://arxiv.org/abs/2512.14982)) |
| **Clarity** | Readability, sentence length, ambiguity | SPELL (EMNLP 2023), PEEM ([2603.10477](https://arxiv.org/abs/2603.10477)) |

Cross-validated findings that inform our engine:

- **Position bias is architectural** — present at initialization, not learned. Front-loading instructions is effective for prompts under 50% of context window (3 papers agree)
- **Moderate compression improves output** — rule-based filler removal doesn't just save tokens, it enhances LLM performance ([2505.00019](https://arxiv.org/abs/2505.00019))
- **Prompt quality is independently measurable** — prompt-only scoring predicts output quality without seeing the response (ACL 2025, [2503.10084](https://arxiv.org/abs/2503.10084))

All analysis runs locally in <1ms per prompt. No LLM calls, no network requests.

## How it works

```
                          ┌─────────────────────────┐
                          │     reprompt check       │  ← single entry point
                          └────────┬────────────────┘
                                   │
               ┌───────────────────┼───────────────────┐
               ▼                   ▼                   ▼
        ┌─────────────┐   ┌──────────────┐   ┌──────────────┐
        │  Score (0-100) │   │   Lint       │   │   Rewrite    │
        │  30+ features  │   │   rule-based │   │   4 layers   │
        │  5 dimensions  │   │   CI-ready   │   │   no LLM     │
        └──────┬──────┘   └──────┬───────┘   └──────┬───────┘
               │                  │                   │
               └───────────────────┼───────────────────┘
                                   ▼
                          ┌──────────────────┐
                          │  Unified Report   │
                          │  score + issues + │
                          │  rewritten prompt │
                          └──────────────────┘

 Data sources:
 ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
 │Claude Code│ │  Cursor  │ │  Aider   │ │ ChatGPT  │ │ 5 more.. │
 └─────┬────┘ └─────┬────┘ └─────┬────┘ └─────┬────┘ └─────┬────┘
       └─────────────┴───────────┴─────────────┴─────────────┘
                                 │
                    scan → dedup → store → analyze
                                 │
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                  ▼
        ┌──────────┐     ┌──────────────┐    ┌──────────┐
        │ insights │     │  patterns    │    │ sessions │
        │ style    │     │  repetition  │    │ projects │
        │ digest   │     │  privacy     │    │ agent    │
        └──────────┘     └──────────────┘    └──────────┘
```

**Key design decisions:**
- **Pure rules, no LLM** -- scoring and rewriting use regex + TF-IDF + research heuristics. Deterministic, private, <1ms per prompt.
- **Adapter pattern** -- each AI tool gets a parser that normalizes to a common `Prompt` model. Adding a new tool = one file.
- **Two-layer dedup** -- SHA-256 for exact matches, TF-IDF cosine similarity for near-dupes. Handles the "same prompt, slightly different wording" problem.
- **Research-calibrated** -- 10 peer-reviewed papers inform the scoring weights. Not vibes, not benchmarks-on-benchmarks.

## Conversation Distillation

`reprompt distill` scores every turn in a conversation using 6 signals:

- **Position** -- first/last turns carry framing and conclusions
- **Length** -- substantial turns contain more information
- **Tool trigger** -- turns that cause tool calls are action-driving
- **Error recovery** -- turns that follow errors show problem-solving
- **Semantic shift** -- topic changes mark conversation boundaries
- **Uniqueness** -- novel phrasing vs repetitive follow-ups

Session type (debugging, feature-dev, exploration, refactoring) is auto-detected and signal weights adapt accordingly.

## Supported AI tools

| Tool | Format | Auto-discovered by `scan` |
|------|--------|--------------------------|
| Claude Code | JSONL | Yes |
| Codex CLI | JSONL | Yes |
| Cursor | .vscdb | Yes |
| Aider | Markdown | Yes |
| Gemini CLI | JSON | Yes |
| Cline (VS Code) | JSON | Yes |
| OpenClaw / OpenCode | JSON | Yes |
| ChatGPT | JSON | Via `reprompt import` |
| Claude.ai | JSON/ZIP | Via `reprompt import` |

## Installation

```bash
pip install reprompt-cli            # core (all features, zero config)
pip install reprompt-cli[chinese]   # + Chinese prompt analysis (jieba)
pip install reprompt-cli[mcp]       # + MCP server for Claude Code / Continue.dev / Zed
```

### Quick start

```bash
reprompt check "your prompt here"   # full diagnostic — score + lint + rewrite
reprompt scan                       # discover prompts from installed AI tools
reprompt                            # see your dashboard
```

### Auto-scan after every session

```bash
reprompt install-hook               # adds post-session hook to Claude Code
```

### Browser extension

Capture prompts from ChatGPT, Claude.ai, and Gemini directly in your browser. Live score badge shows prompt quality as you type — click "Rewrite & Apply" to improve your prompt and replace the text directly in the input box.

1. **Install the extension** from [Chrome Web Store](https://chromewebstore.google.com/detail/reprompt/ojdccpagaanchmkninlbgbgemdcjckhn) or [Firefox Add-ons](https://addons.mozilla.org/addon/reprompt-cli/)
2. **Connect to the CLI:** `reprompt install-extension`
3. **Verify:** `reprompt extension-status`

Captured prompts sync locally via Native Messaging -- nothing leaves your machine.

### CI integration

#### GitHub Action

```yaml
# .github/workflows/prompt-lint.yml
name: Prompt Quality
on: pull_request

jobs:
  lint:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write    # needed for PR comments
    steps:
      - uses: actions/checkout@v4
      - uses: reprompt-dev/reprompt@main
        with:
          score-threshold: 50   # fail if avg prompt score < 50
          strict: true          # fail on warnings too
          comment-on-pr: true   # post quality report as PR comment
```

When `comment-on-pr: true`, every PR gets a quality report:

```
## reprompt lint 🟢 Passed

| Metric          | Value          |
|-----------------|----------------|
| Prompts checked | 12             |
| Errors          | 0              |
| Warnings        | 2              |
| Avg Score       | 62/100 ✅ (threshold: 50) |

📋 2 violation(s) [click to expand]
```

The comment updates on each push — no duplicates. Uses `GITHUB_TOKEN` (no extra secrets needed).

#### pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/reprompt-dev/reprompt
    rev: v2.5.0
    hooks:
      - id: reprompt-lint
```

#### Direct CLI

```bash
reprompt lint --score-threshold 50  # exit 1 if avg score < 50
reprompt lint --strict              # exit 1 on warnings
reprompt lint --json                # machine-readable output
```

#### Project configuration

```bash
reprompt init   # generates .reprompt.toml with all rules documented
```

```toml
# .reprompt.toml (or [tool.reprompt.lint] in pyproject.toml)
[lint]
score-threshold = 50       # fail if avg score < 50

[lint.rules]
min-length = 20            # error if prompt < 20 chars (0 = off)
short-prompt = 40          # warning if < 40 chars (0 = off)
vague-prompt = true        # error on "fix it" etc (false = off)
debug-needs-reference = true
```

## Privacy

- All analysis runs locally. No prompts leave your machine.
- `reprompt privacy` shows exactly what you've sent to which AI tool.
- Optional telemetry sends only anonymous 26-dimension feature vectors -- never prompt text.
- Open source: audit exactly what's collected.

[Privacy policy](https://getreprompt.dev/privacy)

## Links

- **Website:** [getreprompt.dev](https://getreprompt.dev)
- **Chrome Extension:** [Chrome Web Store](https://chromewebstore.google.com/detail/reprompt/ojdccpagaanchmkninlbgbgemdcjckhn)
- **Firefox Add-on:** [Firefox Add-ons](https://addons.mozilla.org/addon/reprompt-cli/)
- **PyPI:** [reprompt-cli](https://pypi.org/project/reprompt-cli/)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **Privacy:** [getreprompt.dev/privacy](https://getreprompt.dev/privacy)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

MIT
