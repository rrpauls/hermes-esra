#!/bin/bash
#
# install.sh
# Install ESRA meta-skills + runtime tools into the Hermes agent home.
#
# Usage:
#   1. Clone: git clone https://github.com/rrpauls/hermes-esra.git
#   2. cd hermes-esra
#   3. ./install.sh
#
# Layout written (Hermes-aligned):
#   $HERMES_HOME/skills/esra/   — meta-skills (Hermes discovers these)
#   $HERMES_HOME/esra/tools/    — Python tools package (stable absolute paths)
#   $HERMES_HOME/esra/manifest.json
#   $HERMES_HOME/AGENTS.md
#
# Env:
#   HERMES_HOME  — Hermes profile root (default: ~/.hermes)
#   ESRA_HOME    — override ESRA package root (default: $HERMES_HOME/esra)
#

set -euo pipefail

echo "=========================================="
echo "  Hermes ESRA Installer"
echo "=========================================="
echo

# Resolve paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_SKILLS="$SCRIPT_DIR/skills"
SOURCE_TOOLS="$SCRIPT_DIR/tools"
AGENTS_SOURCE="$SCRIPT_DIR/AGENTS.md"

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
ESRA_HOME="${ESRA_HOME:-$HERMES_HOME/esra}"
SKILLS_DEST="$HERMES_HOME/skills/esra"
TOOLS_DEST="$ESRA_HOME/tools"
AGENTS_DEST="$HERMES_HOME/AGENTS.md"
MANIFEST_DEST="$ESRA_HOME/manifest.json"

# Validate sources
if [ ! -d "$SOURCE_SKILLS" ]; then
    echo "❌ Error: Skills directory not found: $SOURCE_SKILLS"
    echo "   Run this script from the hermes-esra repository root (or via path to install.sh)."
    exit 1
fi

if [ ! -d "$SOURCE_TOOLS" ]; then
    echo "❌ Error: Tools directory not found: $SOURCE_TOOLS"
    exit 1
fi

echo "📁 HERMES_HOME:   $HERMES_HOME"
echo "📁 ESRA_HOME:     $ESRA_HOME"
echo "📁 Skills →       $SKILLS_DEST"
echo "📁 Tools  →       $TOOLS_DEST"
echo

# Create directories with restricted permissions when new
mkdir -p "$SKILLS_DEST"
mkdir -p "$TOOLS_DEST"
chmod 700 "$HERMES_HOME" 2>/dev/null || true
chmod 700 "$ESRA_HOME" 2>/dev/null || true

# --- Skills (Hermes discovery tree) ---
echo "📦 Installing meta-skills → $SKILLS_DEST"
# Refresh skill tree: copy each skill directory (keeps sibling categories intact)
for skill_path in "$SOURCE_SKILLS"/*/; do
    [ -d "$skill_path" ] || continue
    name="$(basename "$skill_path")"
    rm -rf "${SKILLS_DEST:?}/$name"
    cp -R "$skill_path" "$SKILLS_DEST/$name"
done
echo "✅ Skills installed"

# --- Tools (ESRA package under Hermes home) ---
echo "📦 Installing tools → $TOOLS_DEST"
# Replace tools package cleanly so deleted files do not linger
if [ -d "$TOOLS_DEST" ]; then
    find "$TOOLS_DEST" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
fi
cp -R "$SOURCE_TOOLS"/. "$TOOLS_DEST"/
# Drop bytecode caches if any were copied
find "$TOOLS_DEST" -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
find "$TOOLS_DEST" -type f -name '*.pyc' -delete 2>/dev/null || true
chmod 755 "$TOOLS_DEST"/*.py 2>/dev/null || true
echo "✅ Tools installed"

# --- Manifest (machine-readable paths for Hermes + tools) ---
echo "📄 Writing manifest → $MANIFEST_DEST"
INSTALLED_AT="$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u)"
TOOLS_JSON="["
first=1
for f in "$TOOLS_DEST"/*.py; do
    [ -f "$f" ] || continue
    name="$(basename "$f")"
    # Skip package markers from the public tool inventory
    [ "$name" = "__init__.py" ] && continue
    if [ "$first" -eq 1 ]; then
        TOOLS_JSON="${TOOLS_JSON}\"${name}\""
        first=0
    else
        TOOLS_JSON="${TOOLS_JSON}, \"${name}\""
    fi
done
TOOLS_JSON="${TOOLS_JSON}]"
cat > "$MANIFEST_DEST" <<EOF
{
  "name": "hermes-esra",
  "version": "1.2",
  "installed_at": "$INSTALLED_AT",
  "hermes_home": "$HERMES_HOME",
  "esra_home": "$ESRA_HOME",
  "skills_dir": "$SKILLS_DEST",
  "tools_dir": "$TOOLS_DEST",
  "agents_md": "$AGENTS_DEST",
  "tools": ${TOOLS_JSON}
}
EOF
chmod 600 "$MANIFEST_DEST" 2>/dev/null || true
echo "✅ Manifest written"

# --- AGENTS.md (with installed tool path section injected if template markers exist) ---
if [ -f "$AGENTS_SOURCE" ]; then
    echo "📄 Installing AGENTS.md → $AGENTS_DEST"
    cp "$AGENTS_SOURCE" "$AGENTS_DEST"
    chmod 600 "$AGENTS_DEST" 2>/dev/null || true
    echo "✅ AGENTS.md installed"
else
    echo "⚠️  AGENTS.md not found in the repository (skipping)"
fi

echo
echo "📋 Installed ESRA skills:"
ls -1 "$SKILLS_DEST" | sed 's/^/   - /'
echo
echo "🔧 Installed ESRA tools:"
ls -1 "$TOOLS_DEST"/*.py 2>/dev/null | xargs -n1 basename | sed 's/^/   - /'
echo

echo "=========================================="
echo "  Next Steps"
echo "=========================================="
echo
echo "1. Restart Hermes (or use /skills in chat to refresh)."
echo
echo "2. Hermes can discover tools via the esra-runtime skill, or run:"
echo "   python $TOOLS_DEST/evolution_hook.py"
echo "   python $TOOLS_DEST/evolution_hook.py --force-cycle"
echo "   python $TOOLS_DEST/skill_validator.py --verbose --skills-dir $SKILLS_DEST"
echo
echo "3. Paths are recorded in:"
echo "   $MANIFEST_DEST"
echo
echo "4. Recommended first tests in Hermes:"
echo "   - Activate 'esra-runtime' (where tools live)"
echo "   - Activate 'hermes-evolution-orchestrator'"
echo "   - Try 'ooda-framework' on an uncertain decision"
echo
echo "=========================================="
echo "  Installation completed successfully!"
echo "=========================================="
