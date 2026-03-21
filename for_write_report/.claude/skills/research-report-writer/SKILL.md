---
name: research-report-writer
description: Writes comprehensive research report chapters based on report_structure.md using available MCP servers for data collection. Use when users want to write, draft, or generate specific chapters or sections of their research report. Triggers include "write chapter X", "draft section Y", "create the full report", "generate chapter content", or when report_structure.md exists and user wants to begin writing. Automatically uses appropriate MCP servers (academic databases, search engines, data APIs, repositories, etc.) for deep literature search and data collection.
---

# Research Report Writer

## Overview

This skill generates comprehensive, well-researched content for research report chapters based on the structure defined in `report_structure.md`. It automatically selects appropriate MCP servers for data collection, conducts deep literature searches when needed, writes content in the appropriate style for the report type, generates figures and tables from collected data, and manages citations.

**Key capabilities**: Supports all report types, adaptive writing style, deep search using Task tool, automatic MCP server selection, figure/table generation with Japanese font support, citation management, **direct LaTeX writing**, complete reference list generation, automatic PDF compilation.

## Workflow

### Step 1: Identify Structure File and Target Chapters

Read `report_structure.md` (or user-specified file) to understand the report structure, then ask user which chapter(s) to write.

**Continuation session check** 🔄: Check if `report/params.json` exists.
- **If it exists**: Read and display the saved parameters to the user:
  ```
  前回確認済みパラメータ（report/params.json）:
  - レポートタイプ: [type]
  - 詳細レベル: [level]
  - 目標ページ数: [pages]ページ
  - 確認日時: [date]

  これらのパラメータで続けますか？変更がある場合はお知らせください。
  ```
  If user confirms, **skip Step 2** and proceed to Step 3 using saved parameters.
  If user wants to change any parameter, update `report/params.json` and proceed.
- **If it does not exist**: Proceed to Step 2 normally.

### Step 2: Determine Writing Parameters

🛑 **MANDATORY**: You MUST ask user to confirm the following parameters. Do NOT skip this step even if report_structure.md contains these values.

Ask user to confirm the following parameters:

1. **Report type/writing style**: Scientific, business, market research, etc. (see `references/writing_styles.md`)
   - If report_structure.md specifies a type, present it to user for confirmation

2. **Content detail level**:
   - Concise: Brief overview, minimal depth
   - Standard: Balanced coverage (recommended)
   - Detailed: Comprehensive, in-depth analysis
   - If report_structure.md specifies a level, present it to user for confirmation

3. **Target page count**: 🔴 **CRITICAL** - You MUST explicitly ask user for desired page count
   - If report_structure.md contains "Estimated Total Pages" or "target_pages", present this to user and ask: **"The structure file suggests X-Y pages. Is this your target page count, or would you like a different range?"**
   - If user is uncertain, suggest typical ranges based on report type:
     - Executive summary: 2-5 pages
     - Technical chapter: 10-20 pages per chapter
     - Comprehensive report: 50-150 pages total
   - Use target page count to adjust:
     - Content depth (more/less detail per topic)
     - Number of examples and case studies
     - **Table and figure density** (more pages = more figures)
     - Reference list length
   - **IMPORTANT**: Store the confirmed page count and check against it in Step 9

After user confirms all parameters, **save to `report/params.json`**:
```json
{
  "report_type": "[confirmed type]",
  "detail_level": "[concise|standard|detailed]",
  "target_pages": [number],
  "confirmed_at": "[YYYY-MM-DD HH:MM]"
}
```
Create `report/` directory if it doesn't exist. This file ensures parameters survive session boundaries.

Map detail level to search depth (concise→basic search, standard→moderate search, detailed→deep search).

### Step 3: Data Collection Strategy

Analyze chapter requirements, select appropriate MCPs (consult `references/mcp_selection.md`), and determine if deep search is needed (consult `references/deep_search_strategies.md`).

### Step 4: Execute Data Collection

For basic search: Directly query 1-2 MCPs with focused queries.
For deep search: Use Task tool (Explore agent) for comprehensive coverage (50-100+ sources). Parallel queries on additional MCPs as needed.

### Step 5: Write Chapter Content in LaTeX

**IMPORTANT**: Write content directly in LaTeX format, not Markdown.

1. **Use LaTeX template** (see `references/latex_template.md`)
2. **Follow structure outline** from report_structure.md
3. **Apply appropriate writing style** (from `references/writing_styles.md`)
4. **Format sections**:
   - Chapters: `\chapter{タイトル}`
   - Sections: `\section{タイトル}`
   - Subsections: `\subsection{タイトル}`

5. **Writing style - Prioritize narrative paragraphs** 🔴 **CRITICAL**:

   **PRIMARY**: Write content as **flowing narrative paragraphs** (≈90% of content)

   **SECONDARY**: Use bullet points sparingly (≈10% of content, varies by context)

   **Use PARAGRAPHS for**:
   - Explanations, analysis, and detailed descriptions
   - Data interpretation and discussion
   - Literature review and context
   - Figure/table commentary

   **Use BULLET POINTS sparingly for**:
   - Listing discrete items or properties
   - Key points summary
   - Structured comparisons

   **AVOID**: Excessive bullet points, using lists as default format

