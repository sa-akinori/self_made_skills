# self_made_skills

Claude Code のカスタムスキル集です。

## 利用可能なスキル

### /hypothesis-refinement

仮説の検証・洗練スキル。ユーザーが入力した仮説に対して文献・特許を調査し、新規性の評価・弱点の特定・洗練の提案を行います。

**使い方:**
```
/hypothesis-refinement <あなたの仮説>
```

**例:**
```
/hypothesis-refinement 腸内細菌叢の多様性が睡眠の質に直接的な因果関係を持つ
```

## プロジェクト構成

- `hypothesis_refinement/` — 仮説検証スキルの本体・テンプレート・ドキュメント
- `.claude/commands/` — Claude Code スラッシュコマンド定義
- `.claude/settings.json` — MCP サーバー等のプロジェクト設定
