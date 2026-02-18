# Research Kit - 研究レポート自動生成システム

包括的な研究レポートを自動生成するための完全なワークフローシステムです。トピックの拡張から構造設計、執筆、品質管理まで、レポート作成の全プロセスを自動化します。

## 🎯 主な機能

### コア機能

- **📝 自動レポート生成** - 構造化されたLaTeXレポートを自動作成
- **🔍 深い文献調査** - MCP serverを使用した包括的な情報収集
- **✨ 品質管理** - 自動的な誤字脱字・内容チェックと修正
- **🌐 多様なレポートタイプ** - 学術論文、ビジネスレポート、市場調査など

### 新機能 (v2.0)

- **📸 バージョン管理** - レポート全体をv1, v2, v3...として管理
- **📚 参考文献自動ダウンロード** - 引用した論文のPDFを自動取得
- **🌐 ウェブページPDF化** - 参照したウェブページを自動的にPDF変換
- **📖 専門用語の自動説明** - 技術用語を初出時に自動的に解説
- **🔔 Discord通知** - タスク完了・許可要求時に自動通知
- **📱 NotebookLM連携** - すべての参考資料をNotebookLMで分析可能

## 🚀 クイックスタート

### 1. 初期セットアップ

```bash
cd /home/sato/Research/Kit

# Discord通知の設定（オプション）
nano .claude/hooks/discord-notify.sh
# DISCORD_WEBHOOK_URL を設定

# ウェブページPDF化ツールのインストール（オプション）
sudo apt-get install wkhtmltopdf
```

### 2. レポートトピックを定義

`report.md` を作成：

```markdown
# あなたの研究トピック

- 調査項目1
- 調査項目2
- 調査項目3
```

### 3. 完全自動でレポート生成

```bash
skill research-report-writer-orchestration
```

このコマンドで以下が自動実行されます：
1. トピックの拡張 → `update_report.md`
2. 構造設計 → `report_structure.md`
3. ツール推奨・インストール
4. レポート執筆 → `report/*.pdf`
5. 品質チェック・修正
6. バージョン保存 → `versions/v1/`

**所要時間:** 1-4時間（レポートの規模による）

### 4. 参考文献のダウンロード（オプション）

```bash
python3 .claude/scripts/download-references.py
```

PDFは `references/papers/` に保存されます。

## 📚 5つのコアスキル

Research Kitは5つの専門スキルで構成されています：

### 1. research-report-enhancer

**役割:** 研究トピックの拡張と深掘り

```bash
skill research-report-enhancer
```

- `report.md` を読み込み
- 追加調査項目を提案（8-15項目）
- 番号付きリストで出力
- 結果: `update_report.md`

### 2. research-report-structure-planner

**役割:** レポートの構造設計

```bash
skill research-report-structure-planner
```

- `update_report.md` から詳細な章立てを作成
- 各章のセクション・サブセクション・内容指示
- 結果: `report_structure.md`

### 3. skill-recommender

**役割:** 必要なツールの推奨

```bash
skill skill-recommender
```

- `update_report.md` を分析
- 関連するMCP serverとスキルを推奨
- 結果: `mcp-servers/install-skills.txt`

### 4. skill-mcp-installer

**役割:** ツールの一括インストール

```bash
skill skill-mcp-installer
```

- `mcp-servers/install-skills.txt` から一括インストール
- スキルは `./skills/` に、MCP serverは `./mcp-servers/` に配置

### 5. research-report-writer

**役割:** レポート本体の執筆と品質管理

```bash
skill research-report-writer
```

**機能:**
- LaTeX形式で直接執筆
- 深い文献調査（50-100+件のソース）
- 図表の自動生成
- 引用管理
- **品質チェック（2-4回反復）**
  - Phase A: PDF形式チェック（日本語レンダリング、キャプション等）
  - Phase B: 内容品質チェック（誤字、文法、論理、データ精度等）
- **専門用語の自動説明**
- **参考文献のダウンロード**
- **バージョン自動保存**
- PDF自動コンパイル

結果: `report/*.pdf`, `report/*.tex`, `report/figures/`

## 🎨 オーケストレーション

### research-report-writer-orchestration

全スキルを統合し、完全なワークフローを自動実行：

```bash
skill research-report-writer-orchestration
```

**実行モード:**
- **完全自動** - 全ステップを実行（初回推奨）
- **スキップモード** - ツールインストールなど一部をスキップ
- **レジューム** - 中断箇所から再開

**ユーザー確認ポイント:**
1. ワークフローモード選択
2. 拡張トピックのレビュー
3. 構造の承認
4. ツール推奨数の選択
5. ツールインストール確認
6. 章選択・パラメータ確認

## 🛠️ ユーティリティスクリプト

### バージョン管理

レポート全体をバージョン管理：

