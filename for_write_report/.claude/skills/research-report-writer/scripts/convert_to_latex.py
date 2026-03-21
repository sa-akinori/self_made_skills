#!/usr/bin/env python3
"""
Convert Markdown research report to LaTeX with Japanese support
Handles citations, tables, figures, and complex formatting
"""
import re
from pathlib import Path

def markdown_to_latex(md_file, tex_file):
    """Convert Markdown to LaTeX with Japanese support"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # LaTeX header with Japanese support
    latex = r"""\documentclass[12pt,a4paper]{report}

% Japanese language support - MUST be loaded first
\usepackage{fontspec}
\usepackage{xeCJK}

% Set fonts for Japanese text using system font names
\setCJKmainfont{IPAexMincho}
\setCJKsansfont{IPAexGothic}
\setCJKmonofont{IPAGothic}

% Set default fonts for Latin text
\setmainfont{Latin Modern Roman}
\setsansfont{Latin Modern Sans}
\setmonofont{Latin Modern Mono}

% Packages
\usepackage[margin=2.5cm]{geometry}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{tabularx}
\usepackage{array}
\usepackage{xcolor}
\usepackage{listings}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{float}
\usepackage{setspace}
\usepackage{hyperref}

% Hyperref setup
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,
    urlcolor=cyan,
    citecolor=red,
    pdftitle={Kit阻害剤開発 総合調査レポート},
    pdfauthor={Research Team},
    bookmarks=true,
}

% Header and footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\leftmark}
\fancyhead[R]{\thepage}
\fancyfoot[C]{Kit阻害剤開発 総合調査レポート}

% Title formatting
\titleformat{\chapter}[display]
  {\normalfont\huge\bfseries\color{blue!70!black}}
  {\chaptertitlename\ \thechapter}{20pt}{\Huge}
\titlespacing*{\chapter}{0pt}{-20pt}{20pt}

% Code listing style
\lstset{
    basicstyle=\ttfamily\small,
    breaklines=true,
    frame=single,
    backgroundcolor=\color{gray!10}
}

% Table settings
\renewcommand{\arraystretch}{1.0}

% Line spacing
\setstretch{1.5}

\begin{document}

% Title page
\begin{titlepage}
    \centering
    \vspace*{2cm}

    {\Huge\bfseries Kit阻害剤開発 総合調査レポート\par}
    \vspace{0.5cm}
    {\LARGE 変異耐性克服と次世代創薬戦略\par}
    \vspace{2cm}

    {\Large 作成日: 2026年1月27日\par}
    {\Large バージョン: 1.0\par}
    \vspace{1cm}

    {\large 分類: 科学技術調査レポート（詳細レベル4）\par}

    \vfill

    {\large Research Department\par}

\end{titlepage}

% Table of contents
\tableofcontents
\listoffigures
\listoftables

