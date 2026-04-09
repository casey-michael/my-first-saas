import streamlit as st
import requests

# Function to validate the subscription status
def check_subscription(license_key):
    """Verifies if the license key is valid and the monthly sub is active."""
    url = "https://api.lemonsqueezy.com/v1/licenses/validate"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {st.secrets['LEMON_API_KEY']}"
    }
    payload = {"license_key": license_key}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        # 'valid' ensures the key exists; status 'active' ensures they paid this month
        is_valid = data.get("valid", False)
        status = data.get("meta", {}).get("status")
        
        return is_valid and status == "active"
    except Exception:
        return False

# --- UI Layout ---
st.set_page_config(page_title="Word Sorter Pro", page_icon="📝")

st.sidebar.title("🔑 Subscription")
user_key = st.sidebar.text_input("Enter License Key", type="password")

if user_key:
    if check_subscription(user_key):
        st.sidebar.success("Access Granted ✅")
        
        # --- YOUR CORE APP LOGIC ---
        st.title("Word Sorter Pro")
        st.info("Premium Monthly Subscription Active")
        
        text_input = st.text_area("Enter your words (one per line):", height=250)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sort A-Z"):
                words = [w.strip() for w in text_input.split('\n') if w.strip()]
                words.sort()
                st.session_state['result'] = '\n'.join(words)
        
        with col2:
            if st.button("Sort Z-A"):
                words = [w.strip() for w in text_input.split('\n') if w.strip()]
                words.sort(reverse=True)
                st.session_state['result'] = '\n'.join(words)

        if 'result' in st.session_state:
            st.text_area("Sorted List:", value=st.session_state['result'], height=250)
        # ---------------------------
        
    else:
        st.sidebar.error("Invalid or Expired Key ❌")
        st.error("### 💳 Subscription Required")
        st.write("Your key is either incorrect or your monthly payment failed.")
        st.link_button("Renew / Fix Subscription", "https://your-store.lemonsqueezy.com/checkout/...")
else:
    st.title("Welcome to Word Sorter Pro")
    st.write("Please enter your license key in the sidebar to unlock the tool.")
    st.divider()
    st.write("### No key? Get started today!")
    st.write("Subscribe for **$15 initially** ($5 setup fee + $10 first month), then just $10/month.")
    st.link_button("Get Pro Access Now", "https://your-store.lemonsqueezy.com/checkout/...")
    st.stop() # This prevents non-paying users from seeing the code logic
