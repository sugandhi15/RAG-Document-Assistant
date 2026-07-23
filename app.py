import streamlit as st
import os

from ingest import load_documents, create_chunks

from rag import (
    create_embeddings,
    build_faiss_index,
    embed_query,
    search_index,
    retrieve_chunks,
    create_context,
    ask_gemini
)

# ------------------------------------
# Page Config
# ------------------------------------

st.set_page_config(
    page_title="RAG Document Chatbot",
    page_icon="📄",
    layout="wide"
)

st.title("📄 RAG Document Chatbot")
st.write("Upload one or more PDF files and ask questions.")

# ------------------------------------
# Session State
# ------------------------------------

if "index" not in st.session_state:
    st.session_state.index = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------------
# Sidebar
# ------------------------------------

with st.sidebar:

    st.header("Upload Documents")

    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        os.makedirs("data", exist_ok=True)

        # Delete previous PDFs
        for file in os.listdir("data"):

            path = os.path.join("data", file)

            if os.path.isfile(path):
                os.remove(path)

        # Save uploaded PDFs
        for file in uploaded_files:

            with open(
                os.path.join("data", file.name),
                "wb"
            ) as f:

                f.write(file.getbuffer())
                

        with st.spinner("Processing documents..."):

            docs = load_documents("data")

            chunks = create_chunks(docs)

            embeddings = create_embeddings(chunks)

            st.write("Documents:", len(docs))
            st.write("Chunks:", len(chunks))
            st.write("Embeddings Shape:", embeddings.shape)

            index = build_faiss_index(embeddings)

            st.session_state.index = index
            st.session_state.chunks = chunks

        st.success("Documents processed successfully!")

        st.write("### Uploaded Files")

        for file in uploaded_files:
            st.write("📄", file.name)

# ------------------------------------
# Display Chat History
# ------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ------------------------------------
# Chat Input
# ------------------------------------

question = st.chat_input(
    "Ask something about your documents..."
)

if question:

    # Show User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Check whether PDFs are uploaded
    if st.session_state.index is None:

        answer = "Please upload one or more PDF files first."

    else:

        with st.spinner("Searching documents..."):

            query_embedding = embed_query(question)

            distances, indices = search_index(
                query_embedding,
                st.session_state.index,
                k=3
            )

            retrieved = retrieve_chunks(
                indices,
                st.session_state.chunks
            )

            context = create_context(retrieved)

            answer = ask_gemini(
                question,
                context
            )

        with st.expander("Retrieved Context"):

            st.write(context)

        with st.expander("Source Documents"):

            shown = set()

            for chunk in retrieved:

                if chunk["file_name"] not in shown:

                    st.write("📄", chunk["file_name"])

                    shown.add(chunk["file_name"])

    # Display Assistant Message
    with st.chat_message("assistant"):

        st.markdown(answer)

    # Save Assistant Response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )