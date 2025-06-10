---
title: Motion Canvas Docs MCP Server
emoji: 📁
colorFrom: red
colorTo: gray
sdk: docker
app_port: 7860
pinned: true
short_description: "MCP Fileserver to read Motion Canvas docs."
---


# Motion Canvas Docs MCP Server

This is a simple MCP server based on Gradio that allows you to read doc files for Motion Canvas.
It is based on the Gradio Fileserver MCP Server: https://huggingface.co/spaces/prathje/gradio_fileserver_mcp
The API is a simpler version of https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem


## Run

```bash
docker build -t mc_docs_mcp .
docker run -p 7860:7860 mc_docs_mcp
```
The docs and source files are copied from the main motion canvas repository and reside in */app/files*.