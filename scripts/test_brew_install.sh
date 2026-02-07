#!/bin/bash
# Script to verify the Homebrew Formula for Agent Skill Kit

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
FORMULA_PATH="$PROJECT_ROOT/Formula/agent-skill-kit.rb"
FORMULA_NAME="agent-skill-kit"

echo "🧪 Verifying Homebrew Formula..."

# 1. Check syntax
echo "   Checking syntax..."
ruby -c "$FORMULA_PATH"

# 2. Test installation
echo "   Testing installation from local formula..."
# Remove any existing installation
brew uninstall --force "$FORMULA_NAME" >/dev/null 2>&1 || true

# Setup temporary tap
TAP_NAME="ask-verify-$(date +%s)"
TAP_DIR="$(brew --repo)/Library/Taps/homebrew/homebrew-$TAP_NAME"
mkdir -p "$TAP_DIR/Formula"
cp "$FORMULA_PATH" "$TAP_DIR/Formula/"

# Install from temporary tap
echo "   Installing from temporary tap homebrew/$TAP_NAME..."
# We use --build-from-source to ensure it builds using the formula's instructions
if brew install --build-from-source "homebrew/$TAP_NAME/$FORMULA_NAME"; then
    echo "✅ Installation successful!"
    rm -rf "$TAP_DIR"
else
    echo "❌ Installation failed."
    rm -rf "$TAP_DIR"
    exit 1
fi

# 3. Verify functionality
echo "   Verifying installed command..."

# Ensure Homebrew bin is in PATH
if [[ -d "/opt/homebrew/bin" ]]; then
    export PATH="/opt/homebrew/bin:$PATH"
elif [[ -d "/usr/local/bin" ]]; then
    export PATH="/usr/local/bin:$PATH"
fi

if command -v ask >/dev/null; then
    echo "   Found at: $(command -v ask)"
    if ask --version; then
        echo "✅ ask command is working!"
    else
        echo "❌ ask command failed."
        exit 1
    fi
else
    echo "❌ ask command not found in PATH."
    echo "   Current PATH: $PATH"
    exit 1
fi

echo ""
echo "🎉 Formula Verification Complete!"
