#!/bin/bash

# Script to manage VS Code extensions for Python projects
# This helps reduce memory usage and terminal responsiveness issues

echo "🔧 VS Code Extension Manager for Python Projects"
echo "=============================================="

# Extensions to disable for Python-focused work
WEB_EXTENSIONS=(
    "svelte.svelte-vscode"
    "bradlc.vscode-tailwindcss"
    "dbaeumer.vscode-eslint"
    "esbenp.prettier-vscode"
    "csstools.postcss"
    "pranaygp.vscode-css-peek"
    "rvest.vs-code-prettier-eslint"
    "formulahendry.auto-rename-tag"
    "ms-vscode.vscode-typescript-next"
    "ms-vscode.vscode-json"
)

# Essential extensions for Python development
PYTHON_EXTENSIONS=(
    "ms-python.python"
    "ms-python.vscode-pylance"
    "ms-python.debugpy"
    "ms-python.flake8"
    "ms-python.black-formatter"
)

disable_web_extensions() {
    echo "🚫 Disabling web development extensions..."
    for ext in "${WEB_EXTENSIONS[@]}"; do
        echo "  Disabling: $ext"
        code --disable-extension "$ext" 2>/dev/null || echo "    Extension not found or already disabled"
    done
    echo "✅ Web extensions disabled"
}

enable_web_extensions() {
    echo "✅ Enabling web development extensions..."
    for ext in "${WEB_EXTENSIONS[@]}"; do
        echo "  Enabling: $ext"
        code --enable-extension "$ext" 2>/dev/null || echo "    Extension not found"
    done
    echo "✅ Web extensions enabled"
}

show_running_processes() {
    echo "📊 Current VS Code extension processes:"
    ps aux | grep -E "(Code Helper|eslint|prettier|svelte|tailwind)" | grep -v grep | head -10
}

case "$1" in
    "disable")
        disable_web_extensions
        ;;
    "enable")
        enable_web_extensions
        ;;
    "status")
        show_running_processes
        ;;
    *)
        echo "Usage: $0 {disable|enable|status}"
        echo ""
        echo "Commands:"
        echo "  disable  - Disable web development extensions"
        echo "  enable   - Enable web development extensions"
        echo "  status   - Show running extension processes"
        echo ""
        echo "💡 After running disable/enable, restart VS Code for changes to take effect"
        ;;
esac
