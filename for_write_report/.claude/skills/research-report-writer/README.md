# Research Report Writer

包括的な研究レポートを**直接LaTeX形式**で生成するスキルです。

## 概要

このスキルは、`report_structure.md` に基づいて、深い文献調査を行い、**LaTeX形式で直接執筆**し、高品質なPDFレポートを生成します。

### 主な機能

✅ **直接LaTeX執筆**: Markdownを経由せず、直接LaTeX形式でコンテンツを書く
✅ **日本語完全対応**: XeLaTeXとIPAexフォントでプロフェッショナルなPDF生成
✅ **深い文献調査**: MCP servers (PubMed, Google Scholar, ChEMBL等) を使用
✅ **図表の自動生成**: matplotlib で日本語ラベル付きの図を生成
✅ **完全な参考文献**: 全ての参考文献を完全に記載（省略なし）
✅ **表の最適化**: 中央揃え、キャプション上配置、longtableで自動調整
✅ **図の最適化**: キャプション下配置、適切な位置固定

## 使用方法

### 1. レポート構造の定義

`report_structure.md` にレポートの構造を定義します：

```markdown
# Report Title

## Chapter 1: Introduction
- Section 1.1
- Section 1.2

## Chapter 2: Background
...
```

### 2. レポートの生成

research-report-writerスキルを使用してレポートを生成します。スキルは：

1. **LaTeX形式で直接執筆**: コンテンツを`{report_name}.tex`に書く
2. **PDF生成**: `xelatex`で3回コンパイル
3. **完成**: `{report_name}.pdf`が生成される

**ワークフロー**:
```
データ収集 → LaTeX執筆 → xelatex × 3 → PDF完成
```

### 3. 既存Markdownの変換（オプション）

既存のMarkdownファイルをLaTeXに変換する場合のみ：

```bash
# 変換 + PDF生成
python research-report-writer/scripts/convert_to_latex.py input.md --compile
```

**注意**: 通常のレポート生成では、この変換ステップは不要です（直接LaTeXで書くため）。

## 出力形式

### デフォルト出力: LaTeX → PDF

**ファイル**:
- `{name}.tex` - LaTeX ソースファイル（主要な作業ファイル）
- `{name}.pdf` - 最終PDF（成果物）

**LaTeX の特徴**:
- **日本語フォント**: IPAexMincho (本文), IPAexGothic (見出し)
- **ドキュメントクラス**: report (章、節、小節の構造)
- **フォントサイズ**: 11pt（読みやすく、適度にコンパクト）
- **本文行間**: 1.2（読みやすく、効率的なページ密度）
- **自動生成**: タイトルページ、目次、図表リスト
- **表の設定**:
  - longtable（複数ページ対応）
  - 中央揃えセル: `>{\centering\arraybackslash}m{幅}`
  - キャプション: 表の上に配置、日本語（**表1**、**表2**、**表3**...）
  - 番号: 章をまたいで連続
  - 行間: 1.0（標準）
  - 自動列幅調整: テキスト幅を列数で均等分割
- **図の設定**:
  - [H] 配置で位置固定
  - キャプション: 図の下に配置、日本語（**図1**、**図2**、**図3**...）
  - 番号: 章をまたいで連続
  - サイズ: 0.7\textwidth（標準）
- **引用**: 上付き文字 [1], [2] 形式
- **品質保証**: 自動品質チェックと修正ループを実施

### その他の形式（オプション）

- **HTML**: `convert_to_html.py` でブラウザ印刷用のHTMLを生成（レガシー用）
- **Markdown**: 既存のMarkdownファイルがある場合のみ

## ファイル構成

```
research-report-writer/
├── SKILL.md                     # スキル定義
├── README.md                    # このファイル
├── references/
│   ├── writing_styles.md        # 文書スタイルガイド
│   ├── mcp_selection.md         # MCP server 選択ガイド
│   ├── deep_search_strategies.md # 深い検索戦略
│   └── citation_formats.md      # 引用形式ガイド
└── scripts/
    ├── generate_figure.py       # 図表生成（日本語フォント対応）
    ├── convert_to_latex.py      # Markdown → LaTeX 変換
    ├── convert_to_html.py       # Markdown → HTML 変換
    └── merge_chapters.py        # 章の統合（オプション）
```

## 必要な環境

### LaTeX (必須)

```bash
# XeLaTeX と日本語フォント
sudo apt-get install texlive-xetex
sudo apt-get install fonts-ipafont fonts-ipaexfont

# 追加LaTeXパッケージ
sudo apt-get install texlive-latex-extra texlive-fonts-extra
```

### Python 依存関係

```bash
pip install matplotlib numpy
```

### フォント確認

```bash
# 利用可能な日本語フォントを確認
fc-list :lang=ja
```

## LaTeX 変換の詳細

### convert_to_latex.py の機能

1. **日本語サポート**
   - xeCJK パッケージを使用
   - IPAexMincho (明朝体) とIPAexGothic (ゴシック体) を設定
   - 完全なUnicodeサポート

