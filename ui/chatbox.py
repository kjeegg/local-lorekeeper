import streamlit as st
import sys
sys.path.append('.') # Allow importing from parent directory

from lore_engine.agent import LorekeeperAgent, load_mood_styles
from lore_engine.classifier import ChapterClassifier
from memory.memory_store import connect_db

# Initialize the agent and classifier (can be cached by Streamlit)
@st.cache_resource
def get_lorekeeper_components():
    agent = LorekeeperAgent()
    classifier = ChapterClassifier(agent)
    mood_styles = load_mood_styles()
    return agent, classifier, mood_styles

agent, classifier, mood_styles = get_lorekeeper_components()

def save_memory(content, chapter=None, mood=None):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO memories (content, chapter, mood) VALUES (?, ?, ?)", (content, chapter, mood))
    conn.commit()
    conn.close()

def render_chatbox():
    st.header("Chat with the Lorekeeper")

    # Add Mood and Style selection for the chat response
    col1, col2 = st.columns(2)
    with col1:
        selected_mood = st.selectbox("Lorekeeper's Mood:", ['neutral', 'joyful', 'melancholic', 'reflective', 'hopeful']) # Example moods
    with col2:
        selected_style = st.selectbox("Lorekeeper's Style:", list(mood_styles.keys()))

    # Initialize chat history in session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Speak your thoughts, memories, or questions..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # --- Process User Input ---
        # Generate response from the agent, passing selected mood and style
        with st.chat_message("assistant"):
            with st.spinner("Lorekeeper is pondering..."):
                # You might want to fetch recent memories as context for the agent
                # context_memories = get_recent_memories(limit=5) # Need to implement this function
                # context_text = "\n".join([f"Timestamp: {m[1]}\nChapter: {m[2]}\nMood: {m[3]}\nContent: {m[0]}" for m in context_memories])
                # For now, just use the prompt directly
                agent_response = agent.generate_response(prompt, mood=selected_mood, style=selected_style)
                st.markdown(agent_response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": agent_response})

    # --- Separate Input for Saving Memories ---
    st.markdown("---")
    st.subheader("Add a New Memory")
    memory_content = st.text_area("Enter your memory, thought, or idea here:")
    # Optional: Allow user to select chapter and mood manually for the memory itself
    # chapter_select = st.selectbox("Chapter", classifier.chapters, key='memory_chapter')
    # mood_select = st.text_input("Mood", key='memory_mood')

    if st.button("Save Memory"):
        if memory_content:
            # Automatically classify the memory content
            classified_chapter = classifier.classify(memory_content)
            # Mood detection could be added here using the agent or another method
            # For now, mood is None or a placeholder, or could be a user input field
            save_memory(memory_content, chapter=classified_chapter, mood="neutral") # Placeholder mood
            st.success(f"Memory saved to '{classified_chapter}' chapter!")
            # Clear the text area after saving
            st.experimental_rerun() # Rerun to clear text area and update timeline/chapters views
        else:
            st.warning("Memory content cannot be empty.")

# Example usage in app.py:
# from ui.chatbox import render_chatbox
# if selected_page == "Chat with Lorekeeper":
#     render_chatbox()
