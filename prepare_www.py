"""GitHub Pages用のHTMLを、iOSアプリ用に最小限だけ調整する。
   ゲームロジックには一切触らない。"""
import io, os, shutil, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else '.'
DST = sys.argv[2] if len(sys.argv) > 2 else 'www'

os.makedirs(DST, exist_ok=True)

# --- そのままコピーするもの ---
for f in ['style.css', 'script.js']:
    p = os.path.join(SRC, f)
    if os.path.exists(p):
        shutil.copy(p, os.path.join(DST, f))
        print('copy', f)

for d in ['BGM', 'SE', 'Reel', 'GOGO', 'font', 'icon']:
    p = os.path.join(SRC, d)
    if os.path.isdir(p):
        dst = os.path.join(DST, d)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(p, dst)
        print('copy dir', d, len(os.listdir(dst)), 'files')

# --- index.html だけ iOS 向けに調整 ---
h = io.open(os.path.join(SRC, 'index.html'), encoding='utf-8').read()

old = '<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">'
new = ('<meta name="viewport" content="width=device-width, initial-scale=1.0, '
       'maximum-scale=1.0, user-scalable=no, viewport-fit=cover">\n'
       '<meta name="apple-mobile-web-app-capable" content="yes">\n'
       '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
       '<meta name="format-detection" content="telephone=no">')
assert h.count(old) == 1, 'viewportタグが見つかりません'
h = h.replace(old, new)

# iOS特有の挙動を抑止するCSS/JSを </head> 直前に差し込む
inject = """<style>
/* ===== iOSアプリ(WKWebView)用の調整 ===== */
html, body {
  /* ノッチ・ホームインジケータを避ける */
  padding-top: env(safe-area-inset-top, 0px);
  padding-bottom: env(safe-area-inset-bottom, 0px);
  box-sizing: border-box;
  /* 端までスワイプした時のバウンドを止める */
  overscroll-behavior: none;
  -webkit-overflow-scrolling: auto;
}
* {
  /* 長押しの選択・コールアウト・タップ時のハイライトを無効化
     (停止ボタンを連打した時に文字が選択されるのを防ぐ) */
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}
</style>
<script>
/* ダブルタップによる拡大を無効化(停止ボタンの連打で発動してしまうため) */
document.addEventListener('gesturestart', e => e.preventDefault());
let __lastTouch = 0;
document.addEventListener('touchend', e => {
  const now = Date.now();
  if (now - __lastTouch <= 300) e.preventDefault();
  __lastTouch = now;
}, { passive: false });
</script>
"""
h = h.replace('</head>', inject + '</head>')

io.open(os.path.join(DST, 'index.html'), 'w', encoding='utf-8').write(h)
print('index.html -> iOS向けに調整して出力')
