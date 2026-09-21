# アイムジャグラーEX シミュレーター — iOS (.ipa) ビルド

Windows だけで `.ipa` を作るためのリポジトリです。
**Mac は一切不要**で、GitHub Actions のクラウド Mac がビルドします。

- アプリ名: **アイムジャグラーEX シミュレーター**
- Bundle ID: `io.github.h1ro223.imjuggler`
- 署名: **しません**（AltStore / AltServer 側で署名します）

---

## 手順

### STEP 1. 新しい公開リポジトリを作る

GitHub で新規リポジトリを作成します。名前は何でも構いません（例: `ImJugglerEX6_iOS`）。

> **必ず「Public（公開）」にしてください。**
> GitHub Actions の macOS ランナーは、公開リポジトリなら**無料・無制限**です。
> 非公開にすると月200分程度しか無料枠がなく、数回ビルドしただけで使い切ります。

### STEP 2. ファイルを配置する

次の形になるようにファイルを置きます。

```
（リポジトリのルート）
├── .github/
│   └── workflows/
│       └── build-ios.yml      ← このzipに入っています
├── capacitor.config.json      ← このzipに入っています
├── package.json               ← このzipに入っています
├── .gitignore                 ← このzipに入っています
├── prepare_www.py             ← このzipに入っています（任意）
└── www/                       ← ★ゲーム本体をここに入れる
    ├── index.html
    ├── style.css
    ├── script.js
    ├── BGM/
    ├── SE/
    ├── Reel/
    ├── GOGO/
    ├── font/
    └── icon/
```

**`www/` の中身の作り方は2通りあります。**

**（A）スクリプトを使う（おすすめ）**

`prepare_www.py` を使うと、iOS 向けの調整（ノッチ対応・ダブルタップ拡大の無効化など）を
自動で入れた `www/` を作れます。Python が入っていれば実行できます。

```powershell
# 今のシミュレーターのフォルダを指定して実行
python prepare_www.py "C:\path\to\ImJugglerEX6_Simulator" www
```

**（B）手でコピーする**

今のシミュレーターのファイル一式を、そのまま `www/` フォルダにコピーするだけでも動きます。
ただし iOS 向けの調整は入りません（動作はしますが、ノッチに被る・ダブルタップで拡大する等の癖が残ります）。

### STEP 3. push する

```powershell
git add .
git commit -m "iOS build setup"
git push
```

push した時点で**自動的にビルドが始まります**。

### STEP 4. `.ipa` をダウンロード

1. GitHub のリポジトリページ → 上部の **「Actions」** タブ
2. 一番上の実行結果をクリック（緑のチェックが付けば成功、赤い×なら失敗）
3. ページ下部の **「Artifacts」** から `ImJugglerEX-ipa` をダウンロード
4. zip を解凍すると `ImJugglerEX.ipa` が出てきます

所要時間は **5〜10分** 程度です。

### STEP 5. AltStore でインストール

いつも通りの手順です。

1. `ImJugglerEX.ipa` を iPhone に転送（AirDrop / iCloud Drive / メール等）
2. AltStore を開く → **My Apps** → 左上の **＋**
3. `ImJugglerEX.ipa` を選択
4. Apple ID のパスワードを入力すると署名されてインストールされます

> 無料の Apple ID の場合、**7日ごとに AltStore で Refresh** が必要です。

---

## ビルドが失敗したら

「Actions」タブの実行結果を開くと、**どのステップで失敗したか**が赤く表示されます。
そのステップをクリックするとログが読めるので、ログをそのまま貼って相談してください。

よくある失敗と対処:

| エラー | 原因 | 対処 |
|---|---|---|
| `www/ フォルダがありません` | ゲーム本体を置き忘れ | STEP 2 をやり直す |
| `npx cap add ios` で失敗 | Capacitor のバージョン不整合 | `package.json` のバージョンを下げる（後述） |
| `xcodebuild` で失敗 | Xcode / Capacitor の組み合わせ | ログの `error:` 行を確認 |
| アプリは入るが真っ白 | パス参照の問題 | `index.html` 内が `./` 形式になっているか確認 |

**Capacitor のバージョンを下げたい場合**は `package.json` の `^8.0.0` を `^7.0.0` に変えてください。
（Capacitor 8 は Xcode 26 以上が必要です。GitHub の `macos-latest` は対応済みですが、
将来ランナーの構成が変わった場合はこちらに切り替えると安定します）

---

## 中止したくなったら

このリポジトリを削除するだけで完了です。
**元の `ImJugglerEX6_Simulator` には一切影響しません**（別リポジトリなので）。
