# Nefesh MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io) server that gives AI agents real-time awareness of human physiological state — stress level, confidence, and behavioral adaptation prompts.

## What it does

Your AI agent sends sensor data (heart rate, voice, video, text) via the Nefesh API. The MCP server returns a unified stress score (0–100), a state label (Calm → Acute Stress), and an adaptation prompt that tells the agent how to adjust its behavior.

**Signals supported:** cardiovascular (HR, HRV, RR intervals), vocal (pitch, jitter, shimmer), visual (facial action units), textual (sentiment, keywords)

## Setup

### 1. Get an API key

Get your key at [nefesh.ai/pricing](https://nefesh.ai/pricing) ($25/month, 50,000 calls).

### 2. Add to your AI agent

Find your agent's MCP config file:

| Agent | Config file |
|-------|-------------|
| **Cursor** | `~/.cursor/mcp.json` |
| **Windsurf** | `~/.codeium/windsurf/mcp_config.json` |
| **Claude Desktop** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Claude Code** | `.mcp.json` (project root) |
| **VS Code (Copilot)** | `.vscode/mcp.json` or `~/Library/Application Support/Code/User/mcp.json` |
| **Cline** | `cline_mcp_settings.json` (via UI: "Configure MCP Servers") |
| **Continue.dev** | `.continue/config.yaml` |
| **Roo Code** | `.roo/mcp.json` |
| **Amazon Q** | `~/.aws/amazonq/mcp.json` |
| **JetBrains IDEs** | Settings → Tools → MCP Server |
| **Zed** | `~/.config/zed/settings.json` (uses `context_servers`) |
| **OpenAI Codex CLI** | `~/.codex/config.toml` |
| **Goose CLI** | `~/.config/goose/config.yaml` |
| **ChatGPT Desktop** | Settings → Apps → Add MCP Server (UI) |
| **Gemini CLI** | Settings (UI) |
| **Augment** | Settings Panel (UI) |
| **Replit** | Integrations Page (web UI) |
| **LibreChat** | `librechat.yaml` (self-hosted) |

Add the following configuration (works with most agents):

```json
{
  "mcpServers": {
    "nefesh": {
      "url": "https://mcp.nefesh.ai/mcp",
      "headers": {
        "X-Nefesh-Key": "<YOUR_API_KEY>"
      }
    }
  }
}
```

<details>
<summary><strong>VS Code (Copilot)</strong> — uses <code>servers</code> instead of <code>mcpServers</code></summary>

```json
{
  "servers": {
    "nefesh": {
      "type": "http",
      "url": "https://mcp.nefesh.ai/mcp",
      "headers": {
        "X-Nefesh-Key": "<YOUR_API_KEY>"
      }
    }
  }
}
```
</details>

<details>
<summary><strong>Zed</strong> — uses <code>context_servers</code> in settings.json</summary>

```json
{
  "context_servers": {
    "nefesh": {
      "settings": {
        "url": "https://mcp.nefesh.ai/mcp",
        "headers": {
          "X-Nefesh-Key": "<YOUR_API_KEY>"
        }
      }
    }
  }
}
```
</details>

<details>
<summary><strong>OpenAI Codex CLI</strong> — uses TOML in <code>~/.codex/config.toml</code></summary>

```toml
[mcp_servers.nefesh]
url = "https://mcp.nefesh.ai/mcp"
```
</details>

<details>
<summary><strong>Continue.dev</strong> — uses YAML in <code>.continue/config.yaml</code></summary>

```yaml
mcpServers:
  - name: nefesh
    type: streamable-http
    url: https://mcp.nefesh.ai/mcp
```
</details>

All agents connect via [Streamable HTTP](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) — no local installation required.

## Tools

| Tool | Description |
|------|-------------|
| `get_human_state` | Returns current stress state, score (0-100), and confidence for a session |
| `ingest` | Send biometric signals — heart rate, voice tone, facial expression, sentiment, and 50+ more fields |
| `get_session_history` | Returns chronological state history for a session |
| `get_trigger_memory` | Returns psychological trigger profile — which topics cause stress, active vs. resolved |
| `delete_subject` | Deletes all stored data for a subject (GDPR compliance) |

## Trigger Memory

Nefesh doesn't just read the current state — it remembers what stresses each user.

When you send `user_message` and `ai_response` alongside biometric signals, Nefesh automatically:
1. Extracts psychological topics from the conversation
2. Correlates topics with stress levels over time
3. Classifies triggers as **active** (currently causing stress) or **resolved** (stress decreased)

Query a user's trigger profile:
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_trigger_memory",
    "arguments": { "subject_id": "user-123" }
  }
}
```

Response:
```json
{
  "triggers": {
    "work_deadline": { "status": "active", "avg_stress": 74, "sessions": 5 },
    "relationship": { "status": "resolved", "avg_stress": 31, "sessions": 3 }
  },
  "active": ["work_deadline"],
  "resolved": ["relationship"]
}
```

## Supported Signals

**57 fields across 10 categories.** Send any combination per API call.

| Category | Fields | Fused in v1 |
|----------|--------|-------------|
| Cardiovascular | heart_rate, rmssd, sdnn, pnn50, mean_ibi, ibi_count, spo2 | ✅ |
| Vocal | tone, speech_rate, pitch_variability | ✅ |
| Visual | expression, gaze, posture, engagement | ✅ |
| Textual | sentiment (-1.0 to 1.0), urgency | ✅ |
| Metabolic | glucose_mg_dl, glucose_mmol_l, glucose_trend | Planned |
| Neural | eeg_alpha_power, eeg_beta_power, eeg_theta_power, cognitive_load | Planned |
| Electrodermal | eda, skin_temperature | Planned |
| Respiratory | respiratory_rate | Planned |
| Movement | steps_last_minute, activity_level | Planned |
| Sleep | sleep_stage | Planned |

> **Note:** `sentiment` is a **float** (-1.0 to 1.0), not a string. The field `sdnn` has no prefix — use `sdnn`, not `hrv_sdnn`.

## Quick test

After adding the config, ask your AI agent:

> "What tools do you have from Nefesh?"

It should list the 5 tools above.

## State labels

| Score | State |
|-------|-------|
| 0–19 | Calm |
| 20–39 | Relaxed |
| 40–59 | Focused |
| 60–79 | Stressed |
| 80–100 | Acute Stress |

## Authentication

API Key Format: `nfsh_...` — get yours at [nefesh.ai/pricing](https://nefesh.ai/pricing) ($25/month, 50,000 calls).

## Documentation

- [Quick Start](https://nefesh.ai/docs/quickstart)
- [API Reference](https://nefesh.ai/llms-full.txt)
- [State Mapping](https://nefesh.ai/docs/states)

## Privacy

- No video uploads — edge processing runs client-side
- No PII stored — strict schema validation
- GDPR/BIPA compliant — cascading deletion via `delete_subject`
- Not a medical device — for contextual AI adaptation only

## License

MIT — see [LICENSE](LICENSE).

