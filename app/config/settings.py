"""
設定値（定数）を集約するモジュール。

目的:
- アプリ全体で参照する設定値を1か所にまとめる
- UI文言やキャッシュTTLなど、変更しやすくする
"""

# アプリ表示名
APP_TITLE = "YouTube要約アプリ（Phase1）"
APP_CAPTION = "URLを入力 → 字幕を取得して表示"

# StreamlitキャッシュのTTL（秒）
CACHE_TTL_SECONDS = 60 * 60  # 1時間

# 字幕取得時の優先言語（上から順に探す）
PREFERRED_LANGS = ["ja", "ja-JP", "en", "en-US"]

# 字幕表示欄の高さ
TRANSCRIPT_TEXTAREA_HEIGHT = 320

# 使用モデル
OPENAI_CHAT_MODEL = "gpt-4o-mini"