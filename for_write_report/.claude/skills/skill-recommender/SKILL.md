---
name: skill-recommender
description: Analyzes update_report.md and report_structure.md to recommend relevant MCP servers and Claude skills. Recommends two categories - data collection tools (domain-specific databases, APIs, search tools) and report enhancement tools (visualization, analysis, formatting). Use when the user wants tool or skill recommendations based on their research report. Triggers include requests to "recommend skills", "suggest tools for my research", "what MCP servers should I use", or "find useful skills for this research".
---

# Skill Recommender

## Overview

This skill analyzes the content of update_report.md and report_structure.md to recommend relevant MCP servers and Claude skills that would support the research workflow. It categorizes recommendations into:
- **Category A (Data Collection)**: Tools for gathering research data (academic databases, APIs, search tools, data repositories)
- **Category B (Report Enhancement)**: Tools for visualization and report quality (plotting libraries, diagram tools, analysis frameworks)

It uses web search to find appropriate tools and presents numbered recommendations to the user.

## Workflow

Follow these steps in order:

### Step 1: Check for input files

Check for both `update_report.md` and `report_structure.md` in the current working directory using the Read tool.

**Priority order:**
1. If **both files exist**: Read both files (recommended for best recommendations)
2. If only **report_structure.md exists**: Read it and proceed (can identify specific data/visualization needs)
3. If only **update_report.md exists**: Read it and proceed (can identify general research domain)
4. If **neither file exists**:
   - Inform the user that neither file was found
   - Suggest using research-report-enhancer and research-report-structure-planner first
   - STOP the workflow here

**Read the available file(s) using the Read tool and proceed to Step 2.**

### Step 2: Ask user about recommendation preferences

Use the AskUserQuestion tool to ask the user about preferences for each category:

**Question 1: Category A - Data Collection Tools**
How many data collection tools (academic databases, APIs, search engines, data repositories, etc.) do you need?
- Options:
  - 2-3 recommendations
  - 4-5 recommendations
  - 6-8 recommendations
  - 10+ recommendations

**Question 2: Category B - Report Enhancement Tools**
How many report enhancement tools (plotly, matplotlib, data visualization, diagram generation, etc.) do you need?
- Options:
  - 2-3 recommendations
  - 4-5 recommendations
  - 6-8 recommendations
  - 10+ recommendations
  - None (I only need data collection tools)

**Question 3: Tool Type Preference**
What type of tools should be recommended?
- Options:
  - Both MCP servers and Claude skills (recommended)
  - Claude skills only
  - MCP servers only

### Step 3: Analyze input files content

Based on the available file(s), identify different aspects:

**From update_report.md (if available):**
1. **Research domain** (e.g., machine learning, financial analysis, social sciences, engineering, linguistics, environmental science)
2. **Research topics and questions** (identify key themes, methodologies, research questions)
3. **General data needs** (e.g., academic papers, datasets, APIs, public records, survey data)

**From report_structure.md (if available):**
1. **Specific figure types needed** (e.g., "comparison chart", "workflow diagram", "statistical plot", "network graph")
2. **Table types and formats** (e.g., data tables, comparison matrices, summary tables)
3. **Analysis requirements** (e.g., statistical analysis, time-series analysis, correlation studies, predictive modeling)
4. **Data sources mentioned** (identify any specific databases, APIs, or data sources referenced)

**Categorize needs into:**
- **Category A (Data Collection)**: Academic databases, domain-specific APIs, data repositories, search tools
- **Category B (Report Enhancement)**: Visualization libraries, diagram tools, statistical analysis, data processing frameworks

### Step 4: Search for relevant tools by category

Use WebSearch to find tools for each category based on user's requested counts:

**Category A - Data Collection Tools:**

Based on the research domain identified in Step 3, search for relevant data sources:

1. **Identify the research domain** from the input files:
   - Extract key domain indicators from the content (e.g., terminology, methodologies, cited sources)
   - Examples of diverse domains: machine learning, financial markets, linguistics, environmental science, education, engineering, sociology, etc.

2. **Search for domain-specific data sources:**
   - General academic: "academic database MCP server 2026", "research paper MCP", "scholarly search MCP"
   - Domain-specific: "[identified domain] database MCP server", "[identified domain] data source MCP"
   - Examples of search queries based on diverse domains:
     - Machine learning research → search "[ML topic] dataset MCP", "benchmark data MCP", "model repository MCP"
     - Financial research → search "financial data MCP", "market data API MCP", "economic indicators MCP"
     - Social science → search "survey data MCP", "census data MCP", "public records MCP"
     - Linguistics → search "corpus MCP", "language data MCP", "linguistic database MCP"
     - Environmental → search "climate data MCP", "environmental monitoring MCP", "geospatial data MCP"

