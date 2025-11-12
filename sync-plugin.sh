#!/bin/bash
# Sync cc-plugins from development to marketplace

PLUGIN_NAME="cc-plugins"
DEV_DIR="$HOME/.claude/plugins/$PLUGIN_NAME"
MARKET_DIR="$HOME/code/claude-plugins/plugins/$PLUGIN_NAME"

echo "🔄 Syncing $PLUGIN_NAME from development to marketplace..."

# Check if development directory exists
if [ ! -d "$DEV_DIR" ]; then
    echo "❌ Error: Development directory not found: $DEV_DIR"
    exit 1
fi

# Remove old version
echo "  Removing old version..."
rm -rf "$MARKET_DIR"

# Copy new version
echo "  Copying new version..."
cp -r "$DEV_DIR" "$MARKET_DIR"

# Remove nested git
echo "  Cleaning up nested git repo..."
rm -rf "$MARKET_DIR/.git"

echo "✅ Synced successfully!"
echo ""
echo "Next steps:"
echo "  cd ~/code/claude-plugins"
echo "  git add -A"
echo "  git commit -m 'Update $PLUGIN_NAME to vX.X.X'"
echo "  git push"
