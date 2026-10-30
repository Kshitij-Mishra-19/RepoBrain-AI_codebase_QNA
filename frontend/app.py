
import streamlit as st

from backend.index_repository import index_repository
from backend.answer import answer_question

st.set_page_config(
    page_title="RepoBrain",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 RepoBrain")
st.subheader("Chat with any GitHub codebase")
st.write("Index a public GitHub repository and ask questions about its code.")

repo_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/psf/requests",
)

if st.button("Connect Repository", type="primary"):
    if not repo_url.strip():
        st.warning("Please enter a GitHub repository URL.")
    else:
        try:
            with st.spinner("Indexing repository..."):
                total = index_repository(repo_url.strip())

            st.session_state["repo_url"] = repo_url.strip()
            st.session_state["indexed"] = True
            st.session_state["messages"] = []

            st.success(f"Repository indexed successfully! {total} chunks indexed.")

        except Exception as exc:
            st.error(f"Repository indexing failed: {exc}")

if st.session_state.get("indexed", False):
    st.divider()
    st.subheader("💬 Ask your codebase")

    st.caption(f"Connected repository: {st.session_state['repo_url']}")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask a question about this codebase...")

    if question:
        st.session_state["messages"].append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching code and generating an answer..."):
                try:
                    answer = answer_question(question)
                    st.markdown(answer)

                    st.session_state["messages"].append(
                        {"role": "assistant", "content": answer}
                    )
                except Exception as exc:
                    st.error(f"Could not generate an answer: {exc}")