```bash
# 新しいバージョンとして保存
.claude/scripts/version-manager.sh save "Initial complete report"

# バージョン一覧
.claude/scripts/version-manager.sh list

# 以前のバージョンに戻す
.claude/scripts/version-manager.sh restore v1

# バージョン間の差分
.claude/scripts/version-manager.sh diff v1 v2

# バージョン詳細
.claude/scripts/version-manager.sh info v2
```

**保存場所:** `versions/v1/`, `versions/v2/`, ...

### 参考文献ダウンロード

引用論文のPDFとウェブページを自動ダウンロード・変換：

```bash
# 自動検出（論文PDF + ウェブページPDF化）
python3 .claude/scripts/download-references.py

# ファイル指定
python3 .claude/scripts/download-references.py report/references.bib
python3 .claude/scripts/download-references.py report/report.tex

# ウェブページ変換をスキップ
python3 .claude/scripts/download-references.py --no-webpages

# カスタム出力先
python3 .claude/scripts/download-references.py -o custom/path
```

**対応ソース:**
- ✅ arXiv（論文PDF）
- ✅ Unpaywall（オープンアクセス論文）
- ✅ PubMed Central（医学論文）
- ✅ ウェブページ（PDF変換、wkhtmltopdf必要）
- ❌ 有料論文（機関アクセス必要）

**ウェブページPDF化:**
```bash
# wkhtmltopdfのインストール（初回のみ）
sudo apt-get install wkhtmltopdf
```

**保存場所:** `references/papers/`
- 論文: `arxiv_*.pdf`, `doi_*.pdf`, `pmid_*.pdf`
- ウェブページ: `webpage_*.pdf`

### Discord通知

```bash
.claude/hooks/discord-notify.sh "メッセージ" "カラーコード"

# 例
.claude/hooks/discord-notify.sh "タスク完了" "3066993"
```

**カラーコード:**
- 緑（成功）: `3066993`
- オレンジ（警告）: `16753920`
- 赤（エラー）: `15158332`
- 青（情報）: `3447003`

## 📁 ディレクトリ構造

```
/home/sato/Research/Kit/
├── report.md                          # 初期トピック定義
├── update_report.md                   # 拡張されたトピック
├── report_structure.md                # レポート構造
│
├── report/                            # 生成されたレポート
│   ├── {name}.pdf                     # 最終PDF
│   ├── {name}.tex                     # LaTeXソース
│   └── figures/                       # 図表
│
├── versions/                          # バージョン履歴
│   ├── v1/                            # バージョン1
│   ├── v2/                            # バージョン2
│   └── .metadata                      # バージョン情報
│
├── references/                        # 参考文献
│   └── papers/                        # ダウンロードしたPDF
│
├── skills/                            # インストールされたスキル
├── mcp-servers/                       # インストールされたMCP servers
│   └── install-skills.txt             # インストールリスト
│
├── .claude/                           # Claude Code設定
│   ├── settings.local.json            # 許可設定・hooks
│   ├── hooks/
│   │   ├── discord-notify.sh          # Discord通知スクリプト
│   │   └── README.md                  # Hooks設定ガイド
│   └── scripts/
│       ├── version-manager.sh         # バージョン管理
│       ├── download-references.py     # 参考文献ダウンロード
│       └── README.md                  # スクリプト使い方
│
├── research-report-enhancer/          # スキル1: トピック拡張
├── research-report-structure-planner/ # スキル2: 構造設計
├── skill-recommender/                 # スキル3: ツール推奨
├── skill-mcp-installer/               # スキル4: ツールインストール
├── research-report-writer/            # スキル5: レポート執筆
└── research-report-writer-orchestration/ # オーケストレーション
```

## 🔄 典型的なワークフロー

### シナリオ1: 初めてのレポート作成

```bash
# 1. トピック定義
echo "# あなたの研究テーマ" > report.md
echo "- 調査項目1" >> report.md
echo "- 調査項目2" >> report.md

# 2. 完全自動実行
skill research-report-writer-orchestration

# 3. PDFを確認
ls report/*.pdf

# 4. 参考文献をダウンロード
python3 .claude/scripts/download-references.py

# 5. NotebookLMにインポート
# references/papers/*.pdf をアップロード
```

### シナリオ2: 既存レポートに追加

```bash
# 1. 現在のバージョンを確認
.claude/scripts/version-manager.sh list

# 2. 追加したい内容を伝える
# 「○○の章を追加してください」

# 3. レポート再生成
skill research-report-writer

# 4. 新バージョンとして自動保存（v2, v3...）

# 5. 差分確認
.claude/scripts/version-manager.sh diff v1 v2
```

### シナリオ3: 以前のバージョンに戻す

```bash
# 1. バージョン一覧
.claude/scripts/version-manager.sh list

# 2. 特定バージョンの詳細
.claude/scripts/version-manager.sh info v2

# 3. 復元
.claude/scripts/version-manager.sh restore v2
```

