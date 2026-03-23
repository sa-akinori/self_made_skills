---
name: research-report-writer-orchestration
description: Complete research report generation pipeline from report.md to final PDF. Orchestrates all report generation skills (enhancer → planner → recommender → installer → writer) in sequence with user confirmations at key decision points. Use when you want to generate a complete research report automatically through the full workflow.
---

# Research Report Writer Orchestration

## Overview

This orchestration skill automates the complete research report generation workflow by coordinating five specialized skills and three subagents:

**Skills** (invoked directly by the orchestrator):

1. **research-report-enhancer** - Suggests additional investigation topics
2. **research-report-structure-planner** - Generates detailed chapter structure
3. **skill-recommender** - Recommends necessary MCP servers and Claude skills
4. **skill-mcp-installer** - Installs recommended tools
5. **research-report-writer** - Writes and compiles the final report

**Subagents** (delegated for tasks requiring independent context or specific models):

- **report-architect** (Opus) - Designs report structure from update_report.md. Used in Step 3 instead of the orchestrator running the planner skill directly, because structural design determines overall report quality and benefits from Opus-level reasoning.
- **report-writer** (Opus) - Writes the report body and handles revisions. Used in Step 6 for writing and revision cycles.
- **report-reviewer** (Sonnet) - Reviews the completed report and produces review_log.md with fix instructions. Never edits original files. Used in Step 6 for quality checking.

The orchestrator manages the workflow, handles intermediate files, asks for user confirmation at key decision points, and provides comprehensive progress tracking.

**Key features**:

- Automated workflow from report.md to final PDF
- User control at each major decision point
- Optional steps can be skipped
- Support for resuming from any step
- Comprehensive error handling
- Progress tracking and time estimates
- Final summary with all generated files

---

## Workflow

**CRITICAL REQUIREMENT**:

- **MUST use the Skill tool** to invoke component skills (research-report-enhancer, skill-recommender, skill-mcp-installer) for Steps 2, 4, 5
- **MUST use subagents** for Steps 3 and 6:
  - Step 3: Delegate to **report-architect** agent (Opus) for structure design
  - Step 6 writing: Delegate to **report-writer** agent (Opus) for report writing and revisions
  - Step 6 review: Delegate to **report-reviewer** agent (Sonnet) for quality checking
- **DO NOT** manually perform the work of these skills or agents
- **DO NOT** skip skill/agent invocation and attempt to generate outputs directly
- Each skill and agent has specialized workflows, prompts, and error handling that must be followed
- Failure to use the proper skill or agent will result in incomplete or incorrect outputs

---

### Step 0: Initial Setup and User Preferences

Before starting the pipeline, gather user preferences to minimize interruptions:

1. **Ask about workflow preferences** using AskUserQuestion:

```
Questions:
1. What language should the report be generated in?
   Options:
   - "Japanese (日本語)"
   - "English"

2. Which steps do you want to run?
   Options:
   - "Full pipeline (all steps)" (Recommended)
   - "Skip topic enhancement (start from planning)"
   - "Skip tools (no recommender/installer)"
   - "Custom (I'll choose at each step)"

3. Do you want automatic progression or manual confirmation at each step?
   Options:
   - "Automatic (only confirm at major decisions)"
   - "Manual (confirm every step)"

4. Report detail level preference:
   Options:
   - "Quick overview (detail level 2-3)"
   - "Standard report (detail level 3-4)" (Recommended)
   - "Comprehensive analysis (detail level 4-5)"
   - "I'll decide later"
```

1. **Store user preferences** for the session:
   - Language preference (Japanese or English)
   - Workflow scope (full, partial, custom)
   - Progression mode (automatic or manual)
   - Detail level preference

2. **Display the planned workflow** based on user choices
3. **Confirm to proceed**

### **CRITICAL: Language Usage Throughout Workflow**

**After Step 0 is complete**, you MUST use the language selected by the user for ALL subsequent user-facing communications:

- **If user selected "Japanese (日本語)"**:
  - ALL messages, questions, summaries, progress updates, and error messages to the user MUST be in Japanese
  - Display formats, tables, summaries MUST use Japanese
  - Tool names and technical terms can remain in English
  - Internal operations (file reads, tool calls, code) can use English