6. **Integrate citations**: Use `\textsuperscript{[1]}` format
6. **Create tables**: Use longtable with centered cells (see below)
7. **Include figures**: Use figure environment with [H] placement
8. **Include section summaries**

**Table format** (caption on top, centered cells):
```latex
\begin{longtable}{|>{\centering\arraybackslash}m{3cm}|>{\centering\arraybackslash}m{3cm}|}
\caption{キャプション} \\
\hline
\textbf{ヘッダー1} & \textbf{ヘッダー2} \\
\hline
\endfirsthead
\caption{キャプション (続き)} \\
\hline
\textbf{ヘッダー1} & \textbf{ヘッダー2} \\
\hline
\endhead
\hline
\endfoot
\hline
\endlastfoot
データ1 & データ2 \\
\hline
\end{longtable}
```

**Figure format** (caption on bottom):
```latex
\begin{figure}[H]
\centering
\includegraphics[width=0.7\textwidth]{figures/filename.png}
\caption{キャプション}
\end{figure}
```

**重要**: キャプションに番号（"表 1:"、"図 1:"など）を含めない。LaTeXが自動的に連続番号を付与する。

**Special character escaping**: Escape `&`, `%`, `$`, `#`, `_`, `{`, `}`, `~`, `^`, `\`

5. **Explain technical terms inline**:
   - **CRITICAL**: When introducing technical terms for the first time, provide brief inline explanations
   - **Format**: 専門用語（英語表記: 簡単な説明）
   - **Example**: 機械学習（Machine Learning: データからパターンを自動的に学習する技術）
   - **Do NOT create a separate glossary section** - explain terms in context where they first appear
   - Keep explanations concise (1 sentence or phrase)
   - Only explain terms that may not be familiar to the target audience
   - Track which terms have been explained to avoid repetition

6. **Review each chapter after writing**:
   - **CRITICAL**: After completing each chapter, perform an immediate review
   - Check for factual errors, logical inconsistencies, and unclear explanations
   - Verify that all data and numbers are accurate
   - Check for typos and grammar errors (especially Japanese particles: は/が/を/に)
   - Ensure proper citation usage
   - Confirm terminology consistency
   - Verify that all technical terms have inline explanations at first occurrence
   - **Fix any issues immediately** before proceeding to the next chapter
   - This prevents accumulation of errors and ensures quality throughout

### Step 5.5: Extract Required Figures and Tables from report_structure.md

🛑 **MANDATORY**: Before generating any figures, you MUST extract the complete list of required figures and tables from report_structure.md.

1. **Read report_structure.md completely**: Use Read tool to read the entire structure file
2. **Extract all figure specifications**: Use Grep to find all lines matching `- **図[0-9]` pattern
3. **Extract all table specifications**: Use Grep to find all lines matching `- **表[0-9]` pattern
4. **Create a checklist**: Document all required figures and tables with:
   - Figure/Table number (e.g., 図1-1, 表2-1)
   - Description/title
   - Chapter location
   - Data requirements (what data is needed to create it)
5. **Verify completeness**: Count total figures and tables, confirm all are accounted for

**Example extraction**:
```bash
grep -E "- \*\*図" report_structure.md
grep -E "- \*\*表" report_structure.md
```

**Output**: Create a checklist like:
- [ ] 図1-1: Kit変異スペクトラムの概要（疾患別）
- [ ] 図2-1: Kitタンパク質のドメイン構造（模式図）
- [ ] 表1-1: 主要Kit阻害剤の比較
- [ ] ... (continue for all figures/tables)

🔴 **CRITICAL**: Do NOT proceed to Step 6 without completing this extraction.

### Step 6: Generate Figures and Tables

🛑 **MANDATORY - DO NOT SKIP**: This step is REQUIRED. You MUST generate ALL figures and tables specified in report_structure.md.

**Pre-flight checks** (answer these before starting):
- [ ] Have I extracted the complete list of required figures from report_structure.md? (Step 5.5)
- [ ] Have I extracted the complete list of required tables from report_structure.md? (Step 5.5)
- [ ] Do I know how many figures need to be generated? (Count: ___)
- [ ] Do I know how many tables need to be generated? (Count: ___)
- [ ] Have I collected the necessary data to create each figure/table?

**If ANY answer is "No", go back to Step 5.5 and complete the extraction.**

---

**Figure/Table Generation Process**:

1. **Create figures directory**:
   ```bash
   mkdir -p report/figures
   ```

2. **For EACH figure in your checklist** (from Step 5.5):

   a. **Identify figure type**:
      - Data visualization (bar chart, line plot, heatmap, scatter plot)
      - Structural diagram (protein structure, pathway diagram)
      - Flowchart (algorithm, workflow)
      - Comparison chart (Venn diagram, comparison table as image)

   b. **Collect/prepare data**:
      - Extract data from MCP search results
      - Use collected literature data
      - Create synthetic data if needed for illustration

   c. **Generate figure using appropriate method**:
      - **Python matplotlib/seaborn**: Use `scripts/generate_figure.py` for data visualizations
      - **Manual creation**: For complex diagrams, create using appropriate tools
      - **Template modification**: Adapt existing figure templates from `assets/figure_templates/`

   d. **Configure Japanese font support and minimum font sizes** (CRITICAL):
      ```python
      import matplotlib
      import matplotlib.pyplot as plt
      import matplotlib.font_manager as fm

      # Add Japanese font
      fm.fontManager.addfont('/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf')
      plt.rcParams['font.sans-serif'] = ['IPAexGothic']
      plt.rcParams['font.family'] = 'sans-serif'
      matplotlib.rcParams['axes.unicode_minus'] = False

      # Minimum font size: 14pt (REQUIRED for all figures)
      matplotlib.rcParams['font.size'] = 14
      matplotlib.rcParams['axes.labelsize'] = 14
      matplotlib.rcParams['axes.titlesize'] = 16
      matplotlib.rcParams['xtick.labelsize'] = 14
      matplotlib.rcParams['ytick.labelsize'] = 14
      matplotlib.rcParams['legend.fontsize'] = 14
      matplotlib.rcParams['figure.titlesize'] = 18
      ```

      **IMPORTANT - Minimum font size rule**: All text in figures (labels, titles, tick labels,
      legends, annotations, table text) must be **14pt minimum**. Never use hardcoded
      `fontsize=` values below 14 in figure generation code. This ensures legibility in the
      printed PDF. The rcParams above set global defaults; verify any per-element fontsize
      arguments also respect this minimum.

      **MANDATORY layout rules** — apply to EVERY figure before saving:

      1. **X-axis label rotation** — for bar/grouped charts with Japanese labels:
         ```python
         ax.set_xticklabels(labels, rotation=45, ha='right')
         plt.tight_layout()
         ```
         Apply whenever: (a) labels are Japanese multi-character text, OR (b) there are 4+ categories.

      2. **Text contrast** — never use white text on light backgrounds:
         - ❌ Avoid: white text on `#f39c12`, `#95a5a6`, `#2ecc71`, `#1abc9c`, `#f1c40f`, or any pastel/light color
         - ✅ Safe: white text on `#2c3e50`, `#e74c3c`, `#8e44ad`, `#16a085`, `#1a5276`, `#c0392b`
         - Rule of thumb: if the hex color has any channel R/G/B > 180, use dark text (`color='#1a1a1a'`) instead
         ```python
         # Helper to choose text color based on background
         def text_color(bg_hex):
             r, g, b = int(bg_hex[1:3],16), int(bg_hex[3:5],16), int(bg_hex[5:7],16)
             return 'white' if (0.299*r + 0.587*g + 0.114*b) < 140 else '#1a1a1a'
         ```

      3. **Edge colors on patches** — avoid `edgecolor='white'` on figures with white background:
         - ❌ `edgecolor='white'` makes borders invisible against white figure background
         - ✅ Use `edgecolor='#2c3e50'` (dark border) or a darker shade of the fill color

      4. **Timeline/scatter label staggering** — for events clustered in time:
         - Use 3+ distinct vertical levels above AND below the axis
         - Minimum separation between adjacent label centers: 1.5× the label height

   e. **Save with descriptive filename**:
      - Format: `fig{chapter}_{number}_{description}.png`
      - Example: `fig1_1_mutation_spectrum.png`, `fig2_1_kit_domain_structure.png`
      - Save to `report/figures/` directory

   f. **Verify Japanese text rendering**:
      - Open the generated PNG file
      - Check that all Japanese text displays correctly (no boxes □ or garbled text)
      - If issues found, regenerate with proper font configuration

   g. **Update checklist**: Mark figure as completed ✅

