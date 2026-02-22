# self_made_skills

Claude Code のカスタムスキル集です。

## 利用可能なスキル

### /hypothesis-refinement

仮説の検証・洗練スキル。ユーザーが入力した仮説に対して文献・特許を調査し、新規性の評価・弱点の特定・洗練の提案を行います。

**使い方:**

1. プロジェクトルートに `hypothesis.txt` を作成し、検証したい仮説を記載する
2. `/hypothesis-refinement` を実行する

```
/hypothesis-refinement
```

`hypothesis.txt` にはテキストだけでなく、図表やASCIIアート、構造化された説明も自由に記載できます。

## プロジェクト構成

- `hypothesis.txt` — ユーザーが仮説を記載する入力ファイル（各自で作成）
- `hypothesis_refinement/` — 仮説検証スキルの本体・テンプレート・ドキュメント
- `.claude/commands/` — Claude Code スラッシュコマンド定義
- `.claude/settings.json` — MCP サーバー等のプロジェクト設定
