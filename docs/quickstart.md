# 🚀 Quick Start Guide

This stack lets you run ComfyUI workflows on RunPod Serverless GPUs for scalable image and video generation.

**Recommended setup order:**

```
ComfyGen (CLI engine)
        ↓
RunPod Serverless Endpoint (auto-created)
        ↓
BlockFlow (optional visual UI)
```

## 1️⃣ Install ComfyGen

ComfyGen is the engine that runs ComfyUI workflows on RunPod Serverless.

It can be used by:
- humans
- scripts
- AI agents (Claude Code, Cursor, Codex, Gemini CLI, etc.)

### Install (macOS / Linux)

Requires Python 3.11+

```bash
brew install pipx        # macOS — or: apt install pipx / pip install pipx
pipx ensurepath          # adds pipx bin dir to PATH (restart your shell after)

git clone https://github.com/Hearmeman24/ComfyGen.git
cd ComfyGen
pipx install --editable .
pipx inject comfy-gen boto3
```

### Install (Windows)

Requires Python 3.11+ — make sure **"Add Python to PATH"** is checked during installation.

```powershell
pip install pipx
pipx ensurepath          # restart your terminal after this

git clone https://github.com/Hearmeman24/ComfyGen.git
cd ComfyGen
pipx install --editable .
pipx inject comfy-gen boto3
```

> **If `comfy-gen` is not found after install:** add Python's `Scripts` directory to your PATH manually (e.g. `C:\Users\<you>\AppData\Local\Programs\Python\Python3xx\Scripts`).

### Verify

```bash
comfy-gen --help
```

## 2️⃣ Run the Setup Wizard

This step creates your RunPod serverless endpoint and storage configuration automatically.

```bash
comfy-gen init
```

The wizard will configure:
- RunPod API access
- your serverless endpoint
- S3-compatible storage for inputs/outputs

Once this completes, your generation infrastructure is ready.

## 3️⃣ Download Models

Download models directly to your RunPod network volume.

Example:

```bash
comfy-gen download civitai 456789 --dest loras
```

or

```bash
comfy-gen download url https://huggingface.co/.../model.safetensors --dest checkpoints
```

Files are downloaded directly to the serverless GPU volume, not your local machine.

## 4️⃣ Run Your First Workflow

Submit a ComfyUI API workflow:

```bash
comfy-gen submit workflow.json
```

Example output:

```json
{
  "ok": true,
  "output": {
    "url": "https://bucket.s3.region.amazonaws.com/output.png"
  }
}
```

Your generated image/video will be available at the returned URL.

## 5️⃣ (Optional) Install BlockFlow

BlockFlow is a visual pipeline editor for building generation pipelines.

It lets you visually chain steps like:

```
Prompt Writer → ComfyUI Gen → Video Viewer → Upscale
```

### Install

```bash
git clone https://github.com/Hearmeman24/BlockFlow
cd BlockFlow

cp .env.example .env
uv run app.py
```

The app will start:

```
Frontend: http://localhost:3000
Backend:  http://localhost:8000
```

## 💡 When Should You Use Each Tool?

### ComfyGen

Use when you want:
- automation
- scripting
- agent workflows
- bulk generation
- CLI control

### BlockFlow

Use when you want:
- visual pipeline editing
- prompt generation via LLMs
- media viewing and upscaling
- human-in-the-loop workflows

## 📖 Full Documentation

**Before you start, please read the full ComfyGen README carefully:**

**https://github.com/Hearmeman24/ComfyGen#readme**

It covers everything in detail — configuration options, storage providers, workflow format, output format, model downloads, error handling, and more. Taking 10 minutes to read it will save you hours of troubleshooting.

## ⚠️ Important

These tools are 100% free and open source.
They are still BETA, so expect bugs and rough edges.

## Repositories

- **ComfyGen**: https://github.com/Hearmeman24/ComfyGen — **[Read the full README](https://github.com/Hearmeman24/ComfyGen#readme)**
- **BlockFlow**: https://github.com/Hearmeman24/BlockFlow
