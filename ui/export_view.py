import streamlit as st
import pandas as pd
import sys
sys.path.append('.') # Allow importing from parent directory
import os
from datetime import datetime

from memory.memory_store import connect_db

# Import fpdf2 for PDF export
try:
    from fpdf import FPDF
except ImportError:
    st.error("Please install fpdf2: `pip install fpdf2`")
    FPDF = None # Set to None if import fails

EXPORT_DIR = 'memory/export'

# Ensure export directory exists
if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)

def get_all_memories_for_export():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, timestamp, chapter, mood FROM memories ORDER BY timestamp ASC")
    memories = cursor.fetchall()
    conn.close()
    return memories

def export_to_markdown(memories):
    if not memories:
        return ""

    markdown_content = "# Local Lorekeeper - Memory Export\n\n"
    markdown_content += f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    markdown_content += "---\n\n"

    for memory in memories:
        mem_id, content, timestamp, chapter, mood = memory
        markdown_content += f"## Entry #{mem_id} - {timestamp}\n"
        markdown_content += f"**Chapter:** {chapter} | **Mood:** {mood}\n\n"
        markdown_content += f"{content}\n\n"
        markdown_content += "---\n\n"

    return markdown_content

def export_to_pdf(memories):
    if not FPDF:
        return None # Cannot export if fpdf2 is not installed

    if not memories:
        return None

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Local Lorekeeper - Memory Export", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.ln(10)

    for memory in memories:
        mem_id, content, timestamp, chapter, mood = memory
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(0, 10, txt=f"Entry #{mem_id} - {timestamp}", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 10, txt=f"Chapter: {chapter} | Mood: {mood}", ln=True)
        pdf.ln(2)
        pdf.set_font("Arial", size=10)
        # Add content, handling potential line breaks
        pdf.multi_cell(0, 5, txt=content)
        pdf.ln(5)
        pdf.cell(0, 0, "", line=1, ln=True) # Horizontal line
        pdf.ln(5)

    # Save the PDF to a bytes object
    return pdf.output(dest='S').encode('latin1') # Use latin1 encoding for bytes

def render_export_view():
    st.header("Export Memories")

    memories = get_all_memories_for_export()

    if not memories:
        st.info("No memories recorded yet to export.")
        return

    st.write(f"Found {len(memories)} memories to export.")

    # Markdown Export
    markdown_content = export_to_markdown(memories)
    st.download_button(
        label="Export to Markdown (.md)",
        data=markdown_content,
        file_name=f"lorekeeper_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        mime="text/markdown"
    )

    # PDF Export
    if FPDF:
        pdf_output = export_to_pdf(memories)
        if pdf_output:
             st.download_button(
                label="Export to PDF (.pdf)",
                data=pdf_output,
                file_name=f"lorekeeper_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
        else:
             st.warning("Could not generate PDF export.")
    else:
        st.warning("PDF export requires the 'fpdf2' library. Please install it.")

# Example usage in app.py:
# from ui.export_view import render_export_view
# if selected_page == "Export":
#     render_export_view()