3. **For EACH table in your checklist** (from Step 5.5):

   a. **Determine if table should be generated as**:
      - LaTeX longtable (preferred for text-heavy tables)
      - Figure/image (for complex formatted tables)

   b. **If LaTeX table**: Include directly in Step 5 (Write Chapter Content)

   c. **If table as figure**: Generate using matplotlib or similar, save to `report/figures/`

4. **Embed figures in LaTeX** (in Step 5 or update existing content):

   ```latex
   \begin{figure}[H]
   \centering
   \includegraphics[width=0.7\textwidth]{figures/fig1_1_mutation_spectrum.png}
   \caption{Kit変異スペクトラムの概要（疾患別）}
   \label{fig:mutation_spectrum}
   \end{figure}
   ```

   **IMPORTANT**:
   - Use `[H]` placement to keep figures in place
   - Use relative path `figures/filename.png` (not absolute path)
   - Do NOT include figure numbers in caption (LaTeX auto-numbers)
   - Reference figures in text using: `図\ref{fig:mutation_spectrum}` or simply `図1`

5. **Add source citations to figure captions** (when applicable):
   ```latex
   \caption{Kit変異スペクトラムの概要（疾患別）。データ出典: COSMIC database\textsuperscript{[42]}}
   ```

6. **Final verification checklist**:
   - [ ] ALL figures from Step 5.5 checklist have been generated ✅
   - [ ] ALL tables from Step 5.5 checklist have been created ✅
   - [ ] All figure files exist in `report/figures/` directory
   - [ ] All figures are embedded in LaTeX with proper syntax
   - [ ] All Japanese text in figures renders correctly (no mojibake)
   - [ ] All figures have descriptive captions
   - [ ] Figure references in text match figure numbers in document
   - [ ] All tables are formatted correctly (longtable or figure)

