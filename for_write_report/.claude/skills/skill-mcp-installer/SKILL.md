---
name: skill-mcp-installer
description: Batch installs Claude Code skills and MCP servers at project level from a list file (install-skills.txt). Use when the user wants to install multiple skills or MCP servers at once from a file. Triggers include requests to "install skills from a list", "batch install skills", "install MCP servers", or "install from install-skills.txt".
---

# Skill & MCP Installer

## Overview

This skill enables batch installation of Claude Code skills and MCP servers from a list file at the project level. It reads an `install-skills.txt` file containing skill names/URLs and MCP server package names, then automatically downloads and installs all listed items in the current project directory.

## Workflow

### Step 1: Check for install-skills.txt

First, check if `install-skills.txt` exists in the current working directory using the Read tool.

**If install-skills.txt does NOT exist:**
- Inform the user that install-skills.txt was not found
- Prompt them to create the file first
- Provide the expected format:

```text
# Claude Skills Format: skill <skill-name> <URL>
# MCP Servers Format: mcp <package-name> <type>
# Types: npm, git, python
# Lines starting with # are treated as comments

# Claude Skills
skill research-tools https://example.com/research-tools.skill
skill pdf-editor https://example.com/pdf-editor.skill

# MCP Servers
mcp @cyanheads/pubmed-mcp-server npm
mcp https://github.com/user/repo.git git
mcp biorxiv-mcp python
```

- STOP the workflow here and wait for the user to create the file

**If install-skills.txt exists:**
- Read the file using the Read tool
- Proceed to Step 2

### Step 2: Parse and validate the file

Parse the install-skills.txt file to extract skills and MCP servers with **strict validation**:

1. **Read each line** and identify the type (skill or mcp)
2. **Skip** empty lines and lines starting with `#` (comments)
3. **Strictly validate each entry** - reject malformed lines with clear error messages:

   **For Claude Skills** (`skill <name> <URL>`):
   - MUST have exactly 3 space-separated parts
   - First part MUST be the word "skill"
   - Second part is the skill name
   - Third part MUST be a valid HTTP/HTTPS URL
   - URL should end with `.skill` (warn if not)
   - **Error example**: Line has only 2 parts or no URL
   - **Error message**: "Line X: Malformed skill entry. Expected format: skill <name> <URL>. Found: [actual content]"

   **For MCP Servers** (`mcp <package-name-or-URL> <type>`):
   - MUST have exactly 3 space-separated parts
   - First part MUST be the word "mcp"
   - Second part is package name (npm/python) OR GitHub URL (git)
   - Third part MUST be one of: `npm`, `git`, `python`
   - **For git type**: Second part should be a valid GitHub/GitLab URL ending with .git
   - **For npm type**: Second part should be a package name (may start with @scope/)
   - **For python type**: Second part should be a package name
   - **Error example**: Line has wrong type, missing parts, or invalid format
   - **Error message**: "Line X: Malformed MCP entry. Expected format: mcp <package/URL> <type>. Type must be npm, git, or python. Found: [actual content]"

4. **Display validation results**:

   **If ALL entries are valid**:
   ```
   ✅ Format validation passed!

   Found N items to install:

   Claude Skills:
   1. skill-name: https://url.com/skill.skill

   MCP Servers:
   2. https://github.com/org/repo.git (git)
   3. @scope/package-name (npm)
   4. package-name (python)
   ```

   **If ANY entries are invalid**:
   ```
   ❌ Format validation failed!

   Errors found:
   - Line 11: Missing format. Expected: skill <name> <URL> or mcp <package/URL> <type>. Found: "some-skill-name"
   - Line 17: Invalid MCP type. Expected: npm, git, or python. Found: "mcp package-name unknown-type"

   Valid entries found: X
   Invalid entries found: Y

   Please fix the format errors in install-skills.txt before proceeding.
   Expected format examples:
     skill my-skill https://example.com/my-skill.skill
     mcp https://github.com/org/repo.git git
     mcp @scope/package npm
     mcp package-name python
   ```

5. **Handle validation failures**:
   - If validation fails, **STOP the workflow immediately**
   - Display clear error messages for each malformed line
   - Show correct format examples
   - Ask user to fix install-skills.txt and run the skill again
   - **DO NOT proceed with partial installation**

6. **If validation succeeds**, proceed to Step 3

