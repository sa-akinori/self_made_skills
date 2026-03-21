---
name: research-report-structure-planner
description: Generates detailed chapter structures for research and investigation reports based on topic lists. Use when users need to create comprehensive outlines for investigation reports, research documents, survey reports, or analysis documents. Triggers include requests like "create report structure", "generate chapter outline", "plan report sections", "organize research into chapters", or when update_report.md exists with topic lists and user wants to structure their research. Supports multiple report types (scientific, business, market research, competitive analysis, etc.) and five detail levels from minimal outlines to comprehensive frameworks.
---

# Research Report Structure Planner

## Overview

This skill helps create detailed, professional chapter structures for various types of research and investigation reports. Starting from a simple topic list (typically in `update_report.md`), it generates a comprehensive report outline with appropriate chapters, sections, subsections, and content guidance tailored to the report type and desired detail level.

**Key capabilities**:
- Supports 7 report types (scientific, business, market research, competitive analysis, technology evaluation, product development, custom)
- 5 detail levels from minimal (chapter titles only) to comprehensive (full framework with methodology)
- Automatic adaptation of structure to user's topic list
- Professional formatting with front matter, appendices, and cross-references
- Saves output to `report_structure.md` for easy reference

## Workflow

### Step 1: Identify Input File

**Default behavior**: Look for `update_report.md` in the current working directory.

**User-specified file**: If the user mentions a specific file, use that instead.

**Action**:
1. Check if the input file exists using the Read tool
2. If not found, inform the user and ask them to create it or specify the correct path
3. Read the file content to understand the topic list

**Expected format** of input file:
- Title or heading (usually line 1)
- List of research topics/questions (bulleted or numbered)
- May include comments or categories

**Examples**:

*Drug discovery research:*
```markdown
# Protein-Targeted Drug Discovery

- Mutation hotspots and resistance mechanisms
- Structure-based drug design approaches
- Clinical trial data and treatment strategies
- Novel therapeutic modalities (PROTACs, molecular glues)
```

*AI/ML research:*
```markdown
# Deep Learning for Medical Image Analysis

- Dataset curation and annotation strategies
- Model architecture selection and comparison
- Explainability and interpretability methods
- Clinical validation and deployment considerations
```

*Business strategy:*
```markdown
# Market Entry Strategy for Emerging Markets

- Regulatory landscape and compliance requirements
- Competitive analysis and positioning
- Distribution channel optimization
- Localization and cultural adaptation strategies
```

### Step 2: Determine Report Type

Ask the user to select the report type that best matches their research:

**Question format**:
```
What type of research report are you creating?

1. Scientific & Technical Research (drug development, materials science, engineering)
2. Business Strategy Report (strategic planning, market entry, business models)
3. Market Research Report (market sizing, customer analysis, opportunities)
4. Competitive Analysis Report (competitor assessment, market positioning)
5. Technology Evaluation Report (technology selection, vendor evaluation)
6. Product Development Research (new product planning, user research)
7. Custom/General Research (unique or multi-disciplinary research)

Please select 1-7, or describe your report type if none fit exactly.
```

**Handling responses**:
- If user selects 1-6: Load the corresponding section from `references/report_types.md`
- If user selects 7 or describes custom type: Use general research report pattern, adapted to their description
- If unclear: Ask follow-up questions about the report's purpose and audience

**For reference**: Read `references/report_types.md` to understand each type's characteristics and recommended structure patterns.

### Step 3: Select Detail Level

Ask the user to choose the desired detail level:

**Question format**:
```
How detailed should the chapter structure be?

1. Minimal - Chapter titles only (quick outline)
2. Concise - Chapters with subsections
3. Standard - Chapters, subsections, and brief descriptions (recommended for most cases)
4. Detailed - Comprehensive guidance with content suggestions and analysis frameworks
5. Comprehensive - Maximum detail with methodology, data sources, and complete framework

Please select 1-5.
```

**Default recommendation**: Level 3 (Standard) for most users.

**Handling responses**:
- Accept numeric input (1-5) or descriptive input ("detailed", "comprehensive", etc.)
- If user is uncertain, recommend Level 3 and explain it provides clear guidance without overwhelming detail
- For reference on what each level includes, consult `references/detail_levels.md`

### Step 3.5: Determine Target Page Count

🛑 **MANDATORY**: You MUST ask the user for their target page count. This is REQUIRED for proper report planning.

**Question format**:
```
What is your target page count for the final report?

Typical ranges by report type:
- Executive summary: 2-5 pages
- Quick analysis report: 15-30 pages
- Standard research report: 50-100 pages
- Comprehensive technical report: 100-200 pages
- Book-length research: 200+ pages

Please specify either:
1. A specific page count (e.g., "80 pages")
2. A range (e.g., "100-150 pages")
3. "Not sure" (we'll suggest based on your topics and detail level)
```

**Handling responses**:

1. **If user provides specific count or range**:
   - Record the target page count
   - Use this to calculate appropriate pages per chapter
   - Adjust figure/table density accordingly
   - Include in report_structure.md metadata

