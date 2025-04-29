import streamlit as st

def render_sidebar():
    st.sidebar.title("Local Lorekeeper")
    st.sidebar.markdown("Your Offline Storytelling AI")

    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Memory Timeline", "Lore Chapters", "Chat with Lorekeeper", "Export"]) # Added Export page

    st.sidebar.header("Settings")
    # Theme selection placeholder
    theme = st.sidebar.selectbox("Select Theme", ["Fantasy", "Sci-Fi", "Minimal", "Default"])

    # Ollama Model selection placeholder (optional, could be in .env)
    # model_name = st.sidebar.text_input("Ollama Model", value="mistral")

    return page, theme

# Example usage in app.py:
# from ui.sidebar import render_sidebar
# page, theme = render_sidebar()
# if page == "Dashboard":
#     render_dashboard()
# elif page == "Memory Timeline":
#     render_timeline()
# # etc.
