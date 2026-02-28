"""
ユーティリティ（汎用関数）を置くモジュール。

YouTubeなど特定ドメインに依存しない処理はここに置くと
再利用・テストが簡単になる。
"""

import re
from urllib.parse import urlparse, parse_qs


def extract_video_id(url: str) -> str:
    """
    YouTube URL から video_id を抽出する。

    なぜ必要？
    - youtube-transcript-api は URL ではなく video_id が必要なため

    対応例:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/shorts/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID

    Args:
        url: YouTube動画URL

    Returns:
        video_id（抽出できない場合は空文字）
    """
    if not url:
        return ""

    parsed = urlparse(url.strip())
    host = (parsed.netloc or "").lower()
    path = parsed.path or ""

    # youtu.be/VIDEO_ID
    if "youtu.be" in host:
        return path.lstrip("/").split("/")[0]

    # youtube.com/watch?v=VIDEO_ID
    if path == "/watch":
        qs = parse_qs(parsed.query)
        return (qs.get("v") or [""])[0]

    # youtube.com/shorts/VIDEO_ID
    m = re.match(r"^/shorts/([^/?]+)", path)
    if m:
        return m.group(1)

    # youtube.com/embed/VIDEO_ID
    m = re.match(r"^/embed/([^/?]+)", path)
    if m:
        return m.group(1)

    # ここまでで取れないなら空
    return ""