- **If user selected "English"**:
  - ALL communications remain in English

**Implementation**:

- After Step 0, immediately note the language preference
- For EVERY user-facing message in Steps 1-7, use the selected language
- When invoking skills, pass the language preference when applicable
- Progress messages, confirmations, errors: ALL in selected language

**Example**:

```
# User selected Japanese
✓ Step 2 完了: トピック拡張
→ Continuing to Step 3...  # ❌ WRONG
→ ステップ3に進みます...    # ✓ CORRECT

# User selected English
✓ Step 2 Complete: Topic Enhancement
→ ステップ3に進みます...    # ❌ WRONG
→ Continuing to Step 3...  # ✓ CORRECT
```

---

### Step 1: Pre-flight Check

**Goal**: Verify initial conditions and detect existing progress

1. **Check for report.md**:
   - If NOT found → Stop and inform user to create report.md first
   - If found → Read and display summary (topic, main points)

2. **Check for existing intermediate files**:

   ```
   Files to check:
   - update_report.md (from enhancer)
   - report_structure.md (from planner)
   - mcp-servers/install-skills.txt (from recommender)
   - report/ directory (from writer)
   ```

3. **If intermediate files exist**:
   - Display what's already been completed
   - **Ask user**: "Found existing progress. How would you like to proceed?"
     - Options:
       - "Resume from where I left off" (Recommended)
       - "Start fresh (overwrite existing files)"
       - "Skip completed steps (keep existing files)"

4. **Display pipeline plan**:

   ```
   Pipeline Plan:
   ═══════════════════════════════════════
   Step 1: ✓ Pre-flight Check
   Step 2: [TODO/SKIP/DONE] Topic Enhancement
   Step 3: [TODO/SKIP/DONE] Structure Planning
   Step 4: [TODO/SKIP/DONE] Tool Recommendation
   Step 5: [TODO/SKIP/DONE] Tool Installation
   Step 6: [TODO] Report Writing
   Step 7: [TODO] Summary
   ═══════════════════════════════════════
   Estimated total time: [X] hours
   ```

---

### Step 2: Topic Enhancement (Optional)

**Goal**: Generate additional investigation topics to enrich the report

**Skip if**:

- User chose to skip in Step 0
- update_report.md already exists and user wants to keep it

**Execute**:

1. **Inform user**: "Starting topic enhancement..."

2. **Run research-report-enhancer** using Skill tool:

   ```
   Skill tool:
   - skill: "research-report-enhancer"
   - args: none
   ```

3. **Wait for enhancer to complete**:
   - Enhancer will display numbered suggestions
   - Enhancer does NOT create any files (only provides suggestions)
   - **Note**: The enhancer can generate suggestions in the preferred language from Step 0

4. **Ask user** using AskUserQuestion:

   ```
   Question: "The enhancer has provided suggestions. What would you like to do?"
   Options:
   - "Create update_report.md with all suggestions"
   - "Let me manually create update_report.md"
   - "Skip enhancement and use original report.md"
   ```

5. **Handle user choice**:

   **If "Create update_report.md with all suggestions"**:
   - Read report.md
   - Append enhancer's suggestions to the content
   - Write to update_report.md
   - Inform user: "✓ Created update_report.md with enhanced topics"

   **If "Let me manually create update_report.md"**:
   - Display message: "Please create update_report.md manually"
   - Display message: "Press Enter when ready to continue..."
   - Wait for user confirmation
   - Check if update_report.md exists
   - If not exists → Ask again or skip

   **If "Skip enhancement"**:
   - Set flag to use report.md instead of update_report.md
   - Inform user: "⊘ Skipped enhancement, using original report.md"

6. **Mark step as complete**: ✓ Topic Enhancement

---

### Step 3: Structure Planning

**Goal**: Generate detailed chapter structure with sections and detail levels

**Agent**: Use the **report-architect** agent for this step. This agent runs on Opus and operates in its own context window, ensuring high-quality structural design without being influenced by prior conversation context.

**Skip if**:

- User chose to skip in Step 0
- report_structure.md already exists and user wants to keep it

