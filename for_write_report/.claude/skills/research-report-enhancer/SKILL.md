---
name: research-report-enhancer
description: Analyzes research reports (report.md) and suggests additional investigation topics in a numbered format. Creates update_report.md with enhanced topic list. Use when the user wants to enhance their research report with additional investigation items. Triggers include requests to "suggest additional topics", "improve my research report", "what else should I investigate", or "enhance my research scope". For tool/skill recommendations, use skill-recommender instead.
---

# Research Report Enhancer

## Overview

This skill helps enhance research reports by analyzing the current content and suggesting additional investigation topics. It reads an existing report.md file, proposes numbered suggestions for further research in two groups (direct responses to original items + enhancement topics), receives user selection, and generates an updated report (update_report.md) with the selected items appended.

**Single Responsibility**: This skill focuses ONLY on topic enhancement. For tool and skill recommendations, use **skill-recommender** instead.

## Workflow

Follow these steps in order:

### Step 1: Check for report.md

First, check if `report.md` exists in the current working directory.

**If report.md does NOT exist:**
- Inform the user that report.md was not found
- Prompt them to create report.md first
- Provide guidance on the format, suggesting they structure it similar to the example below:

```markdown
# Research Report: [Topic Name]

## Overview
[Brief description of the research topic]

## Current Findings
### [Subtopic 1]
[Details...]

### [Subtopic 2]
[Details...]

## Next Steps
[Planned investigations]
```

- STOP the workflow here and wait for the user to create the file

**If report.md exists:**
- Read the file using the Read tool
- Proceed to Step 2

### Step 2: Identify original investigation items

**Parse the original investigation items from report.md:**