🔴 **CRITICAL ERROR PREVENTION**:
- Do NOT say "figures will be added later" or "placeholder for figure"
- Do NOT leave figure references without actual figures
- Do NOT skip figures because they are "complex" or "time-consuming"
- If you cannot generate a specific figure type (e.g., complex protein structure), CREATE A PLACEHOLDER FIGURE with text explaining what should be shown, rather than leaving it missing

**Time estimate**: Expect 5-15 minutes per figure depending on complexity. Budget time accordingly.

### Step 7: Build Complete Reference List

**CRITICAL**: Always generate complete reference lists with full citations. Never use placeholders like "200+ references (to be added)" or "[Full reference list]".

- Maintain reference list following citation format guidelines
- For each citation [1], [2], etc., include: Authors, Title, Journal/Source, Year, Volume, Pages
- Verify all citations have matching references
- Number references sequentially from [1] to [N]

### Step 8: Compile LaTeX to PDF

**IMPORTANT**: Since content is written directly in LaTeX, simply compile to PDF.

1. **Create report directory**: Run `mkdir -p report` to create the report directory if it doesn't exist
2. **Save LaTeX file**: Write all content to `report/{report_name}.tex`
3. **Compile to PDF**: Run `xelatex` three times in the report directory
   - Pass 1: Generate document structure
   - Pass 2: Update table of contents and references
   - Pass 3: Finalize cross-references

**Compilation command**:
```bash
cd report
xelatex -interaction=nonstopmode {report_name}.tex
xelatex -interaction=nonstopmode {report_name}.tex
xelatex -interaction=nonstopmode {report_name}.tex
cd ..
```

**Alternative (using -output-directory)**:
```bash
mkdir -p report
xelatex -output-directory=report -interaction=nonstopmode report/{report_name}.tex
xelatex -output-directory=report -interaction=nonstopmode report/{report_name}.tex
xelatex -output-directory=report -interaction=nonstopmode report/{report_name}.tex
```

**LaTeX document features**:
- Japanese language support using XeLaTeX and IPAex fonts
- Professional document formatting with chapters, sections, subsections
- Font size: 11pt (readable and compact)
- Line spacing: 1.2 for body text (readable with efficient page density), 1.0 for tables
- Automatic table of contents, list of figures, list of tables
- Tables with centered cells and captions on top
- Figure captions on bottom
- Proper citation formatting with superscripts

If user requests other formats:
- **Markdown** (.md): Can be generated separately if needed (not recommended as primary format)
- Use `convert_to_latex.py` only for converting existing Markdown files

### Step 9: Display Preliminary Summary

⚠️ **WARNING: This is NOT the final step. Quality checks are MANDATORY before completion.**

Display **preliminary** completion summary with statistics:
- **Pages written**: X pages (Target: Y pages) - Note if significantly over/under target
- Word count (approximate)
- Number of references
- Number of figures/tables
- MCP servers used for data collection
- Output files generated (report/{report_name}.tex, report/{report_name}.pdf)
- PDF file size and page count

**Page Count Analysis**:
- If actual pages significantly exceed target (>20% over): Consider if content can be condensed
- If actual pages significantly under target (>20% under): Consider if more detail/examples needed
- Note: Final page count may change slightly after quality checks and fixes

**Output file locations**:
- LaTeX source: `report/{report_name}.tex`
- PDF document: `report/{report_name}.pdf`
- Figures: `report/figures/*.png`
- Auxiliary files: `report/{report_name}.aux`, `.log`, `.toc`, `.lof`, `.lot`

🛑 **IMPORTANT**:
- **DO NOT save version yet** (Step 11 must wait)
- **DO NOT consider the report complete**
- **You MUST proceed immediately to Step 10 (Quality Check)**
- **Step 10 is MANDATORY and cannot be skipped**

---

### Step 10: Quality Check and Revision Loop (🛑 MANDATORY - BLOCKING STEP)

**CRITICAL - MANDATORY**: This step is NOT optional. After generating the PDF, you MUST perform comprehensive quality checks and fix ALL issues until the report meets quality standards. Do NOT skip this step.

**This is a multi-iteration process**: You will likely need to fix issues and recompile multiple times. Continue until all checks pass.

🔒 **PRE-FLIGHT CHECKLIST - Answer these questions before proceeding:**

Before moving to Step 11, you MUST confirm:
- [ ] Have I extracted PDF text using `pdftotext`?
- [ ] Have I completed ALL Phase A format checks?
- [ ] Have I completed ALL Phase B content checks?
- [ ] Have I opened and visually inspected the PDF figures for Japanese text rendering?
- [ ] Have I read through key sections of each chapter for errors?
- [ ] Have I documented all issues found (Critical/Important/Minor)?
- [ ] Have I fixed all Critical issues?
- [ ] Have I fixed all Important issues?
- [ ] Have I recompiled the PDF after fixes?
- [ ] Have I re-checked to verify all fixes worked?

