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


# Filesystem MCP Server

This is a simple MCP server based on Gradio that allows you to read and write files to a local directory. Please note that this code is a proof of concept and not meant for production.
You can configure whether you want to allow editing the files by setting the environment variable `ALLOW_EDITING`. The files reside in `/app/files`. Using Docker, you can mount external directories as well.
The API is a simpler version of https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem . 


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


## Mounting External Files

You can use Docker to mount external directories as well:


```bash
docker build -t fs_mcp .
docker run -p 7860:7860 -v $LOCAL_DIR:/app/files fs_mcp
```

If you do not want to allow editing the files, you can use *ALLOW_EDITING=false* and also prevent changes to your local filesystem by making the mount readonly: 


```bash
docker build -t fs_mcp .
docker run -p 7860:7860 -v $LOCAL_DIR:/app/files:ro -e ALLOW_EDITING=false fs_mcp
```