
import streamlit as st
import pandas as pd
import sys
sys.path.append('.') # Allow importing from parent directory

from memory.memory_store import connect_db, delete_memory, get_memories_by_chapter, get_memory_by_id, update_memory # Import update functions
from lore_engine.classifier import ChapterClassifier # Import classifier for chapter selection
from lore_engine.agent import LorekeeperAgent # Import agent to get chapters

# Initialize classifier to get chapter list (can be cached)
@st.cache_resource
def get_classifier():
    # Note: This might require Ollama to be running even if not classifying here
    # A better approach might be to store chapters in a config or the DB
    # For now, let's initialize the agent/classifier to get the list
    try:
        agent = LorekeeperAgent() # This might fail if Ollama is not available
        classifier = ChapterClassifier(agent)
        return classifier
    except Exception as e:
        st.warning(f"Could not initialize LorekeeperAgent for chapter list: {e}. Using default chapters.")
        class MockClassifier:
            def __init__(self):
                self.chapters = ["Learning", "Challenges", "Dreams", "Achievements", "Reflections", "Ideas", "Daily Life"]
        return MockClassifier()

classifier = get_classifier()

# Moved get_memories_by_chapter to memory_store.py
# def get_memories_by_chapter():
#     conn = connect_db()
#     cursor = conn.cursor()
#     # Fetch all memories, ordered by chapter and then timestamp
#     cursor.execute("SELECT id, content, timestamp, chapter, mood FROM memories ORDER BY chapter ASC, timestamp ASC")
#     memories = cursor.fetchall()
#     conn.close()
#     # Convert to pandas DataFrame
#     df = pd.DataFrame(memories, columns=['id', 'content', 'timestamp', 'chapter', 'mood'])
#     return df

def render_chapters_browser():
    st.header("Lore Chapters")

    memories_df = pd.DataFrame(get_memories_by_chapter(), columns=['id', 'content', 'timestamp', 'chapter', 'mood'])

    if memories_df.empty:
        st.info("No memories recorded yet. Add some in the Chat or Dashboard!")
        return

    # Add Search functionality
    search_query = st.text_input("Search memories within chapters:", "")

    filtered_memories_df = memories_df
    if search_query:
        # Filter memories based on content, chapter, or mood (case-insensitive)
        filtered_memories_df = memories_df[
            memories_df['content'].str.contains(search_query, case=False, na=False) |
            filtered_memories_df['chapter'].str.str.contains(search_query, case=False, na=False).fillna(False) |
            filtered_memories_df['mood'].str.str.contains(search_query, case=False, na=False).fillna(False)
        ]

    if filtered_memories_df.empty:
        st.info("No memories match your search query in any chapter.")
    else:
        # State variable to track which memory is being edited (for chapters view)
        if 'editing_chapter_memory_id' not in st.session_state:
            st.session_state.editing_chapter_memory_id = None

        # Get unique chapters from the FILTERED dataframe
        chapters = filtered_memories_df['chapter'].unique()

        # Display memories grouped by chapter
        for chapter in chapters:
            st.subheader(f"Chapter: {chapter}")
            # Filter the already filtered dataframe for the current chapter
            chapter_memories = filtered_memories_df[filtered_memories_df['chapter'] == chapter]

            if chapter_memories.empty:
                 # This case should ideally not happen if the chapter is in filtered_memories_df['chapter'].unique()
                 st.write("No entries in this chapter match the search query.")
            else:
                for index, row in chapter_memories.iterrows():
                    mem_id = row['id']

                    # If this memory is being edited, display the edit form
                    if st.session_state.editing_chapter_memory_id == mem_id:
                        st.subheader(f"Editing Entry #{mem_id} in Chapter '{chapter}'")
                        memory_details = get_memory_by_id(mem_id)
                        if memory_details:
                            edit_content = st.text_area("Content:", value=memory_details[1], key=f"edit_chapter_content_{mem_id}")
                            # Find the index of the current chapter in the list for the selectbox default
                            current_chapter = memory_details[3] if memory_details[3] in classifier.chapters else classifier.chapters[0]
                            chapter_index = classifier.chapters.index(current_chapter) if current_chapter in classifier.chapters else 0

                            edit_chapter = st.selectbox("Chapter:", classifier.chapters, index=chapter_index, key=f"edit_chapter_chapter_{mem_id}")
                            edit_mood = st.text_input("Mood:", value=memory_details[4] or '', key=f"edit_chapter_mood_{mem_id}")

                            col_save, col_cancel = st.columns(2)
                            with col_save:
                                if st.button("Save Changes", key=f"save_chapter_edit_{mem_id}"):
                                    update_memory(mem_id, edit_content, edit_chapter, edit_mood)
                                    st.success(f"Memory #{mem_id} updated.")
                                    st.session_state.editing_chapter_memory_id = None # Exit edit mode
                                    st.experimental_rerun() # Rerun to update the list
                            with col_cancel:
                                 if st.button("Cancel", key=f"cancel_chapter_edit_{mem_id}"):
                                    st.session_state.editing_chapter_memory_id = None # Exit edit mode
                                    st.experimental_rerun() # Rerun to exit edit mode
                        else:
                            st.error("Could not load memory details for editing.")

                    # If not editing, display the memory snippet and action buttons
                    else:
                        col1, col2, col3 = st.columns([4, 0.5, 0.5]) # Use columns for content, edit, and delete buttons
                        with col1:
                            st.markdown(f"* **Entry #{row['id']}** ({row['timestamp']}) - {row['content'][:100]}... (Mood: {row['mood']})") # Display snippet
                            # Optional: Add an expander to show full content
                            with st.expander("Read More"):
                                st.write(row['content'])
                        with col2:
                            # Add an edit button
                            if st.button("Edit", key=f"edit_chapter_{mem_id}"):
                                st.session_state.editing_chapter_memory_id = mem_id # Enter edit mode for this memory
                                st.experimental_rerun() # Rerun to show the edit form
                        with col3:
                             # Add a delete button
                            if st.button("Delete", key=f"delete_chapter_{mem_id}"):
                                delete_memory(mem_id)
                                st.success(f"Memory #{mem_id} deleted from chapter '{chapter}'.")
                                st.session_state.editing_chapter_memory_id = None # Clear editing state if deleting the edited one
                                st.experimental_rerun() # Rerun to update the list

                st.markdown("---") # Separator between memories within a chapter

# Example usage in app.py:
# from ui.chapters_view import render_chapters_browser
# if selected_page == "Lore Chapters":
#     render_chapters_browser()
