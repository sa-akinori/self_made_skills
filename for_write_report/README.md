# Research Kit - 研究レポート自動生成システム

包括的な研究レポートを自動生成するための完全なワークフローシステムです。トピックの拡張から構造設計、執筆、品質管理まで、レポート作成の全プロセスを自動化します。

## 🎯 主な機能

### コア機能

- **📝 自動レポート生成** - 構造化されたLaTeXレポートを自動作成
- **🔍 深い文献調査** - MCP serverを使用した包括的な情報収集
- **✨ 品質管理** - レビュアーエージェントによる指摘 → ライターエージェントによる修正のフィードバックループ
- **🌐 多様なレポートタイプ** - 学術論文、ビジネスレポート、市場調査など

### 新機能 (v3.0)

- **🤖 サブエージェント連携** - Opus/Sonnetを使い分ける3つの専門エージェント
- **🔄 ライター↔レビュアーループ** - 執筆と校閲の自動フィードバック（最大3回）
- **📸 バージョン管理** - レポートを`report/v1/`, `report/v2/`...として管理
- **📚 参考文献自動ダウンロード** - 引用した論文のPDFを自動取得
- **🌐 ウェブページPDF化** - 参照したウェブページを自動的にPDF変換
- **📖 専門用語の自動説明** - 技術用語を初出時に自動的に解説
- **🔔 Discord通知** - タスク完了・許可要求時に自動通知
- **📱 NotebookLM連携** - すべての参考資料をNotebookLMで分析可能

## 📋 セットアップ

### 必要なソフトウェア

| ソフトウェア | 用途 | 必須/オプション |
|---|---|---|
| Claude Code | オーケストレーション・執筆・レビュー | 必須 |
| Docker | devcontainer（安全な実行環境） | 強く推奨 |
| Gemini APIキー | 概念図の生成（Nano Banana 2） | オプション |

LaTeX環境、Python、日本語フォントなどはDockerfileに記述するか、Claude Codeが実行時に自動インストールします。

### Step 1: Research Kit のクローン

プロジェクトディレクトリで以下を実行してください：

```bash
# リポジトリをクローン
git clone https://github.com/sa-akinori/self_made_skills.git

# for_write_report の中身だけをプロジェクトディレクトリにコピー
cp -r self_made_skills/for_write_report/* .
cp -r self_made_skills/for_write_report/.claude .

# 不要なファイルを削除
rm -rf self_made_skills
```

このディレクトリにスキル、エージェント、スクリプトなど必要なファイルがすべて配置されます。

### Step 2: report.md の作成

レポートのテーマと調査項目を `report.md` に箇条書きで記述します：

```bash
cat > report.md << 'EOF'
# あなたの研究トピック

- 調査項目1
- 調査項目2
- 調査項目3
- 関連して調べたいこと
EOF
```

例（Kit阻害剤の場合）：

```markdown
# Kitの阻害剤開発

- Kitとは何か？
- Mutantがどこに入りやすいのか？
- Mutantにつよい阻害剤設計
- MDでうまく行った事例はあるのか
- 製薬企業の開発動向
- 選択的にKitを阻害する薬剤
- 関連して、選択的Kinase阻害剤の設計方法の指針やアプローチ
```

完璧な文章である必要はありません。箇条書きのメモで十分です。オーケストレーションが自動的に拡張・構造化します。

### Step 3: Docker環境の起動（推奨）

Research KitにはDockerfileが同梱されています。LaTeX、Python、Claude Code、日本語フォントなど必要な環境がすべてプリインストールされています。

**メリット:**

- 許可プロンプトが一切出ない（`--dangerously-skip-permissions`が安全に使える）
- 環境構築不要（LaTeX、Python等はDockerイメージに含まれている）
- ホスト環境を汚さない（壊れたらコンテナを破棄するだけ）
- プロジェクトディレクトリ以外にはアクセス不可

**3-1. Docker のインストール**

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-v2
sudo usermod -aG docker $USER

# 反映のため再ログイン
newgrp docker

