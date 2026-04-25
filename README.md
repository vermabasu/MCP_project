# Quick Start Guide

## 🎥 Demo Video

Watch the MCP Project in action:

[![Watch the demo](./preview.gif)](./MCP_Project.mp4)

---

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install streamlit mcp
```
NOTE:- You need "GROQ API" to run clinet llm (opensource) model. Keep it in ".env" file. 

### Step 2: Start the Streamlit App
```bash
cd ./mcp-server-client
streamlit run app.py
```

Or use the provided script:
```bash
bash run.sh
```

### Step 3: Use the Application

#### On the Server Page (🖥️)
1. Select transport method: **stdio** or **sse**
2. Click **▶️ Start Server**
3. Wait for confirmation message
4. Monitor logs and status

#### On the Client Page (💻)
1. Select the **same transport method** as the server
2. Click **🔗 Connect to Server**
3. Select a tool from the dropdown
4. Enter parameters
5. Click **📤 Call Tool**
6. View results

---

## 📋 File Structure

```
mcp-server-client/
├── app.py                    ← Main app (start here)
├── mcp-server.py             ← MCP server with tools
├── pages/
│   ├── 1_Server.py           ← Server control panel
│   └── 2_Client.py           ← Client interface
├── mcp-client-langchain_sse.py      ← SSE client class
├── mcp-client-langchain_stdio.py    ← Stdio client class
├── SETUP.md                  ← Full documentation
├── IMPLEMENTATION_SUMMARY.md ← Architecture overview
└── run.sh                    ← Quick start script
```

---

## 🛠️ Available Tools

| Tool | Input | Output | Example |
|------|-------|--------|---------|
| `add` | a, b (int) | sum | add(5, 3) = 8 |
| `subtract` | a, b (int) | difference | subtract(10, 3) = 7 |
| `get_weather` | state (str) | alerts | get_weather("CA") |
| `echo` | message (str) | echo | echo("Hello") |

---

## 🌐 Transport Methods

| Method | Use Case | Configuration |
|--------|----------|---------------|
| **stdio** | Local testing, quick start | Automatic - no config needed |
| **sse** | Web clients, network testing | URL: http://0.0.0.0:8000/sse |

---


## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│          Streamlit Multi-Page App               │
│                  (app.py)                       │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────────┐   ┌──────────────────┐  │
│  │  1_Server.py     │   │  2_Client.py     │  │
│  │                  │   │                  │  │
│  │ • Start/Stop     │   │ • Connect/Disc   │  │
│  │ • Transport sel  │   │ • Tool selection │  │
│  │ • Status display │   │ • Param input    │  │
│  │ • Logs & history │   │ • Result display │  │
│  └──────────────────┘   └──────────────────┘  │
│         ↓ (manages)             ↓ (calls)      │
└─────────────────────────────────────────────────┘
          ↓                            ↓
┌──────────────────────┐      ┌──────────────────┐
│   mcp-server.py      │      │ Client Classes   │
│                      │      │                  │
│ FastMCP Server       │      │ SSE/Stdio class  │
│ • add/subtract       │      │ • Connection mgm │
│ • get_weather        │      │ • Tool execution │
│ • echo resource      │      │ • Results parse  │
│                      │      │                  │
│ Transports:          │      │ Transports:      │
│ • stdio              │      │ • http://..sse   │
│ • sse (port 8000)    │      │ • stdio          │
└──────────────────────┘      └──────────────────┘
```


---

## 🧪 Testing Individual Clients

### Test SSE Client Directly
```bash
python mcp-client-langchain_sse.py
```
- Automatically connects to server
- Lists available tools
- Calls example tools
- Shows results

### Test Stdio Client Directly
```bash
python mcp-client-langchain_stdio.py
```
- Starts server automatically
- Lists available tools
- Calls example tools
- Shows results

---

## 🚨 Important Notes

⚠️ **Before running**: Make sure you have Python 3.7+ installed
⚠️ **Port 8000**: Required for SSE mode, must be available
⚠️ **Server first**: Always start Server before connecting Client
⚠️ **Same transport**: Client and Server must use same transport method

---

Good luck! 🚀