### Step 3: Confirm installation plan

Display the installation plan and ask for confirmation:

1. **Show summary**:
   - Total number of items to be installed
   - Number of Claude skills
   - Number of MCP servers (broken down by type: npm, git, python)

2. **Inform about Step 3.5**:
   ```
   次のステップ（Step 3.5）では、すべてのMCPサーバーについて公式READMEを確認し、
   正しいインストール方法を検証します。これには数分かかる場合があります。
   ```

3. **Ask for confirmation**:
   - "インストールを続行しますか？（Step 3.5で公式READMEの確認を行います）"
   - Provide yes/no options

**If user confirms:** Proceed to Step 3.5 (MANDATORY README VERIFICATION)
**If user declines:** Stop the workflow

**IMPORTANT:** Do NOT skip Step 3.5 under any circumstances. It is mandatory for all installations.

---

### Step 3.5: Verify Official Installation Methods (CRITICAL - MANDATORY FOR ALL SERVERS)

**THIS STEP IS MANDATORY AND MUST BE COMPLETED FOR EVERY SINGLE MCP SERVER BEFORE PROCEEDING TO STEP 4.**

**BLOCKING REQUIREMENT:** You MUST verify the official installation method for **ALL** MCP servers listed in install-skills.txt. Do NOT skip any server. Do NOT proceed to Step 4 until this verification is complete for every single server.

#### Why This Step is Critical

Many MCP servers have specific installation requirements that differ from simple git clone:
- Some should be installed via **package managers** (pip, npm, uvx, npx)
- Some require **specific build steps** or dependencies
- Some need **environment variables** or **API keys**
- Entry points may vary (dist/, build/, src/, or package commands)

Skipping this step will result in **non-functional MCP servers**.

#### Mandatory Verification Process (For EVERY MCP Server):

**FOR EACH AND EVERY MCP SERVER in install-skills.txt, you MUST:**

1. **Identify the server and its source**:
   - For git URLs: Extract the repository URL
   - For package names: Identify the package name and type (npm/python)

2. **Locate and read the official README.md**:
   - **For git URLs**: Use WebFetch or Bash (with curl/gh api) to read the GitHub README
     ```bash
     # Example for GitHub:
     gh api repos/OWNER/REPO/readme --jq '.content' | base64 -d
     # Or use WebFetch with raw.githubusercontent.com
     ```
   - **For npm packages**: Search for the package on npmjs.com or use `npm view <package> --readme`
   - **For python packages**: Search for the package on PyPI or use `pip show <package>`
   - **If README is not found**: Mark as "README NOT FOUND" and attempt to find documentation elsewhere (GitHub search, official website)

3. **Extract the official installation method from README**:

   **Check for package manager installation (PRIORITY):**
   ```bash
   # Look for these patterns in README:
   pip install package-name          # → Python package (use python/pip)
   npm install package-name          # → npm package (use npm/npx)
   uvx package-name                  # → Python with uv (use uvx)
   npx package-name                  # → npm executable (use npx)
   ```

   **Check for git clone + build:**
   ```bash
   # Look for these patterns:
   git clone <url>
   npm install && npm run build      # → Git clone + Node.js build
   pip install -e .                  # → Git clone + Python editable install
   ```

4. **Document the configuration format**:
   - **command**: What command to use (node, python3, uvx, npx, etc.)
   - **args**: What arguments are needed
   - **env**: Required environment variables (API keys, email, etc.)
   - **Entry point**: Exact path or module name (build/index.js, dist/index.js, src/index.ts, module name)

5. **Create a verification table** (MANDATORY OUTPUT):

   For EVERY server, create a table entry with:
   ```
   | Server Name | Type in install-skills.txt | Official Installation Method | Entry Point | Requires Env Vars? | Status |
   |-------------|---------------------------|------------------------------|-------------|-------------------|--------|
   | pubmed      | npm @ncukondo/pubmed-mcp  | npx -y @ncukondo/pubmed-mcp  | (package)   | No                | ✅ Correct |
   | paper-search| git https://...           | pip install paper-search-mcp | python -m   | Yes (NCBI_EMAIL)  | ❌ Wrong type in txt |
   | arxiv       | python arxiv-mcp-server   | pip install OR python -m     | python -m   | No                | ✅ Correct |
   ```

