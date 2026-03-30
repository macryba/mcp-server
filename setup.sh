#!/bin/bash
# Setup script for Wikipedia MCP Server with FastMCP

set -e

echo "🔧 Setting up Wikipedia MCP Server..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install it first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install it first."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Make scripts executable
chmod +x wikipedia_client.py
chmod +x wikipedia_mcp_server.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the MCP server, run:"
echo "   source venv/bin/activate"
echo "   python wikipedia_mcp_server.py"
echo ""
echo "📝 To configure Claude Code, add to ~/.claude/settings.json:"
echo ""
cat <<'EOF'
{
  "mcpServers": {
    "polish-history-wikipedia": {
      "command": "/home/macryba/mcp-server/venv/bin/python",
      "args": ["/home/macryba/mcp-server/wikipedia_mcp_server.py"]
    }
  }
}
EOF
echo ""
echo "🔍 Test the search client:"
echo "   python wikipedia_client.py 'Bolesław III Krzywousty' pl 3"
echo ""
