# basecamp-mcp

An MCP (Model Context Protocol) server that gives Claude read access to your Basecamp account. Works with Claude Desktop, Claude Code, and any MCP-compatible client.

**V1 is read-only** — search, browse, and read your Basecamp projects, messages, todos, documents, and files. No write operations.

## Setup

### 1. Register a Basecamp OAuth App (once per team)

Someone on your team registers an OAuth app with Basecamp. Everyone else can reuse the same Client ID and Secret — each person authorizes their own account separately.

1. Go to [launchpad.37signals.com/integrations](https://launchpad.37signals.com/integrations) and log in with your Basecamp account
2. Click **"Register another application"**
3. Fill in the form:
   - **Name:** `Basecamp MCP` (or whatever you like)
   - **Company:** Your company name
   - **Website URL:** `https://github.com/jacobfiler/basecamp-mcp`
   - **Redirect URI:** `http://localhost:8000/callback` — **must be exact**
4. Click **"Register this app"**
5. You'll see your **Client ID** and **Client Secret** — share these with your team

### 2. Install

```bash
pip install basecamp-mcp
```

**Windows:**
```bash
py -m pip install basecamp-mcp
```

### 3. Authorize

```bash
basecamp-mcp auth
```

**Windows** (if `basecamp-mcp` isn't on PATH):
```bash
py -m basecamp_mcp.server auth
```

This will:
1. Ask for the Client ID and Client Secret from step 1
2. Open your browser to authorize with Basecamp — click **"Yes, I'll allow access"**
3. Save your tokens locally (`~/.config/basecamp-mcp/` on Mac/Linux, `%APPDATA%\basecamp-mcp\` on Windows)
4. Automatically configure Claude Desktop (if installed)

That's it! Restart Claude Desktop and your Basecamp tools are ready.

### Manual Claude Desktop Setup (if auto-config didn't work)

Open Claude Desktop's config file:
- **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add the basecamp server (merge with any existing `mcpServers`):

```json
{
  "mcpServers": {
    "basecamp": {
      "command": "basecamp-mcp",
      "args": []
    }
  }
}
```

### 4. Use It

Ask Claude things like:
- "List my Basecamp projects"
- "Find the style guide in our Basecamp"
- "Show me the messages in the Marketing project"
- "Search all projects for the onboarding checklist"
- "What todos are assigned in the Q2 Planning project?"
- "Read the latest message in HQ"
- "Browse the docs and files in the Marketing project"

## Available Tools

| Tool | Description |
|------|-------------|
| `list_projects` | List all projects you can access |
| `get_project` | Get project details by ID or name (fuzzy match) |
| `search_project` | Search a project's messages, docs, files, and todos by keyword |
| `search_all_projects` | Search across ALL projects by keyword |
| `browse_vault` | Browse a project's Docs & Files (folders, documents, uploads) |
| `list_messages` | List messages on a project's message board |
| `read_message` | Read a message + all its comments |
| `list_todolists` | List todolists in a project |
| `list_todos` | List todos in a todolist (pending or completed) |
| `read_todo` | Read a todo + its comments |
| `list_people` | List all people in the account |
| `list_documents` | List docs in a vault folder |
| `read_document` | Read a document's content |

## Optional: Document Search

If you have a document ingestion service that indexes `.docx` files from Basecamp, you can connect it for full-text search:

```bash
basecamp-mcp connect-docs
```

This adds two additional tools: `search_document_content` and `document_stats`.

## How It Works

```
Config file  (your credentials, never shared)
     |
basecamp-mcp (MCP stdio server, runs locally)
     |
Basecamp API (https://3.basecampapi.com)
```

- Each user runs their own instance with their own OAuth tokens
- The Client ID/Secret identify the app, not the user — safe to share across a team
- No shared server — credentials never leave your machine
- Tokens auto-refresh when they expire (access tokens last 2 weeks, refresh tokens last 10 years)
- Config stored at `~/.config/basecamp-mcp/` (Mac/Linux) or `%APPDATA%\basecamp-mcp\` (Windows)

## Development

```bash
git clone https://github.com/jacobfiler/basecamp-mcp.git
cd basecamp-mcp
pip install -e .

# Run auth flow
basecamp-mcp auth

# Run server directly
basecamp-mcp
```

## License

MIT