6. **Identify discrepancies**:
   - Compare install-skills.txt format with official installation method
   - Flag any mismatches (wrong type, wrong package name, missing dependencies)

7. **Generate corrected install-skills.txt** (if needed):
   - If ANY discrepancies found, generate a corrected version
   - Show side-by-side comparison:
     ```
     ❌ CURRENT (install-skills.txt):
     mcp https://github.com/openags/paper-search-mcp.git git

     ✅ CORRECT (from official README):
     mcp paper-search-mcp python
     ```

#### Example Official Installations:

**Example 1: @ncukondo/pubmed-mcp (npm package)**
```
Official README shows:
  npm install -g @ncukondo/pubmed-mcp
  # OR in .mcp.json:
  "command": "npx",
  "args": ["-y", "@ncukondo/pubmed-mcp"]

install-skills.txt format:
  mcp @ncukondo/pubmed-mcp npm       ✅ CORRECT

.mcp.json configuration:
  "pubmed": {
    "command": "npx",
    "args": ["-y", "@ncukondo/pubmed-mcp"]
  }
```

**Example 2: paper-search-mcp (Python package, NOT git clone)**
```
Official README shows:
  pip install paper-search-mcp
  # OR
  uvx paper-search-mcp

install-skills.txt format:
  mcp https://github.com/openags/paper-search-mcp.git git  ❌ WRONG
  mcp paper-search-mcp python                              ✅ CORRECT

.mcp.json configuration:
  "paper-search": {
    "command": "uvx",
    "args": ["paper-search-mcp"],
    "env": {"NCBI_EMAIL": "user@example.com"}
  }
```

**Example 3: arxiv-mcp-server (Python module)**
```
Official README shows:
  pip install arxiv-mcp-server
  python -m arxiv_mcp_server

install-skills.txt format:
  mcp arxiv-mcp-server python        ✅ CORRECT

.mcp.json configuration:
  "arxiv": {
    "command": "python3",
    "args": ["-m", "arxiv_mcp_server"]
  }
```

**Example 4: PDB MCP Server (git + npm build)**
```
Official README shows:
  git clone <url>
  npm install
  npm run build

install-skills.txt format:
  mcp https://github.com/.../PDB-MCP-Server.git git  ✅ CORRECT

.mcp.json configuration:
  "pdb": {
    "command": "node",
    "args": ["/full/path/to/build/index.js"]
  }
```

#### Mandatory Output Before Proceeding:

**YOU MUST DISPLAY THE FOLLOWING BEFORE GOING TO STEP 4:**

1. **Verification Summary Table** (ALL servers):
   - Show verification status for every single server
   - Mark ✅ correct or ❌ needs correction

2. **Discrepancy Report** (if any found):
   - List all servers with incorrect formats
   - Show side-by-side comparison (current vs correct)

3. **Corrected install-skills.txt** (if needed):
   - Generate the complete corrected file content
   - Ask user for confirmation to update the file

4. **Configuration Notes**:
   - List any required environment variables
   - Note any special requirements (API keys, etc.)

#### Update install-skills.txt if Corrections Needed

**MANDATORY: If ANY discrepancies are found:**

1. **STOP the workflow immediately**
2. **Display the verification table** showing all issues
3. **Generate corrected install-skills.txt** with proper formats
4. **ASK USER**: "install-skills.txtに誤りが見つかりました。修正したファイルで上書きしますか？"
5. **WAIT for user confirmation** (yes/no)
6. **If yes**: Update install-skills.txt with corrected content
7. **If no**: Ask user to manually fix the file and re-run the skill

**DO NOT PROCEED TO STEP 4 WITHOUT COMPLETING THIS VERIFICATION FOR ALL SERVERS.**

#### Proceed to Step 4

**CHECKPOINT:** Before proceeding to Step 4, verify:
- ✅ README verified for ALL servers (16/16 in current install-skills.txt)
- ✅ Official installation methods documented for ALL
- ✅ Verification table completed and displayed
- ✅ install-skills.txt corrected if needed
- ✅ User confirmed or no corrections needed

**Only after ALL checkpoints are complete, proceed to Step 4.**

---

### Step 4: Install skills and MCP servers

**IMPORTANT: Verify Installation Methods Before Executing**

Before running batch installation, verify that install-skills.txt contains the corrected formats from Step 3.5.

#### Installation Methods by Type:

