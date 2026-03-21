# LaTeX Template for Research Reports

このファイルは、research-report-writerスキルでレポートを直接LaTeX形式で執筆する際のテンプレートとガイドラインです。

## 基本的なドキュメント構造

```latex
\documentclass[11pt,a4paper]{report}

% Japanese language support - MUST be loaded first
\usepackage{fontspec}
\usepackage{xeCJK}

% Set fonts for Japanese text
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
\usepackage{chngcntr}
\usepackage{hyperref}

% Remove chapter numbering from figures and tables (continuous numbering)
\counterwithout{figure}{chapter}
\counterwithout{table}{chapter}

% Hyperref setup
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,
    urlcolor=cyan,
    citecolor=red,
    pdftitle={レポートタイトル},
    pdfauthor={Research Team},
    bookmarks=true,
}

% Header and footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\leftmark}
\fancyhead[R]{\thepage}
\fancyfoot[C]{レポートタイトル}

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

% Caption settings
\captionsetup[table]{position=top}
\captionsetup[figure]{position=bottom}

% Japanese caption names
\renewcommand{\tablename}{表}
\renewcommand{\figurename}{図}

% Line spacing
\setstretch{1.2}

\begin{document}

% Title page
\begin{titlepage}
    \centering
    \vspace*{2cm}
    {\Huge\bfseries レポートタイトル\par}
    \vspace{0.5cm}
    {\LARGE サブタイトル\par}
    \vspace{2cm}
    {\Large 作成日: 2026年1月28日\par}
    {\Large バージョン: 1.0\par}
    \vspace{1cm}
    {\large 分類: 調査レポート\par}
    \vfill
    {\large Research Department\par}
\end{titlepage}

% Table of contents
\tableofcontents
\listoffigures
\listoftables

% ここからコンテンツ

\chapter{第1章のタイトル}
\label{ch:1}

コンテンツ...

\section{セクション}

コンテンツ...

\subsection{サブセクション}

コンテンツ...

\end{document}
```

## 文書要素の書き方

### 1. 章・節・小節

```latex
\chapter{第1章のタイトル}
\label{ch:1}

\section{セクションタイトル}

\subsection{サブセクションタイトル}

\subsubsection{サブサブセクションタイトル}
```

### 2. 段落と改行

```latex
これは段落です。

新しい段落は空行で区切ります。

強制改行は\\を使います。\\
次の行はここから始まります。
```

### 3. テキスト装飾

```latex
\textbf{太字}

\textit{イタリック}

\textbf{\textit{太字とイタリック}}

\texttt{等幅フォント（コード）}

\underline{下線}
```

### 4. リスト

**箇条書き**:
```latex
\begin{itemize}
\item 第1項目
\item 第2項目
\item 第3項目
\end{itemize}
```

**番号付きリスト**:
```latex
\begin{enumerate}
\item 第1項目
\item 第2項目
\item 第3項目
\end{enumerate}
```

### 5. 表（longtable、中央揃え、キャプション上）

**基本的な表**:
```latex
\begin{longtable}{|>{\centering\arraybackslash}m{4cm}|>{\centering\arraybackslash}m{4cm}|>{\centering\arraybackslash}m{4cm}|}
\caption{表のキャプション} \\
\hline
\textbf{ヘッダー1} & \textbf{ヘッダー2} & \textbf{ヘッダー3} \\
\hline
\endfirsthead

\caption{表のキャプション (続き)} \\
\hline
\textbf{ヘッダー1} & \textbf{ヘッダー2} & \textbf{ヘッダー3} \\
\hline
\endhead

\hline
\endfoot

\hline
\endlastfoot

データ1 & データ2 & データ3 \\
\hline
データ4 & データ5 & データ6 \\
\hline
\end{longtable}
```

**重要**:
- キャプションには"表 1:"のような番号を含めない
- LaTeXが自動的に"表1"、"表2"と連続番号を付与する
- 章をまたいでも連続番号（表1、表2、表3...）となる

**列幅の計算**:
- 3列の場合: 14cm ÷ 3 = 約4.7cm
- 4列の場合: 14cm ÷ 4 = 3.5cm
- 5列の場合: 14cm ÷ 5 = 2.8cm
- 6列以上: 12cm ÷ 列数

**セルの揃え**:
- 中央揃え（推奨）: `>{\centering\arraybackslash}m{幅}`
- 左揃え: `>{\raggedright\arraybackslash}m{幅}`
- 右揃え: `>{\raggedleft\arraybackslash}m{幅}`

