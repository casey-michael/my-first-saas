import streamlit as st
import requests

st.set_page_config(page_title="WordSorter Pro", page_icon="🚀")

# --- CONFIGURATION ---
LEMON_SQUEEZY_API_KEY = st.secrets["LEMON_API_KEY"] # Put this in your Streamlit Secrets

def validate_license(license_key):
    """Checks with Lemon Squeezy if the key is valid and not used by others"""
    url = "https://api.lemonsqueezy.com/v1/licenses/activate"
    headers = {"Accept": "application/json"}
    data = {
        "license_key": license_key,
        "instance_name": "User_Device" # This locks it to their current browser/session
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Settings")
    user_key = st.text_input("Enter your License Key:", type="password")
    is_pro = False
    
    if user_key:
        result = validate_license(user_key)
        if result.get("activated"):
            st.success("Pro Active!")
            is_pro = True
        else:
            st.error("Invalid or Already Used Key")

    st.divider()
    if not is_pro:
        st.write("Unlock Unlimited Sorting for $10")
        st.link_button("🚀 Buy Pro License", "https://yourstore.lemonsqueezy.com/checkout/...")

# --- MAIN APP ---
st.title("📝 WordSorter Pro")

if is_pro:
    # --- PRO FEATURES ---
    text = st.text_area("Paste your list:")
    sort_choice = st.selectbox("Select Sorting Method:", 
                               ["A to Z", "Z to A", "By Length (Shortest first)", "By Length (Longest first)"])
    
    if text:
        words = text.split()
        
        # New Feature: Advanced Sorting Logic
        if sort_choice == "A to Z":
            words.sort()
        elif sort_choice == "Z to A":
            words.sort(reverse=True)
        elif sort_choice == "By Length (Shortest first)":
            words.sort(key=len)
        else:
            words.sort(key=len, reverse=True)

        st.write("✅ Sorted Results:")
        st.write(words)
        st.download_button("Export to CSV", data="\n".join(words))

else:
    # --- FREE FEATURES ---
    st.warning("Free version: Sorting A to Z only (Max 5 words)")
    free_text = st.text_area("Paste words:")
    if free_text:
        words = sorted(free_text.split()[:5])
        st.write(words)