**Execute**:

1. **Check input file**:
   - Use update_report.md if it exists
   - Otherwise use report.md
   - Display: "Using [filename] for structure planning"

2. **Inform user**: "Starting structure planning with report-architect agent (Opus)..."

3. **Delegate to report-architect agent**:
   - Pass the input file (update_report.md or report.md) to the report-architect agent
   - The agent will read the input and design the chapter structure
   - The agent will output report_structure.md

4. **Run research-report-structure-planner** using Skill tool as a fallback only if report-architect agent is unavailable:

   ```
   Skill tool:
   - skill: "research-report-structure-planner"
   - args: none
   ```

   **IMPORTANT**: When the planner asks about report type and detail level:
   - Use the detail level preference from Step 0
   - When the planner generates the structure, ensure it uses the language preference from Step 0 (Japanese or English)
   - If the planner initially generates in the wrong language, request regeneration in the correct language

5. **Wait for planner to complete**:
   - Planner will create report_structure.md in the preferred language
   - Planner will display the structure summary

6. **Read and analyze report_structure.md**:
   - Count total chapters
   - Count total sections
   - Calculate estimated pages
   - Identify key chapters

7. **Display structure summary**:

   ```
   Structure Generated:
   ═══════════════════════════════════════
   Total Chapters: [N]
   Total Sections: [M]
   Estimated Pages: [P]
   Detail Level: [average level]

   Key Chapters:
   1. [Chapter 1 name] ([X] sections, detail level [Y])
   2. [Chapter 2 name] ([X] sections, detail level [Y])
   ...
   ═══════════════════════════════════════
   File: report_structure.md
   ```

8. **Ask user** using AskUserQuestion:

   ```
   Question: "Review the generated structure. How would you like to proceed?"
   Options:
   - "Approve and continue" (Recommended)
   - "Regenerate with different parameters"
   - "Let me edit report_structure.md manually"
   ```

9. **Handle user choice**:

   **If "Approve and continue"**:
   - Inform user: "✓ Structure approved"
   - Proceed to next step

   **If "Regenerate"**:
   - Inform user: "Please delete or rename report_structure.md, then run the planner manually with desired parameters"
   - Ask: "Continue with current structure or stop pipeline?"
   - If stop → Exit gracefully

   **If "Let me edit manually"**:
   - Display: "Please edit report_structure.md manually"
   - Display: "Press Enter when ready to continue..."
   - Wait for user confirmation

10. **Mark step as complete**: ✓ Structure Planning

---

### Step 4: Tool Recommendation (Optional)

**Goal**: Recommend MCP servers and Claude skills needed for data collection

**Skip if**:

- User chose to skip tools in Step 0
- mcp-servers/install-skills.txt already exists and user wants to keep it

**Execute**:

1. **Ask user** using AskUserQuestion (if not already decided in Step 0):

   ```
   Question: "Do you need tool recommendations for data collection?"
   Options:
   - "Yes, recommend tools" (Recommended for first-time reports)
   - "No, I already have the tools I need"
   - "Skip all tool-related steps"
   ```

2. **If user chooses "No" or "Skip"**:
   - Inform user: "⊘ Skipped tool recommendation"
   - Set flag to skip Step 5 as well
   - Proceed to Step 6

3. **If user chooses "Yes"**:

   **Inform user**: "Starting tool recommendation..."

4. **Run skill-recommender** using Skill tool:

   ```
   Skill tool:
   - skill: "skill-recommender"
   - args: none
   ```

5. **Wait for recommender to complete**:
   - Recommender will read update_report.md and report_structure.md
   - Recommender will ask user for Category A and Category B counts
   - Recommender will display recommendations
   - Recommender will ask user if they want to create install-skills.txt
   - Recommender will create mcp-servers/install-skills.txt

6. **Check if install-skills.txt was created**:
   - If exists → Read and display summary
   - If not exists → Inform user recommendations were provided but file wasn't created

7. **Display recommendation summary**:

   ```
   Tool Recommendations:
   ═══════════════════════════════════════
   Category A (Data Collection): [N] tools
   Category B (Visualization): [M] tools

   File: mcp-servers/install-skills.txt
   ═══════════════════════════════════════
   ```

