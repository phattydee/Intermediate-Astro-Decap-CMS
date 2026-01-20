# MCP Integration Guide

## Astro Docs MCP Server Integration

This project now includes integration with the official Astro Docs MCP (Model Context Protocol) server.

### What's Been Configured

1. **VS Code MCP Configuration** (`.vscode/mcp.json`):
   ```json
   {
     "servers": {
       "astro-docs": {
         "type": "http",
         "url": "https://mcp.docs.astro.build/mcp"
       }
     }
   }
   ```

2. **Standalone MCP Configuration** (`mcp-config.json`):
   ```json
   {
     "mcpServers": {
       "astro-docs": {
         "command": "npx",
         "args": ["-y", "mcp-remote", "https://mcp.docs.astro.build/mcp"]
       }
     }
   }
   ```

### Server Details

- **URL**: `https://mcp.docs.astro.build/mcp`
- **Protocol Version**: `2025-06-18`
- **Transport**: Streamable HTTP
- **Capabilities**: Tools (with listChanged support), Logging
- **Server Name**: "Astro Docs server"
- **Version**: "1.0.0"

### How to Use

#### For VS Code with Copilot
1. Ensure MCP is enabled in VS Code settings (`Chat > MCP`)
2. The `.vscode/mcp.json` file will be automatically detected
3. Restart VS Code if needed

#### For Other AI Tools
Use the `mcp-config.json` configuration or add the server manually:
- **Name**: `astro-docs`
- **URL**: `https://mcp.docs.astro.build/mcp`
- **Transport**: HTTP (streamable)

### Available Tools

The server exposes a `search_astro_docs` tool that allows AI assistants to:
- Search the entire Astro documentation in real-time
- Get accurate, up-to-date answers about Astro features
- Access current API documentation and best practices

### Testing

To test the connection:
```bash
npx @modelcontextprotocol/inspector
```

Or test directly with curl:
```bash
curl -X POST "https://mcp.docs.astro.build/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0.0"}}}'
```

### Benefits

- **Real-time Documentation**: Access to the latest Astro docs
- **Accurate Code Generation**: AI assistants use current APIs and patterns
- **Better Troubleshooting**: Up-to-date solutions for Astro issues
- **Reduced Context Switching**: Get answers directly in your coding environment

### Example Questions You Can Now Ask

- "How do I set up image optimization in Astro v5?"
- "What's the current syntax for View Transitions?"
- "Show me how to configure Decap CMS with Astro"
- "What are the latest Astro integrations available?"

### Troubleshooting

If your AI tool doesn't support streamable HTTP transport, use the `mcp-remote` proxy approach from the `mcp-config.json` file.