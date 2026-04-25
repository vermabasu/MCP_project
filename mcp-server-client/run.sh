#!/bin/bash

# MCP Server-Client Streamlit App Launcher
# This script starts the Streamlit application

echo "🚀 Starting MCP Server-Client Streamlit Application..."
echo ""
echo "The app will open in your browser at http://localhost:8501"
echo "If it doesn't open automatically, visit the URL above."
echo ""
echo "Navigation:"
echo "  📖 Home: Overview and instructions"
echo "  🖥️ Server: Start/stop the MCP server"
echo "  💻 Client: Connect and call tools"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit is not installed."
    echo "Install it with: pip install streamlit mcp"
    exit 1
fi

# Run the Streamlit app
streamlit run app.py --logger.level=info
