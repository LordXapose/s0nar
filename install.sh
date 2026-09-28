#!/usr/bin/env bash
#
# S0NAR — Kali Linux installer
#
# Automates:
#   1. Prerequisite installation (pipx, nmap, amass, git, golang)
#   2. Go-based backends (subfinder, nuclei)
#   3. PATH setup for ~/go/bin
#   4. Nuclei template updates
#   5. S0NAR installation via pipx
#   6. Verification of every component
#
# Usage:
#   chmod +x install-kali.sh
#   ./install-kali.sh
#
# Author: LordXapose
# Repo:   https://github.com/LordXapose/s0nar
# License: MIT

set -o pipefail

# ─────────────────────────────────────────────────────────────────────
# Colors & helpers
# ─────────────────────────────────────────────────────────────────────

if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    CYAN='\033[0;36m'
    MAGENTA='\033[0;35m'
    BOLD='\033[1m'
    DIM='\033[2m'
    RESET='\033[0m'
else
    RED=''; GREEN=''; YELLOW=''; CYAN=''; MAGENTA=''; BOLD=''; DIM=''; RESET=''
fi

info()    { echo -e "${CYAN}ℹ${RESET}  $*"; }
success() { echo -e "${GREEN}✔${RESET}  $*"; }
warn()    { echo -e "${YELLOW}⚠${RESET}  $*"; }
error()   { echo -e "${RED}✘${RESET}  $*"; }
step()    { echo -e "\n${BOLD}${MAGENTA}▶ $*${RESET}"; }
dim()     { echo -e "${DIM}$*${RESET}"; }

die() {
    error "$*"
    exit 1
}

# ─────────────────────────────────────────────────────────────────────
# Pre-flight checks
# ─────────────────────────────────────────────────────────────────────

step "Pre-flight checks"

# Must not be run as root
if [ "$EUID" -eq 0 ]; then
    die "Do not run this script as root. Run as your normal user; it will prompt for sudo when needed."
fi

# Must be a Debian-based system
if ! command -v apt >/dev/null 2>&1; then
    die "This installer only supports Debian/Kali/Ubuntu. 'apt' not found."
fi

# Warn (but don't fail) if not Kali
if ! grep -qi "kali" /etc/os-release 2>/dev/null; then
    warn "This doesn't look like Kali Linux. Continuing anyway, but the script is tuned for Kali."
fi

# Confirm sudo access up front so we don't fail halfway through
if ! sudo -v; then
    die "Sudo access is required. Please run 'sudo -v' first, or run this script from an account with sudo privileges."
fi

success "Pre-flight checks passed"

# ─────────────────────────────────────────────────────────────────────
# 1. Install system prerequisites
# ─────────────────────────────────────────────────────────────────────

step "Installing system prerequisites"

REQUIRED_PKGS=(pipx nmap git curl ca-certificates)
OPTIONAL_PKGS=(amass golang-go)

# Check what's already installed
to_install=()
for pkg in "${REQUIRED_PKGS[@]}"; do
    if dpkg -s "$pkg" >/dev/null 2>&1; then
        success "$pkg already installed"
    else
        info "$pkg needs to be installed"
        to_install+=("$pkg")
    fi
done

# Optional packages — install only if missing, but don't fail if unavailable
to_install_optional=()
for pkg in "${OPTIONAL_PKGS[@]}"; do
    if dpkg -s "$pkg" >/dev/null 2>&1; then
        success "$pkg already installed"
    else
        info "$pkg needs to be installed (optional backend)"
        to_install_optional+=("$pkg")
    fi
done

