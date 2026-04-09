import streamlit as st
import requests

# --- CONFIGURATION ---
# Replace the URL below with your actual Lemon Squeezy Checkout Link
CHECKOUT_URL = "https://your-store.lemonsqueezy.com/checkout/..."

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
        
        # 'valid' ensures the key exists
        # 'status' must be 'active' to ensure they paid their $10 this month
        is_valid = data.get("valid", False)
        status = data.get("meta", {}).get("status")
        
        return is_valid and status == "active"
    except Exception:
        return False

# --- PAGE SETUP ---
st.set_page_config(page_title="Word Sorter Pro", page_icon="📝")

# --- SIDEBAR: LICENSE VERIFICATION ---
st.sidebar.title("🔐 Premium Access")
user_key = st.sidebar.text_input("Enter License Key", type="password", help="Enter the key sent to your email after purchase.")

if user_key:
    if check_subscription(user_key):
        st.sidebar.success("Subscription Active ✅")
        
        # --- CORE APP LOGIC (ONLY SHOWN TO PAID USERS) ---
        st.title("Word Sorter Pro")
        st.write("Welcome back! Your premium tool is ready.")
        
        text_input = st.text_area("Paste your words or list here (one per line):", height=300)
        
        col1, col2 = st.columns(2)
        
        if text_input:
            words = [w.strip() for w in text_input.split('\n') if w.strip()]
            
            with col1:
                if st.button("Sort Alphabetically (A-Z)"):
                    words.sort()
                    st.session_state['result'] = '\n'.join(words)
            
            with col2:
                if st.button("Sort Reverse (Z-A)"):
                    words.sort(reverse=True)
                    st.session_state['result'] = '\n'.join(words)

            if 'result' in st.session_state:
                st.subheader("Your Sorted Results:")
                st.text_area("", value=st.session_state['result'], height=300, label_visibility="collapsed")
                
                # Professional Download Feature
                st.download_button(
                    label="📥 Download as .txt file",
                    data=st.session_state['result'],
                    file_name="sorted_words.txt",
                    mime="text/plain"
                )
        else:
            st.info("Waiting for input... Paste words above to start sorting.")
            
    else:
        st.sidebar.error("Invalid or Expired Key ❌")
        st.error("### 💳 Subscription Required")
        st.write("We couldn't verify an active **$10/month** subscription for this key.")
        st.link_button("Renew / Fix Subscription", CHECKOUT_URL)
else:
    # --- PUBLIC LANDING PAGE ---
    st.title("🚀 Word Sorter Pro")
    st.write("The fastest way to organize lists, keywords, and data.")
    st.divider()
    st.write("### Unlock Pro Access")
    st.write("Join other pro users for just **$15 today** ($5 setup fee + $10 first month), then only $10/month after that.")
    st.link_button("Get Your License Key Now", CHECKOUT_URL)
    
    st.image("https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?auto=format&fit=crop&w=800", caption="Organize your workflow instantly.")
    st.stop() # Strictly prevents the rest of the code from running