2. **表の処理**
   - longtable で複数ページにまたがる表をサポート
   - 列数に応じて自動的に列幅を計算
   - 5列以下: 14cm / 列数
   - 6列以上: 12cm / 列数
   - 全ての行に `\hline` を追加

3. **図の処理**
   - `![caption](path)` を `\includegraphics` に変換
   - [H] 配置でテキストの位置に固定
   - 幅は 0.8\textwidth に自動設定

4. **引用の処理**
   - `[1]`, `[2]` を `\textsuperscript{[1]}` に変換
   - 参考文献セクションは自動的に処理

5. **その他の要素**
   - 章: `# 第N章 タイトル` → `\chapter{タイトル}`
   - 節: `## タイトル` → `\section{タイトル}`
   - 小節: `### タイトル` → `\subsection{タイトル}`
   - リスト: `- item` → `\begin{itemize}\item item\end{itemize}`
   - 番号付きリスト: `1. item` → `\begin{enumerate}\item item\end{enumerate}`
   - 太字: `**text**` → `\textbf{text}`
   - 斜体: `*text*` → `\textit{text}`
   - リンク: `[text](url)` → `\href{url}{text}`

### PDF コンパイル

```bash
# 手動コンパイル（3回実行が推奨）
xelatex report.tex
xelatex report.tex  # 目次更新
xelatex report.tex  # 相互参照更新

# または、--compile オプションで自動実行
python scripts/convert_to_latex.py report.md --compile
```

## トラブルシューティング

### 問題: 日本語が文字化けする

**原因**: 日本語フォントが未インストール

**解決**:
```bash
sudo apt-get install fonts-ipafont fonts-ipaexfont
fc-cache -f -v
```

### 問題: 表がページからはみ出る

**原因**: 列数が多すぎる、または内容が長すぎる

**解決**:
- convert_to_latex.py は自動的に列幅を調整します
- 必要に応じて .tex ファイルを手動編集して列幅を調整
- 表を分割することを検討

### 問題: コンパイルエラー

**原因**: LaTeXパッケージの不足

**解決**:
```bash
sudo apt-get install texlive-latex-extra texlive-fonts-extra
```

### 問題: 図が表示されない

**原因**: 図ファイルのパスが間違っている

**解決**:
- 図ファイルが正しいパスに存在することを確認
- 相対パスを使用している場合は、.texファイルからの相対位置を確認

## 例

### 基本的な使用例

```bash
# レポートの生成（スキル内で自動実行）
# 1. report_structure.md を読み込み
# 2. データ収集（MCP servers使用）
# 3. 各章のコンテンツをLaTeX形式で執筆
# 4. {report_name}.tex に保存
# 5. xelatex でコンパイル（3回）
# 6. {report_name}.pdf を生成
```

**新しいワークフロー**（直接LaTeX執筆）:
```
report_structure.md → データ収集 → LaTeX執筆 → xelatex × 3 → PDF
```

**従来のワークフロー**（Markdown経由）:
```
report_structure.md → データ収集 → Markdown執筆 → LaTeX変換 → xelatex × 3 → PDF
```

### 既存のMarkdownをLaTeXに変換（レガシー用）

既存のMarkdownファイルがある場合のみ：

```bash
cd /home/sato/Research/Kit

# 変換 + 自動コンパイル
python research-report-writer/scripts/convert_to_latex.py kit_report_full.md --compile
```

### PDFコンパイルの出力例

```
🔨 Compiling LaTeX to PDF...
   Pass 1/3...
   Pass 2/3...
   Pass 3/3...
✅ PDF created: kit_report_full.pdf (917.0 KB)
🧹 Cleaned up auxiliary files
```

最終的に生成されるPDF:
- **ページ数**: 107ページ（タイトルページ、目次、全章を含む）
- **サイズ**: 約900 KB
- **用紙**: A4
- **品質**: プロフェッショナルなレイアウト
- **日本語**: 完全対応、文字化けなし
- **表**: 中央揃え、キャプション上、自動調整
- **図**: キャプション下、適切な位置

## 今後の使用

### 新しいレポートを作成する場合

1. **構造定義**: `report_structure.md` でレポート構造を定義
2. **スキル実行**: research-report-writerスキルを使用
3. **自動生成**: スキルが自動的に：
   - データ収集
   - LaTeX形式で執筆（`{name}.tex`）
   - PDFにコンパイル（`{name}.pdf`）

### 既存のMarkdownファイルがある場合

レガシーのMarkdownファイルを変換するには：

```bash
python scripts/convert_to_latex.py existing_report.md --compile
```

### LaTeXを手動編集する場合

生成された`.tex`ファイルを直接編集してから再コンパイル：

```bash
# ファイルを編集
vim report.tex

# 再コンパイル
xelatex report.tex
xelatex report.tex
xelatex report.tex
```

## ライセンス

このスキルは汎用的な研究レポート生成システムです。任意の研究プロジェクトで使用できます。
