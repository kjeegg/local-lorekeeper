import streamlit as st
import pandas as pd
import sys
sys.path.append('.') # Allow importing from parent directory
import plotly.express as px # Import Plotly for charts

from memory.memory_store import connect_db

def get_memory_stats():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM memories")
    total_memories = cursor.fetchone()[0]

    # Get counts per chapter
    cursor.execute("SELECT chapter, COUNT(*) FROM memories GROUP BY chapter")
    chapter_counts = cursor.fetchall()

    # Get counts per mood (assuming mood is saved)
    cursor.execute("SELECT mood, COUNT(*) FROM memories WHERE mood IS NOT NULL AND mood != '' GROUP BY mood")
    mood_counts = cursor.fetchall()

    # Get recent memories (e.g., last 5)
    cursor.execute("SELECT id, content, timestamp, chapter, mood FROM memories ORDER BY timestamp DESC LIMIT 5")
    recent_memories = cursor.fetchall()

    conn.close()

    return total_memories, chapter_counts, mood_counts, recent_memories

def render_dashboard():
    st.header("Dashboard")
    st.write("Welcome back, Lorekeeper. Here's a glimpse into your journey.")

    total_memories, chapter_counts, mood_counts, recent_memories = get_memory_stats()

    st.subheader("Overall Stats")
    st.info(f"Total Memories Recorded: {total_memories}")

    # Chapter Distribution Chart
    st.subheader("Memories per Chapter")
    if chapter_counts:
        chapter_df = pd.DataFrame(chapter_counts, columns=['Chapter', 'Count'])
        # Replace None chapter with 'Unclassified' for display
        chapter_df['Chapter'] = chapter_df['Chapter'].fillna('Unclassified')
        fig_chapters = px.pie(chapter_df, values='Count', names='Chapter', title='Distribution of Memories by Chapter')
        st.plotly_chart(fig_chapters, use_container_width=True)
    else:
        st.write("No chapters created yet.")

    # Mood Distribution Chart
    st.subheader("Mood Distribution")
    if mood_counts:
        mood_df = pd.DataFrame(mood_counts, columns=['Mood', 'Count'])
        fig_moods = px.bar(mood_df, x='Mood', y='Count', title='Distribution of Recorded Moods')
        st.plotly_chart(fig_moods, use_container_width=True)
    else:
        st.write("No mood data recorded yet.")

    st.subheader("Recent Activity")
    if recent_memories:
        # Display recent memories
        for mem in recent_memories:
            mem_id, content, timestamp, chapter, mood = mem
            st.markdown(f"*   **Entry #{mem_id}** ({timestamp}) - **{chapter or 'Unclassified'}** ({mood or 'N/A'}): {content[:150]}...") # Display snippet
    else:
        st.info("No recent memories. Add some in the Chat!")

# Example usage in app.py:
# from ui.dashboard_view import render_dashboard
# if selected_page == "Dashboard":
#     render_dashboard()