2. **If user is uncertain**:
   - Analyze the topic count and detail level
   - Suggest a range based on:
     ```
     Estimated pages = (Number of topics × Pages per topic × Detail multiplier)

     Detail multipliers:
     - Level 1 (Minimal): 0.5x
     - Level 2 (Concise): 1.0x
     - Level 3 (Standard): 1.5x
     - Level 4 (Detailed): 2.0x
     - Level 5 (Comprehensive): 3.0x

     Pages per topic baseline:
     - Simple topic: 5-8 pages
     - Complex topic: 10-15 pages
     - Multi-faceted topic: 15-25 pages
     ```
   - Present the calculated range to user for confirmation
   - Example: "Based on your 8 topics and Detail Level 5, I suggest 120-150 pages. Does this sound right?"

3. **Record in metadata**:
   - Store target page count at the top of report_structure.md:
     ```markdown
     **Estimated Total Pages**: 120-150 pages
     ```
   - Or for specific count:
     ```markdown
     **Target Page Count**: 100 pages
     ```

4. **Use for chapter planning**:
   - Allocate pages proportionally to chapters
   - Add page estimates to each chapter (for Levels 3-5)
   - Adjust number of figures/tables per chapter based on available pages
   - Example:
     ```markdown
     ## Chapter 3: Methodology (15-18 pages)
     ```

**CRITICAL**: Do NOT proceed to Step 4 without obtaining and recording the target page count.

### Step 4: Generate Report Structure

Using the information gathered, generate the chapter structure:

**Process**:

1. **Map topics to chapters**:
   - Analyze the user's topic list from the input file
   - Group related topics into logical chapters
   - Use the report type's recommended chapter pattern as a framework
   - Ensure coverage of all user topics while maintaining logical flow

2. **Apply detail level**:
   - Use `references/detail_levels.md` as a guide for the selected level
   - Level 1: Chapter titles only
   - Level 2: Add subsections (2-4 per chapter)
   - Level 3: Add subsections with brief descriptions
   - Level 4: Add content guidance, suggested figures/tables, key questions
   - Level 5: Add methodology details, data sources, analysis frameworks, cross-references

3. **Adapt and customize**:
   - Merge similar topics into unified chapters
   - Add specialized chapters for unique topics
   - Adjust technical depth based on report type
   - Ensure logical progression: Background → Analysis → Conclusions
   - Include appropriate front matter and appendices

4. **Structure the output**:
   - Title and metadata
   - Front matter (Table of Contents, List of Figures/Tables)
   - Chapter 1: Executive Summary
   - Chapter 2: Background/Objectives
   - Chapters 3-N: Topic-specific analysis chapters
   - Final Chapter: Conclusions and Recommendations
   - Appendices

**Quality checks**:
- All user topics are addressed
- Chapters flow logically
- Detail level is consistent throughout
- Professional formatting with clear hierarchy
- Page estimates included (for Levels 3-5)

### Step 5: Save and Display Output

**Actions**:

1. **Save to file**:
   - Create `report_structure.md` in the current working directory
   - Use clear Markdown formatting with proper heading levels
   - Include all generated content

2. **Display summary to user**:
```
✅ Report structure generated successfully!

Output saved to: report_structure.md

Summary:
- Report type: [Type]
- Detail level: [Level]
- Total chapters: [N]
- Estimated pages: [X-Y] (if applicable)

Main chapters:
1. Executive Summary
2. [Chapter 2 title]
3. [Chapter 3 title]
...

You can now use this structure to:
- Guide your research process
- Organize collected information
- Begin writing the full report
- Share the framework with collaborators
```

3. **Offer next steps**:
   - Suggest relevant MCP servers for data collection (if applicable)
   - Offer to refine specific chapters if needed
   - Mention that the structure can be adjusted as research progresses

## Tips for Best Results

**Input file preparation**:
- Be specific with topic descriptions
- Group related topics together in the list
- Include key questions you want to answer
- Note any specific requirements (e.g., "must include clinical data")

**Report type selection**:
- Choose the type that best matches your PRIMARY purpose
- For multi-purpose reports, select the dominant focus
- Custom/General works well for hybrid or unique reports

**Detail level selection**:
- Level 1-2: When you want flexibility and know the domain well
- Level 3: Best for most users - provides clear guidance without overwhelming
- Level 4-5: For complex reports, team collaboration, or when you need extensive planning

**Customizing output**:
- The generated structure is a starting point
- Feel free to modify, merge, or split chapters as needed
- Adjust technical depth based on your audience
- Add or remove sections based on available data

## Bundled Resources

### references/report_types.md
Detailed descriptions of 7 report types with recommended chapter patterns:
- Scientific & Technical Research Report
- Business Strategy Report
- Market Research Report
- Competitive Analysis Report
- Technology Evaluation Report
- Product Development Research Report
- Custom/General Research Report

**When to read**: After user selects report type in Step 2.

### references/detail_levels.md
Comprehensive definitions and examples of all 5 detail levels:
- Level 1: Minimal (chapter titles only)
- Level 2: Concise (chapters with subsections)
- Level 3: Standard (with descriptions) - recommended default
- Level 4: Detailed (with content guidance and suggestions)
- Level 5: Comprehensive (maximum detail with methodology)

**When to read**: When generating structure in Step 4, to understand what elements to include.

### assets/template_general.md
Basic template showing minimal report structure. Primarily for reference; actual structures are generated dynamically based on user input.

**When to use**: Rarely needed; most structures are generated fresh. May be useful as a starting point for completely custom reports.