8. **Mark step as complete**: ✓ Tool Recommendation

---

### Step 5: Tool Installation (Optional)

**Goal**: Install recommended MCP servers and Claude skills using skill-mcp-installer

**Skip if**:

- User chose to skip tools in Step 0
- Step 4 was skipped
- mcp-servers/install-skills.txt does not exist

**CRITICAL REQUIREMENT**:

- **MUST use skill-mcp-installer** - DO NOT manually install tools with git clone, npm install, or other commands
- skill-mcp-installer automatically handles:
  - Cloning git repositories to correct locations
  - Installing npm/python packages locally
  - Running build steps (npm install, npm run build)
  - Generating .claude/mcp_config.json with correct entry points
  - Detecting entry points automatically
- Manual installation will result in:
  - Incorrect directory structure
  - Missing mcp_config.json configuration
  - Broken entry points
  - Wasted time fixing errors

**Execute**:

1. **Check for install-skills.txt**:
   - If NOT found → Inform user and skip this step
   - If found → Read and validate format
   - **Validate format**: Ensure file uses correct format (skill/mcp lines with 3 parts each)
   - If format is incorrect → Warn user and offer to fix it or regenerate with skill-recommender

2. **Display installation plan**:

   ```
   Installation Plan:
   ═══════════════════════════════════════
   Claude Skills: [N] items
   MCP Servers: [M] items
   Total: [N+M] items

   Method: skill-mcp-installer (automated)
   Estimated time: [X] minutes
   ═══════════════════════════════════════
   ```

3. **Ask user** using AskUserQuestion:

   ```
   Question: "Ready to install the recommended tools using skill-mcp-installer?"
   Options:
   - "Yes, install all tools automatically" (Recommended)
   - "No, I'll install manually later" (Not recommended - will require manual mcp_config.json setup)
   - "Let me review install-skills.txt first"
   ```

4. **Handle user choice**:

   **If "Yes"**:
   - Inform user: "Starting automated tool installation with skill-mcp-installer..."
   - **IMPORTANT: MUST run skill-mcp-installer** using Skill tool:

     ```
     Skill tool:
     - skill: "skill-mcp-installer"
     - args: none
     ```

   - **DO NOT** manually run git clone, npm install, or other installation commands
   - Wait for installer to complete
   - skill-mcp-installer will:
     - Display progress for each tool
     - Run npm install and npm run build automatically
     - Generate .claude/mcp_config.json with correct paths
     - Display installation summary
   - After completion, verify .claude/mcp_config.json was created

   **If "No"**:
   - Inform user: "⊘ Skipped automated installation."
   - **Warn user**: "Manual installation requires:"
     - Cloning repositories to correct directories (./skills/ or ./mcp-servers/)
     - Running npm install and npm run build for each MCP server
     - Manually creating .claude/mcp_config.json with correct entry points
     - This is error-prone and time-consuming
   - Inform user: "Note: report-writer may not have access to recommended data sources"
   - **Recommend**: "Consider using skill-mcp-installer instead - run it manually later"

   **If "Let me review"**:
   - Display: "Please review mcp-servers/install-skills.txt"
   - Display: "Verify the format is correct (each line: skill/mcp <name/URL> <URL/type>)"
   - Display: "Edit the file if needed, then press Enter to continue..."
   - Wait for user confirmation
   - Return to the "Ready to install?" question

5. **Verify installation** (if user chose "Yes"):
   - Check if .claude/mcp_config.json exists
   - If exists → Read and count configured servers
   - If missing → Warn that installation may have failed
   - Display number of successfully installed tools

6. **Mark step as complete**: ✓ Tool Installation

