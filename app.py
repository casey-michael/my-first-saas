import streamlit as st
import requests

st.set_page_config(page_title="WordSorter SaaS", page_icon="💳")

# --- LICENSE CHECK FUNCTION ---
def check_subscription(license_key):
    """Checks if the license key is currently active and paid for."""
    url = "https://api.lemonsqueezy.com/v1/licenses/validate"
    headers = {"Accept": "application/json"}
    data = {"license_key": license_key}
    
    try:
        response = requests.post(url, headers=headers, data=data)
        res_data = response.json()
        
        # Check if the license is valid AND active (not expired)
        if res_data.get("valid") and res_data.get("license_key", {}).get("status") == "active":
            return True, "Active"
        elif res_data.get("license_key", {}).get("status") == "expired":
            return False, "Subscription Expired"
        else:
            return False, "Invalid Key"
    except:
        return False, "Connection Error"

# --- SIDEBAR SETUP ---
with st.sidebar:
    st.title("Pro Dashboard")
    user_key = st.text_input("Enter Subscription Key:", type="password")
    
    is_pro = False
    if user_key:
        valid, message = check_subscription(user_key)
        if valid:
            st.success("✅ Subscription Active")
            is_pro = True
        else:
            st.error(f"❌ {message}")
            st.info("Visit the billing portal to renew.")

    st.divider()
    if not is_pro:
        st.write("Monthly Pro Plan: $10/mo")
        st.link_button("💳 Subscribe Now", "https://yourstore.lemonsqueezy.com/checkout/...")

# --- MAIN APP LOGIC ---
st.title("📝 WordSorter Pro")

if is_pro:
    # --- PREMIUM FEATURES ---
    text = st.text_area("Paste your list:")
    order = st.selectbox("Order:", ["A-Z", "Z-A", "Shortest first", "Longest first"])
    
    if text:
        words = text.split()
        if order == "A-Z": words.sort()
        elif order == "Z-A": words.sort(reverse=True)
        elif order == "Shortest first": words.sort(key=len)
        elif order == "Longest first": words.sort(key=len, reverse=True)
        
        st.write(words)
        st.download_button("Download CSV", "\n".join(words))
else:
    # --- FREE FEATURES ---
    st.info("Free Mode: A-Z sorting only (max 5 words).")
    free_input = st.text_area("Input words:")
    if free_input:
        st.write(sorted(free_input.split()[:5]))