3. **Search for general research tools:**
   - Literature search: "literature search MCP", "academic search skill"
   - Data repositories: "data repository MCP", "open data MCP"
   - Specialized databases: Based on keywords found in files

4. **Let WebSearch discover relevant tools:**
   - Use queries like: "[identified domain] MCP server 2026"
   - Use queries like: "[data type mentioned in files] database MCP"
   - Don't assume specific databases - let search results guide recommendations

**Category B - Report Enhancement Tools:**

Based on the visualization and analysis needs identified in Step 3:

1. **Identify needed visualization types** from report_structure.md (if available):
   - Look for figure descriptions (e.g., "comparison chart", "workflow diagram", "statistical plot")

2. **Search for appropriate visualization tools:**
   - General visualization: "data visualization MCP server 2026", "chart generation skill"
   - Specific types: "[figure type] generation MCP", "[chart type] tool skill"
   - Examples based on identified needs:
     - Workflow diagrams → search "diagram MCP", "flowchart generation skill"
     - Statistical plots → search "plotting MCP", "statistical visualization skill"
     - Interactive charts → search "interactive visualization MCP"

3. **Search for analysis tools:**
   - Statistical analysis: "statistical analysis MCP", "data analysis skill"
   - Data processing: "data processing MCP", "data transformation skill"

4. **Search for report formatting tools:**
   - Document generation: "document generation MCP", "report formatting skill"
   - Table tools: "table generation MCP", "data table skill"

**General approach:**
- **Never assume specific tools** - always search based on identified domain and needs
- Use search queries like: "[identified need] MCP server 2026" or "Claude Code [identified need] skill"
- Look for actively maintained tools with good documentation
- Prioritize tools that match the specific needs identified in Step 3
- Let the research domain and requirements guide the search, not pre-defined categories

### Step 5: Generate categorized recommendations

Create a numbered list of recommendations organized by category:

```
========================================
Recommended Tools for Your Research
========================================

CATEGORY A: DATA COLLECTION TOOLS
------------------------------------------

Claude Skills:
1. [Skill Name]
   Description: [What it does]
   Why useful: [How it helps collect/access research data]
   URL: [Installation URL or search guidance]

MCP Servers:
2. [MCP Server Name]
   Description: [What data it provides]
   Why useful: [How it relates to the research data needs]
   Installation: [npm/git/python and package details]

[Continue for Category A based on user's requested count...]

CATEGORY B: REPORT ENHANCEMENT TOOLS
------------------------------------------

Claude Skills:
[N]. [Skill Name]
   Description: [What visualization/analysis it provides]
   Why useful: [How it improves report quality - reference specific figures from report_structure.md]
   URL: [Installation URL or search guidance]

MCP Servers:
[N+1]. [MCP Server Name]
   Description: [What visualization/processing capability]
   Why useful: [How it addresses specific report needs]
   Installation: [npm/git/python and package details]

[Continue for Category B based on user's requested count...]
```

**Important formatting:**
- Clearly separate Category A and Category B
- Within each category, separate Claude skills and MCP servers
- Number all items sequentially starting from 1
- For Category B, explicitly reference figure types from report_structure.md when applicable
- Include URLs or installation instructions when available
- If URLs aren't found, provide clear search guidance

### Step 6: Present recommendations and ask for user input

1. Display all recommendations clearly to the user
2. Ask the user which items they would like to include in an install-skills.txt file
3. Accept responses in various formats:
   - "1, 3, 5" (comma-separated numbers)
   - "1-5" (range)
   - "all"
   - "none"
   - Or the user might decline creating the file

### Step 7: Create mcp-servers/install-skills.txt (if requested)

If the user wants to create install-skills.txt:

**CRITICAL: This file MUST follow the exact format expected by skill-mcp-installer. Any deviation will cause installation failures.**

