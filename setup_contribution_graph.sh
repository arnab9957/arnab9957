#!/bin/bash

echo "🚀 Setting up Daily Contribution Graph for your GitHub README"
echo "============================================================"

# Create necessary directories
mkdir -p .github/workflows
mkdir -p scripts

echo "✅ Created necessary directories"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 is available"

# Install required packages
echo "📦 Installing required Python packages..."
pip3 install -r requirements.txt --user

echo "✅ Python packages installed"

# Generate initial contribution graph
echo "🎨 Generating initial contribution graph..."
python3 test_graph.py

echo "✅ Initial contribution graph generated"

# Check if git is configured
if ! git config user.name &> /dev/null; then
    echo "⚠️  Git user.name is not configured. Please run:"
    echo "   git config --global user.name 'Your Name'"
fi

if ! git config user.email &> /dev/null; then
    echo "⚠️  Git user.email is not configured. Please run:"
    echo "   git config --global user.email 'your.email@example.com'"
fi

echo ""
echo "🎉 Setup complete! Next steps:"
echo ""
echo "1. Commit and push all files to your GitHub repository:"
echo "   git add ."
echo "   git commit -m 'Add daily contribution graph automation'"
echo "   git push"
echo ""
echo "2. The GitHub Action will run daily at midnight UTC"
echo "3. You can also trigger it manually from the Actions tab"
echo ""
echo "4. Your README now includes both:"
echo "   - Custom generated contribution graph (contribution_graph.png)"
echo "   - Dynamic GitHub activity graph from github-readme-activity-graph"
echo ""
echo "📝 Note: The GitHub Action requires GITHUB_TOKEN which is automatically"
echo "   provided by GitHub Actions. No additional setup needed!"