if [ ${#to_install[@]} -gt 0 ]; then
    info "Updating apt package lists..."
    sudo apt update -qq || die "apt update failed"

    info "Installing: ${to_install[*]}"
    sudo apt install -y "${to_install[@]}" || die "Failed to install required packages"
    success "Required packages installed"
fi

if [ ${#to_install_optional[@]} -gt 0 ]; then
    info "Installing optional: ${to_install_optional[*]}"
    if sudo apt install -y "${to_install_optional[@]}"; then
        success "Optional packages installed"
    else
        warn "Optional packages failed — S0NAR will still work without them"
    fi
fi

# Verify Go is available (needed for subfinder + nuclei)
if ! command -v go >/dev/null 2>&1; then
    warn "Go is not installed. subfinder and nuclei will be skipped."
    warn "Install with: sudo apt install golang-go"
    SKIP_GO_TOOLS=1
else
    GO_VERSION=$(go version | awk '{print $3}')
    success "Go detected: $GO_VERSION"
    SKIP_GO_TOOLS=0
fi

# ─────────────────────────────────────────────────────────────────────
# 2. Install Go-based backends
# ─────────────────────────────────────────────────────────────────────

if [ "$SKIP_GO_TOOLS" -eq 0 ]; then
    step "Installing Go-based backends"

    # Ensure Go bin dir exists
    mkdir -p "$HOME/go/bin"

    # subfinder
    if [ -x "$HOME/go/bin/subfinder" ]; then
        success "subfinder already installed"
    else
        info "Installing subfinder..."
        if go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest 2>&1 | tail -1; then
            success "subfinder installed"
        else
            warn "subfinder install failed — S0NAR will skip it"
        fi
    fi

    # nuclei
    if [ -x "$HOME/go/bin/nuclei" ]; then
        success "nuclei already installed"
    else
        info "Installing nuclei (this can take a minute)..."
        if go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest 2>&1 | tail -1; then
            success "nuclei installed"
        else
            warn "nuclei install failed — S0NAR will use built-in checks only"
        fi
    fi
fi

# ─────────────────────────────────────────────────────────────────────
# 3. Configure PATH
# ─────────────────────────────────────────────────────────────────────

step "Configuring shell PATH"

GO_BIN_LINE='export PATH="$PATH:$HOME/go/bin"'

# Add to ~/.bashrc if not already there
if grep -Fxq "$GO_BIN_LINE" "$HOME/.bashrc" 2>/dev/null; then
    success "~/go/bin already in ~/.bashrc"
else
    echo "" >> "$HOME/.bashrc"
    echo "# Added by S0NAR installer" >> "$HOME/.bashrc"
    echo "$GO_BIN_LINE" >> "$HOME/.bashrc"
    success "Added ~/go/bin to ~/.bashrc"
fi

# Add to ~/.zshrc if it exists
if [ -f "$HOME/.zshrc" ]; then
    if grep -Fxq "$GO_BIN_LINE" "$HOME/.zshrc" 2>/dev/null; then
        success "~/go/bin already in ~/.zshrc"
    else
        echo "" >> "$HOME/.zshrc"
        echo "# Added by S0NAR installer" >> "$HOME/.zshrc"
        echo "$GO_BIN_LINE" >> "$HOME/.zshrc"
        success "Added ~/go/bin to ~/.zshrc"
    fi
fi

# Apply to current session so the rest of the installer can use it
export PATH="$PATH:$HOME/go/bin"

# ─────────────────────────────────────────────────────────────────────
# 4. Update Nuclei templates
# ─────────────────────────────────────────────────────────────────────

if command -v nuclei >/dev/null 2>&1; then
    step "Updating Nuclei templates"
    info "This downloads 10,000+ community templates (first-time ~200MB)..."
    if nuclei -update-templates -silent 2>&1 | tail -3; then
        success "Nuclei templates updated"
    else
        warn "Template update had warnings — nuclei may still work"
    fi
fi

# ─────────────────────────────────────────────────────────────────────
# 5. Install S0NAR
# ─────────────────────────────────────────────────────────────────────

step "Installing S0NAR"

# Determine script directory (the S0NAR repo)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Verify we're in a S0NAR repo
if [ ! -f "$SCRIPT_DIR/pyproject.toml" ]; then
    die "pyproject.toml not found in $SCRIPT_DIR. Run this script from the S0NAR repo root."
fi

# Verify pyproject.toml is valid (no BOM, no syntax errors)
if ! python3 -c "import tomllib; tomllib.load(open('$SCRIPT_DIR/pyproject.toml','rb'))" 2>/dev/null; then
    # Older Pythons (<3.11) don't have tomllib — try tomli as fallback
    if ! python3 -c "import tomli; tomli.load(open('$SCRIPT_DIR/pyproject.toml','rb'))" 2>/dev/null; then
        warn "Could not validate pyproject.toml (missing tomllib/tomli). Continuing anyway."
    fi
fi

# Ensure pipx is fully initialized
info "Running 'pipx ensurepath'..."
pipx ensurepath >/dev/null 2>&1 || warn "pipx ensurepath reported warnings"

# Install S0NAR in editable mode
if pipx list 2>/dev/null | grep -q "package s0nar"; then
    info "S0NAR already installed via pipx — reinstalling in editable mode"
    pipx reinstall -e "$SCRIPT_DIR" || die "pipx reinstall failed"
else
    info "Installing S0NAR in editable mode from $SCRIPT_DIR"
    pipx install -e "$SCRIPT_DIR" || die "pipx install failed"
fi

success "S0NAR installed"

# ─────────────────────────────────────────────────────────────────────
# 6. Verification
# ─────────────────────────────────────────────────────────────────────

step "Verifying installation"

# Refresh PATH for the current shell
export PATH="$PATH:$HOME/.local/bin"

check_cmd() {
    local cmd="$1"
    local label="$2"
    if command -v "$cmd" >/dev/null 2>&1; then
        success "$label: $("$cmd" --version 2>&1 | head -1)"
        return 0
    else
        warn "$label: not found in PATH"
        return 1
    fi
}

echo ""
dim "Backends:"
check_cmd nmap      "nmap"      || true
check_cmd subfinder "subfinder" || true
check_cmd amass     "amass"     || true
check_cmd nuclei    "nuclei"    || true

echo ""
dim "S0NAR:"
if command -v sonar >/dev/null 2>&1; then
    success "sonar: $(sonar --version 2>&1 | head -1)"
else
    warn "sonar: not found in PATH"
    warn "Try: close this terminal and open a new one, then run 'sonar --version'"
fi

# ─────────────────────────────────────────────────────────────────────
# 7. Final summary
# ─────────────────────────────────────────────────────────────────────

echo ""
echo -e "${BOLD}${GREEN}════════════════════════════════════════════════════════════${RESET}"
echo -e "${BOLD}${GREEN}  S0NAR installation complete${RESET}"
echo -e "${BOLD}${GREEN}════════════════════════════════════════════════════════════${RESET}"
echo ""

cat <<EOF
${BOLD}Next steps:${RESET}

  1. ${YELLOW}Close this terminal and open a new one${RESET}
     (so PATH changes take effect)

  2. Verify the install:

        ${CYAN}sonar --version${RESET}
        ${CYAN}sonar banner${RESET}

  3. Run your first scan:

        ${CYAN}sonar test -d example.com --fast${RESET}

  4. Full pipeline against a domain you own:

        ${CYAN}sonar test -d yourdomain.com${RESET}

${BOLD}Documentation:${RESET}
  ${CYAN}sonar --help${RESET}
  ${CYAN}sonar test --help${RESET}
  ${CYAN}https://github.com/LordXapose/s0nar${RESET}

${BOLD}Uninstall:${RESET}
  ${CYAN}pipx uninstall s0nar${RESET}

EOF

# ─────────────────────────────────────────────────────────────────────
# Offer to open a new shell
# ─────────────────────────────────────────────────────────────────────

read -r -p "$(echo -e "${CYAN}?${RESET}  Open a new shell now to test? [y/N] ")" answer
if [[ "$answer" =~ ^[Yy]$ ]]; then
    exec "$SHELL" -l
fi

success "Done."
