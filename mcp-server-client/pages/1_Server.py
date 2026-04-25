import streamlit as st
import subprocess
import sys
import os
import psutil
import time

st.set_page_config(page_title="MCP Server", page_icon="🖥️")

st.title("🖥️ MCP Server")
st.markdown("Start and manage the MCP server instance")

# Server status tracking in session state
if "server_process" not in st.session_state:
    st.session_state.server_process = None
if "server_running" not in st.session_state:
    st.session_state.server_running = False
if "transport_method" not in st.session_state:
    st.session_state.transport_method = "stdio"
if "server_logs" not in st.session_state:
    st.session_state.server_logs = []

# Sidebar controls
with st.sidebar:
    st.subheader("Server Controls")
    transport_method = st.radio(
        "Select Transport Method:",
        ["stdio", "sse"],
        key="transport_select"
    )
    st.session_state.transport_method = transport_method

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Server Configuration")
    st.info(f"**Transport Method**: {st.session_state.transport_method.upper()}")
    
    if st.session_state.transport_method == "sse":
        st.markdown("**Server Address**: http://0.0.0.0:8000/sse")
    else:
        st.markdown("**Transport**: Standard Input/Output (stdio)")

with col2:
    st.subheader("Status")
    if st.session_state.server_running:
        st.success("✅ Server is Running")
    else:
        st.warning("⚠️ Server is Stopped")

# Server control buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶️ Start Server", use_container_width=True):
        if not st.session_state.server_running:
            try:
                # Get the directory where this script is running
                script_dir = os.path.dirname(os.path.abspath(__file__))
                server_script = os.path.join(script_dir, "..", "mcp-server.py")
                
                # Start the server process
                st.session_state.server_process = subprocess.Popen(
                    [sys.executable, server_script, st.session_state.transport_method],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=os.path.dirname(server_script)
                )
                st.session_state.server_running = True
                st.session_state.server_logs.append(
                    f"[{time.strftime('%H:%M:%S')}] Server started with {st.session_state.transport_method} transport"
                )
                st.success(f"✅ Server started with {st.session_state.transport_method} transport!")
            except Exception as e:
                st.error(f"❌ Failed to start server: {str(e)}")

with col2:
    if st.button("⏹️ Stop Server", use_container_width=True):
        if st.session_state.server_running and st.session_state.server_process:
            try:
                st.session_state.server_process.terminate()
                st.session_state.server_process.wait(timeout=5)
                st.session_state.server_running = False
                st.session_state.server_logs.append(
                    f"[{time.strftime('%H:%M:%S')}] Server stopped"
                )
                st.success("✅ Server stopped!")
            except Exception as e:
                st.error(f"❌ Failed to stop server: {str(e)}")

with col3:
    if st.button("🔄 Restart Server", use_container_width=True):
        if st.session_state.server_running and st.session_state.server_process:
            try:
                st.session_state.server_process.terminate()
                st.session_state.server_process.wait(timeout=5)
                time.sleep(1)
            except:
                pass
        
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            server_script = os.path.join(script_dir, "..", "mcp-server.py")
            
            st.session_state.server_process = subprocess.Popen(
                [sys.executable, server_script, st.session_state.transport_method],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(server_script)
            )
            st.session_state.server_running = True
            st.session_state.server_logs.append(
                f"[{time.strftime('%H:%M:%S')}] Server restarted with {st.session_state.transport_method} transport"
            )
            st.success(f"✅ Server restarted with {st.session_state.transport_method} transport!")
        except Exception as e:
            st.error(f"❌ Failed to restart server: {str(e)}")

# Server Information
st.divider()
st.subheader("Available Tools on Server")

tools_info = {
    "add": "Add two numbers - Args: a (int), b (int)",
    "subtract": "Subtract two numbers - Args: a (int), b (int)",
    "get_weather": "Get weather alerts for a US state - Args: state (str, e.g., 'CA')",
    "echo": "Echo a message as a resource - Args: message (str)"
}

for tool_name, description in tools_info.items():
    st.write(f"**{tool_name}**: {description}")

# Server Logs
st.divider()
st.subheader("Server Logs")

if st.session_state.server_logs:
    log_container = st.container()
    with log_container:
        for log in st.session_state.server_logs[-10:]:  # Show last 10 logs
            st.code(log, language="text")
else:
    st.info("No logs yet. Start the server to see logs.")

if st.button("Clear Logs"):
    st.session_state.server_logs = []
    st.rerun()
