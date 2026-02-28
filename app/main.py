"""
main.py

Streamlitアプリのエントリーポイント。

役割:
- UI表示の順序を制御する（オーケストレーター）
- 各処理モジュールを呼び出すだけにする
- ビジネスロジックは書かない

処理フロー:
1. ページ初期設定
2. ヘッダー表示
3. 入力UI表示
4. 字幕取得
5. 要約生成
6. フッター表示
"""

import streamlit as st

# ==============================
# UI関連
# ==============================
from ui.layout import configure_page, render_header, render_footer
from ui.components import (
    render_inputs,
    handle_clear,
    render_transcript,
    render_error,
    render_summary_options,
)

# ==============================
# Core処理（業務ロジック）
# ==============================
from core.utils import extract_video_id
from core.youtube import fetch_transcript
from core.summarizer import summarize_transcript

# ==============================
# 設定値
# ==============================
from config.settings import OPENAI_CHAT_MODEL


def run_transcript_flow(url: str, summary_mode: str, chain_type: str) -> None:
    """
    【アプリのメイン処理】

    ユーザーが「字幕取得」を押した後に実行される。

    処理内容:
    1. URL → YouTube動画IDを抽出
    2. 字幕取得APIを呼ぶ
    3. 字幕を画面表示
    4. LangChainで要約生成
    5. 要約結果を表示

    ※ UIから呼ばれるユースケース関数（UseCase層）
    """

    # ------------------------------
    # ① URLから動画ID抽出
    # ------------------------------
    video_id = extract_video_id(url)

    if not video_id:
        st.error("URL解析失敗（YouTube URLを確認してください）")
        return

    # ------------------------------
    # ② 字幕取得
    # ------------------------------
    # Streamlitのローディング表示
    with st.spinner("字幕取得中..."):
        try:
            # YouTube API から字幕取得
            result = fetch_transcript(video_id)

            # UIへ字幕表示
            render_transcript(result)

        except Exception as e:
            # UI側のエラーハンドリングに委譲
            render_error(e)
            return

    # ------------------------------
    # ③ 要約生成（LangChain）
    # ------------------------------
    with st.spinner("要約中..."):
        try:
            summary = summarize_transcript(
                transcript_text=result["text"],  # 字幕全文
                summary_mode=summary_mode,       # short / detailed
                chain_type=chain_type,           # stuff / map_reduce
                model=OPENAI_CHAT_MODEL,
            )

            # 要約表示
            st.subheader("要約結果")
            st.markdown(summary)

        except Exception as e:
            st.error(f"要約に失敗しました: {e}")


def main() -> None:
    """
    【Streamlitアプリ起動関数】

    画面描画の順序だけを管理する。

    設計思想:
    - main() は「司令塔」
    - 処理は各モジュールへ委譲
    - 可読性最優先
    """

    # ------------------------------
    # ① ページ設定
    # ------------------------------
    configure_page()

    # ------------------------------
    # ② ヘッダー描画
    # ------------------------------
    render_header()

    # ------------------------------
    # ③ 入力UI表示
    # ------------------------------
    # URL入力 + ボタン状態取得
    url, fetch_btn, clear_btn = render_inputs()

    # クリアボタン押下時の処理
    handle_clear(clear_btn)

    # ------------------------------
    # ④ 要約オプションUI
    # ------------------------------
    # 要約粒度 / 要約方式を選択
    summary_mode, chain_type = render_summary_options()

    # ------------------------------
    # ⑤ メイン処理実行
    # ------------------------------
    if fetch_btn:
        run_transcript_flow(url, summary_mode, chain_type)

    # ------------------------------
    # ⑥ フッター描画
    # ------------------------------
    render_footer()


# ======================================
# Python直接実行時のエントリーポイント
# ======================================
if __name__ == "__main__":
    main()