**For Claude Skills:**
```bash
# Download .skill file and extract to .claude/skills/
curl -o ./skills/skill-name.skill <URL>
# (Automatic extraction handled by Claude Code)
```

**For npm packages:**
```bash
# Install via npx (no local installation needed for npx execution)
# Configuration will use: "command": "npx", "args": ["-y", "package-name"]
# OR install locally if needed:
mkdir -p ./mcp-servers/npm-packages
cd ./mcp-servers/npm-packages
npm install <package-name>
```

**For git repositories (Node.js):**
```bash
# Clone and build
mkdir -p ./mcp-servers
cd ./mcp-servers
git clone <repo-url> <repo-name>
cd <repo-name>
npm install
npm run build  # If build script exists in package.json
```

**For Python packages:**
```bash
# Install via pip
pip install <package-name>
# Configuration will use: "command": "python3", "args": ["-m", "module_name"]
# OR install with uvx (recommended for isolated execution):
# uvx <package-name>
```

#### Recommended Installation Process:

**Option A: Use batch_install.py script (if available)**

Check if the script exists:
```bash
ls -la scripts/batch_install.py
```

If exists, run:
```bash
python3 scripts/batch_install.py install-skills.txt
```

The script will:
1. Read and parse the install-skills.txt file
2. For each Claude skill:
   - Download the .skill file from the URL using curl
   - Extract the skill to the project's skills directory
3. For each MCP server:
   - **npm type**: Install locally or note for npx usage
   - **git type**: Clone repository to `./mcp-servers/<repo-name>` and run `npm install && npm run build`
   - **python type**: Install using `pip install <package-name>`
4. Report progress for each item
5. Display a summary at the end

**Option B: Manual installation (if script not available or fails)**

For EACH MCP server in install-skills.txt, execute the appropriate installation commands based on type:

1. **npm packages**: Install with npm or note for npx usage
2. **git repositories**: Clone, npm install, npm run build
3. **Python packages**: pip install or note for uvx usage

**All installations are local to the current project directory:**
- Claude skills: `.claude/skills/`
- MCP servers (npm/git): `./mcp-servers/`
- MCP servers (python): System-wide pip OR uvx (isolated)

**Monitor the output** and report any errors to the user.

#### Post-Installation Verification:

After installation completes, verify:

1. **For git-cloned servers**:
   ```bash
   # Check if entry point exists
   ls -la ./mcp-servers/repo-name/build/index.js
   # Or check dist/ or src/ based on Step 3.5 verification
   ```

2. **For npm packages**:
   ```bash
   # Verify package is accessible
   npx -y package-name --version  # If it supports --version
   ```

3. **For Python packages**:
   ```bash
   # Verify module is importable
   python3 -m module_name --help  # If it supports --help
   # OR
   pip show package-name
   ```

**If any verification fails**, note the server name and report to user in Step 5.

### Step 5: Report results and create MCP configuration

After installation completes:

1. **Display a summary:**
   - Number of Claude skills successfully installed
   - Number of MCP servers successfully installed
   - Number of failed installations (if any)
   - List of successfully installed items

2. **Handle failures** (if any):
   - List which items failed to install
   - Suggest possible reasons (invalid URL, network issues, missing dependencies, etc.)
   - Offer to retry failed installations individually

3. **Create project-level MCP configuration (.mcp.json):**

   **CRITICAL: Use Information from Step 3.5 Verification**

   For EACH MCP server, you MUST:
   - **USE the configuration details collected in Step 3.5** (command, args, entry point, env vars)
   - Do NOT re-read READMEs - use the verification table data from Step 3.5
   - Do NOT guess or auto-detect entry points - use what was documented in Step 3.5

   **Configuration Generation Process:**

   1. **For each successfully installed MCP server**:
      - Retrieve the configuration details from Step 3.5 verification table
      - Generate the appropriate .mcp.json entry

   2. **Configuration Patterns (based on Step 3.5 data):**

      **npm packages (npx execution):**
      ```json
      {
        "server-name": {
          "command": "npx",
          "args": ["-y", "package-name"]
        }
      }
      ```

      **Python packages (pip installed, uvx execution):**
      ```json
      {
        "server-name": {
          "command": "uvx",
          "args": ["package-name"],
          "env": {
            "ENV_VAR": "value-if-required"
          }
        }
      }
      ```

      **Python modules (python -m execution):**
      ```json
      {
        "server-name": {
          "command": "python3",
          "args": ["-m", "module_name"]
        }
      }
      ```

      **Git-cloned Node.js servers (node execution):**
      ```json
      {
        "server-name": {
          "command": "node",
          "args": ["/absolute/path/to/mcp-servers/repo-name/build/index.js"]
        }
      }
      ```

      **Git-cloned TypeScript servers (tsx/bun execution):**
      ```json
      {
        "server-name": {
          "command": "npx",
          "args": ["-y", "tsx", "/absolute/path/to/mcp-servers/repo-name/src/index.ts"]
        }
      }
      ```

   3. **Generate complete .mcp.json**:
      - Use absolute paths for all git-cloned servers
      - Include all successfully installed MCP servers
      - Include required environment variables from Step 3.5 verification
      - Format with proper JSON indentation (2 spaces)

   4. **Display the generated .mcp.json** before writing:
      - Show the complete file content
      - Ask user for confirmation: "この設定で.mcp.jsonを作成しますか？"

   5. **Write .mcp.json** to project root after confirmation