## ⚙️ 設定

### Discord通知の設定

1. **Webhook URLを取得:**
   - Discord → サーバー設定 → 連携サービス → ウェブフック
   - 新しいウェブフック作成
   - URLをコピー

2. **設定ファイルを編集:**
   ```bash
   nano .claude/hooks/discord-notify.sh
   ```

   8行目を変更：
   ```bash
   DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/あなたのURL"
   ```

3. **テスト:**
   ```bash
   .claude/hooks/discord-notify.sh "テスト通知" "3066993"
   ```

### 許可設定

`.claude/settings.local.json` で以下を制御：
- 自動実行を許可するコマンド
- Hooksの設定
- セッション開始時の動作

## 🎓 ベストプラクティス

### 初回作成時

1. **完全自動モードを使用** - すべてのステップを実行
2. **中間ファイルをレビュー** - `update_report.md` と `report_structure.md` を確認
3. **品質チェックの結果を確認** - 何が修正されたか確認

### 反復改善時

1. **バージョンを保存してから修正** - 安全のため
2. **具体的な追加要求** - 「○○の章を追加」など明確に
3. **差分を確認** - 何が変わったかチェック

### ツール管理

1. **初回は全ツールをインストール** - 包括的な調査のため
2. **2回目以降はスキップ可能** - 既にインストール済み
3. **定期的にツール更新** - 新しいMCP serverが追加されることがある

## 🐛 トラブルシューティング

### レポート生成失敗

**問題:** LaTeXコンパイルエラー

**解決策:**
```bash
# 日本語フォントのインストール
sudo apt-get install fonts-noto-cjk fonts-ipafont fonts-ipaexfont

# XeLaTeXのインストール確認
which xelatex
```

### バージョン管理

**問題:** "report/ directory not found"

**解決策:** 先にレポートを生成してください
```bash
skill research-report-writer
```

### 参考文献ダウンロード

**問題:** 多くのダウンロード失敗

**解決策:** 有料論文は自動ダウンロード不可。機関アクセスで手動取得してください。

### Discord通知

**問題:** 通知が届かない

**解決策:**
1. Webhook URLが正しいか確認
2. Discordチャンネルの権限確認
3. 手動テスト: `.claude/hooks/discord-notify.sh "Test" "3066993"`

## 📊 品質保証

### 自動品質チェック

**Phase A: PDF形式チェック**
- ✅ 日本語の正しいレンダリング
- ✅ 図表キャプションと番号の整合性
- ✅ セクション構造
- ✅ 参照の完全性

**Phase B: 内容品質チェック**
- ✅ 誤字脱字（特に日本語の誤変換）
- ✅ 文法エラー（助詞の誤用）
- ✅ 論理的矛盾
- ✅ データの正確性
- ✅ 引用の適切性
- ✅ 用語の一貫性

**反復回数:** 2-4回（すべてのチェックが通るまで）

### 専門用語の説明

すべての技術用語は初出時に自動的に説明されます：

**フォーマット:**
```
機械学習（Machine Learning: データからパターンを自動的に学習する技術）
```

- 用語集セクションは作成しない
- 文脈内で説明
- 簡潔（1文または1フレーズ）
- 対象読者に適した説明レベル

## 🔗 外部ツール連携

### NotebookLM

ダウンロードした参考文献をNotebookLMで分析：

1. `python3 .claude/scripts/download-references.py` 実行
2. https://notebooklm.google.com/ を開く
3. 新しいノートブック作成
4. `references/papers/*.pdf` をアップロード
5. 論文の要約・質問を実行

### Git（バージョン管理と組み合わせ）

```bash
# レポートのGit管理
git add report/ versions/
git commit -m "v2: Added methodology chapter"
git tag v2
```

## 📖 詳細ドキュメント

- **スキル詳細:** 各スキルディレクトリの `SKILL.md`
- **スクリプト使い方:** `.claude/scripts/README.md`
- **Hooks設定:** `.claude/hooks/README.md`
- **オーケストレーション:** `research-report-writer-orchestration/README.md`

## 🆘 サポート

問題が発生した場合：

1. **エラーメッセージを確認** - 具体的な修正方法が含まれています
2. **ドキュメントを参照** - 各ディレクトリのREADME.md
3. **バージョンを復元** - 問題が発生したら以前のバージョンに戻す
4. **ログを確認** - Claude Codeのログに詳細情報

## 🎉 完成したレポート

レポートが完成すると：
- ✅ `report/{name}.pdf` - 高品質なPDF
- ✅ `versions/vX/` - バージョン保存済み
- ✅ `references/papers/` - 参考文献PDF
- ✅ Discord通知（設定済みの場合）

NotebookLMにアップロードして、さらなる分析や質問応答に活用できます。

---

**Research Kit v2.0** - Powered by Claude Code

*包括的な研究レポートを、数時間で自動生成* 📝✨
