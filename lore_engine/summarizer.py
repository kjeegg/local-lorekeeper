import sqlite3
import sys
sys.path.append('.') # Allow importing from parent directory

from memory.memory_store import connect_db
from lore_engine.agent import LorekeeperAgent

class MemorySummarizer:
    def __init__(self, agent: LorekeeperAgent):
        self.agent = agent

    def get_memories(self, chapter=None, start_date=None, end_date=None):
        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT content, timestamp, chapter, mood FROM memories WHERE 1=1"
        params = []

        if chapter:
            query += " AND chapter = ?"
            params.append(chapter)
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)

        query += " ORDER BY timestamp ASC"

        cursor.execute(query, params)
        memories = cursor.fetchall()
        conn.close()
        return memories

    def summarize_memories(self, chapter=None, start_date=None, end_date=None, style='reflective'):
        memories = self.get_memories(chapter, start_date, end_date)

        if not memories:
            return "No memories found for the specified criteria."

        # Format memories for the agent
        memory_text = "\n---\n".join([f"Timestamp: {m[1]}\nChapter: {m[2]}\nMood: {m[3]}\nContent: {m[0]}" for m in memories])

        # Craft a prompt for the agent to summarize
        summary_prompt = f"Summarize the following memories in a narrative style, focusing on key events, lessons, and feelings. Adopt a {style} tone.\n\nMemories:\n{memory_text}"

        try:
            summary = self.agent.generate_response(summary_prompt, style=style)
            return summary
        except Exception as e:
            print(f"Error during summarization: {e}")
            return "Error: Could not generate summary."

# Example usage (for testing)
# if __name__ == '__main__':
#     # This requires the database to have some entries and Ollama to be running
#     # Example: Insert some dummy data first
#     # conn = connect_db()
#     # cursor = conn.cursor()
#     # cursor.execute("INSERT INTO memories (content, chapter, mood) VALUES (?, ?, ?)", ("Learned Python basics.", "Learning", "excited"))
#     # cursor.execute("INSERT INTO memories (content, chapter, mood) VALUES (?, ?, ?)", ("Finished the first chapter of my book.", "Achievements", "proud"))
#     # conn.commit()
#     # conn.close()

#     agent = LorekeeperAgent()
#     summarizer = MemorySummarizer(agent)
#     # Example: Summarize all memories
#     # summary = summarizer.summarize_memories()
#     # print("\n--- Full Summary ---\n", summary)

#     # Example: Summarize 'Learning' chapter
#     # learning_summary = summarizer.summarize_memories(chapter='Learning', style='reflective')
#     # print("\n--- Learning Summary ---\n", learning_summary)

#     # Example: Summarize memories from a specific date range (adjust dates as needed)
#     # date_summary = summarizer.summarize_memories(start_date='2023-01-01 00:00:00', end_date='2024-12-31 23:59:59', style='poetic')
#     # print("\n--- Date Range Summary ---\n", date_summary)
