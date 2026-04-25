import streamlit as st

# Page configuration
st.set_page_config(
    page_title="MCP Server-Client Application",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page title and description
st.title("🔗 MCP Server-Client Application")
st.markdown("""
Welcome to the **MCP (Model Context Protocol) Server-Client Application**. 
This application allows you to run an MCP server and connect clients to interact with it.

### Features:
- **Server Page**: Start and manage the MCP server with different transport methods
- **Client Page**: Connect to the server and call available tools

### Navigation:
Use the pages in the sidebar to access the Server and Client interfaces.
""")

st.sidebar.markdown("---")
st.sidebar.info(
    "**How to use:**\n\n"
    "1. Go to the **Server** page and start the MCP server\n"
    "2. Go to the **Client** page and connect to the server\n"
    "3. Call tools and see the results"
)