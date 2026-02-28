"""
UIコンポーネント（入力欄・ボタン・結果表示）をまとめたモジュール。

責務:
- 入力フォームやボタンなどの部品化
- 成功/失敗の表示部品
"""

import streamlit as st
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)

from config.settings import TRANSCRIPT_TEXTAREA_HEIGHT


def render_inputs() -> tuple[str, bool, bool]:
    """
    URL入力欄と操作ボタン（中央縦並び）を描画する。

    Returns:
        url: 入力されたURL
        fetch_btn: 「字幕取得」が押されたか
        clear_btn: 「クリア」が押されたか
    """
    url = st.text_input("YouTube URL")

    # 中央カラムにボタンを寄せる（左・右は余白）
    _, center, _ = st.columns([1, 2, 1])
    with center:
        fetch_btn = st.button("字幕取得", use_container_width=True)
        clear_btn = st.button("クリア", use_container_width=True)

    return url, fetch_btn, clear_btn


def handle_clear(clear_btn: bool) -> None:
    """
    クリアボタン押下時の処理:
    - キャッシュ削除
    - 画面リロード
    """
    if clear_btn:
        st.cache_data.clear()
        st.rerun()


def render_transcript(result: dict) -> None:
    """
    字幕取得成功時の表示。
    """
    st.success(f"取得成功 language={result['language']} video_id={result['video_id']}")

    st.subheader("字幕プレビュー")
    st.text_area(
        "transcript",
        result["text"],
        height=TRANSCRIPT_TEXTAREA_HEIGHT,
        label_visibility="collapsed",
    )


def render_error(e: Exception) -> None:
    """
    字幕取得失敗時の表示。
    主要な例外だけメッセージを整形し、それ以外はそのまま表示。
    """
    if isinstance(e, VideoUnavailable):
        st.error("動画が利用不可（削除/非公開/地域制限など）")
        return
    if isinstance(e, TranscriptsDisabled):
        st.error("字幕が無効化されています")
        return
    if isinstance(e, NoTranscriptFound):
        st.error("取得可能な字幕が見つかりませんでした")
        return

    st.error(str(e))


def render_summary_options():
    """
    Phase2: 要約タイプ（短い/詳しい）と方式（map_reduce/stuff）を選ぶUI
    """
    _, center, _ = st.columns([1, 2, 1])
    with center:
        summary_mode = st.selectbox(
            "要約タイプ",
            options=["short", "detailed"],
            format_func=lambda x: "短い" if x == "short" else "詳しい",
            index=0,
        )
        chain_type = st.selectbox(
            "要約方式",
            options=["map_reduce", "stuff"],
            format_func=lambda x: "Map-Reduce（長文に強い）" if x == "map_reduce" else "Stuff（速い/短文向き）",
            index=0,
        )
    return summary_mode, chain_type