1. Identify all investigation items, research questions, or topics listed in report.md
2. Extract them as a numbered list (these are the "original items" the user wants to investigate)
3. Count how many original items exist (let's call this N)
4. Display the original items to the user for confirmation

Example output:
```
Found N original investigation items in report.md:
1. [Original item 1]
2. [Original item 2]
...
N. [Original item N]
```

**If no clear investigation items are found:**
- Treat the entire report.md as a general research topic
- Set N = 0 (no specific original items)
- Proceed to generate only enhancement suggestions

### Step 3: Ask user about suggestion count

Use the AskUserQuestion tool to ask the user how many suggestions they would like:

- Question: "How many additional research topics would you like me to suggest (beyond the N topics that directly address your original items)?"
- Provide options: 3-5, 5-10, or 10+ suggestions
- Include an option for the user to specify a custom number
- Clarify that you will generate TWO groups:
  - **Group 1**: N topics directly addressing the N original items
  - **Group 2**: Additional enhancement topics (user-specified count)

### Step 4: Analyze content and generate two groups of numbered suggestions

**Group 1: Direct responses to original investigation items (numbered 1 to N)**

For each of the N original items identified in Step 2:
1. Generate a topic that directly addresses that specific item
2. Ensure 1:1 correspondence between original items and suggested topics
3. Number these suggestions 1 through N

**Group 2: Additional enhancement topics (numbered N+1 onwards)**

Based on the report.md content and Group 1 topics:
1. Identify gaps not covered by the original items
2. Consider related topics not yet covered
3. Suggest deeper investigations, foundational knowledge, or advanced techniques
4. Propose comparative or alternative approaches
5. Include emerging technologies, clinical/regulatory aspects, market analysis, etc.

Generate suggestions in the following format:

```
## Suggested Additional Investigation Topics:

### Part 1: Direct Responses to Your Original Items (1-N)

**1. [Response to original item 1]**
[Detailed description explaining how this addresses original item 1]
→ Addresses: [Original item 1]

**2. [Response to original item 2]**
[Detailed description explaining how this addresses original item 2]
→ Addresses: [Original item 2]

...

**N. [Response to original item N]**
[Detailed description]
→ Addresses: [Original item N]

---

### Part 2: Additional Enhancement Topics (N+1 onwards)

**N+1. [Enhancement topic title]**
[Detailed description explaining why this topic would be valuable]
→ Category: [e.g., "Foundational knowledge", "Advanced techniques", "Clinical applications", "Regulatory/Market"]

**N+2. [Enhancement topic title]**
[Detailed description]
→ Category: [...]

...
```

**Present both groups clearly** with:
- Clear separation between Part 1 (direct responses) and Part 2 (enhancements)
- Explicit mapping showing which topics address which original items
- Categories or tags for enhancement topics

**Display a coverage matrix:**
```
Coverage Check:
✓ Original item 1 → Topic #1
✓ Original item 2 → Topic #2
...
✓ Original item N → Topic #N
```

### Step 5: Receive user selection

Ask the user which suggestions they want to include in the updated report.

**Recommend including all of Group 1** (direct responses to original items) by default, since these directly address what the user originally wanted to investigate.

Accept responses in various formats:
- "all" - include all suggestions from both groups (recommended)
- "group 1" or "part 1" - include only direct responses (topics 1-N)
- "1, 3, 5" (comma-separated numbers)
- "1 and 3 and 5"
- "1-5" (range)
- "group 1 + 7, 9, 12" - mix of group selection and specific numbers
- "none" - skip creating update_report.md

Parse the user's response to identify which numbered items were selected.

**Validate coverage:**
- If user selects only some items from Group 1, warn them which original items won't have corresponding topics
- Example: "Warning: Original item 3 won't be covered if you skip topic #3"

### Step 6: Generate update_report.md

Create update_report.md by:

1. **Copying the original content of report.md AS-IS**
   - Do NOT add a separate "当初の調査項目" or "Original Investigation Items" section
   - The original items are already in report.md and should not be duplicated

2. **Adding a new section at the end titled "## Additional Investigation Topics"**

3. **Under this section, add the selected suggestions with appropriate formatting:**
   - Group selected topics logically (if both groups are included, maintain the Part 1/Part 2 structure)
   - Each selected item should be added as a subsection with the suggestion title and details
   - Include the mapping information (→ Addresses: ...) for Group 1 topics if user wants it

Example structure of update_report.md:

```markdown
# [Original report.md content - unchanged]
- [Original item 1]
- [Original item 2]
...

## Additional Investigation Topics

### Part 1: Direct Responses to Original Items

### 1. [Title addressing original item 1]
[Details...]
→ Addresses: [Original item 1]

### 2. [Title addressing original item 2]
[Details...]
→ Addresses: [Original item 2]

### Part 2: Enhancement Topics

### 7. [Enhancement topic title]
[Details...]

### 8. [Enhancement topic title]
[Details...]
```

**Alternative minimal structure** (if user prefers no explicit grouping):

```markdown
# [Original report.md content - unchanged]

## Additional Investigation Topics

### 1. [Topic title]
[Details...]

### 2. [Topic title]
[Details...]
```

Use the Write tool to create update_report.md with the combined content.

**After creating the file:**
1. Inform the user that update_report.md has been created successfully
2. Display a summary:
   - Total topics added: X
   - Original items covered: N/N (or N-M/N if some were skipped)
   - Enhancement topics added: Y

### Step 7: Complete

After creating update_report.md:

1. **Inform user that enhancement is complete**:
   ```
   ✅ Enhancement complete!

   update_report.md has been created with your enhanced research topics.
   ```

2. **Display summary**:
   ```
   Summary:
   - Original investigation items: [N]
   - Additional topics added: [M]
   - Total topics in update_report.md: [N+M]
   - File location: ./update_report.md
   ```

3. **Suggest next steps** to the user:
   ```
   Next Steps:

   1. Review update_report.md to verify all topics are correct

   2. Generate report structure:
      → Use research-report-structure-planner to create detailed chapter outline

   3. Get tool recommendations:
      → Use skill-recommender to find relevant MCP servers and tools
      → This will analyze your topics and suggest data collection tools

   4. Or manually edit update_report.md if you want to refine topics further
   ```

**IMPORTANT:**
- **DO NOT recommend skills or MCP servers in this step**
- **DO NOT use WebSearch to find tools**
- **DO NOT create install-skills.txt**
- Tool and skill recommendations are the responsibility of **skill-recommender**
- This skill's responsibility ends after creating update_report.md

## Important Notes

- **Always preserve the original report.md** - never modify it
- **Two-phase suggestion approach**:
  - Group 1 (1-N): Direct responses to original investigation items (1:1 mapping)
  - Group 2 (N+1 onwards): Additional enhancement topics beyond original scope
- **Coverage verification**: Ensure all original items have corresponding topics in Group 1
- **No duplication in update_report.md**: Do NOT create a separate "当初の調査項目" section; the original items are already in report.md
- **Number all suggestions clearly** starting from 1 (Group 1) and continuing through Group 2
- **Be specific in suggestions** - avoid generic topics like "do more research"
- **Consider the research domain** and adjust suggestion depth accordingly
- **Explicit mapping**: Show which Group 1 topics address which original items
- **Categories for Group 2**: Label enhancement topics by category (foundational, advanced, clinical, regulatory, etc.)
- **Single responsibility**: This skill ONLY handles topic enhancement. DO NOT recommend tools, skills, or MCP servers - that is skill-recommender's job
- **No WebSearch for tools**: DO NOT search for tools or create install-skills.txt in this skill
- **Clean workflow**: After creating update_report.md, this skill's job is complete
