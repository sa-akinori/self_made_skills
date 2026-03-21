#!/bin/bash
#
# Version Manager for Research Reports
# Manages report versions (v1, v2, v3...)
#
# Usage:
#   version-manager.sh save [description]     - Save current report as new version
#   version-manager.sh list                   - List all versions
#   version-manager.sh restore <version>      - Restore specific version
#   version-manager.sh diff <v1> <v2>         - Show differences between versions
#   version-manager.sh info <version>         - Show version details
#

set -e

# Directories
PROJECT_ROOT="$(pwd)"
REPORT_DIR="$PROJECT_ROOT/report"
VERSIONS_DIR="$PROJECT_ROOT/versions"
VERSION_METADATA="$VERSIONS_DIR/.metadata"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Functions
command_save() {
    local description="${1:-No description provided}"

    # Check if report directory exists
    if [ ! -d "$REPORT_DIR" ]; then
        echo -e "${RED}Error: report/ directory not found${NC}"
        echo "Please generate a report first."
        exit 1
    fi

    # Create versions directory if it doesn't exist
    mkdir -p "$VERSIONS_DIR"
    touch "$VERSION_METADATA"

    # Determine next version number
    local version_num=1
    if [ -f "$VERSION_METADATA" ]; then
        local last_version=$(grep -E "^v[0-9]+" "$VERSION_METADATA" | tail -1 | cut -d'|' -f1 | sed 's/v//')
        if [ -n "$last_version" ]; then
            version_num=$((last_version + 1))
        fi
    fi

    local version_name="v${version_num}"
    local version_path="$VERSIONS_DIR/$version_name"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    echo -e "${BLUE}Creating version: ${version_name}${NC}"

    # Copy report directory to version
    cp -r "$REPORT_DIR" "$version_path"

    # Save metadata
    echo "${version_name}|${timestamp}|${description}" >> "$VERSION_METADATA"

    # Calculate size
    local size=$(du -sh "$version_path" | cut -f1)

    echo -e "${GREEN}✓ Version ${version_name} created successfully${NC}"
    echo -e "  Timestamp: ${timestamp}"
    echo -e "  Size: ${size}"
    echo -e "  Description: ${description}"
    echo -e "  Location: ${version_path}"
}

command_list() {
    if [ ! -d "$VERSIONS_DIR" ] || [ ! -f "$VERSION_METADATA" ]; then
        echo -e "${YELLOW}No versions found${NC}"
        echo "Create your first version with: version-manager.sh save \"Initial version\""
        exit 0
    fi

    echo -e "${BLUE}=== Report Versions ===${NC}\n"

    while IFS='|' read -r version timestamp description; do
        local version_path="$VERSIONS_DIR/$version"
        if [ -d "$version_path" ]; then
            local size=$(du -sh "$version_path" | cut -f1)
            local pdf_count=$(find "$version_path" -name "*.pdf" | wc -l)

            echo -e "${GREEN}${version}${NC}"
            echo "  Created: ${timestamp}"
            echo "  Size: ${size}"
            echo "  PDFs: ${pdf_count}"
            echo "  Description: ${description}"
            echo ""
        fi
    done < "$VERSION_METADATA"
}

command_restore() {
    local version="$1"

    if [ -z "$version" ]; then
        echo -e "${RED}Error: Version not specified${NC}"
        echo "Usage: version-manager.sh restore <version>"
        echo "Example: version-manager.sh restore v1"
        exit 1
    fi

    local version_path="$VERSIONS_DIR/$version"

    if [ ! -d "$version_path" ]; then
        echo -e "${RED}Error: Version ${version} not found${NC}"
        echo "Available versions:"
        command_list
        exit 1
    fi

    # Backup current report before restoring
    if [ -d "$REPORT_DIR" ]; then
        local backup_name="report_backup_$(date +%Y%m%d_%H%M%S)"
        echo -e "${YELLOW}Backing up current report to: ${backup_name}${NC}"
        mv "$REPORT_DIR" "$PROJECT_ROOT/${backup_name}"
    fi

    # Restore version
    echo -e "${BLUE}Restoring version: ${version}${NC}"
    cp -r "$version_path" "$REPORT_DIR"

    echo -e "${GREEN}✓ Version ${version} restored successfully${NC}"
    echo -e "  Location: ${REPORT_DIR}"
}