"""

    # Split content into lines for processing
    lines = content.split('\n')

    # Skip title and metadata (already in LaTeX header)
    start_idx = 0
    for i, line in enumerate(lines):
        if '## 目次' in line or '第1章' in line:
            start_idx = i
            break

    # Process content
    processed_lines = []
    in_table = False
    table_headers = []
    skip_toc = True
    table_counter = 0

    i = start_idx
    while i < len(lines):
        line = lines[i]

        # Skip table of contents section
        if '## 目次' in line or '## 図表リスト' in line:
            skip_toc = True
            i += 1
            continue

        if skip_toc and (line.startswith('**第') or line.startswith('# 第')):
            skip_toc = False

        if skip_toc and (line.strip().startswith('-') or line.strip().startswith('**第') or '...' in line):
            i += 1
            continue

        # Convert headers
        if line.startswith('# 第'):
            chapter_match = re.match(r'^# 第(\d+)章 (.+?)$', line)
            if chapter_match:
                num, title = chapter_match.groups()
                processed_lines.append(f'\n\\chapter{{{title}}}')
                processed_lines.append(f'\\label{{ch:{num}}}')
                i += 1
                continue

        if line.startswith('## '):
            section_title = line[3:].strip()
            if not any(x in section_title for x in ['目次', '図表リスト']):
                processed_lines.append(f'\n\\section{{{section_title}}}')
            i += 1
            continue

        if line.startswith('### '):
            subsection_title = line[4:].strip()
            processed_lines.append(f'\n\\subsection{{{subsection_title}}}')
            i += 1
            continue

        # Horizontal rules
        if line.strip() == '---':
            processed_lines.append('\\vspace{1em}\\hrule\\vspace{1em}')
            i += 1
            continue

        # Figures
        if line.strip().startswith('!['):
            match = re.match(r'!\[(.*?)\]\((.*?)\)', line.strip())
            if match:
                caption = match.group(1)
                path = match.group(2)
                processed_lines.append('\\begin{figure}[H]')
                processed_lines.append('\\centering')
                processed_lines.append(f'\\includegraphics[width=0.8\\textwidth]{{{path}}}')
                if caption:
                    processed_lines.append(f'\\caption{{{escape_latex(caption)}}}')
                processed_lines.append('\\end{figure}')
                processed_lines.append('')
                i += 1
                continue

        # Tables
        if '|' in line and not in_table:
            # Start table
            in_table = True
            table_counter += 1

            # Get headers
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            table_headers = cells
            num_cols = len(cells)

            # Calculate column width
            text_width = 14  # cm
            if num_cols > 5:
                text_width = 12
            col_width = text_width / num_cols

            # Use longtable for multi-page support with centered content
            # >{\centering\arraybackslash}m{width} centers both horizontally and vertically
            col_spec = '|' + '|'.join([f'>{{\\centering\\arraybackslash}}m{{{col_width:.1f}cm}}'] * num_cols) + '|'
            processed_lines.append(f'\\begin{{longtable}}{{{col_spec}}}')

            # Caption at the top of the table
            processed_lines.append(f'\\caption{{表 {table_counter}}} \\\\')
            processed_lines.append('\\hline')
            processed_lines.append(' & '.join([f'\\textbf{{{escape_latex(c)}}}' for c in cells]) + ' \\\\')
            processed_lines.append('\\hline')
            processed_lines.append('\\endfirsthead')
            processed_lines.append('')
            # Continued header for multi-page tables
            processed_lines.append(f'\\caption{{表 {table_counter} (続き)}} \\\\')
            processed_lines.append('\\hline')
            processed_lines.append(' & '.join([f'\\textbf{{{escape_latex(c)}}}' for c in cells]) + ' \\\\')
            processed_lines.append('\\hline')
            processed_lines.append('\\endhead')
            processed_lines.append('')
            processed_lines.append('\\hline')
            processed_lines.append('\\endfoot')
            processed_lines.append('')
            processed_lines.append('\\hline')
            processed_lines.append('\\endlastfoot')
            processed_lines.append('')
            i += 1

            # Skip separator line
            if i < len(lines) and '---' in lines[i]:
                i += 1
            continue

        elif '|' in line and in_table:
            # Check if separator line
            if re.match(r'^\|[\s\-:]+\|', line):
                i += 1
                continue

            # Data row
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if cells:
                processed_lines.append(' & '.join(escape_latex(c) for c in cells) + ' \\\\')
                processed_lines.append('\\hline')
            i += 1
            continue

        elif in_table and '|' not in line:
            # End table
            processed_lines.append('\\end{longtable}')
            processed_lines.append('')
            in_table = False
            table_headers = []

        # Citations [1], [2], etc.
        line = re.sub(r'\[(\d+)\]', r'\\textsuperscript{[\\1]}', line)

        # Bold and italic
        line = re.sub(r'\*\*\*(.*?)\*\*\*', r'\\textbf{\\textit{\\1}}', line)
        line = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\\1}', line)
        line = re.sub(r'\*(.*?)\*', r'\\textit{\\1}', line)

        # Inline code
        line = re.sub(r'`([^`]+)`', r'\\texttt{\\1}', line)

        # Links
        line = re.sub(r'\[(.*?)\]\((.*?)\)', r'\\href{\\2}{\\1}', line)

        # Lists
        if line.strip().startswith('- '):
            if i == 0 or not lines[i-1].strip().startswith('- '):
                processed_lines.append('\\begin{itemize}')
            item = line.strip()[2:]
            processed_lines.append(f'\\item {escape_latex(item)}')
            if i == len(lines) - 1 or not lines[i+1].strip().startswith('- '):
                processed_lines.append('\\end{itemize}')

        elif re.match(r'^\d+\. ', line.strip()):
            if i == 0 or not re.match(r'^\d+\. ', lines[i-1].strip()):
                processed_lines.append('\\begin{enumerate}')
            item = re.sub(r'^\d+\. ', '', line.strip())
            processed_lines.append(f'\\item {escape_latex(item)}')
            if i == len(lines) - 1 or not re.match(r'^\d+\. ', lines[i+1].strip()):
                processed_lines.append('\\end{enumerate}')

        # Regular paragraphs
        elif line.strip() and not line.startswith('%') and not in_table:
            processed_lines.append(escape_latex(line))

        elif not line.strip():
            processed_lines.append('')

        i += 1

    # Close any open table
    if in_table:
        processed_lines.append('\\end{longtable}')

    # Add all processed lines
    latex += '\n'.join(processed_lines)

    # Document end
    latex += """

