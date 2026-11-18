
import streamlit as st 
from search_dcoument import search_documents

st.set_page_config(
    page_title="WaterSafe Search",
    page_icon="💧",
    layout="wide"
)

# Page heading
st.title("💧 WaterSafe Search")

st.write(
    "Search trusted water, sanitation and hygiene "
    "documents from WHO, UNICEF and CDC."
)

st.caption(
    "Powered by OpenSearch and BM25 relevance ranking"
)

st.divider()

# Sidebar
with st.sidebar:
    st.header("Search Settings")

    source_option = st.selectbox(
        "Document source",
        ["All Sources", "WHO", "UNICEF", "CDC"]
    )

    top_k = st.slider(
        "Number of results",
        min_value=5,
        max_value=20,
        value=10
    )

    st.divider()

    st.metric("PDF Documents", "49")
    st.metric("Indexed Chunks", "4,200")

# Search form
with st.form("search_form"):
    query = st.text_input(
        "Enter your search query",
        placeholder="e.g. How to purify drinking water?"
    )

    search_clicked = st.form_submit_button(
        "🔍 Search",
        type="primary"
    )

# Search results
if search_clicked:
    if not query.strip():
        st.warning("Please enter a search query.")

    else:
        source = (
            None
            if source_option == "All Sources"
            else source_option.lower()
        )

        try:
            with st.spinner("Searching documents..."):
                results = search_documents(
                    query=query,
                    top_k=top_k,
                    source=source
                )

            st.subheader("Search Results")

            st.write(
                f"Showing {len(results)} matching passages"
            )

            if not results:
                st.info("No matching documents found.")

            for position, result in enumerate(
                results, start=1
            ):
                with st.container(border=True):
                    st.markdown(
                        f"### {position}. "
                        f"{result['title']}"
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.write(
                            f"**Source:** "
                            f"{result['source'].upper()}"
                        )

                    with col2:
                        st.write(
                            f"**BM25 Score:** "
                            f"{result['score']:.3f}"
                        )

                    with col3:
                        st.write(
                            f"**Chunk ID:** "
                            f"{result['chunk_id']}"
                        )

                    st.write(
                        f"**PDF:** {result['filename']}"
                    )

                    text = result.get("text", "")

                    st.write(text[:600] + (
                        "..." if len(text) > 600 else ""
                    ))

                    with st.expander(
                        "Read full passage"
                    ):
                        st.write(text)

        except Exception as error:
            st.error(
                f"Search failed: {error}"
            )