7. **MANDATORY: Prompt user to restart session before proceeding**:

   After installation completes, **STOP the pipeline** and display the following message:

   ```
   ╔═══════════════════════════════════════════════════════════════╗
   ║  ⚠️  ACTION REQUIRED: Restart Session Before Continuing       ║
   ╠═══════════════════════════════════════════════════════════════╣
   ║                                                               ║
   ║  MCP servers and skills are installed, but they are NOT       ║
   ║  available in the current session yet.                        ║
   ║                                                               ║
   ║  Please follow these steps before running the report writer:  ║
   ║                                                               ║
   ║  1. Type /exit to end this session                            ║
   ║  2. Run: claude -r                                            ║
   ║  3. Run /mcp  — verify all installed MCP servers appear       ║
   ║  4. Run /skills — verify all installed skills appear          ║
   ║  5. Once /mcp and /skills are verified, tell us you are ready  ║
   ║     and Step 6 will begin automatically.                      ║
   ║                                                               ║
   ║  ⛔ DO NOT proceed to report writing in this session.         ║
   ║     The report writer needs live access to the installed MCP  ║
   ║     servers to collect research data. Running without them    ║
   ║     will produce an incomplete report.                        ║
   ╚═══════════════════════════════════════════════════════════════╝
   ```

   - **DO NOT invoke research-report-writer** in this session
   - **DO NOT ask the user** whether they want to skip the restart
   - **STOP HERE** and wait for the user to restart and resume
   - When the user returns after restarting and confirms that /mcp and /skills
     show the expected tools, **immediately proceed to Step 6** without asking
     any further questions

---

### Step 6: Report Writing and Quality Review

**Goal**: Generate the complete research report in LaTeX and PDF format, then review and revise through a writer-reviewer feedback loop.

**Agents**:

- **report-writer** (Opus) — Writes the report body and handles revisions
- **report-reviewer** (Sonnet) — Reviews the completed report and produces review_log.md

**This step is mandatory** - cannot be skipped

**Execute**:

1. **Final verification**:
   - Check report_structure.md exists
   - If not found → Error: "Cannot proceed without report_structure.md"

2. **Inform user**: "Starting report writing with report-writer agent (Opus)..."

3. **Display writing plan**:
   - Read report_structure.md
   - Count chapters to be written
   - Estimate total time based on detail levels

   ```
   Report Writing Plan:
   ═══════════════════════════════════════
   Total Chapters: [N]
   Estimated Pages: [P]
   Estimated Time: [X] hours

   Workflow:
   1. report-writer agent writes the full report
   2. report-reviewer agent checks for issues
   3. If issues found → report-writer agent revises
   4. report-reviewer agent re-checks (max 3 loops)
   ═══════════════════════════════════════
   ```

4. **Ask user** using AskUserQuestion:

   ```
   Question: "Ready to start writing? (This may take 1-3 hours)"
   Options:
   - "Yes, write the full report" (Recommended)
   - "Write specific chapters only"
   - "Stop here, I'll run the writer manually"
   ```

5. **Handle user choice**:

   **If "Yes, write full report"**:
   - Proceed to sub-step 6a

   **If "Write specific chapters"**:
   - Inform user: "The report-writer agent will ask you which chapters to write"
   - Proceed to sub-step 6a

   **If "Stop here"**:
   - Inform user: "Pipeline stopped before writing step"
   - Skip to Step 7 (Summary) with note about incomplete pipeline
   - Exit

#### Sub-step 6a: Writing (report-writer agent)

1. **Delegate to report-writer agent**:
   - The agent runs on Opus with its own context window
   - Pass report_structure.md as input
   - The agent will:
     - Determine the version number (check existing directories under report/)
     - Conduct literature searches using available MCP servers
     - Use K-Dense skills: citation-management (references), scientific-writing (structure), literature-review (synthesis)
     - Write LaTeX content for each chapter
     - Generate figures and tables
     - Compile to PDF
   - Output: `report/vN/*.tex`, `report/vN/figures/`, `report/vN/*.pdf`
   - **IMPORTANT**: Ensure the agent generates content in the language preference from Step 0

2. **Verify writing output**:
   - Check report/vN/ directory exists
   - Check for .tex files
   - Check for .pdf file
   - If any missing → Error and offer retry

#### Sub-step 6b: Quality Review (report-reviewer agent)

1. **Delegate to report-reviewer agent**:
   - The agent runs on Sonnet with its own context window
   - Pass `report/vN/*.tex` and `report/vN/*.pdf` as input
   - The agent will:
     - Phase A: Check PDF format (rendering, figures, references)
     - Phase B: Check content quality (typos, grammar, logic, data)
     - Use K-Dense skills: peer-review (ScholarEval 8-dimension scoring), scholar-evaluation (publication readiness)
   - Output: `report/vN/review_log.md`
   - **CRITICAL**: The reviewer agent NEVER edits original .tex files

2. **Check review results**:
   - Read `report/vN/review_log.md`
   - Count issues by severity (high / medium / low)
   - Display summary to user:

     ```
     Review Results:
     ═══════════════════════════════════════
     Total issues: [N]
       High:   [X] (must fix)
       Medium: [Y] (should fix)
       Low:    [Z] (optional)
     ═══════════════════════════════════════
     ```

3. **Decide whether to revise**:
   - If **zero issues** → Proceed to step completion
   - If **issues found** → Proceed to sub-step 6c

#### Sub-step 6c: Revision Loop (report-writer ↔ report-reviewer)

**Version tracking**: Let N be the version produced in sub-step 6a (e.g., v1). Each revision cycle creates a new version: v(N+1), v(N+2), etc. The original draft is never overwritten.

1. **Delegate revision to report-writer agent**:
   - Pass `report/vN/review_log.md` to the report-writer agent (activates revision mode)
   - The agent will:
     - Copy all files from `report/vN/` to `report/v(N+1)/`
     - Apply fixes to files in `report/v(N+1)/` only (original `report/vN/` is untouched)
     - Process each issue by severity (high → medium → low)
     - Apply fixes, partial fixes, or skip with reasoning
     - Record all actions in `report/v(N+1)/revision_log.md`
     - Recompile PDF in `report/v(N+1)/`
   - Output: `report/v(N+1)/*.tex`, `report/v(N+1)/revision_log.md`, `report/v(N+1)/*.pdf`

2. **Delegate re-review to report-reviewer agent**:
   - Pass the revised files in `report/v(N+1)/` to the report-reviewer agent
   - The agent produces `report/v(N+1)/review_log.md`

3. **Check re-review results**:
   - If **zero issues** → Loop complete, proceed to step completion
   - If **issues remain AND loop count < 3** → Increment N, return to step 1 of sub-step 6c
   - If **loop count >= 3** → Stop loop, inform user:

     ```
     Maximum review iterations (3) reached.
     Remaining issues: [N] (high: [X], medium: [Y], low: [Z])
     These can be addressed manually in the .tex files.
     ```

4. **Display final revision summary**:

   ```
   Revision Summary:
   ═══════════════════════════════════════
   Review iterations: [N]
   Versions created:  v1 (draft) → v2 (revised) → v3 (if needed)
   Issues found:     [total across all iterations]
   Issues fixed:     [total fixed]
   Issues remaining: [total remaining]
   Final version:    report/vM/
   ═══════════════════════════════════════
   ```

#### Step 6 Completion

1. **Verify final output**:
   - Identify the latest version directory (report/vM/ where M is the highest version number)
   - Confirm it contains .tex and .pdf files
   - Get file sizes and page count
   - Confirm revision_log.md exists (if revisions were made)
   - Display: "Draft: report/v1/ | Final: report/vM/"

2. **Mark step as complete**: ✓ Report Writing and Quality Review

---

### Step 7: Pipeline Summary

**Goal**: Provide comprehensive summary of the entire pipeline execution

1. **Collect execution data**:
   - Total time elapsed
   - Steps completed vs skipped
   - Files generated
   - File sizes

2. **Display comprehensive summary**:

```
═══════════════════════════════════════════════════════════════
  Pipeline Execution Complete! 🎉
═══════════════════════════════════════════════════════════════

Execution Time: [X] hours [Y] minutes

Pipeline Steps:
┌─────────────────────────────────────────────┬──────────┬──────────┐
│ Step                                        │ Status   │ Duration │
├─────────────────────────────────────────────┼──────────┼──────────┤
│ 1. Pre-flight Check                         │ ✓ Done   │ 1 min    │
│ 2. Topic Enhancement                        │ ✓ Done   │ 5 min    │
│ 3. Structure Planning                       │ ✓ Done   │ 3 min    │
│ 4. Tool Recommendation                      │ ✓ Done   │ 8 min    │
│ 5. Tool Installation                        │ ✓ Done   │ 12 min   │
│ 6. Report Writing & Quality Review             │ ✓ Done   │ 95 min   │
│ 7. Summary                                  │ ✓ Done   │ 1 min    │
└─────────────────────────────────────────────┴──────────┴──────────┘

Generated Files:
┌────────────────────────────────────────────────────────────────┐
│ Intermediate Files:                                            │
│  ✓ update_report.md                    ([X] KB)                │
│  ✓ report_structure.md                 ([Y] KB)                │
│  ✓ mcp-servers/install-skills.txt      ([Z] KB)                │
│                                                                 │
│ Final Report (report/vN/):                                     │
│  ✓ report/vN/{report_name}.tex         ([A] KB)                │
│  ✓ report/vN/{report_name}.pdf         ([B] KB, [P] pages)     │
│  ✓ report/vN/figures/                  ([N] figures)           │
│  ✓ report/vN/review_log.md             (quality review)        │
│  ✓ report/vN/revision_log.md           (revision record)       │
│                                                                 │
│ Installed Tools:                                               │
│  ✓ skills/                             ([M] skills)            │
│  ✓ mcp-servers/                        ([K] MCP servers)       │
└────────────────────────────────────────────────────────────────┘

Report Statistics:
  • Total Pages: [P]
  • Total Chapters: [N]
  • Total Sections: [M]
  • References: [R]
  • Figures: [F]
  • Tables: [T]

Next Steps:
  1. Review the PDF: report/vN/{report_name}.pdf
  2. Check review and revision logs: report/vN/review_log.md, report/vN/revision_log.md
  3. Make edits if needed: report/vN/{report_name}.tex
  4. Regenerate specific chapters: use report-writer agent
  5. Share your report! 📄

═══════════════════════════════════════════════════════════════
```

1. **Ask user** using AskUserQuestion:

   ```
   Question: "Pipeline complete! What would you like to do next?"
   Options:
   - "Open the PDF (show file path)"
   - "View pipeline log details"
   - "Run quality check again"
   - "Nothing, I'm done"
   ```

2. **Handle final actions** based on user choice

3. **Save pipeline log** (optional):
   - Create `pipeline_log.txt` with full execution details
   - Include timestamps, durations, files generated
   - Save to project root

---

## Error Handling

### During Step Execution

If any skill fails or returns an error:

1. **Capture the error message**
2. **Display error clearly**:

   ```
   ❌ Error in Step [N]: [Step Name]

   Error Message:
   [Error details]

   What would you like to do?
   1. Retry this step
   2. Skip this step and continue
   3. Stop the pipeline
   ```

3. **Ask user how to proceed** using AskUserQuestion

4. **Handle user choice**:
   - **Retry**: Run the skill again
   - **Skip**: Mark step as skipped, continue to next step
   - **Stop**: Exit gracefully with summary of completed steps

### Missing Required Files

If a required file is missing at any step:

1. **Identify which step should have created it**
2. **Inform user**: "Required file [filename] is missing. It should have been created by [step name]."
3. **Offer solutions**:
   - Re-run the specific step that creates the file
   - Manually create the file
   - Stop the pipeline

### User Interruption

If user interrupts the pipeline (Ctrl+C or similar):

1. **Save current state**
2. **Display**: "Pipeline interrupted. Progress saved."
3. **Show**: Which steps were completed
4. **Inform**: "You can resume by running this skill again and choosing 'Resume from where I left off'"

---

## Important Notes

### Resumability

- **The pipeline is fully resumable**: If interrupted, run the skill again and choose "Resume from where I left off"
- **Intermediate files are preserved**: update_report.md, report_structure.md, install-skills.txt
- **Completed steps are detected**: The pipeline will skip already-completed steps

### Flexibility

- **Optional steps can be skipped**: Enhancement, recommendation, and installation are optional
- **User control at every stage**: Major decisions require user confirmation
- **Manual intervention supported**: User can manually edit files at any point

### Time Estimates

Approximate execution times (highly variable based on report complexity):