4. **Success message:**
   - Confirm MCP configuration file creation (`.mcp.json` in project root)
   - Inform user that MCP servers are now configured at project level
   - **IMPORTANT**: Instruct user to restart the session to load new tools:
     - Use `/exit` command to exit the current session
     - Then run `claude -r` to resume the session with tools loaded
     - After restart, verify with `/mcp` (MCP servers) and `/skills` (Claude skills)
     - Alternative: Exit and restart Claude Code manually

## Using the Scripts

### scripts/install_from_url.py

Installs a single skill from a URL.

**Usage:**
```bash
python3 scripts/install_from_url.py <url> [--skill-name <name>]
```

**Example:**
```bash
python3 scripts/install_from_url.py https://example.com/my-skill.skill --skill-name my-skill
```

### scripts/batch_install.py

Batch installs multiple skills from a list file.

**Usage:**
```bash
python3 scripts/batch_install.py [file_path]
```

**Default:** Uses `install-skills.txt` if no file path is provided.

**Example:**
```bash
python3 scripts/batch_install.py install-skills.txt
```

## Important Notes

- The skill assumes `curl` is available for downloading files
- For MCP servers: `npm`, `git`, `pip` must be available depending on the type
- Network connectivity is required to download skills and MCP servers
- Invalid URLs or network issues will cause individual installations to fail
- The original install-skills.txt file is never modified
- Failed installations can be retried individually
- **All installations are local to the project directory** (not global)
- **MCP configuration is automatically created** in `.mcp.json` at project root
- Claude skills are extracted to `.claude/skills/` directory
- MCP servers (npm/git) are installed to `./mcp-servers/` directory
- MCP servers (python) are installed to `./mcp-servers/python-packages/` directory
- **No sudo required** - all installations are at project level

### Using Installed Tools After Installation

**CRITICAL**: After MCP servers and Claude skills are installed, you MUST restart the session to load them:

1. **Exit the current session**: Use `/exit` command
2. **Resume with tools loaded**: Run `claude -r` (or `claude --resume`)
3. **Verify tools are loaded**:
   - Use `/mcp` command to list available MCP servers
   - Use `/skills` command to list available Claude skills

**Why this is necessary**: Claude Code loads MCP server configurations (`.mcp.json`) and skills only at session startup. The tools will not be available until you restart the session.

## Error Handling

Common errors and solutions:

1. **File not found:** Ensure install-skills.txt exists in the current directory
2. **Malformed lines:** Check format: `skill <name> <URL>` or `mcp <package> <type>`
3. **Download failures:** Verify URLs are accessible and correct
4. **Installation failures (MCP):** Ensure npm/git/pip is installed and accessible
5. **Permission errors:** Usually not needed for project-level installs, check directory write permissions
6. **Tools not working / `/mcp` shows "No MCP servers configured" or `/skills` doesn't show new skills:**
   - Check that `.mcp.json` was created in project root
   - Check that skills were installed to `.claude/skills/` directory
   - **Most common issue**: You need to restart the session!
     - Use `/exit` to exit
     - Run `claude -r` to resume with tools loaded
   - Verify with `/mcp` (MCP servers) and `/skills` (Claude skills) after restart
7. **Node modules missing:** Run `npm install` in the MCP server directory if needed
