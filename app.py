import streamlit as st
import requests

# --- CONFIGURATION ---
CHECKOUT_URL = "https://your-store.lemonsqueezy.com/checkout/..."
FREE_LIMIT = 10

def is_premium(license_key):
    """Checks if the license key is valid and subscription is active."""
    if not license_key:
        return False
    url = "https://api.lemonsqueezy.com/v1/licenses/validate"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {st.secrets['LEMON_API_KEY']}"
    }
    try:
        response = requests.post(url, json={"license_key": license_key}, headers=headers)
        data = response.json()
        return data.get("valid", False) and data.get("meta", {}).get("status") == "active"
    except:
        return False

# --- UI SETUP ---
st.set_page_config(page_title="Word Sorter Pro", page_icon="📝")
st.title("📝 Word Sorter Pro")

# --- SIDEBAR ---
st.sidebar.title("Settings")
user_key = st.sidebar.text_input("Premium License Key", type="password")
has_premium = is_premium(user_key)

if has_premium:
    st.sidebar.success("Premium Active ✅")
else:
    st.sidebar.info(f"Free Version: Max {FREE_LIMIT} words")

# --- MAIN APP LOGIC ---
text_input = st.text_area("Paste your words (one per line):", height=250)

if text_input:
    # Process the list
    words = [w.strip() for w in text_input.split('\n') if w.strip()]
    word_count = len(words)
    
    st.write(f"**Word Count:** {word_count}")

    # Check if user is allowed to sort
    if word_count <= FREE_LIMIT or has_premium:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Sort A-Z"):
                words.sort()
                st.session_state['result'] = '\n'.join(words)
        
        with col2:
            if st.button("Sort Z-A"):
                words.sort(reverse=True)
                st.session_state['result'] = '\n'.join(words)

        if 'result' in st.session_state:
            st.divider()
            st.subheader("Sorted Results:")
            st.text_area("Result Output", value=st.session_state['result'], height=250, label_visibility="collapsed")
            
            st.download_button(
                label="📥 Download List",
                data=st.session_state['result'],
                file_name="sorted_words.txt"
            )
    else:
        # --- PAYWALL ---
        st.error(f"🛑 Limit Reached! You are trying to sort **{word_count}** words.")
        st.warning(f"The free version is limited to **{FREE_LIMIT}** words.")
        st.write("### Unlock Unlimited Sorting")
        st.write("Subscribe for **$15 initially** (includes setup fee), then just **$10/month**.")
        st.link_button("Upgrade to Premium Now", CHECKOUT_URL)
else:
    st.info("Paste some words above to get started!")
