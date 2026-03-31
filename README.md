# Nefesh MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io) server that gives AI agents real-time awareness of human physiological state.

## What it does

Send sensor data (heart rate, voice, facial expression, text sentiment), get back a unified state with a machine-readable action your agent can follow directly. Zero prompt engineering required.

On the 2nd+ call, the response includes `adaptation_effectiveness` — telling your agent whether its previous approach actually worked. A closed-loop feedback system for self-improving agents.

## Setup

### 1. Get an API key

**Option A:** Sign up at [nefesh.ai/signup](https://nefesh.ai/signup) — free tier, no credit card.

**Option B:** Let your AI agent get one automatically via the `request_api_key` tool (see [Self-Provisioning](#api-key-self-provisioning) below).

### 2. Add to your AI agent

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
| **JetBrains IDEs** | Settings > Tools > MCP Server |
| **Zed** | `~/.config/zed/settings.json` (uses `context_servers`) |
| **OpenAI Codex CLI** | `~/.codex/config.toml` |
| **Goose CLI** | `~/.config/goose/config.yaml` |
| **ChatGPT Desktop** | Settings > Apps > Add MCP Server (UI) |
| **Gemini CLI** | Settings (UI) |
| **Augment** | Settings Panel (UI) |
| **Replit** | Integrations Page (web UI) |
| **LibreChat** | `librechat.yaml` (self-hosted) |

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
| `get_human_state` | Get current stress state, score, confidence, and suggested action for a session |
| `ingest` | Send biometric signals, get unified state back |
| `get_trigger_memory` | Get psychological trigger profile for a subject |
| `get_session_history` | Get state history over time |
| `delete_subject` | Delete all stored data for a subject (GDPR) |
| `request_api_key` | Request a free API key by email (no auth required) |
| `check_api_key_status` | Poll for API key activation (no auth required) |

## API Key Self-Provisioning

AI agents can get their own free API key without manual signup. The developer only clicks one email link.

1. Agent calls `request_api_key` with the developer's email
2. Agent polls `check_api_key_status` every 10 seconds
3. Developer clicks the verification link in the email
4. Next poll returns the API key

Both tools work **without an existing API key**.

## Quick test

After adding the config, ask your AI agent:

> "What tools do you have from Nefesh?"

It should list the 7 tools above.

## Pricing

| Plan | Price | Included |
|------|-------|----------|
| **Free** | $0 | Get started, no credit card |
| **Solo** | $25/month | Higher limits |
| **Enterprise** | Custom | Custom SLA |

Get your free key at [nefesh.ai/signup](https://nefesh.ai/signup).

## Documentation

- [Full API Reference](https://nefesh.ai/llms-full.txt)
- [Quick Start](https://nefesh.ai/docs/quickstart)
- [State Mapping](https://nefesh.ai/docs/states)

## Privacy

- No video or audio uploads — edge processing runs client-side
- No PII stored
- GDPR/BIPA compliant — cascading deletion via `delete_subject`
- Not a medical device — for contextual AI adaptation only

## License

MIT — see [LICENSE](LICENSE).