**If ANY answer is "No", you MUST complete that task before proceeding to Step 11.**

---

**Quality Check Process**:

1. **Extract PDF text**: Use `pdftotext report/{report_name}.pdf` to extract text from the PDF

2. **Phase A: PDF Format Quality Check**:
   - ✅ **Japanese display**: Verify Japanese characters in body text are correctly rendered (no garbled text)

   - ✅ **Figure completeness** (🔴 CRITICAL):
     - **Step 1**: Get the figure checklist from Step 5.5 (list of ALL required figures from report_structure.md)
     - **Step 2**: Count expected figures: `grep -c "- \*\*図" report_structure.md`
     - **Step 3**: Count actual figures in PDF: `pdfimages -list report/{report_name}.pdf | wc -l`
     - **Step 4**: Compare counts - if mismatch, identify missing figures
     - **Step 5**: For EACH figure in checklist, verify it appears in the PDF
     - **Result**: All figures from report_structure.md MUST be present
     - **If missing**: Go back to Step 6, generate missing figures, recompile PDF

   - ✅ **Table completeness** (🔴 CRITICAL):
     - **Step 1**: Get the table checklist from Step 5.5 (list of ALL required tables)
     - **Step 2**: Count expected tables: `grep -c "- \*\*表" report_structure.md`
     - **Step 3**: Count actual tables in PDF: `grep -c "^表 [0-9]" extracted_text.txt`
     - **Step 4**: Compare counts - if mismatch, identify missing tables
     - **Result**: All tables from report_structure.md MUST be present
     - **If missing**: Go back to Step 6, create missing tables, recompile PDF

   - ✅ **Figure Japanese text rendering**: **CRITICAL** - Visually inspect ALL figures in the PDF to verify Japanese text displays correctly without mojibake (文字化け). Look for:
     - Boxes (□) instead of Japanese characters
     - Garbled characters or question marks (?)
     - Missing text in figure labels, titles, or legends
     - If ANY figure shows text rendering issues, regenerate figures with proper Japanese font configuration (IPAexGothic). Use `regenerate_figures.py` or update figure generation scripts to explicitly set `matplotlib.rcParams['font.sans-serif'] = ['IPAexGothic']`

   - ✅ **Figure/Table minimum font size** (🔴 CRITICAL): All text in figures must be **14pt minimum**.
     - Check all generated PNG files for small text (labels, tick labels, legends, annotations)
     - If any text appears smaller than 14pt, regenerate with proper rcParams:
       ```python
       matplotlib.rcParams['font.size'] = 14
       matplotlib.rcParams['axes.labelsize'] = 14
       matplotlib.rcParams['axes.titlesize'] = 16
       matplotlib.rcParams['xtick.labelsize'] = 14
       matplotlib.rcParams['ytick.labelsize'] = 14
       matplotlib.rcParams['legend.fontsize'] = 14
       ```
     - Also audit all hardcoded `fontsize=N` arguments in generation code — replace any N < 14 with 14
     - For LaTeX tables: body text is controlled by the document font size (11pt default); if table text
       appears too small in PDF, wrap content in `{\large ...}` or increase column font size

   - ✅ **Figure/Table readability and text overlap** (🔴 CRITICAL): Visually inspect ALL figures and tables for layout issues:

     **X-axis label overlap** (most common problem - check EVERY bar/grouped chart):
     - If x-axis has 4+ categories with Japanese text (multi-character labels), they WILL overlap unless rotated
     - **MANDATORY**: Always set `ax.set_xticklabels(labels, rotation=45, ha='right')` for bar charts with Japanese labels
     - For very long labels or many categories (6+): use `rotation=45` or `rotation=90`, increase figure width, or shorten labels
     - For grouped bar charts: use `rotation=45, ha='right'` on xticklabels
     - After setting rotation, always call `plt.tight_layout()` or `fig.tight_layout()` so labels are not clipped

     **Text overlap in annotations/timeline/scatter plots**:
     - Check that value labels on bar tops don't overlap each other (happens when bars are narrow or values are close)
     - For timeline figures: stagger labels at multiple vertical levels (3+ levels above and below) so nearby events don't collide
     - For scatter plots: check data point labels don't overlap each other

     **Text contrast (white-on-light background)**:
     - Check ALL colored boxes/patches: never use white text on light colors (yellow `#f39c12`, light gray `#95a5a6`, light green `#2ecc71`, light teal `#1abc9c`)
     - Rule: use white text only on dark colors (dark blue, dark red, dark purple, dark green with L < 50%)
     - For light backgrounds: use dark text (`#2c3e50` or `#1a1a1a`)
     - Check `edgecolor`: avoid `edgecolor='white'` on colored patches with white figure background — borders will be invisible. Use `edgecolor='#2c3e50'` or a darker shade of the fill color instead

     **Other layout issues**:
     - **Legend overlap with data**: Ensure legends do not obscure data points or bars. Move legend outside plot area if needed (`bbox_to_anchor=(1.05, 1), loc='upper left'`)
     - **Axis label clipping**: Verify axis labels are fully visible and not cut off at figure edges
     - **Bar/pie label visibility**: Confirm value labels on bars and pie slices are clearly readable against the background color
     - **Table cell overflow**: Check that all table cell text fits within cells without overflowing or being truncated
     - If any readability issue is found, regenerate the figure with appropriate fixes

     **Pre-generation checklist** (apply BEFORE saving each figure):
     - [ ] X-axis labels: rotated if Japanese text with 4+ categories?
     - [ ] Text contrast: no white text on light-colored backgrounds?
     - [ ] Edge colors: visible against figure background?
     - [ ] Annotations: no overlap with each other or data?
     - [ ] `tight_layout()` called?
     - [ ] Figure size adequate for the number of elements?

   - ✅ **Figure and table content duplication**: Check that no two figures or tables present the same data or convey the same message.
     - Compare all figures with each other: do any show the same dataset, same variables, or near-identical charts?
     - Compare all tables with each other: do any contain the same rows/columns or redundant information?
     - Compare figures against tables: is any figure merely a graphical version of an adjacent table showing identical data? If so, remove the redundant one or combine them.
     - If duplication is found: either remove one instance, merge the information, or clearly differentiate the scope/angle of each visualization.

   - ✅ **Table/Figure captions**: Confirm captions show "表1", "表2", "図1", "図2" (not "Table 1", "Figure 1")
   - ✅ **Table/Figure references**: Verify text references show "表1", "表2", "図1", "図2"
   - ✅ **Continuous numbering**: Ensure tables and figures are numbered continuously across chapters
   - ✅ **Table overflow**: Check that tables fit within page margins (no "Overfull hbox" warnings)
   - ✅ **Reference completeness**: Verify all citations [1], [2], etc. have corresponding references
   - ✅ **LaTeX compilation**: Ensure no critical errors in .log file

