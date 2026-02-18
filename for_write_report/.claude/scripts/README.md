# Research Kit Utility Scripts

This directory contains utility scripts to enhance your research report workflow.

## 📸 Version Manager

Manage report versions for iterative improvements.

### Features

- Save complete report snapshots (v1, v2, v3...)
- Restore previous versions
- Compare differences between versions
- Track version history with descriptions

### Usage

**Save current report as new version:**
```bash
.claude/scripts/version-manager.sh save "Initial complete report"
.claude/scripts/version-manager.sh save "Added methodology chapter"
.claude/scripts/version-manager.sh save "Revised introduction and conclusion"
```

**List all versions:**
```bash
.claude/scripts/version-manager.sh list
```

**Restore a previous version:**
```bash
.claude/scripts/version-manager.sh restore v1
```

**Compare two versions:**
```bash
.claude/scripts/version-manager.sh diff v1 v2
```

**View version details:**
```bash
.claude/scripts/version-manager.sh info v2
```

### When to Save Versions

- ✅ After completing a full report for the first time
- ✅ After making significant additions or revisions
- ✅ Before making major changes (as a backup)
- ✅ When user requests additional content

### Version Storage

- Location: `versions/` directory in project root
- Each version includes: PDF, LaTeX files, figures, all assets
- Metadata tracked: timestamp, description, file sizes

## 📚 Reference Downloader

Automatically download PDFs of cited papers and convert web pages to PDF.

### Features

- Extract identifiers from BibTeX and LaTeX files
- Download from arXiv, Unpaywall, PubMed Central
- **Convert web pages to PDF** (requires wkhtmltopdf)
- Organize all PDFs for NotebookLM import
- Summary of successful/failed downloads and conversions

### Usage

**Auto-detect and download:**
```bash
python3 .claude/scripts/download-references.py
```

This automatically finds .bib or .tex files in `report/` directory.

**Specify input file:**
```bash
# From BibTeX file
python3 .claude/scripts/download-references.py report/references.bib

# From LaTeX file
python3 .claude/scripts/download-references.py report/report.tex
```

**Custom output directory:**
```bash
python3 .claude/scripts/download-references.py -o custom/path
```

**Quiet mode (less output):**
```bash
python3 .claude/scripts/download-references.py --quiet
```

**Adjust download delay:**
```bash
python3 .claude/scripts/download-references.py --delay 5
```

**Skip web page conversion:**
```bash
python3 .claude/scripts/download-references.py --no-webpages
```

### What Gets Downloaded/Converted

| Source | Availability | Notes |
|--------|--------------|-------|
| arXiv papers | ✅ Always available | Direct PDF download |
| Open access papers (via Unpaywall) | ✅ When available | Direct PDF download |
| PubMed Central papers | ✅ When available | Direct PDF download |
| Web pages | ✅ When wkhtmltopdf installed | Converted to PDF |
| Paywalled papers | ❌ Requires institutional access | Manual download needed |

### Requirements

**For web page PDF conversion:**
```bash
sudo apt-get install wkhtmltopdf
```

If not installed, web pages will be skipped automatically.

### Output

- Downloaded/Converted PDFs: `references/papers/`
- Filename format:
  - arXiv: `arxiv_1234.5678.pdf`
  - DOI: `doi_10.1234_xxxxx.pdf`
  - PubMed: `pmid_12345678.pdf`
  - Web pages: `webpage_<domain>_<path>.pdf`

### NotebookLM Integration

After downloading:
1. Open NotebookLM
2. Create new notebook
3. Upload all PDFs from `references/papers/`
4. Ask NotebookLM to analyze and summarize

## 🔧 Discord Notifier

Send notifications to Discord (configured in hooks).

### Usage

**Manual notification:**
```bash
.claude/hooks/discord-notify.sh "Your message" "color_code"
```

**Color codes (decimal):**
- Green (success): `3066993`
- Orange (warning): `16753920`
- Red (error): `15158332`
- Blue (info): `3447003`

**Examples:**
```bash
.claude/hooks/discord-notify.sh "Test notification" "3066993"
.claude/hooks/discord-notify.sh "Warning message" "16753920"
```

### Configuration

Edit `.claude/hooks/discord-notify.sh`:
```bash
DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR/URL"
```

Or use environment variable (more secure):
```bash
export DISCORD_WEBHOOK_URL_CLAUDE="your_webhook_url"
```

## 📋 Workflow Integration

### Typical Workflow

1. **Create initial report:**
   ```bash
   skill research-report-writer-orchestration
   ```

2. **Save as version 1:**
   ```bash
   .claude/scripts/version-manager.sh save "Initial complete report"
   ```

3. **Download referenced papers:**
   ```bash
   python3 .claude/scripts/download-references.py
   ```

4. **User requests additions:**
   - "Add chapter on X"
   - "Expand section on Y"

5. **Generate updated report:**
   ```bash
   skill research-report-writer
   ```

6. **Save as version 2:**
   ```bash
   .claude/scripts/version-manager.sh save "Added chapter on X and expanded Y"
   ```

7. **Compare versions:**
   ```bash
   .claude/scripts/version-manager.sh diff v1 v2
   ```

### Automatic Integration

The `research-report-writer` skill automatically:
- ✅ Adds inline explanations for technical terms
- ✅ Performs quality checks
- ✅ Saves version after completion
- ✅ Optionally downloads references

## 📖 Technical Term Explanations

When writing reports, technical terms are automatically explained inline:

**Format:**
```
専門用語（English: 簡単な説明）
```

**Example:**
```
機械学習（Machine Learning: データからパターンを自動的に学習する技術）
```

**Rules:**
- Explanation added at first occurrence only
- Concise (1 sentence or phrase)
- Context-appropriate for target audience
- No separate glossary section

## 🆘 Troubleshooting

### Version Manager

**"Error: report/ directory not found"**
- Generate a report first before saving versions

**Restore fails**
- Check version exists: `.claude/scripts/version-manager.sh list`
- Use correct version name (e.g., `v1`, not `1`)

### Reference Downloader

**"No .bib or .tex files found"**
- Ensure report has been generated in `report/` directory
- Specify file manually: `python3 .claude/scripts/download-references.py path/to/file.bib`

**Many failed downloads**
- Normal for paywalled papers
- Download manually via institutional access
- Check if papers are truly cited (not just mentioned)

**HTTP errors**
- Some servers may block requests
- Increase delay: `--delay 5`
- Download manually from publisher

**Web page conversion not working**
- Check if wkhtmltopdf is installed: `which wkhtmltopdf`
- Install if missing: `sudo apt-get install wkhtmltopdf`
- Skip web pages if not needed: `--no-webpages`

**Web page conversion timeout or errors**
- Some pages may be too complex or have JavaScript issues
- Download the page manually and save as PDF from browser
- Increase timeout in script if needed

### Discord Notifications

**"Warning: Discord Webhook URL not configured"**
- Edit `.claude/hooks/discord-notify.sh`
- Set `DISCORD_WEBHOOK_URL` variable

**No notifications appearing**
- Verify webhook URL is correct
- Check Discord channel permissions
- Test manually: `.claude/hooks/discord-notify.sh "Test" "3066993"`

## 📚 Additional Resources

- Version control best practices: Save before major changes
- NotebookLM: https://notebooklm.google.com/
- Discord webhooks: Server Settings → Integrations → Webhooks

---

**Happy Research! 📝✨**
