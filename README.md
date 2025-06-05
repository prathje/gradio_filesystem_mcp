---
title: Gradio Filesystem MCP Server
emoji: 📁
colorFrom: blue
colorTo: gray
sdk: docker
app_port: 7860
pinned: true
short_description: Simple MCP Fileserver to read and write from a local directory.
tags:
    - mcp-server-track
---

## Run

```bash
docker build -t fs_mcp .
docker run -p 7860:7860 fs_mcp
```
The files reside in */app/files*. It should also be possible to mount external files via docker.
One can disable editing files using the env variable *ALLOW_EDITING=false*:

```bash
docker run -p 7860:7860 -e ALLOW_EDITING=false fs_mcp
```

The MCP server will be available under *http://localhost:7860*