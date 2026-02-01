import streamlit as st
import streamlit.components.v1 as components
import time

# ========= REQUIRED SNIPPET FOR PAGE MAINTENANCE ==================
# This will "ping" our server to indicate that the page is active.
# Once the page is closed or inactive, the pings will stop.
components.html("""
    <script>
        setInterval(function() {
            var timestamp = new Date().getTime();
            var img = new Image();
            img.src = "http://127.0.0.1:8502/ping?t=" + timestamp;
        }, 5000); // One ping every 5 seconds
    </script>
""", height=0)
# ------------------------------------------------------------------

# Basic Streamlit setup
st.set_page_config(page_title="My Streamlit EXE", layout="centered")
st.title("Template Page")

st.write(
    "The main issue when creating an EXE for Streamlit is that, when closed, "
    "the app continues running in the background because a terminal command is necessary. "
    "This is addressed by monitoring page activity."
)

user_text = st.text_input("Write something delicious")

if st.button("Send"):
    if user_text:
        st.success(f"I like eating {user_text}")
        st.balloons()
    else:
        st.warning("Please write something.")

# Sidebar example
with st.sidebar:
    st.header("Sidebar")
    st.info("If this works (or doesn't) for you, please open an issue on the GitHub repo.")
    st.markdown("[🔗 Streamlit-to-EXE Template](https://github.com/Gustyper/streamlit-to-exe-template)")