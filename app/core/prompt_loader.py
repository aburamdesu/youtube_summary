from pathlib import Path


def load_prompt_md(filename: str) -> str:
    """
    app/prompts 配下の Markdown プロンプトを文字列として読み込む。

    例: load_prompt_md("map_prompt.md")

    - Streamlit / VSCode / Cloud など実行場所がブレても動くように
      このファイルの位置（app/core）から相対的に app/prompts を解決する。
    """
    app_dir = Path(__file__).resolve().parents[1]  # .../app
    prompt_path = app_dir / "prompts" / filename

    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    return prompt_path.read_text(encoding="utf-8")