# 確認
docker --version
```

**3-2. 初回認証（サブスクリプションの場合）**

Claudeのサブスクリプション（Pro/Max）を使う場合、先にホスト側でログインしてください。コンテナはこの認証情報を共有します：

```bash
# ホスト側でClaude Codeにログイン（初回のみ）
claude
# ブラウザが開くのでログイン → 完了したら /exit で終了
```

APIキー（従量課金）を使う場合はこの手順は不要です。

**⚠️ 認証情報に関する注意:**

- Claude Codeの認証情報（OAuthトークン）はホームディレクトリの`~/.claude/`に保存されます（プロジェクトディレクトリではありません）
- `docker-run.sh`はこの`~/.claude/`をコンテナ内にマウントすることでログインを共有します
- コンテナ内から`~/.claude/`への書き込みが可能なため、`--dangerously-skip-permissions`で実行中にホスト側の認証情報が書き換えられる可能性があります。万が一ログインできなくなった場合は、ホスト側で`claude`を再実行してログインし直してください

**3-3. コンテナの起動**

```bash
./docker-run.sh
```

初回はDockerイメージのビルドに数分かかります。2回目以降は即起動します。

コンテナ内に入ったら、Claude Codeを起動してください：

```bash
# 通常モード（毎回許可プロンプトが出る）
claude

