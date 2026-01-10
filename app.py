from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

# 環境変数読み込み（.envがある場合）
load_dotenv()

# --------------------------------
# LLM問い合わせ関数
# --------------------------------
def ask_llm(user_input: str, expert_type: str) -> str:
    """
    入力テキストと専門家タイプを受け取り、
    LLMの回答を返す
    """

    # 専門家ごとの system メッセージ
    if expert_type == "A":
        system_prompt = """
あなたは熟練したソフトウェアエンジニアです。
Python、Webアプリ、AI開発の観点から、
具体例を交えて分かりやすく回答してください。
"""
    else:  # B
        system_prompt = """
あなたは経験豊富なビジネスコンサルタントです。
専門用語は避け、非エンジニアにも理解できるように
要点を整理して実務的に回答してください。
"""

    # LLM定義
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input),
    ]

    # --- 修正箇所: llm(messages) ではなく llm.invoke(messages) を使用 ---
    response = llm.invoke(messages)
    return response.content


# --------------------------------
# Streamlit UI
# --------------------------------
st.set_page_config(page_title="LLM専門家切替デモ", layout="centered")

st.title("🤖 LLM専門家切替 Webアプリ")

st.markdown("""
## 📘 アプリ概要
このアプリは **LangChain** を利用して  
入力されたテキストを **LLM にプロンプトとして送信**し、
回答結果を画面に表示します。

## 🛠 使い方
1. 下のラジオボタンで専門家を選択  
2. 質問・相談内容を入力  
3. 「送信」ボタンを押す  

選択した専門家の立場で LLM が回答します。
""")

# 専門家選択
expert = st.radio(
    "専門家の種類を選択してください",
    options=["A", "B"],
    format_func=lambda x: "A：ソフトウェアエンジニア" if x == "A" else "B：ビジネスコンサルタント"
)

# 入力欄
user_text = st.text_area(
    "質問・相談内容を入力してください",
    height=160,
    placeholder="例：新しいWebアプリを作るときの注意点を教えてください"
)

# 送信処理
if st.button("送信"):
    if not user_text.strip():
        st.warning("質問内容を入力してください。")
    else:
        try:
            with st.spinner("LLMが回答を生成しています..."):
                answer = ask_llm(user_text, expert)

            st.subheader("💡 回答")
            st.write(answer)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")