\\end{document}
"""

    # Write output
    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(latex)

    print(f"✅ LaTeX file created: {tex_file}")
    print(f"📄 Compile with: xelatex {tex_file}")
    print(f"   (Run twice for proper references)")

def escape_latex(text):
    """Escape special LaTeX characters"""
    # Characters that need escaping
    replacements = {
        '\\': '\\textbackslash{}',
        '&': '\\&',
        '%': '\\%',
        '$': '\\$',
        '#': '\\#',
        '_': '\\_',
        '{': '\\{',
        '}': '\\}',
        '~': '\\textasciitilde{}',
        '^': '\\textasciicircum{}',
    }

    # Don't escape if already in LaTeX command
    if '\\' in text and any(cmd in text for cmd in ['\\textbf', '\\textit', '\\href', '\\textsuperscript']):
        return text

    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    return text

if __name__ == '__main__':
    import sys
    import subprocess

    if len(sys.argv) < 2:
        print("Usage: python convert_to_latex.py input.md [output.tex] [--compile]")
        print("  input.md: Input Markdown file")
        print("  output.tex: Output LaTeX file (optional, defaults to input.tex)")
        print("  --compile: Automatically compile to PDF with xelatex (optional)")
        sys.exit(1)

    input_file = sys.argv[1]

    # Determine output file
    if len(sys.argv) >= 3 and not sys.argv[2].startswith('--'):
        output_file = sys.argv[2]
    else:
        output_file = input_file.replace('.md', '.tex')

    # Check for --compile flag
    compile_pdf = '--compile' in sys.argv

    # Convert
    markdown_to_latex(input_file, output_file)

    # Compile if requested
    if compile_pdf:
        print("\n🔨 Compiling LaTeX to PDF...")
        for i in range(3):
            print(f"   Pass {i+1}/3...")
            result = subprocess.run(
                ['xelatex', '-interaction=nonstopmode', output_file],
                capture_output=True,
                text=True
            )

        pdf_file = output_file.replace('.tex', '.pdf')
        if Path(pdf_file).exists():
            size_kb = Path(pdf_file).stat().st_size / 1024
            print(f"✅ PDF created: {pdf_file} ({size_kb:.1f} KB)")

            # Clean up auxiliary files
            base_name = output_file.replace('.tex', '')
            for ext in ['.aux', '.log', '.out', '.toc', '.lof', '.lot']:
                aux_file = base_name + ext
                if Path(aux_file).exists():
                    Path(aux_file).unlink()
            print("🧹 Cleaned up auxiliary files")
        else:
            print(f"❌ PDF compilation failed. Check {output_file.replace('.tex', '.log')}")
