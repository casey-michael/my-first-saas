import streamlit as st

st.set_page_config(page_title="WordSorter SaaS", page_icon="📝")

st.title("📝 Smart Word Sorter")

# 1. Sidebar for Access
with st.sidebar:
    st.header("Settings")
    access_code = st.text_input("Enter Pro Access Code:", type="password")
    
    # The Lemon Squeezy Button
    st.divider()
    st.write("Don't have a code?")
    st.link_button("🚀 Get Pro Access ($5)", "https://your-store.lemonsqueezy.com/checkout/...") 

# 2. Free vs Pro Logic
if access_code == "NIGERIA2026": # You can change this or automate it later
    st.success("Pro Access Active!")
    # PRO FEATURES
    user_input = st.text_area("Paste giant list (Pro Mode):")
    if user_input:
        words = sorted(user_input.split())
        st.write(words)
        st.download_button("Download as CSV", data="\n".join(words))
else:
    # FREE FEATURES
    st.info("Free Mode: Sort up to 10 words.")
    user_input = st.text_area("Paste your words:")
    if user_input:
        words = user_input.split()[:10] # Limit to 10 words
        st.write(sorted(words))
        if len(user_input.split()) > 10:
            st.warning("Only the first 10 words were sorted. Upgrade to Pro for unlimited!")
