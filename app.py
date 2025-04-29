import streamlit as st
import os

# st.set_page_config() must be the first Streamlit command
st.set_page_config(page_title='Local Lorekeeper', layout='wide')

# Function to load CSS
def load_css(theme_name):
    css_file_path = 'static/style.css'
    if os.path.exists(css_file_path):
        with open(css_file_path) as f:
            css_content = f.read()
        # Inject CSS with a theme-specific class applied to the body or a main container
        # Targeting Streamlit's main content div might be necessary
        # Let's try injecting the CSS and adding a class to the body via JS if possible, or rely on CSS selectors.
        # A simpler approach for now is to just inject the CSS and use selectors like .stApp for targeting.
        st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
        # Attempt to add a class to the body or a main container using JS injection (less reliable in Streamlit)
        # st.markdown(f"<script>document.body.className = '{theme_name.lower()}-theme';</script>", unsafe_allow_html=True)
        # Let's rely on CSS selectors targeting Streamlit's structure with theme prefixes
    else:
        st.warning("CSS file not found.")

# Now import other modules that might contain Streamlit calls
from ui.sidebar import render_sidebar
from ui.timeline_view import render_timeline
from ui.chapters_view import render_chapters_browser
from ui.chatbox import render_chatbox
from ui.export_view import render_export_view
from ui.dashboard_view import render_dashboard

# Render the sidebar and get the selected page and theme
selected_page, selected_theme = render_sidebar()

# Load and apply CSS based on the selected theme
# We need a way to map theme name to a class or set of styles
# For now, let's just load the CSS file. The CSS file itself will need to handle theme switching
# based on a class applied to a parent element, or by using Streamlit's theming options (if applicable) or custom CSS targeting.
# Let's modify the CSS injection to add a class to the main Streamlit container if possible.

# Streamlit's main content is often within a div with class 'stApp'.
# We can try to inject CSS that targets this div with a theme class.

def apply_theme_css(theme_name):
    css_file_path = 'static/style.css'
    if os.path.exists(css_file_path):
        with open(css_file_path) as f:
            css_content = f.read()
        # Inject CSS. We'll rely on the CSS file having rules like .fantasy-theme .stApp {...}
        st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
        # We can't easily add a class to .stApp directly from Python.
        # The CSS file needs to contain rules that are specific enough.
        # For example, .stApp.fantasy-theme { ... } or body.fantasy-theme .stApp { ... }
        # Since we can't add a class to body or .stApp easily, let's adjust the CSS file to use a different strategy.
        # We can inject theme-specific CSS variables or target elements more directly.
        # Let's revert to just injecting the CSS file content and rely on the CSS file itself to manage themes, perhaps using Streamlit's built-in theme options or targeting specific elements.
        # Given the difficulty of applying a theme class to a parent div, let's simplify.
        # The CSS file will contain all theme styles, and we'll just inject it.
        # The user will need to manually select the theme in the sidebar, but the CSS won't dynamically change the *look* based on that selection without more complex JS injection or relying on Streamlit's limited built-in theme options.
        # Let's stick to the original plan of injecting the CSS file content and assume the CSS file handles themes, perhaps by targeting elements directly or using Streamlit's theming config if the user sets it up.
        # Re-reading the prompt, it asks for 
cat << 'EOF' > app.py
import streamlit as st
import os

# st.set_page_config() must be the first Streamlit command
st.set_page_config(page_title='Local Lorekeeper', layout='wide')

# Function to load and apply theme CSS
def load_theme_css(theme_name):
    theme_map = {
        "Default": "style.css", # Using style.css as the default/base
        "Fantasy": "fantasy.css",
        "Sci-Fi": "sci-fi.css",
        "Minimal": "minimal.css",
    }
    css_file = theme_map.get(theme_name, "style.css")
    css_path = os.path.join('static', css_file)

    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        st.warning(f"Theme CSS file not found: {css_path}")

# Now import other modules that might contain Streamlit calls
from ui.sidebar import render_sidebar
from ui.timeline_view import render_timeline
from ui.chapters_view import render_chapters_browser
from ui.chatbox import render_chatbox
from ui.export_view import render_export_view
from ui.dashboard_view import render_dashboard

# Render the sidebar and get the selected page and theme
selected_page, selected_theme = render_sidebar()

# Load and apply the selected theme CSS
load_theme_css(selected_theme)

# --- Page Routing ---
if selected_page == "Dashboard":
    render_dashboard()

elif selected_page == "Memory Timeline":
    render_timeline()

elif selected_page == "Lore Chapters":
    render_chapters_browser()

elif selected_page == "Chat with Lorekeeper":
    render_chatbox()

elif selected_page == "Export":
    render_export_view()

# You can use selected_theme later for logic, but CSS handles the look
# st.write(f"Current Theme: {selected_theme}") # For debugging