### 6. 図（キャプション下）

```latex
\begin{figure}[H]
\centering
\includegraphics[width=0.7\textwidth]{figures/filename.png}
\caption{図のキャプション}
\label{fig:1}
\end{figure}
```

**重要**:
- キャプションには"図 1:"のような番号を含めない
- LaTeXが自動的に"図1"、"図2"と連続番号を付与する
- 章をまたいでも連続番号（図1、図2、図3...）となる

**図のサイズ**:
- 小さい図: `width=0.5\textwidth`
- 標準: `width=0.7\textwidth`
- 大きい図: `width=0.9\textwidth`
- 全幅: `width=\textwidth`

### 7. 引用・参照

**文献引用**:
```latex
この研究では重要な発見がありました\textsuperscript{[1]}。
複数の文献を引用する場合\textsuperscript{[2,3,4]}。
```

**図表の参照**:
```latex
図\ref{fig:1}に示すように...
表\ref{tab:1}を参照してください。
```

### 8. 特殊文字のエスケープ

LaTeXで特別な意味を持つ文字はエスケープが必要:

```latex
\&  % &
\%  % %
\$  % $
\#  % #
\_  % _
\{  % {
\}  % }
\textasciitilde{}  % ~
\textasciicircum{}  % ^
\textbackslash{}   % \
```

### 9. 水平線

```latex
\vspace{1em}
\hrule
\vspace{1em}
```

### 10. リンク

```latex
\href{https://example.com}{リンクテキスト}
```

## 参考文献セクション

```latex
\chapter{参考文献}

\begin{enumerate}
\item Vaswani A, Shazeer N, Parmar N, et al. Attention is all you need. In: Proceedings of NeurIPS 2017; 2017. p. 5998-6008.
\item Devlin J, Chang MW, Lee K, Toutanova K. BERT: Pre-training of deep bidirectional transformers for language understanding. In: Proceedings of NAACL-HLT 2019; 2019. p. 4171-4186.
\item ...
\end{enumerate}
```

または、longtableを使用:

```latex
\chapter{参考文献}

\begin{longtable}{|>{\raggedright\arraybackslash}m{1.5cm}|>{\raggedright\arraybackslash}m{12.5cm}|}
\hline
\textbf{番号} & \textbf{文献} \\
\hline
\endfirsthead
\hline
\textbf{番号} & \textbf{文献} \\
\hline
\endhead
\hline
\endfoot
\hline
\endlastfoot

[1] & Vaswani A, Shazeer N, Parmar N, et al. Attention is all you need. In: Proceedings of NeurIPS 2017; 2017. p. 5998-6008. \\
\hline
[2] & Devlin J, Chang MW, Lee K, Toutanova K. BERT: Pre-training of deep bidirectional transformers for language understanding. In: Proceedings of NAACL-HLT 2019; 2019. p. 4171-4186. \\
\hline
\end{longtable}
```

## ベストプラクティス

1. **表のキャプションは表の上**: `\caption{...}`を最初に配置
2. **図のキャプションは図の下**: `\caption{...}`を最後に配置
3. **表のセルは中央揃え**: `>{\centering\arraybackslash}m{幅}`を使用
4. **表の行間は標準**: `\arraystretch{1.0}`
5. **本文の行間は読みやすく**: `\setstretch{1.2}` (11ptフォント推奨)
6. **特殊文字は必ずエスケープ**: `&`, `%`, `$`, `#`, `_` など
7. **図は[H]配置**: その場所に固定
8. **列幅は均等分割**: テキスト幅を列数で割る

## 注意事項

### よくあるエラー

1. **特殊文字のエスケープ忘れ**
   ```latex
   % 誤り
   50% improvement

   % 正しい
   50\% improvement
   ```

2. **表の列数と区切り文字の不一致**
   ```latex
   % 誤り（3列定義だが2つしかデータがない）
   \begin{longtable}{|m{3cm}|m{3cm}|m{3cm}|}
   A & B \\  % エラー

   % 正しい
   \begin{longtable}{|m{3cm}|m{3cm}|m{3cm}|}
   A & B & C \\
   ```

3. **日本語フォント未設定**
   - 必ず文書の最初で`\setCJKmainfont{IPAexMincho}`を設定

4. **パッケージの読み込み順序**
   - `fontspec`と`xeCJK`は最初に読み込む
   - `hyperref`は最後に読み込む

## まとめ

このテンプレートに従って執筆すれば、高品質なPDFレポートが生成できます。特に表と図のフォーマットに注意してください。
