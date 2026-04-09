import streamlit as st
import requests

# 1. Function to verify the subscription status
def is_subscription_active(license_key):
    """Checks with Lemon Squeezy if the subscription is currently active."""
    url = "https://api.lemonsqueezy.com/v1/licenses/validate"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {st.secrets['LEMON_API_KEY']}"
    }
    payload = {"license_key": license_key}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        # 'valid' means the key exists; 'status' must be 'active' for subscriptions
        status = data.get("meta", {}).get("status")
        return data.get("valid", False) and status == "active"
    except Exception:
        return False

# 2. Sidebar UI for the License Key
st.sidebar.title("🔐 Word Sorter Pro")
user_license = st.sidebar.text_input("Enter your License Key", type="password")

if user_license:
    if is_subscription_active(user_license):
        st.sidebar.success("Subscription Active! ✅")
        
        # --- YOUR MAIN APP CODE STARTS HERE ---
        st.title("Word Sorter Pro")
        st.write("Welcome back! Your premium features are unlocked.")
        
        text_data = st.text_area("Enter words to sort (one per line):", height=200)
        if st.button("Sort Alphabetically"):
            if text_data:
                words = [word.strip() for word in text_data.split('\n') if word.strip()]
                words.sort()
                st.text_area("Sorted Results:", value='\n'.join(words), height=200)
            else:
                st.warning("Please enter some words first.")
        # --- YOUR MAIN APP CODE ENDS HERE ---
        
    else:
        st.sidebar.error("Invalid or Expired Subscription ❌")
        st.error("Your subscription is inactive. Please renew to continue.")
        st.link_button("Renew Subscription ($10/mo)", "https://your-store.lemonsqueezy.com/checkout/...")
else:
    # This part shows if the user hasn't entered a key yet
    st.info("### 🚀 Get Started with Word Sorter Pro")
    st.write("Organize your lists instantly. Subscribe now for just **$15 initially** ($5 setup fee + $10 first month).")
    st.link_button("Subscribe & Get License Key", "https://your-store.lemonsqueezy.com/checkout/...")
    st.stop() # Prevents the rest of the app from loading