3. **Phase B: Content Quality Check** (MANDATORY):
   - ✅ **Typos and spelling errors**: Check for Japanese typos (誤変換) and spelling mistakes in every paragraph
   - ✅ **Grammar errors**: Verify proper Japanese grammar (主語述語の一致, 助詞の適切性: は/が/を/に/で)
   - ✅ **Logical consistency**: Ensure no contradictory statements within or across sections/chapters
   - ✅ **Data accuracy**: Verify ALL numbers in tables match text descriptions, calculations are mathematically correct
   - ✅ **Citation appropriateness**: Confirm EVERY cited reference actually supports the claim made
   - ✅ **Terminology consistency**: Ensure consistent use of technical terms (e.g., don't switch between "機械学習" and "ML" randomly)
   - ✅ **Completeness**: Check for missing information, incomplete sentences, or unexplained jumps in logic
   - ✅ **Readability**: Check for awkward phrasing, overly complex sentences, unclear expressions
   - ✅ **Section coherence**: Verify smooth transitions between sections and chapters
   - ✅ **Factual accuracy**: Cross-check key facts, dates, names, statistics against original sources
   - ✅ **Missing content**: Identify sections that feel too brief or lack sufficient detail
   - ✅ **Redundancy**: Remove unnecessary repetition of the same information
   - ✅ **Figure/Table content duplication (content-level)**: Beyond format checks (Phase A), verify that no two figures or tables duplicate the **narrative meaning** — e.g., two pie charts showing the same mutation frequencies in different chapters, or a bar chart and a table listing identical efficacy data side by side without added value. Duplicates that add no new perspective should be consolidated or removed.

**Content Review Method** (Do NOT skip this):
- Read through EVERY chapter section by section (not just sampling)
- For EACH section, systematically check ALL of the above quality criteria
- Pay EXTRA attention to:
  - Abstract/summary (often has errors because written first)
  - Introduction (sets tone, must be clear)
  - Data tables (often have transcription errors)
  - Conclusion (must align with content)
  - Technical explanations (must be accurate and clear)
- Mark issues as you find them with chapter/section/paragraph location
- Do NOT assume quality - actively look for problems

4. **When issues are found** (EXPECTED - there will always be issues):
   - **Document ALL issues** with specific locations (chapter number, section name, paragraph number or line number)
   - **Categorize by severity**:
     - 🔴 Critical: Factual errors, contradictions, missing content, incorrect data
     - 🟡 Important: Grammar errors, typos, unclear explanations, citation problems
     - 🟢 Minor: Style inconsistencies, awkward phrasing
   - **Fix issues in priority order**:
     1. Fix ALL 🔴 Critical errors first
     2. Fix ALL 🟡 Important errors
     3. Fix 🟢 Minor issues if time permits
   - **Editing process**:
     - Open and edit: `report/{report_name}.tex`
     - Make corrections carefully
     - Verify each fix doesn't introduce new errors
   - **Recompile after fixes**:
     ```bash
     cd report
     xelatex -interaction=nonstopmode {report_name}.tex
     xelatex -interaction=nonstopmode {report_name}.tex
     xelatex -interaction=nonstopmode {report_name}.tex
     cd ..
     ```
   - **Re-check modified sections**: Don't assume the fix worked - verify it

5. **Iteration requirement**:
   - You MUST repeat steps 1-4 until **ALL Phase A and Phase B checks pass**
   - Typically requires 2-4 iterations
   - Do NOT stop after just 1 check - keep going until quality is achieved
   - It's normal for the first check to find 10-20+ issues

6. **Final verification and reporting**:
   - **Confirm** all Phase A checks pass ✅
   - **Confirm** all Phase B checks pass ✅
   - **List** what was fixed (e.g., "Corrected 15 typos, fixed 3 data inconsistencies, improved 8 unclear explanations")
   - **Display** final PDF statistics:
     - Total pages
     - Chapters and sections
     - Number of figures and tables
     - Number of references
     - PDF file size
   - **Report** any known limitations or minor issues that remain (if any)
   - **Declare** report ready for user review

---

🎯 **QUALITY GATE CHECKPOINT**

Before proceeding to Step 11, verify you have completed ALL of the following:
- ✅ Extracted and reviewed PDF text
- ✅ Completed ALL 9 Phase A checks (Japanese display, figure rendering, captions, numbering, overflow, references, compilation, figure presence)
- ✅ Completed ALL 12 Phase B checks (typos, grammar, logic, data accuracy, citations, terminology, completeness, readability, coherence, facts, missing content, redundancy)
- ✅ Fixed all Critical issues
- ✅ Fixed all Important issues
- ✅ Recompiled PDF after fixes
- ✅ Re-verified all fixes worked

**If you cannot check ALL boxes above, DO NOT proceed to Step 11. Go back and complete the missing checks.**

---

### Step 11: Save Report Version

**IMPORTANT**: After completing quality checks and final verification, save the report as a version.

1. **Save current report**:
   ```bash
   .claude/scripts/version-manager.sh save "Description of this version"
   ```

   Example descriptions:
   - "Initial complete report"
   - "Added chapter on methodology"
   - "Revised introduction and conclusion"
   - "Added 3 new sections on experimental results"

2. **Version information**:
   - Versions are numbered sequentially: v1, v2, v3...
   - Saved to `versions/` directory
   - Includes entire `report/` directory (PDF, LaTeX, figures)
   - Allows restoration of previous versions if needed

3. **When to save versions**:
   - After completing a full report for the first time
   - After making significant additions or revisions
   - Before making major changes (as a backup)
   - When user requests additional content

4. **Inform user**:
   - Tell user the version number (e.g., "Saved as v2")
   - Explain they can restore previous versions with: `.claude/scripts/version-manager.sh restore v1`
   - List all versions with: `.claude/scripts/version-manager.sh list`

### Step 12: Download Referenced Papers

**PURPOSE**: Automatically download PDFs of cited papers and web pages for NotebookLM and further analysis.

**IMPORTANT**: This step runs automatically after version is saved.

⚠️ **Reference format requirement**: `download-references.py` requires references in **BibTeX format** (`.bib` file) or as DOI/arXiv/PMID entries parseable from `.tex` files. It does **NOT** support manual `\begin{enumerate}...\item` numbered lists. If the report uses a manual enumerate reference list (which is common), this script will find no references to download — skip this step and inform the user.

**To check compatibility before running**:
```bash
# If references are in BibTeX format (.bib file exists):
ls report/*.bib  # → run download-references.py normally

# If references are manual \item list (no .bib file):
grep -c "\\\\bibitem\|\\\\bibliography" report/*.tex  # → if 0, skip Step 12
```

1. **Automatic execution** (only if BibTeX/parseable format confirmed):
   ```bash
   python3 .claude/scripts/download-references.py
   ```

   This will:
   - Auto-detect .bib or .tex files in report/ directory
   - Extract DOIs, arXiv IDs, PubMed IDs, and URLs from references
   - Download open access PDFs to `references/papers/`
   - **Convert web pages to PDF** (if wkhtmltopdf is installed)
   - Show summary of successful/failed downloads

2. **What gets downloaded/converted**:
   - ✅ arXiv papers (always available)
   - ✅ Open access papers via Unpaywall
   - ✅ PubMed Central (PMC) papers
   - ✅ Web pages converted to PDF (requires wkhtmltopdf)
   - ❌ Paywalled papers (require institutional access)

3. **Web page PDF conversion**:
   - Automatically detects web URLs in references
   - Converts HTML pages to PDF format
   - Preserves layout and formatting
   - Requires `wkhtmltopdf` (install with: `sudo apt-get install wkhtmltopdf`)
   - Skip web page conversion: `python3 .claude/scripts/download-references.py --no-webpages`

4. **Output**:
   - All files saved to: `references/papers/`
   - Papers: `arxiv_*.pdf`, `doi_*.pdf`, `pmid_*.pdf`
   - Web pages: `webpage_*.pdf`

5. **Inform user**:
   - Tell user how many papers were downloaded
   - Tell user how many web pages were converted to PDF
   - Location of downloaded PDFs: `references/papers/`
   - Mention that paywalled papers need manual download
   - Mention if wkhtmltopdf is not installed (web pages skipped)
   - **Suggest importing all PDFs to NotebookLM for analysis**

**Common Issues and Fixes**:

**Phase A (PDF Format Issues)**:

| Issue | Fix |
|-------|-----|
| "Table 1" instead of "表1" | Add `\renewcommand{\tablename}{表}` to preamble |
| "Figure 1" instead of "図1" | Add `\renewcommand{\figurename}{図}` to preamble |
| Japanese text garbled in PDF body | Ensure `\setCJKmainfont{IPAexMincho}` is set in LaTeX preamble |
| **Japanese text garbled in figures (文字化け)** | **CRITICAL**: Regenerate figures with explicit Japanese font config. In Python: `matplotlib.rcParams['font.sans-serif'] = ['IPAexGothic']` and `fm.fontManager.addfont('/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf')`. Use `regenerate_figures.py` script or update figure generation code. |
| Figures missing from PDF | Check figures exist in `report/figures/` and paths in LaTeX are correct. Use `pdfimages -list report.pdf` to verify images are embedded. |
| Table overflow | Reduce column widths or use smaller font |
| Chapter-based numbering (Table 2.1) | Add `\counterwithout{table}{chapter}` |
| Missing references | Check all [N] citations have matching reference entries |

**Phase B (Content Quality Issues)**:

| Issue | Fix |
|-------|-----|
| Typos/誤変換 (e.g., "阻外剤" → "阻害剤") | Search and correct in report/{report_name}.tex |
| Grammar errors (助詞の誤用) | Rewrite sentence with proper particles (は/が/を/に) |
| Contradictory statements | Revise one of the conflicting statements for consistency |
| Data mismatch (table vs text) | Cross-check source data and correct the error |
| Inappropriate citation | Replace with more relevant reference or remove citation |
| Inconsistent terminology | Choose one term and replace all variants |
| Awkward phrasing | Rewrite sentence for clarity and natural flow |
| Missing context/unclear statement | Add explanatory sentence or rephrase with more detail |

## Bundled Resources

### references/latex_template.md
LaTeX template and formatting guide for direct LaTeX writing. Includes document structure, table/figure formatting, special character escaping, best practices.

**When to read**: Step 5 (CRITICAL - read before writing content in LaTeX format).

### references/writing_styles.md
Writing style guides for all report types (scientific, business, market research, etc.). Covers tone, voice, sentence structure, examples.

**When to read**: Step 2 (determine style) and Step 5 (writing).

### references/mcp_selection.md
MCP server selection guide by research topic. Topic-to-MCP mapping, search query optimization, multi-MCP strategies.

**When to read**: Step 3 (data collection strategy).

### references/deep_search_strategies.md
Guide for comprehensive deep searches using Task tool. When to use, how to invoke, ensuring completeness.

**When to read**: Step 3 (determine search depth).

### references/citation_formats.md
Citation format guidelines (numbered/author-year styles), special cases, reference list formatting.

**When to read**: Step 5 (writing) and Step 7 (references).

### scripts/generate_figure.py
Generate bar/line/pie charts and tables with Japanese font support.

**Features**:
- Automatic Japanese font detection and configuration
- **Minimum 14pt font size enforced globally** via rcParams
- Supports matplotlib visualizations with proper UTF-8 encoding
- Handles bar charts, line plots, pie charts, and complex multi-panel figures
- Fallback font configuration when Japanese system fonts are unavailable

**Usage**: Import functions or run standalone: `python3 generate_figure.py`

**When to use**: Step 6 (create visualizations).

**Japanese Font Setup**: The script automatically configures Japanese fonts (Noto Sans CJK JP, IPAexGothic, etc.). If fonts are missing, it provides installation instructions: `sudo apt-get install fonts-noto-cjk fonts-ipafont fonts-ipaexfont`

**Font Size Policy**: All figures must use **minimum 14pt** for all text elements. The script sets:
- `font.size = 14`, `axes.labelsize = 14`, `axes.titlesize = 16`
- `xtick.labelsize = 14`, `ytick.labelsize = 14`, `legend.fontsize = 14`
- `figure.titlesize = 18`
- Any per-element `fontsize=N` argument must also be ≥ 14


### scripts/convert_to_latex.py
Convert existing Markdown reports to LaTeX with XeLaTeX Japanese support.

**NOTE**: This script is for converting **existing Markdown files** to LaTeX. Since the skill now writes directly in LaTeX, this script is only needed for legacy Markdown reports or user-provided Markdown files.

**Features**:
- Full Japanese language support using xeCJK package with IPAex fonts
- Professional document formatting with chapters, sections, titlesec, fancyhdr
- Automatic table of contents, list of figures, list of tables
- Tables with centered cells and automatic overflow prevention using longtable
- Dynamic column width calculation based on number of columns
- Citation formatting with superscripts
- Figure embedding with [H] placement
- Handles complex tables, lists, and references

**Usage**:
```bash
python scripts/convert_to_latex.py input.md output.tex --compile
```

**When to use**: Only when converting existing Markdown files to LaTeX. Not used in normal report generation workflow.


### assets/figure_templates/
Example data templates for figures (bar_chart_template.json, table_template.json).
