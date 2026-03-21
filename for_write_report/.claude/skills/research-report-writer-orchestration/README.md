# Research Report Writer Orchestration

Complete research report generation pipeline that orchestrates all five report generation skills automatically.

## Quick Start

```bash
# In your research project directory with report.md
skill research-report-writer-orchestration
```

The orchestrator will guide you through the entire process from start to finish.

## What This Does

Automatically runs the complete workflow:

```
report.md
   ↓
[Enhancer] → update_report.md
   ↓
[Planner] → report_structure.md
   ↓
[Recommender] → mcp-servers/install-skills.txt
   ↓
[Installer] → Install tools to ./skills/ and ./mcp-servers/
   ↓
[Writer] → report/{name}.pdf
   ↓
Complete! 🎉
```

## Prerequisites

1. **Create report.md** in your project directory with:
   ```markdown
   # Your Research Topic

   - Investigation point 1
   - Investigation point 2
   - Investigation point 3
   ```

2. **All five skills must be available**:
   - research-report-enhancer
   - research-report-structure-planner
   - skill-recommender
   - skill-mcp-installer
   - research-report-writer

## Usage Modes

### Mode 1: Full Automation (Recommended for First-Time)

Run all steps from start to finish:
- Topic enhancement
- Structure planning
- Tool recommendation and installation
- Report writing and compilation

**Estimated time**: 1-4 hours

### Mode 2: Skip Optional Steps

If you already have tools installed or want faster execution:
- Skip topic enhancement
- Skip tool recommendation/installation
- Only run planner and writer

**Estimated time**: 30-60 minutes

### Mode 3: Resume from Interruption

If the pipeline was interrupted:
- Automatically detects completed steps
- Resumes from where you left off
- Preserves all intermediate files

**Estimated time**: Depends on where you left off

## User Interaction Points

The orchestrator will ask for your input at these key points:

1. **Initial setup**: Choose workflow mode (full/skip/custom)
2. **After enhancement**: Review suggestions, create update_report.md
3. **After planning**: Approve or regenerate structure
4. **Tool recommendation**: Choose how many tools to recommend
5. **Tool installation**: Confirm installation
6. **Report writing**: Select chapters, confirm parameters

You can choose automatic progression to minimize interruptions.

## Generated Files

After completion, you'll have:

```
project/
├── update_report.md                 # Enhanced research topics
├── report_structure.md              # Detailed chapter structure
├── mcp-servers/
│   └── install-skills.txt           # Tool list
├── skills/                          # Installed Claude skills
├── mcp-servers/                     # Installed MCP servers
└── report/
    ├── {name}.tex                   # LaTeX source
    ├── {name}.pdf                   # Final PDF report
    └── figures/                     # Generated figures
```

## Examples

### Example 1: Complete First-Time Report

```
$ skill research-report-writer-orchestration

Pipeline: Full workflow
├─ ✓ Pre-flight check: report.md found
├─ ✓ Topic enhancement: 8 suggestions added
├─ ✓ Structure planning: 12 chapters, 45 sections
├─ ✓ Tool recommendation: 8 tools recommended
├─ ✓ Tool installation: 8 tools installed
└─ ✓ Report writing: 35-page PDF generated

Time: 2h 15m
Output: report/research_report.pdf (880 KB)
```

### Example 2: Quick Report (Tools Already Installed)

```
$ skill research-report-writer-orchestration

Pipeline: Skip tools
├─ ✓ Pre-flight check: report.md found
├─ ⊘ Topic enhancement: skipped
├─ ✓ Structure planning: 8 chapters, 28 sections
├─ ⊘ Tool recommendation: skipped
├─ ⊘ Tool installation: skipped
└─ ✓ Report writing: 25-page PDF generated

Time: 45m
Output: report/quick_report.pdf (620 KB)
```

### Example 3: Resume After Interruption

```
$ skill research-report-writer-orchestration

Pipeline: Resume
├─ ✓ Pre-flight check: found existing progress
│   • update_report.md exists
│   • report_structure.md exists
│   • Tools already installed
├─ ⊘ Steps 2-5: already completed
└─ ✓ Report writing: 30-page PDF generated

Time: 50m
Output: report/final_report.pdf (750 KB)
```

## Error Handling

If something goes wrong:

1. **Error is displayed clearly** with context
2. **You can choose to**:
   - Retry the failed step
   - Skip the step and continue
   - Stop the pipeline
3. **Progress is saved**: You can resume later

## Advanced Usage

### Running Specific Steps Only

If you want more control, run each skill individually:

```bash
# Just enhancement
skill research-report-enhancer

# Just planning
skill research-report-structure-planner

# Just writing
skill research-report-writer
```

### Regenerating Parts of the Report

If you want to update specific chapters:

1. Edit `report_structure.md` or `update_report.md`
2. Run `skill research-report-writer`
3. Select only the chapters you want to regenerate

### Using Different Parameters

The orchestrator uses recommended defaults, but you can:
- Edit intermediate files manually
- Run individual skills with custom parameters
- Regenerate any step without re-running everything

## Troubleshooting

### "Pipeline seems stuck"
→ Check if a skill is waiting for user input

### "Steps are being skipped"
→ Intermediate files already exist. Choose "Start fresh" to regenerate

### "Tools not working during writing"
→ Check that tool installation completed: `ls mcp-servers/`

### "LaTeX compilation failed"
→ The writer has built-in quality checks. Review the error in the .log file

## Tips for Best Results

1. **First time**: Run the full pipeline to set everything up
2. **Subsequent reports**: Skip tool steps if already installed
3. **Large reports**: Consider writing chapters one at a time
4. **Review intermediate files**: Check update_report.md and report_structure.md before writing
5. **Save time**: Use automatic progression mode after you're familiar with the workflow

## Time Estimates

- **Pre-flight check**: 1 min
- **Topic enhancement**: 5-10 min
- **Structure planning**: 3-5 min
- **Tool recommendation**: 5-10 min
- **Tool installation**: 5-20 min
- **Report writing**: 30 min - 3 hours ⏰
- **Summary**: 1 min

**Total**: 1-4 hours (depends on report size and complexity)

The writing step takes the longest because it:
- Conducts literature searches for each chapter
- Generates figures and tables
- Writes content in LaTeX
- Compiles to PDF
- Performs quality checks

## Comparison with Manual Workflow

| Task | Manual | Orchestrated |
|------|--------|--------------|
| Run each skill | 5 separate commands | 1 command |
| Create intermediate files | Manual | Automatic |
| Track progress | Manual notes | Automatic tracking |
| Handle errors | Investigate yourself | Guided recovery |
| Resume after interruption | Remember where you left off | Automatic detection |
| Time spent on coordination | 15-30 min | 0 min |

## Support

For issues or questions:
- Check the main SKILL.md for detailed workflow documentation
- Review individual skill documentation for specific steps
- Check error messages carefully - they include recovery suggestions

---

**Happy Report Writing! 📝✨**
