# Research Report Writer Orchestration - 使用手順書

完全自動レポート生成システムの使い方を、ステップバイステップで説明します。

---

## 📋 目次

1. [クイックスタート（5分で理解）](#クイックスタート5分で理解)
2. [詳細な使用手順](#詳細な使用手順)
3. [よくある質問（FAQ）](#よくある質問faq)
4. [トラブルシューティング](#トラブルシューティング)
5. [使用例とテンプレート](#使用例とテンプレート)

---

## クイックスタート（5分で理解）

### 最小限の手順

```bash
# 1. report.mdを作成
cat > report.md << 'EOF'
# あなたの研究トピック

- 調査項目1
- 調査項目2
- 調査項目3
EOF

# 2. オーケストレーションスキルを実行
skill research-report-writer-orchestration

# 3. 質問に答えていく（推奨設定）
# - Workflow: "Full pipeline"
# - Mode: "Manual" (初回)
# - Detail: "Standard report"

# 4. 完成！（1-3時間後）
# report/your_report.pdf が生成される
```

### 全体の流れ（概要）

```
report.md (あなたが作成)
    ↓
[自動] 追加トピック提案 (5-10分)
    ↓
[自動] 章構成生成 (3-5分)
    ↓
[自動] ツール推薦 (5-10分)
    ↓
[自動] ツールインストール (5-20分)
    ↓
[自動] レポート執筆 (30分-3時間) ← 最も時間がかかる
    ↓
[完成] report/{name}.pdf
```

**所要時間**: 合計 1-4時間（レポートの複雑さによる）

---

## 詳細な使用手順

### 事前準備

#### 必要なもの

1. ✅ Claude Code CLI
2. ✅ 以下の5つのスキルがインストール済み：
   - `research-report-enhancer`
   - `research-report-structure-planner`
   - `skill-recommender`
   - `skill-mcp-installer`
   - `research-report-writer`
3. ✅ プロジェクトディレクトリ（例: `/home/sato/Research/Kit`）

#### スキルの確認方法

```bash
# スキル一覧を確認
ls -la | grep research-report

# 期待される出力
# drwxr-xr-x research-report-enhancer
# drwxr-xr-x research-report-structure-planner
# drwxr-xr-x research-report-writer
# drwxr-xr-x research-report-writer-orchestration
# drwxr-xr-x skill-recommender
# drwxr-xr-x skill-mcp-installer
```

---

### Step 0: report.mdの作成

プロジェクトディレクトリに`report.md`を作成します。

#### テンプレート

```markdown
# [あなたの研究トピック]

## 調査項目

- 調査したいポイント1
- 調査したいポイント2
- 調査したいポイント3
- ...

## 背景（オプション）

なぜこのトピックを研究するのか、背景情報など。

## 目的（オプション）

このレポートで明らかにしたいこと。
```

#### 実例1: 技術レポート

```markdown
# GPT-4の技術革新とビジネス応用

## 調査項目

- GPT-4のアーキテクチャと技術的改良点
- 他のLLMモデルとの性能比較
- ビジネス分野での実用例と成功事例
- 導入時の課題とベストプラクティス
- 今後の発展方向性と市場予測

## 背景

大規模言語モデル（LLM）の進化により、ビジネスプロセスの自動化が加速している。
特にGPT-4は、その性能と汎用性から企業での採用が進んでいる。

## 目的

GPT-4の技術的背景を理解し、実務での活用方法を体系的にまとめる。
```

#### 実例2: 市場調査レポート

```markdown
# 日本のEV市場動向と今後の展望

## 調査項目

- 日本国内のEV販売台数と市場シェア推移
- 主要メーカーの戦略比較
- 充電インフラの整備状況
- 消費者の購買意向と課題
- 政府の政策と補助金制度
- 2030年までの市場予測

## 背景

環境規制の強化とカーボンニュートラル目標により、
電気自動車（EV）市場が急速に拡大している。

## 目的

日本のEV市場の現状を分析し、今後5-10年の展望をまとめる。
```

**保存**: `report.md`としてプロジェクトルートに保存

---

### Step 1: オーケストレーションスキルの起動

```bash
cd /home/sato/Research/Kit  # プロジェクトディレクトリに移動
skill research-report-writer-orchestration
```

---

### Step 2: 初期設定（質問に答える）

スキルが起動すると、いくつか質問されます。

#### 質問1: ワークフローの選択

```
Which steps do you want to run?

Options:
1. Full pipeline (all steps) [推奨: 初回]
2. Skip topic enhancement (start from planning)
3. Skip tools (no recommender/installer) [推奨: 2回目以降]
4. Custom (I'll choose at each step)

Your choice:
```

**推奨回答**:
- **初回**: `1` (Full pipeline)
- **2回目以降**: `3` (Skip tools) - ツールは既にインストール済みなので

---

#### 質問2: 進行モードの選択

```
Do you want automatic progression or manual confirmation at each step?

Options:
1. Automatic (only confirm at major decisions) [推奨: 慣れている場合]
2. Manual (confirm every step) [推奨: 初回]

Your choice:
```

**推奨回答**:
- **初回**: `2` (Manual) - 各ステップを確認しながら進める
- **慣れたら**: `1` (Automatic) - 主要な決定点のみ確認

---

#### 質問3: レポートの詳細レベル

```
Report detail level preference:

Options:
1. Quick overview (detail level 2-3)
2. Standard report (detail level 3-4) [推奨]
3. Comprehensive analysis (detail level 4-5)
4. I'll decide later

Your choice:
```

**推奨回答**: `2` (Standard report)

**詳細レベルの違い**:
- **Level 2-3**: 簡潔な概要、10-15ページ程度
- **Level 3-4**: 標準的な詳細さ、20-35ページ程度（推奨）
- **Level 4-5**: 包括的分析、40-60ページ程度

---

### Step 3: パイプライン実行（7ステップ）

#### Step 1/7: Pre-flight Check (1分)

```
═══════════════════════════════════════
Step 1: Pre-flight Check
═══════════════════════════════════════

✓ Checking report.md... found
✓ Checking for existing progress...
  - update_report.md: not found
  - report_structure.md: not found
  - mcp-servers/install-skills.txt: not found
  - report/ directory: not found

No previous progress detected. Starting fresh.

Continue? [Yes/No]
```

**あなたの操作**: `Yes`と入力

---

#### Step 2/7: Topic Enhancement (5-10分)

```
═══════════════════════════════════════
Step 2: Topic Enhancement
═══════════════════════════════════════

Starting research-report-enhancer...

[enhancerが実行され、追加調査項目を提案]

Enhancement Suggestions:
1. GPT-4の学習データと前処理手法の詳細
2. マルチモーダル機能の技術的実装
3. エンタープライズ向けセキュリティ機能
4. コスト効率とROIの定量的評価
5. 競合他社（Claude, Gemini）との詳細比較
6. ファインチューニングとカスタマイズ方法
7. 法的・倫理的考慮事項
8. 今後のロードマップと予測される機能追加

The enhancer has provided suggestions. What would you like to do?

Options:
1. Create update_report.md with all suggestions [推奨]
2. Let me manually create update_report.md
3. Skip enhancement and use original report.md

Your choice:
```

**推奨操作**: `1` (自動作成)

```
✓ Created update_report.md with enhanced topics
  File: update_report.md (8 KB)
```

---

#### Step 3/7: Structure Planning (3-5分)

```
═══════════════════════════════════════
Step 3: Structure Planning
═══════════════════════════════════════

Using update_report.md for structure planning

Starting research-report-structure-planner...

[plannerが実行され、詳細な章構成を生成]

Structure Generated:
═══════════════════════════════════════
Total Chapters: 10
Total Sections: 42
Estimated Pages: 35
Detail Level: 3.5 (Standard)

Key Chapters:
1. はじめに (3 sections, detail level 3)
2. GPT-4の技術的基盤 (5 sections, detail level 4)
3. アーキテクチャと革新的機能 (4 sections, detail level 4)
4. 性能評価と比較分析 (5 sections, detail level 4)
5. ビジネス応用事例 (4 sections, detail level 3)
6. 導入戦略とベストプラクティス (4 sections, detail level 3)
7. コストとROI分析 (3 sections, detail level 3)
8. 課題とリスク管理 (3 sections, detail level 3)
9. 今後の展望 (3 sections, detail level 4)
10. 結論と提言 (2 sections, detail level 3)

File: report_structure.md (15 KB)
═══════════════════════════════════════

Review the generated structure. How would you like to proceed?

Options:
1. Approve and continue [推奨]
2. Regenerate with different parameters
3. Let me edit report_structure.md manually

Your choice:
```

**推奨操作**: `1` (承認して続行)

**オプション**: `report_structure.md`を開いて内容を確認できます
```bash
# 別のターミナルで
cat report_structure.md
```

---

#### Step 4/7: Tool Recommendation (5-10分)

```
═══════════════════════════════════════
Step 4: Tool Recommendation
═══════════════════════════════════════

Do you need tool recommendations for data collection?

Options:
1. Yes, recommend tools [推奨: 初回]
2. No, I already have the tools I need
3. Skip all tool-related steps

Your choice:
```

**推奨操作（初回）**: `1`

```
Starting skill-recommender...

[recommenderが実行され、研究トピックに基づいてツールを推薦]

Category A - Data Collection Tools
How many do you need?

Options:
1. 2-3 recommendations
2. 4-5 recommendations [推奨]
3. 6-8 recommendations
4. 10+ recommendations

Your choice:
```

**推奨操作**: `2` (4-5個)

```
Category B - Report Enhancement Tools
How many do you need?

Options:
1. 2-3 recommendations [推奨]
2. 4-5 recommendations
3. 6-8 recommendations
4. 10+ recommendations
5. None

Your choice:
```

**推奨操作**: `1` (2-3個)

```
Tool Recommendations:
═══════════════════════════════════════

Category A (Data Collection): 5 tools
1. Google-Scholar-MCP-Server (git) - Academic papers
2. paperclip (git) - ArXiv preprints
3. firecrawl-mcp-server (git) - Web scraping
4. GitHub Search MCP (npm) - Code repositories
5. OpenAlex MCP (git) - Multidisciplinary research

Category B (Report Enhancement): 3 tools
1. plotly-generator (skill) - Interactive charts
2. mermaid-diagram (skill) - Flowcharts and diagrams
3. data-visualization-mcp (npm) - Advanced visualizations

File: mcp-servers/install-skills.txt (2 KB)
═══════════════════════════════════════

✓ Tool recommendation complete
```

---

#### Step 5/7: Tool Installation (5-20分)

```
═══════════════════════════════════════
Step 5: Tool Installation
═══════════════════════════════════════

Installation Plan:
═══════════════════════════════════════
Claude Skills: 2 items
MCP Servers: 6 items
Total: 8 items

Estimated time: 12 minutes
═══════════════════════════════════════

Ready to install the recommended tools?

Options:
1. Yes, install all tools [推奨: 初回]
2. No, I'll install manually later
3. Let me review install-skills.txt first

Your choice:
```

**推奨操作（初回）**: `1`

```
Starting skill-mcp-installer...

[installerが実行され、ツールをインストール]

Installing Claude Skills to ./skills/
═══════════════════════════════════════
[1/2] Installing: plotly-generator
  ✓ Downloaded and extracted
[2/2] Installing: mermaid-diagram
  ✓ Downloaded and extracted

Installing MCP Servers to ./mcp-servers/
═══════════════════════════════════════
[1/6] Installing: Google-Scholar-MCP-Server (git)
  ✓ Cloned repository
  ✓ Installed dependencies
[2/6] Installing: paperclip (git)
  ✓ Cloned repository
  ✓ Installed dependencies
[3/6] Installing: firecrawl-mcp-server (git)
  ✓ Cloned repository
  ✓ Installed dependencies
...

Installation Summary:
═══════════════════════════════════════
Claude Skills:
  ✓ Successful: 2
  📦 Total: 2
  📁 Location: ./skills/

MCP Servers:
  ✓ Successful: 6
  📦 Total: 6
  📁 Location: ./mcp-servers/

✅ Created MCP configuration file: .claude/mcp_config.json
   Configuration contains 6 server(s)

✓ Tool installation complete
```

**2回目以降**: このステップはスキップできます

---

#### Step 6/7: Report Writing (30分-3時間) ⏰

```
═══════════════════════════════════════
Step 6: Report Writing
═══════════════════════════════════════

Report Writing Plan:
═══════════════════════════════════════
Total Chapters: 10
Estimated Pages: 35
Estimated Time: 2 hours

This is the longest step. The writer will:
- Conduct literature searches for each chapter
- Generate figures and tables
- Write content in LaTeX format
- Compile to PDF
- Perform quality checks
═══════════════════════════════════════

Ready to start writing? (This may take 1-3 hours)

Options:
1. Yes, write the full report [推奨]
2. Write specific chapters only
3. Stop here, I'll run the writer manually

Your choice:
```

**推奨操作**: `1` (全章執筆)

```
Starting research-report-writer...

[writerが起動し、さらにいくつか質問]

Which chapters would you like to write?

Options:
1. All chapters [推奨]
2. Select specific chapters

Your choice:
```

**推奨操作**: `1`

```
What would you like to name this report?
(e.g., gpt4_technical_report)

Report name:
```

**あなたの操作**: レポート名を入力（例: `gpt4_business_report`）

```
Starting report writing...

📝 Chapter 1/10: はじめに (Progress: 10%)
   🔍 Literature search: 5 papers found
   ✍️  Writing content (1,200 words)...
   ✓ Completed in 8 minutes

📝 Chapter 2/10: GPT-4の技術的基盤 (Progress: 20%)
   🔍 Literature search: 18 papers found
   📊 Generating 2 figures...
   ✍️  Writing content (2,800 words)...
   ✓ Completed in 22 minutes

📝 Chapter 3/10: アーキテクチャと革新的機能 (Progress: 30%)
   🔍 Literature search: 12 papers found
   📊 Generating 1 figure...
   📋 Creating 2 tables...
   ✍️  Writing content (2,400 words)...
   ✓ Completed in 18 minutes

... [進行中] ...

📝 Chapter 10/10: 結論と提言 (Progress: 100%)
   🔍 Literature search: 8 papers found
   ✍️  Writing content (1,500 words)...
   ✓ Completed in 10 minutes

═══════════════════════════════════════

✅ All chapters completed!

Compiling LaTeX to PDF...
  Pass 1/3... ✓
  Pass 2/3... ✓
  Pass 3/3... ✓

PDF generated: report/gpt4_business_report.pdf

Performing quality checks...
  ✓ Phase A: PDF Format Quality Check
    ✓ Japanese characters correctly rendered
    ✓ Figure/table captions in Japanese
    ✓ Continuous numbering verified
    ✓ All references complete

  ✓ Phase B: Content Quality Check
    ✓ No typos detected
    ✓ Grammar verified
    ✓ Logical consistency confirmed
    ✓ Data accuracy checked

All quality checks passed! ✅

✓ Report writing complete
  Time: 1h 55m
  Output: report/gpt4_business_report.pdf (920 KB, 36 pages)
```

---

#### Step 7/7: Summary (1分)

```
═══════════════════════════════════════════════════════════════
  Pipeline Execution Complete! 🎉
═══════════════════════════════════════════════════════════════

Execution Time: 2h 35m

Pipeline Steps:
┌─────────────────────────────────────────────┬──────────┬──────────┐
│ Step                                        │ Status   │ Duration │
├─────────────────────────────────────────────┼──────────┼──────────┤
│ 1. Pre-flight Check                         │ ✓ Done   │ 1 min    │
│ 2. Topic Enhancement                        │ ✓ Done   │ 8 min    │
│ 3. Structure Planning                       │ ✓ Done   │ 4 min    │
│ 4. Tool Recommendation                      │ ✓ Done   │ 10 min   │
│ 5. Tool Installation                        │ ✓ Done   │ 12 min   │
│ 6. Report Writing                           │ ✓ Done   │ 115 min  │
│ 7. Summary                                  │ ✓ Done   │ 1 min    │
└─────────────────────────────────────────────┴──────────┴──────────┘

Generated Files:
┌────────────────────────────────────────────────────────────────┐
│ Intermediate Files:                                            │
│  ✓ update_report.md                    (8 KB)                  │
│  ✓ report_structure.md                 (15 KB)                 │
│  ✓ mcp-servers/install-skills.txt      (2 KB)                  │
│                                                                 │
│ Final Report:                                                  │
│  ✓ report/gpt4_business_report.tex     (52 KB)                 │
│  ✓ report/gpt4_business_report.pdf     (920 KB, 36 pages)      │
│  ✓ report/figures/                     (10 figures)            │
│                                                                 │
│ Installed Tools:                                               │
│  ✓ skills/                             (2 skills)              │
│  ✓ mcp-servers/                        (6 MCP servers)         │
└────────────────────────────────────────────────────────────────┘

Report Statistics:
  • Total Pages: 36
  • Total Chapters: 10
  • Total Sections: 42
  • References: 95
  • Figures: 10
  • Tables: 6

Next Steps:
  1. Review the PDF: report/gpt4_business_report.pdf
  2. Make edits if needed: report/gpt4_business_report.tex
  3. Regenerate specific chapters: skill research-report-writer
  4. Share your report! 📄

═══════════════════════════════════════════════════════════════

Pipeline complete! What would you like to do next?

Options:
1. Open the PDF (show file path)
2. View pipeline log details
3. Run quality check again
4. Nothing, I'm done

Your choice:
```

**あなたの操作**: `1` でPDFの場所を確認、または`4`で終了

---

## よくある質問（FAQ）

### Q1: 所要時間はどのくらいですか？

**A**: レポートの複雑さによりますが：

| ステップ | 時間 |
|---------|------|
| Pre-flight Check | 1分 |
| Topic Enhancement | 5-10分 |
| Structure Planning | 3-5分 |
| Tool Recommendation | 5-10分 |
| Tool Installation | 5-20分（初回のみ） |
| **Report Writing** | **30分-3時間** ⏰ |
| Summary | 1分 |
| **合計** | **1-4時間** |

※ Report Writing（Step 6）が最も時間がかかります

---

### Q2: 途中で中断できますか？

**A**: はい、可能です。

1. **中断方法**: Ctrl+C または画面を閉じる
2. **再開方法**: 同じディレクトリで再度スキルを実行
   ```bash
   skill research-report-writer-orchestration
   ```
3. **継続オプション**: `Resume from where I left off`を選択

スキルが自動的に：
- 完了済みのステップを検出
- 生成済みのファイルを認識
- 中断した箇所から再開

---

### Q3: 2回目以降、ツールのインストールは必要ですか？

**A**: いいえ、不要です。

**2回目以降の推奨設定**:
```
Workflow: "Skip tools"
Mode: "Automatic"
Detail: "Standard report"
```

これで以下がスキップされます：
- Step 4: Tool Recommendation ⊘
- Step 5: Tool Installation ⊘

**所要時間**: 30分-1時間に短縮

---

### Q4: 特定の章だけ書き直すことはできますか？

**A**: はい、可能です。

**方法1**: オーケストレーションスキルで
```
Step 6で "Write specific chapters only" を選択
→ 書き直したい章を選択
```

**方法2**: writerを直接実行
```bash
skill research-report-writer
→ "Select specific chapters" を選択
→ 修正したい章を選ぶ
```

---

### Q5: report.mdの内容はどの程度詳しく書くべきですか？

**A**: 箇条書きで十分です。

**最小限の例**:
```markdown
# トピック名

- 調査項目1
- 調査項目2
- 調査項目3
```

**より詳しい例（推奨）**:
```markdown
# トピック名

## 調査項目
- 調査項目1（具体的な質問）
- 調査項目2（何を明らかにしたいか）
- 調査項目3（期待される結果）

## 背景
なぜこのトピックを研究するのか

## 目的
このレポートで達成したいこと
```

enhancerが自動的に詳細化してくれるので、最初は簡潔でOKです。

---

### Q6: 生成されたレポートを編集できますか？

**A**: はい、以下のファイルを編集できます：

1. **LaTeXソース**: `report/{name}.tex`
   - 内容を直接編集
   - 再コンパイル:
     ```bash
     cd report
     xelatex {name}.tex
     xelatex {name}.tex
     xelatex {name}.tex
     ```

2. **中間ファイル**:
   - `update_report.md` - トピックを編集
   - `report_structure.md` - 章構成を編集
   - その後、writerを再実行

---

### Q7: 生成されたPDFの品質は？

**A**: 以下の特徴があります：

✓ **日本語対応**: IPAexフォント使用
✓ **プロフェッショナル**: 11pt、行間1.2
✓ **自動目次**: 章・節・図表の目次
✓ **図表**: 連番付き（表1、表2、図1、図2）
✓ **参考文献**: 番号付きリスト
✓ **品質チェック済み**: 誤字・文法・論理性を確認

**ページレイアウト**:
- A4サイズ
- 余白: 上下左右 2.5cm
- フォント: 本文11pt、見出しは自動調整

---

### Q8: エラーが出た場合はどうすればいいですか？

**A**: スキルが対処方法を提示します。

```
❌ Error in Step 5: Tool Installation

Error Message:
npm install failed for package '@example/mcp-server'
Network connection timeout

What would you like to do?
1. Retry this step
2. Skip this step and continue
3. Stop the pipeline

Your choice:
```

**推奨**:
1. まず`1`（リトライ）を試す
2. 繰り返し失敗する場合は`2`（スキップ）
3. 解決できない場合は`3`（停止）してエラーを調査

---

### Q9: 複数のレポートを同時に生成できますか？

**A**: いいえ、推奨しません。

1つのディレクトリで1つのパイプラインを実行してください。

**複数のレポートを作成したい場合**:
```bash
# プロジェクト1
cd ~/research/project1
skill research-report-writer-orchestration

# プロジェクト2（別のディレクトリ）
cd ~/research/project2
skill research-report-writer-orchestration
```

---

### Q10: 既存のupdate_report.mdやreport_structure.mdを使えますか？

**A**: はい、自動的に検出して使用します。

```
✓ Checking for existing progress...
  - update_report.md: found ✓
  - report_structure.md: found ✓

Found existing progress. How would you like to proceed?

Options:
1. Resume from where I left off [推奨]
2. Start fresh (overwrite existing files)
3. Skip completed steps (keep existing files)

Your choice:
```

---

## トラブルシューティング

### 問題1: "report.md not found"

**原因**: report.mdがプロジェクトディレクトリにない

**解決方法**:
```bash
# 現在のディレクトリを確認
pwd

# report.mdを作成
cat > report.md << 'EOF'
# あなたのトピック

- 調査項目1
- 調査項目2
EOF

# 再実行
skill research-report-writer-orchestration
```

---

### 問題2: "Skill not found: research-report-enhancer"

**原因**: 必要なスキルがインストールされていない

**解決方法**:
```bash
# スキルの確認
ls -d research-report-* skill-*

# 足りないスキルをインストール
# (スキルのインストール方法に従う)
```

---

### 問題3: パイプラインが途中で止まった

**原因**:
- ユーザー入力待ち
- ネットワークエラー
- ツールのインストールエラー

**解決方法**:
1. **入力待ちの確認**: 画面を確認して質問がないか見る
2. **ログの確認**: 最後のメッセージを読む
3. **再実行**: Ctrl+Cで中断し、再度実行して"Resume"を選択

---

### 問題4: LaTeXコンパイルエラー

**原因**: 特殊文字のエスケープミス、文法エラー

**解決方法**:
```bash
# エラーログを確認
cat report/{name}.log | grep Error

# .texファイルを手動で修正
nano report/{name}.tex

# 再コンパイル
cd report
xelatex {name}.tex
```

---

### 問題5: ツールが使えない（データ収集失敗）

**原因**: MCPサーバーが正しくインストールされていない

**解決方法**:
```bash
# MCP設定を確認
cat .claude/mcp_config.json

# MCPサーバーの存在確認
ls mcp-servers/

# 再インストール
skill skill-mcp-installer
```

---

### 問題6: メモリ不足エラー

**原因**: 大規模なレポート生成時にメモリが足りない

**解決方法**:
1. **章を分割して生成**: 全章ではなく、数章ずつ生成
2. **詳細レベルを下げる**: Level 4-5 → Level 3-4
3. **不要なプロセスを終了**: 他のアプリケーションを閉じる

---

## 使用例とテンプレート

### 例1: 技術レポート（機械学習）

**report.md**:
```markdown
# Transformerアーキテクチャの進化と応用

## 調査項目

- Transformerの基本原理とAttentionメカニズム
- BERT、GPT、T5などの派生モデルの比較
- 自然言語処理での応用事例
- コンピュータビジョンでの応用（ViT、DETR等）
- 最新の研究動向と未来の方向性

## 背景

Transformer は2017年に提案されて以来、NLPの標準アーキテクチャとなり、
さらにCVや音声認識など他分野にも展開されている。

## 目的

Transformerの技術的進化を体系的に整理し、各分野での応用可能性を評価する。
```

**推奨設定**:
- Detail Level: 4 (Comprehensive)
- Category A: 6-8 tools（多めのデータソース）
- Category B: 4-5 tools（多めの図表）

**所要時間**: 3-4時間

---

### 例2: 市場調査レポート

**report.md**:
```markdown
# 日本のクラウドコンピューティング市場分析（2024-2030）

## 調査項目

- 市場規模と成長率の推移
- セグメント別分析（IaaS、PaaS、SaaS）
- 主要プレイヤーとシェア
- 企業の導入状況と課題
- 今後5年間の市場予測

## 背景

DXの加速により、クラウド市場が急拡大している。
日本市場特有の動向を把握する必要がある。

## 目的

日本のクラウド市場の現状と今後を定量的に分析し、
ビジネス戦略立案の基礎資料とする。
```

**推奨設定**:
- Detail Level: 3 (Standard)
- Category A: 4-5 tools
- Category B: 2-3 tools（グラフ中心）

**所要時間**: 2-3時間

---

### 例3: 文献レビュー

**report.md**:
```markdown
# 深層学習による医用画像診断の最新動向（2020-2024）

## 調査項目

- 深層学習の医用画像診断への応用分野
- 主要なアーキテクチャとアプローチ
- 診断精度と臨床での有効性
- 規制と倫理的課題
- 今後の研究課題

## 背景

深層学習による医用画像診断が実用化段階に入りつつある。
最新の研究動向を網羅的にレビューする必要がある。

## 目的

2020年以降の主要な研究成果を体系的に整理し、
今後の研究方向性を示す。
```

**推奨設定**:
- Detail Level: 4 (Comprehensive)
- Category A: 6-8 tools（多数の論文が必要）
- Category B: 2-3 tools

**所要時間**: 3-5時間（文献が多いため）

---

### 例4: クイックレポート（概要のみ）

**report.md**:
```markdown
# ブロックチェーン技術の概要と応用可能性

## 調査項目

- ブロックチェーンの基本概念
- 主要な応用分野（金融、サプライチェーン等）
- メリットとデメリット
- 今後の展望

## 目的

ブロックチェーン技術の基礎を理解し、
自社での応用可能性を検討する。
```

**推奨設定**:
- Detail Level: 2 (Quick overview)
- Category A: 2-3 tools
- Category B: None

**所要時間**: 30分-1時間

---

## チェックリスト

### 実行前

- [ ] プロジェクトディレクトリに移動した
- [ ] report.mdを作成した
- [ ] report.mdに調査項目を記載した
- [ ] 必要なスキルがインストールされている
- [ ] 十分な時間がある（1-4時間）

### 実行中

- [ ] Step 0で適切な設定を選択した
- [ ] Step 1でファイル確認を承認した
- [ ] Step 2で追加トピックを確認した
- [ ] Step 3で章構成を承認した
- [ ] Step 4-5でツールを推薦・インストールした（初回のみ）
- [ ] Step 6でレポート名を入力した

### 実行後

- [ ] PDFが生成されたか確認: `ls report/*.pdf`
- [ ] PDFの内容を確認: PDF viewerで開く
- [ ] 必要に応じて.texファイルを編集
- [ ] 生成ファイルをバックアップ

---

## さらに詳しく

- **SKILL.md**: 技術的な詳細とワークフロー定義
- **README.md**: 概要と機能説明
- **各スキルのドキュメント**: 個別スキルの詳細

---

**更新日**: 2026-01-28
**バージョン**: 1.0