command_diff() {
    local v1="$1"
    local v2="$2"

    if [ -z "$v1" ] || [ -z "$v2" ]; then
        echo -e "${RED}Error: Two versions required${NC}"
        echo "Usage: version-manager.sh diff <version1> <version2>"
        echo "Example: version-manager.sh diff v1 v2"
        exit 1
    fi

    local v1_path="$VERSIONS_DIR/$v1"
    local v2_path="$VERSIONS_DIR/$v2"

    if [ ! -d "$v1_path" ] || [ ! -d "$v2_path" ]; then
        echo -e "${RED}Error: One or both versions not found${NC}"
        exit 1
    fi

    echo -e "${BLUE}=== Differences between ${v1} and ${v2} ===${NC}\n"

    # Compare PDFs
    echo -e "${YELLOW}PDF files:${NC}"
    diff <(cd "$v1_path" && find . -name "*.pdf" | sort) \
         <(cd "$v2_path" && find . -name "*.pdf" | sort) || true
    echo ""

    # Compare sizes
    echo -e "${YELLOW}Directory sizes:${NC}"
    echo "  ${v1}: $(du -sh "$v1_path" | cut -f1)"
    echo "  ${v2}: $(du -sh "$v2_path" | cut -f1)"
    echo ""

    # File count comparison
    local v1_files=$(find "$v1_path" -type f | wc -l)
    local v2_files=$(find "$v2_path" -type f | wc -l)
    echo -e "${YELLOW}File counts:${NC}"
    echo "  ${v1}: ${v1_files} files"
    echo "  ${v2}: ${v2_files} files"
}

command_info() {
    local version="$1"

    if [ -z "$version" ]; then
        echo -e "${RED}Error: Version not specified${NC}"
        echo "Usage: version-manager.sh info <version>"
        exit 1
    fi

    local version_path="$VERSIONS_DIR/$version"

    if [ ! -d "$version_path" ]; then
        echo -e "${RED}Error: Version ${version} not found${NC}"
        exit 1
    fi

    # Get metadata
    local metadata=$(grep "^${version}|" "$VERSION_METADATA")
    local timestamp=$(echo "$metadata" | cut -d'|' -f2)
    local description=$(echo "$metadata" | cut -d'|' -f3)

    echo -e "${BLUE}=== Version ${version} Details ===${NC}\n"
    echo "Created: ${timestamp}"
    echo "Description: ${description}"
    echo "Size: $(du -sh "$version_path" | cut -f1)"
    echo "Location: ${version_path}"
    echo ""

    echo -e "${YELLOW}Contents:${NC}"
    echo "  PDF files: $(find "$version_path" -name "*.pdf" | wc -l)"
    echo "  TeX files: $(find "$version_path" -name "*.tex" | wc -l)"
    echo "  Figures: $(find "$version_path" -name "*.png" -o -name "*.jpg" -o -name "*.pdf" | grep -i figure | wc -l)"
    echo "  Total files: $(find "$version_path" -type f | wc -l)"
    echo ""

    echo -e "${YELLOW}Main PDF files:${NC}"
    find "$version_path" -maxdepth 1 -name "*.pdf" -exec basename {} \;
}

# Main command dispatcher
COMMAND="${1:-help}"

case "$COMMAND" in
    save)
        shift
        command_save "$@"
        ;;
    list|ls)
        command_list
        ;;
    restore)
        shift
        command_restore "$@"
        ;;
    diff)
        shift
        command_diff "$@"
        ;;
    info)
        shift
        command_info "$@"
        ;;
    help|--help|-h)
        echo "Version Manager for Research Reports"
        echo ""
        echo "Usage:"
        echo "  version-manager.sh save [description]     - Save current report as new version"
        echo "  version-manager.sh list                   - List all versions"
        echo "  version-manager.sh restore <version>      - Restore specific version"
        echo "  version-manager.sh diff <v1> <v2>         - Show differences between versions"
        echo "  version-manager.sh info <version>         - Show version details"
        echo ""
        echo "Examples:"
        echo "  version-manager.sh save \"Initial complete report\""
        echo "  version-manager.sh list"
        echo "  version-manager.sh restore v1"
        echo "  version-manager.sh diff v1 v2"
        ;;
    *)
        echo -e "${RED}Error: Unknown command: $COMMAND${NC}"
        echo "Run 'version-manager.sh help' for usage information"
        exit 1
        ;;
esac