# 自律モード（許可プロンプトなし、推奨）
claude --dangerously-skip-permissions
```

初回はDockerイメージのビルドに数分かかります。2回目以降は即起動します。

**Gemini APIキーを使う場合:**

```bash
export GEMINI_API_KEY="あなたのキー"
./docker-run.sh
```

APIキーは <https://aistudio.google.com/apikey> から無料で取得できます。概念図・模式図の生成に使用します（データグラフのみの場合は不要）。

**Dockerを使わない場合:** ホスト環境で直接実行できますが、LaTeX・Python等を手動でインストールする必要があり、毎回許可プロンプトも表示されます。

### Step 4: オプション設定

```bash
# Discord通知（オプション）
nano .claude/hooks/discord-notify.sh
# DISCORD_WEBHOOK_URL を設定
```

## 🚀 クイックスタート

上記のセットアップ完了後、レポート生成は2ステップです。

### 1. 完全自動でレポート生成

```bash
skill research-report-writer-orchestration
```

このコマンドで以下が自動実行されます：

1. トピックの拡張 → `update_report.md`
2. 構造設計（report-architectエージェント） → `report_structure.md`
3. ツール推奨・インストール
4. レポート執筆（report-writerエージェント） → `report/v1/*.pdf`
5. 品質チェック（report-reviewerエージェント） → `report/v1/review_log.md`
6. 修正（report-writerエージェント） → `report/v2/*.pdf` + `report/v2/revision_log.md`

**所要時間:** 1-4時間（レポートの規模による）

### 2. 参考文献のダウンロード（オプション）

```bash
python3 .claude/scripts/download-references.py
```

PDFは `references/papers/` に保存されます。

## 🤖 アーキテクチャ

### スキルとエージェントの役割分担

Research Kitは**5つのスキル**と**3つのサブエージェント**で構成されています。メインのClaude（Sonnet）がオーケストレーターとして全体を管理し、タスクの重さに応じてスキルを直接実行するか、サブエージェントに委任するかを使い分けます。

```
メインClaude（Sonnet） ── オーケストレーター
│
├─ Step 1: Pre-flight Check（メインが直接実行）
├─ Step 2: skill research-report-enhancer（Sonnet）
├─ Step 3: report-architect エージェント（Opus）★
├─ Step 4: skill skill-recommender（Sonnet）
├─ Step 5: skill skill-mcp-installer（Sonnet）
├─ Step 6a: report-writer エージェント（Opus）★
├─ Step 6b: report-reviewer エージェント（Sonnet）★
├─ Step 6c: 修正ループ（writer ↔ reviewer、最大3回）★
└─ Step 7: Summary（メインが直接実行）

★ = サブエージェントに委任
```

### なぜスキルとエージェントを使い分けるのか

- **スキル（Steps 2, 4, 5）**: タスクが軽く、Sonnetで十分な定型処理
- **エージェント（Steps 3, 6）**: コンテキストが大量に必要、またはOpusレベルの推論が必要な重いタスク

エージェントはそれぞれ独立したコンテキストウィンドウで動くため、執筆で膨らんだコンテキストがレビューに影響せず、品質が保たれます。

### 3つのサブエージェント

| エージェント | モデル | 役割 | 配置場所 |
|---|---|---|---|
| report-architect | Opus | 構造設計（章立て・セクション・内容指示） | `.claude/agents/report-architect.md` |
| report-writer | Opus | レポート執筆 + レビュー指摘の修正対応 | `.claude/agents/report-writer.md` |
| report-reviewer | Sonnet | 品質チェック（指摘のみ、修正はしない） | `.claude/agents/report-reviewer.md` |

### ライター↔レビュアー フィードバックループ

Step 6では、執筆と品質チェックが自動的にループします：

```
[report-writer] 執筆 → report/vN/*.pdf
       ↓
[report-reviewer] レビュー → report/vN/review_log.md
       ↓
  指摘あり？──No──→ 完了
       │
      Yes
       ↓
[report-writer] review_log.mdを受けて修正 → report/vN/revision_log.md
       ↓
[report-reviewer] 再チェック
       ↓
  指摘あり？ → 最大3ループで終了
```

レビュアーは絶対に元ファイルを編集しません。指摘を`review_log.md`にまとめ、修正はすべてライターが行います。

## 📚 5つのコアスキル

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

**役割:** レポートの構造設計（report-architectエージェントのフォールバック）

```bash
skill research-report-structure-planner
```

- `update_report.md` から詳細な章立てを作成
- 各章のセクション・サブセクション・内容指示
- 結果: `report_structure.md`

**注:** オーケストレーション経由ではreport-architectエージェント（Opus）が構造設計を担当します。このスキルはエージェントが利用できない場合のフォールバックです。

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

**役割:** レポート本体の執筆と品質管理（report-writer/report-reviewerエージェントのフォールバック）

```bash
skill research-report-writer
```

**注:** オーケストレーション経由ではreport-writerエージェント（Opus）とreport-reviewerエージェント（Sonnet）が執筆と品質管理を担当します。このスキルはエージェントが利用できない場合のフォールバックです。

## 🎨 オーケストレーション

### research-report-writer-orchestration

全スキルとエージェントを統合し、完全なワークフローを自動実行：

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
python3 .claude/scripts/download-references.py report/v1/references.bib
python3 .claude/scripts/download-references.py report/v1/report.tex

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

**保存場所:** `references/papers/`

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
project-directory/
├── Dockerfile                         # Docker環境定義
├── docker-run.sh                      # Docker起動スクリプト
├── report.md                          # 初期トピック定義（ユーザーが作成）
├── update_report.md                   # 拡張されたトピック（自動生成）
├── report_structure.md                # レポート構造（自動生成）
│
├── report/                            # 生成されたレポート
│   ├── v1/                            # バージョン1（初稿）
│   │   ├── {name}.pdf                 # PDF
│   │   ├── {name}.tex                 # LaTeXソース
│   │   ├── figures/                   # 図表
│   │   └── review_log.md             # レビュー指摘
│   ├── v2/                            # バージョン2（修正版）
│   │   ├── ...
│   │   └── revision_log.md           # 修正記録
│   └── ...
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
│   ├── agents/                        # サブエージェント定義
│   │   ├── report-architect.md        # 構造設計（Opus）
│   │   ├── report-writer.md           # 執筆+修正（Opus）
│   │   └── report-reviewer.md         # 品質チェック（Sonnet）
│   ├── hooks/
│   │   ├── discord-notify.sh          # Discord通知スクリプト
│   │   └── README.md                  # Hooks設定ガイド
│   └── scripts/
│       ├── generate_image.py          # 概念図生成（Gemini API）
│       ├── version-manager.sh         # バージョン管理
│       ├── download-references.py     # 参考文献ダウンロード
│       └── README.md                  # スクリプト使い方
│
├── research-report-enhancer/          # スキル1: トピック拡張
├── research-report-structure-planner/ # スキル2: 構造設計（フォールバック）
├── skill-recommender/                 # スキル3: ツール推奨
├── skill-mcp-installer/               # スキル4: ツールインストール
├── research-report-writer/            # スキル5: レポート執筆（フォールバック）
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
ls report/v1/*.pdf

# 4. レビュー結果を確認
cat report/v1/review_log.md
cat report/v1/revision_log.md

# 5. 参考文献をダウンロード
python3 .claude/scripts/download-references.py

# 6. NotebookLMにインポート
# references/papers/*.pdf をアップロード
```

### シナリオ2: 既存レポートに追加

```bash
# 1. 現在のバージョンを確認
ls report/

# 2. 追加したい内容を伝える
# 「○○の章を追加してください」

# 3. レポート再生成（新バージョンとして report/v2/ に保存）
skill research-report-writer-orchestration

# 4. 差分確認
diff report/v1/ report/v2/
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

### エージェントの設定

サブエージェントは `.claude/agents/` に配置します。エージェントファイルを追加・変更した場合は、Claude Codeセッションの再起動が必要です。

```bash
# エージェント一覧の確認
ls .claude/agents/

# セッション再起動（エージェント変更後）
# /exit → claude -r
```

各エージェントの`model`フィールドを変更することで、使用するモデルを切り替えられます：

```yaml
model: opus    # 高品質（構造設計、執筆向け）
model: sonnet  # 高速・低コスト（レビュー向け）
```

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
3. **品質チェックの結果を確認** - `report/vN/review_log.md` と `report/vN/revision_log.md` を読む

### 反復改善時

1. **バージョンを保存してから修正** - 安全のため
2. **具体的な追加要求** - 「○○の章を追加」など明確に
3. **差分を確認** - 何が変わったかチェック

### ツール管理

1. **初回は全ツールをインストール** - 包括的な調査のため
2. **2回目以降はスキップ可能** - 既にインストール済み
3. **定期的にツール更新** - 新しいMCP serverが追加されることがある

### エージェントのカスタマイズ

1. **レビュー基準の調整** - `report-reviewer.md`のチェック項目を編集
2. **執筆スタイルの変更** - `report-writer.md`の執筆方針を編集
3. **構造設計の方針変更** - `report-architect.md`の設計原則を編集
4. **変更後は必ずセッション再起動**

## 🐛 トラブルシューティング

### レポート生成失敗

**問題:** LaTeXコンパイルエラー

**解決策:** LaTeX環境がインストールされているか確認してください。Dockerfileに追記するか、手動でインストールしてください：

```bash
sudo apt-get install -y texlive-xetex texlive-lang-japanese fonts-noto-cjk
which xelatex
```

### エージェントが起動しない

**問題:** サブエージェントが呼び出されない

**解決策:**

1. `.claude/agents/` にファイルが配置されているか確認
2. セッションを再起動（`/exit` → `claude -r`）
3. エージェントのYAMLフロントマターが正しいか確認（name, model, tools）

### 概念図の生成に失敗する

**問題:** `generate_image.py` がエラーを出す

**解決策:**

1. Gemini APIキーが設定されているか確認: `echo $GEMINI_API_KEY`
2. 依存パッケージを確認: `pip install google-genai Pillow`
3. APIキーの取得方法は「セットアップ」のStep 4を参照

### レビューループが終わらない

**問題:** 3回ループしても指摘が残る

**解決策:** これは正常な動作です。残った指摘は`report/vN/review_log.md`に記録されています。手動で`.tex`ファイルを修正してください。

### バージョン管理

**問題:** "report/ directory not found"

**解決策:** 先にレポートを生成してください

```bash
skill research-report-writer-orchestration
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

### 自動品質チェック（report-reviewerエージェント）

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

**フィードバックループ:** 最大3回（レビュアーが指摘 → ライターが修正 → 再チェック）

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
2. <https://notebooklm.google.com/> を開く
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
- **エージェント定義:** `.claude/agents/*.md`
- **スクリプト使い方:** `.claude/scripts/README.md`
- **Hooks設定:** `.claude/hooks/README.md`
- **オーケストレーション:** `research-report-writer-orchestration/README.md`

## 🆘 サポート

問題が発生した場合：

1. **エラーメッセージを確認** - 具体的な修正方法が含まれています
2. **ドキュメントを参照** - 各ディレクトリのREADME.md
3. **レビューログを確認** - `report/vN/review_log.md` に品質問題の詳細
4. **バージョンを復元** - 問題が発生したら以前のバージョンに戻す
5. **ログを確認** - Claude Codeのログに詳細情報

## 🎉 完成したレポート

レポートが完成すると：

- ✅ `report/vN/{name}.pdf` - 高品質なPDF
- ✅ `report/vN/review_log.md` - 品質レビュー結果
- ✅ `report/vN/revision_log.md` - 修正対応記録
- ✅ `references/papers/` - 参考文献PDF
- ✅ Discord通知（設定済みの場合）

NotebookLMにアップロードして、さらなる分析や質問応答に活用できます。

---

**Research Kit v3.0** - Powered by Claude Code + Subagents

*包括的な研究レポートを、数時間で自動生成* 📝✨