1. **Create mcp-servers directory** if it doesn't exist using Bash: `mkdir -p mcp-servers`
2. **Parse the user's selection** to identify which numbered items were chosen
3. **Classify each selected item correctly:**

   **For Claude Skills (downloadable .skill files):**
   - Format: `skill <skill-name> <direct-download-URL>`
   - Example: `skill my-skill https://example.com/my-skill.skill`
   - **Only use this format if the URL points to a downloadable .skill file (ZIP format)**

   **For Git Repositories (including skill collections and MCP servers):**
   - Format: `mcp <github-URL> git`
   - Example: `mcp https://github.com/org/repo-name.git git`
   - **Use this format for:**
     - GitHub/GitLab repositories containing skills (even if called "claude skills")
     - GitHub repositories containing MCP servers
     - Any git-cloneable repository
   - **IMPORTANT:** GitHub repositories are NOT .skill files - they must use the `mcp` format with `git` type

   **For npm Packages (MCP servers only):**
   - Format: `mcp <package-name> npm`
   - Example: `mcp @scope/package-name npm`
   - Use for npm-published MCP servers

   **For Python Packages (MCP servers only):**
   - Format: `mcp <package-name> python`
   - Example: `mcp package-name python`
   - Use for pip/uvx-installable MCP servers

4. **Create mcp-servers/install-skills.txt** with this EXACT format:

```text
# Recommended Tools for [Research Topic]
# Generated by skill-recommender on [date]
# Format: skill <name> <URL> OR mcp <package/URL> <type>

# ========================================
# Claude Skills (.skill files only)
# ========================================
skill <skill-name> <https://direct-download-url/file.skill>

# ========================================
# MCP Servers and Skill Repositories
# ========================================

# Git Repositories (any GitHub/GitLab repos)
mcp <https://github.com/org/repo-name.git> git

# npm Packages
mcp <@scope/package-name> npm
mcp <package-name> npm

# Python Packages
mcp <package-name> python
```

5. **Validation checklist - VERIFY BEFORE WRITING:**
   - ✓ Each line has exactly 3 space-separated parts (type, name/URL, URL/type)
   - ✓ GitHub URLs use `mcp <URL> git` format (NOT `skill` format)
   - ✓ Only .skill download URLs use `skill <name> <URL>` format
   - ✓ npm packages use `mcp <package> npm` format
   - ✓ Python packages use `mcp <package> python` format
   - ✓ No lines with just skill/package names without URLs/types
   - ✓ Comments start with `#` and are ignored by the parser

6. **Common mistakes to AVOID:**
   - ❌ DON'T write: `some-skill-name` (missing format entirely)
   - ❌ DON'T write: `skill repo-name https://github.com/org/repo.git` (GitHub repos are not .skill files)
   - ✓ DO write: `mcp https://github.com/org/repo-name.git git`

   - ❌ DON'T write: `skill some-tool` (missing URL and format)
   - ✓ DO write: `mcp https://github.com/org/some-tool.git git` (for repos)
   - ✓ DO write: `skill some-tool https://example.com/some-tool.skill` (for .skill files)

7. **After creating the file:**
   - Use Write tool to create `mcp-servers/install-skills.txt`
   - **Inform the user** that:
     - mcp-servers/install-skills.txt has been created with the CORRECT format for skill-mcp-installer
     - They should use skill-mcp-installer skill to batch install all items (DO NOT manually install)
     - skill-mcp-installer will automatically:
       - Clone git repositories to appropriate directories
       - Install npm packages locally
       - Install Python packages locally
       - Generate .claude/mcp_config.json with correct entry points
     - All installations will be local to the project directory (./skills/ and ./mcp-servers/)

**IMPORTANT:** Always double-check the format before writing. The skill-mcp-installer expects this exact format and will fail with cryptic errors if the format is incorrect.

## Important Notes

- **Always check for both files**: Read both update_report.md and report_structure.md when available for best recommendations
- **Never assume file contents**: Always use Read tool to check file contents
- **Category A (Data Collection)**: Focus on tools that provide access to research data sources
- **Category B (Report Enhancement)**: Focus on visualization, analysis, and report quality tools
- When report_structure.md is available, reference specific figure types (e.g., "戦略マップ", "比較チャート") in recommendations
- Use WebSearch to find current, relevant tools (search results should be from 2026 or recent)
- Prioritize tools that directly address the research needs identified in the files
- For MCP servers, provide clear installation/configuration instructions
- **Both Claude skills and MCP servers can be included in install-skills.txt** using the updated format
- MCP server installation types: npm (for npm packages), git (for GitHub repos), python (for pip/uvx packages)
- If exact URLs aren't available, provide search guidance or GitHub repository names
- Consider both general-purpose and domain-specific tools
- Verify that recommended tools are actively maintained and well-documented
- Remind users that MCP servers require additional configuration in Claude Desktop config after installation
- Keep Category A and Category B recommendations independent - users may want different quantities for each
