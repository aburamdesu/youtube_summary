"""
YouTube字幕取得に関する処理をまとめたモジュール。

責務:
- youtube-transcript-api を使って字幕を取得
- 取得結果を {video_id, language, text} の形に整形する
- Streamlitキャッシュで高速化する
"""

import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi

from config.settings import CACHE_TTL_SECONDS, PREFERRED_LANGS


@st.cache_data(ttl=CACHE_TTL_SECONDS)
def fetch_transcript(video_id: str) -> dict:
    """
    指定した video_id の字幕を取得して結合テキストとして返す。

    注意:
    - youtube-transcript-api のバージョン差異により、
      fetch() の戻りが dict のlist だったり、オブジェクトのlist だったりする
      → 両方に対応している

    Args:
        video_id: YouTubeの動画ID

    Returns:
        dict: {
          "video_id": str,
          "language": str,  # 実際に取得できた言語コード
          "text": str       # 字幕を結合した本文
        }
    """
    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)

    transcript = None
    used_lang = ""

    # 1) 優先言語を順番に試す
    for lang in PREFERRED_LANGS:
        try:
            transcript = transcript_list.find_transcript([lang])
            used_lang = getattr(transcript, "language_code", "")
            break
        except Exception:
            pass

    # 2) それでも無ければ、とれる字幕の先頭を採用
    if transcript is None:
        transcript = next(iter(transcript_list))
        used_lang = getattr(transcript, "language_code", "")

    items = transcript.fetch()

    # items は dict or object のどちらの場合もあるため吸収する
    lines = []
    for x in items:
        if isinstance(x, dict):
            lines.append(x.get("text", ""))
        else:
            lines.append(getattr(x, "text", ""))

    text = "\n".join([line for line in lines if line]).strip()

    return {"video_id": video_id, "language": used_lang, "text": text}