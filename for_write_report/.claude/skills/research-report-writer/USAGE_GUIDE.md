# Research Report Writer - Usage Guide

## Recent Updates (2026-01-27)

### New Features

1. **LaTeX Output Format**
   - Full Japanese language support using XeLaTeX
   - Professional PDF generation with proper formatting
   - Automatic handling of citations, tables, and figures
   - Use `convert_to_latex.py` to convert Markdown reports to LaTeX

2. **Japanese Font Support in Figures**
   - Fixed character encoding issues in matplotlib-generated figures
   - Automatic font detection and configuration
   - Fallback options when system fonts are unavailable
   - Updated `generate_figure.py` with comprehensive Japanese font setup

3. **Complete Reference Lists**
   - ALWAYS generates full reference lists (no placeholders)
   - Each citation [1], [2], etc. includes complete bibliographic information
   - Formats: Author(s), Title, Journal, Year, Volume, Pages
   - Sequential numbering from [1] to [N]

## Output Formats

### Markdown (.md) - Default
```bash
# Output saved automatically to full_report.md
# Contains inline citations [1], [2], tables, and figure references
```

### HTML (.html) - For Browser PDF Export
```bash
python3 scripts/convert_to_html.py

# Then in browser:
# 1. Open kit_report_full.html
# 2. File → Print → Save as PDF
# 3. Adjust print settings for best results
```

### LaTeX (.tex) - Professional PDF
```bash
python3 scripts/convert_to_latex.py

# Compile with XeLaTeX:
xelatex kit_report_full.tex
xelatex kit_report_full.tex  # Run twice for TOC and references

# Requirements:
# - XeLaTeX installation
# - Japanese fonts (Noto Sans CJK JP or IPAexGothic)
```

## Figure Generation with Japanese Support

### Setup Japanese Fonts (One-time)

Install system fonts for proper Japanese rendering:
```bash
sudo apt-get update
sudo apt-get install fonts-noto-cjk fonts-ipafont fonts-ipaexfont
```

### Generate Figures

The `generate_figure.py` script automatically:
- Detects available Japanese fonts
- Configures matplotlib for UTF-8 support
- Falls back gracefully if fonts are missing
- Provides clear instructions for font installation

```bash
python3 generate_figure.py
# Generates all figures in figures/ directory
# - mutation_frequency.png
# - fig3_2_mutation_frequency.png
# - fig7_2_imatinib_efficacy.png
# - fig1_1_strategy_map.png
# - fig2_2_kit_diseases.png
# - fig8_6_market_size.png
```

## Writing Complete Reports

### Step-by-Step Process

1. **Create report structure** (or use existing `report_structure.md`)
2. **Run the skill** to write chapters with deep literature search
3. **Verify citations** - Skill automatically generates complete reference list
4. **Generate figures** with Japanese support
5. **Convert to desired format(s)**:
   - Keep `.md` for editing
   - Generate `.html` for quick PDF via browser
   - Generate `.tex` for professional LaTeX PDF

### Example Workflow

```bash
# 1. Write full report (done by skill)
# Creates kit_report_full.md with all chapters, tables, and complete references

# 2. Regenerate figures with proper Japanese fonts
python3 generate_figure.py

# 3. Create LaTeX version for professional PDF
python3 convert_to_latex.py
xelatex kit_report_full.tex
xelatex kit_report_full.tex

# 4. Or create HTML version for browser PDF
python3 convert_to_html.py
# Open kit_report_full.html in browser → Print to PDF
```

## Reference List Format

The skill ALWAYS generates complete reference lists. Example format:

```markdown
## 付録E 参考文献

1. Heinrich MC, Corless CL, Demetri GD, et al. Kinase mutations and imatinib response in patients with metastatic gastrointestinal stromal tumor. J Clin Oncol. 2003;21(23):4342-4349.

2. Demetri GD, von Mehren M, Blanke CD, et al. Efficacy and safety of imatinib mesylate in advanced gastrointestinal stromal tumors. N Engl J Med. 2002;347(7):472-480.

... (continues for all N citations)

146. Jorgensen WL. The many roles of computation in drug discovery. Science. 2004;303(5665):1813-1818.
```

## Troubleshooting

### Japanese Text Shows as Squares in Figures

**Problem**: matplotlib can't find Japanese fonts

**Solution**:
```bash
# Install Japanese fonts
sudo apt-get install fonts-noto-cjk fonts-ipafont

# Clear matplotlib cache
rm -rf ~/.cache/matplotlib

# Regenerate figures
python3 generate_figure.py
```

### LaTeX Compilation Fails

**Problem**: `! Package fontspec Error: The font "Noto Sans CJK JP" cannot be found.`

**Solution**:
```bash
# Install XeLaTeX and Japanese fonts
sudo apt-get install texlive-xetex fonts-noto-cjk

# Or edit convert_to_latex.py to use different font:
# Change: \setCJKmainfont{Noto Sans CJK JP}
# To: \setCJKmainfont{IPAexGothic}
```

### HTML PDF Export Has Broken Layout

**Problem**: Page breaks in wrong places

**Solution**: In browser print dialog:
- Enable "Background graphics"
- Set margins to "Default" or "None"
- Use "A4" paper size
- Adjust scale if needed (90-100%)

## Best Practices

1. **Always run generate_figure.py** after creating report to ensure figures have proper Japanese rendering
2. **Generate LaTeX version** for final professional distribution
3. **Keep Markdown version** as source of truth for editing
4. **Verify all citations** have matching entries in reference list (skill does this automatically)
5. **Test PDF generation** early to catch font/formatting issues

## Summary of Key Improvements

| Feature | Old Behavior | New Behavior |
|---------|-------------|--------------|
| Reference lists | Placeholders like "200+ references (planned)" | Complete lists with all [1]-[N] citations |
| Japanese text in figures | Garbled/missing characters | Proper rendering with font auto-detection |
| Output formats | Markdown only | Markdown + HTML + LaTeX support |
| PDF generation | Manual/external tools | Integrated HTML and LaTeX converters |
| Citation format | Inline only | Inline + complete bibliography |

## Contact & Support

For issues or feature requests, update the skill's SKILL.md file or create new documentation in the skill directory.
