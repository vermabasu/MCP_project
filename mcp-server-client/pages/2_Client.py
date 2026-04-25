import streamlit as st
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters
import time

st.set_page_config(page_title="MCP Client", page_icon="💻")

st.title("💻 MCP Client")
st.markdown("Connect to the MCP server and call tools")

# Session state initialization
if "client_session" not in st.session_state:
    st.session_state.client_session = None
if "connected" not in st.session_state:
    st.session_state.connected = False
if "available_tools" not in st.session_state:
    st.session_state.available_tools = []
if "call_history" not in st.session_state:
    st.session_state.call_history = []

# Sidebar configuration
with st.sidebar:
    st.subheader("Connection Settings")
    transport_method = st.radio(
        "Select Transport Method:",
        ["sse", "stdio"],
        help="Choose how to connect to the MCP server"
    )
    
    if transport_method == "sse":
        server_url = st.text_input(
            "Server URL:",
            value="http://0.0.0.0:8000/sse",
            help="SSE server endpoint"
        )
    else:
        st.info("Stdio transport will connect to the server directly")
        server_url = None

# Connection status
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Connection Status")
    if st.session_state.connected:
        st.success("✅ Connected to Server")
    else:
        st.warning("⚠️ Not Connected")

with col2:
    if st.session_state.connected:
        st.info(f"📡 Transport: {transport_method.upper()}")

# Connection buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("🔗 Connect to Server", use_container_width=True):
        try:
            st.session_state.connected = False
            
            async def connect():
                try:
                    if transport_method == "sse":
                        async with sse_client(server_url) as (read_stream, write_stream):
                            async with ClientSession(read_stream, write_stream) as session:
                                await session.initialize()
                                st.session_state.client_session = session
                                
                                # List available tools
                                tools_list = await session.list_tools()
                                st.session_state.available_tools = tools_list.tools
                                st.session_state.connected = True
                                return True
                    else:  # stdio
                        server_params = StdioServerParameters(
                            command="python",
                            args=["mcp-server.py"],
                        )
                        async with stdio_client(server_params) as (read_stream, write_stream):
                            async with ClientSession(read_stream, write_stream) as session:
                                await session.initialize()
                                st.session_state.client_session = session
                                
                                # List available tools
                                tools_list = await session.list_tools()
                                st.session_state.available_tools = tools_list.tools
                                st.session_state.connected = True
                                return True
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
                    return False
            
            # Run async function
            result = asyncio.run(connect())
            if result:
                st.success("✅ Connected successfully!")
                st.session_state.call_history.append(
                    f"[{time.strftime('%H:%M:%S')}] Connected to server via {transport_method}"
                )
        except Exception as e:
            st.error(f"❌ Connection failed: {str(e)}")

with col2:
    if st.button("🔌 Disconnect", use_container_width=True, disabled=not st.session_state.connected):
        try:
            st.session_state.client_session = None
            st.session_state.connected = False
            st.session_state.available_tools = []
            st.success("✅ Disconnected!")
            st.session_state.call_history.append(
                f"[{time.strftime('%H:%M:%S')}] Disconnected from server"
            )
        except Exception as e:
            st.error(f"❌ Disconnect failed: {str(e)}")

st.divider()

if st.session_state.connected and st.session_state.available_tools:
    st.subheader("Available Tools")
    
    # Display tools
    tools_col1, tools_col2 = st.columns(2)
    
    with tools_col1:
        st.write("**Registered Tools:**")
        for tool in st.session_state.available_tools:
            st.write(f"- `{tool.name}`")
    
    with tools_col2:
        selected_tool = st.selectbox(
            "Select a tool to call:",
            [tool.name for tool in st.session_state.available_tools],
            label_visibility="collapsed"
        )
    
    # Show selected tool details
    selected = next((t for t in st.session_state.available_tools if t.name == selected_tool), None)
    if selected:
        st.divider()
        st.subheader(f"Tool: {selected.name}")
        st.write(f"**Description**: {selected.description}")
        
        # Get tool input schema
        if hasattr(selected, 'inputSchema') and selected.inputSchema:
            st.write("**Parameters**:")
            schema = selected.inputSchema
            if hasattr(schema, 'properties'):
                for prop_name, prop_details in schema.properties.items():
                    st.write(f"- `{prop_name}`: {prop_details.get('description', 'No description')}")
        
        # Tool call interface
        st.subheader("Call Tool")
        
        # Dynamic input fields based on tool
        tool_inputs = {}
        
        if selected_tool == "add":
            tool_inputs["a"] = st.number_input("First number (a):", value=5)
            tool_inputs["b"] = st.number_input("Second number (b):", value=3)
        
        elif selected_tool == "subtract":
            tool_inputs["a"] = st.number_input("First number (a):", value=10)
            tool_inputs["b"] = st.number_input("Second number (b):", value=3)
        
        elif selected_tool == "get_weather":
            tool_inputs["state"] = st.text_input("US State code (e.g., CA, NY):", value="CA")
        
        elif selected_tool == "echo":
            tool_inputs["message"] = st.text_input("Message to echo:", value="Hello MCP!")
        
        else:
            st.write("Enter parameters as JSON:")
            json_input = st.text_area("JSON Parameters:", value="{}")
            import json
            try:
                tool_inputs = json.loads(json_input)
            except:
                tool_inputs = {}
        
        # Call tool button
        if st.button("📤 Call Tool", use_container_width=True):
            try:
                st.session_state.call_history.append(
                    f"[{time.strftime('%H:%M:%S')}] Calling {selected_tool} with {tool_inputs}"
                )
                
                async def call_tool():
                    try:
                        if transport_method == "sse":
                            async with sse_client(server_url) as (read_stream, write_stream):
                                async with ClientSession(read_stream, write_stream) as session:
                                    await session.initialize()
                                    result = await session.call_tool(selected_tool, arguments=tool_inputs)
                                    return result.content[0].text if result.content else "No result"
                        else:  # stdio
                            server_params = StdioServerParameters(
                                command="python",
                                args=["mcp-server.py"],
                            )
                            async with stdio_client(server_params) as (read_stream, write_stream):
                                async with ClientSession(read_stream, write_stream) as session:
                                    await session.initialize()
                                    result = await session.call_tool(selected_tool, arguments=tool_inputs)
                                    return result.content[0].text if result.content else "No result"
                    except Exception as e:
                        return f"Error: {str(e)}"
                
                result = asyncio.run(call_tool())
                st.success("✅ Tool call successful!")
                st.write("**Result:**")
                st.code(result, language="text")
                st.session_state.call_history.append(
                    f"[{time.strftime('%H:%M:%S')}] Result: {result}"
                )
            except Exception as e:
                st.error(f"❌ Tool call failed: {str(e)}")
                st.session_state.call_history.append(
                    f"[{time.strftime('%H:%M:%S')}] Error: {str(e)}"
                )

elif st.session_state.connected:
    st.info("No tools available. Check server status.")
else:
    st.info("Connect to the server first to see available tools.")

# Call history
st.divider()
st.subheader("Call History")

if st.session_state.call_history:
    with st.expander("View history"):
        for item in st.session_state.call_history[-20:]:  # Show last 20 calls
            st.code(item, language="text")
    
    if st.button("Clear History"):
        st.session_state.call_history = []
        st.rerun()
else:
    st.info("No calls made yet.")
