"""
画面全体のレイアウト（ヘッダー/フッター/ページ設定）を担当するモジュール。

責務:
- set_page_config
- タイトルや説明文などの共通UI
"""

import streamlit as st
from config.settings import APP_TITLE, APP_CAPTION


def configure_page() -> None:
    """Streamlitのページ設定（タイトルやレイアウトなど）を行う。"""
    st.set_page_config(page_title=APP_TITLE, layout="centered")


def render_header() -> None:
    """画面上部（タイトル/説明）を描画する。"""
    st.title(APP_TITLE)
    st.caption(APP_CAPTION)


def render_footer() -> None:
    """画面下部（次フェーズ案内など）を描画する。"""
    st.divider()
    st.info("Phase2ではLangChainで要約処理を追加します")