- **Step 1 (Pre-flight)**: 1 minute
- **Step 2 (Enhancement)**: 5-10 minutes
- **Step 3 (Planning)**: 3-5 minutes
- **Step 4 (Recommendation)**: 5-10 minutes
- **Step 5 (Installation)**: 5-20 minutes (depends on number of tools)
- **Step 6 (Writing + Review)**: 30 minutes - 3 hours (depends on report size, complexity, and number of review iterations)
- **Step 7 (Summary)**: 1 minute

**Total estimated time**: 1-4 hours for a complete report

### Best Practices

1. **First-time users**: Run the full pipeline with all optional steps
2. **Experienced users**: Skip enhancement and tools if already set up
3. **Multiple reports**: Keep install-skills.txt and reuse installed tools
4. **Large reports**: Consider writing chapters individually rather than all at once
5. **Review intermediate files**: Check update_report.md and report_structure.md before writing

### Limitations

- **Cannot edit mid-execution**: If you need to change parameters, let the current step complete, then interrupt
- **One report at a time**: Don't run multiple pipelines simultaneously in the same directory
- **Skill dependencies**: All five skills must be available (research-report-enhancer, research-report-structure-planner, skill-recommender, skill-mcp-installer, research-report-writer)
- **Agent dependencies**: Three subagents must be defined in `.claude/agents/`: report-architect, report-writer, report-reviewer. If any agent is missing, the orchestrator falls back to running the corresponding skill directly.

### Troubleshooting

**Problem**: "Pipeline seems stuck"

- **Solution**: Check if the current skill is waiting for user input in another window

**Problem**: "Steps are skipped unexpectedly"

- **Solution**: Intermediate files already exist. Choose "Start fresh" in Step 1 to regenerate

**Problem**: "Tools not available during writing"

- **Solution**: Make sure Step 5 (Installation) completed successfully. Check .claude/mcp_config.json

**Problem**: "LaTeX compilation failed"

- **Solution**: The report-writer has built-in quality checks. Review the error message and fix the .tex file manually if needed

---

## Usage Examples

### Example 1: First-Time Complete Pipeline

```
User: "I have report.md ready. Generate the complete research report."

Orchestrator:
1. Checks report.md ✓
2. Asks workflow preferences → User selects "Full pipeline"
3. Runs enhancer → Creates update_report.md ✓
4. Runs planner → Creates report_structure.md ✓
5. Runs recommender → Creates install-skills.txt ✓
6. Runs installer → Installs 8 tools ✓
7. Runs writer → Generates 35-page PDF ✓
8. Shows complete summary

Result: Complete report in 2 hours 15 minutes
```

### Example 2: Quick Report (Skip Optional Steps)

```
User: "I already have tools installed. Just generate the report."

Orchestrator:
1. Checks report.md ✓
2. Asks workflow preferences → User selects "Skip tools"
3. Skips enhancer (user creates update_report.md manually)
4. Runs planner → Creates report_structure.md ✓
5. Skips recommender ⊘
6. Skips installer ⊘
7. Runs writer → Generates 25-page PDF ✓
8. Shows summary

Result: Complete report in 50 minutes
```

### Example 3: Resume After Interruption

```
User: "Continue where I left off yesterday."

Orchestrator:
1. Detects existing files:
   - update_report.md ✓
   - report_structure.md ✓
   - install-skills.txt ✓
   - Tools installed ✓
2. Asks → User selects "Resume from where I left off"
3. Skips Steps 2-5 (already complete)
4. Runs writer → Generates PDF ✓
5. Shows summary

Result: Completed in 45 minutes
```

---

## Developer Notes

This orchestration skill is designed to:

- **Minimize user interruptions**: Gather preferences upfront
- **Maximize flexibility**: Every major decision has user control
- **Enable debugging**: Each step is independent and can be re-run
- **Provide transparency**: Clear progress tracking and time estimates
- **Support iteration**: Users can regenerate specific parts without re-running everything

The skill does NOT:

- Modify the underlying skills (they remain independent)
- Force a rigid workflow (all optional steps can be skipped)
- Hide errors (all errors are surfaced with clear recovery options)

This makes it suitable for both beginners (who want full automation) and experts (who want fine-grained control).
