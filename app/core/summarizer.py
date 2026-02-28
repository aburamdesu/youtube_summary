from langchain_classic.chains.summarize import load_summarize_chain

from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI

from core.prompt_loader import load_prompt_md


def summarize_transcript(
    transcript_text: str,
    summary_mode: str,   # "short" | "detailed"
    chain_type: str,     # "stuff" | "map_reduce"
    model: str = "gpt-4o-mini",
) -> str:
    """
    字幕テキストを LangChain で要約して返す。

    - チャンク分割: RecursiveCharacterTextSplitter
    - チェーン:
        - stuff: 速い（短め向き）
        - map_reduce: 長文に強い（おすすめ）
    - プロンプトは app/prompts/*.md を読み込む
    """
    if not transcript_text or not transcript_text.strip():
        return "字幕テキストが空です。"

    # 1) 文字数ベースで分割（日本語字幕はまずこれが安定）
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=150,
        separators=["\n\n", "\n", "。", " ", ""],
    )
    chunks = splitter.split_text(transcript_text)
    docs = [Document(page_content=c) for c in chunks]

    # 2) 要約の粒度
    style = "短く要点だけ（最大10点）" if summary_mode == "short" else "詳しく（見出し＋箇条書き、重要点は具体例も）"

    # 3) LLM（ChatGPT）
    llm = ChatOpenAI(model=model, temperature=0)

    # 4) プロンプト（mdからロード）
    map_prompt_md = load_prompt_md("map_prompt.md")
    combine_prompt_md = load_prompt_md("combine_prompt.md")

    map_prompt = PromptTemplate.from_template(map_prompt_md)
    combine_prompt = PromptTemplate.from_template(combine_prompt_md)

    # 5) チェーン構築＆実行
    if chain_type == "stuff":
        chain = load_summarize_chain(
            llm=llm,
            chain_type="stuff",
            prompt=combine_prompt,  # stuff は最終要約用プロンプトでOK
        )
        out = chain.invoke({"input_documents": docs, "style": style})
        return out["output_text"]

    # map_reduce
    chain = load_summarize_chain(
        llm=llm,
        chain_type="map_reduce",
        map_prompt=map_prompt,
        combine_prompt=combine_prompt,
    )
    out = chain.invoke({"input_documents": docs, "style": style})
    return out["output_text"]