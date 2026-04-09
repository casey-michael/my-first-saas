import streamlit as st
import requests
import re
import pandas as pd
from fpdf import FPDF
from io import BytesIO

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

# --- EXPORT FUNCTIONS ---
def create_pdf(word_list):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Word Sorter Pro - Results", ln=1, align='C')
    for word in word_list:
        pdf.cell(200, 10, txt=word, ln=1)
    return pdf.output(dest='S').encode('latin-1')

def create_excel(word_list):
    df = pd.DataFrame(word_list, columns=["Sorted Words"])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

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
    st.sidebar.info(f"Free Version: Sorting first {FREE_LIMIT} words only.")

# --- MAIN APP LOGIC ---
text_input = st.text_area("Paste your story or paragraph:", height=200)

if text_input:
    all_words = re.findall(r'\b\w+\b', text_input)
    total_count = len(all_words)
    
    # Process Slicing
    if has_premium:
        words_to_sort = all_words
    else:
        words_to_sort = all_words[:FREE_LIMIT]

    col1, col2 = st.columns(2)
    sorted_result = None

    with col1:
        if st.button("Sort A-Z"):
            words_to_sort.sort(key=str.lower)
            sorted_result = words_to_sort
    
    with col2:
        if st.button("Sort Z-A"):
            words_to_sort.sort(key=str.lower, reverse=True)
            sorted_result = words_to_sort

    if sorted_result:
        st.divider()
        st.write(", ".join(sorted_result))
        
        # --- EXPORT SECTION ---
        st.subheader("📥 Export Results")
        
        # Basic .txt is free for everyone
        st.download_button("Download as Text (.txt)", data="\n".join(sorted_result), file_name="words.txt")

        # Premium Exports
        if has_premium:
            c1, c2 = st.columns(2)
            with c1:
                pdf_data = create_pdf(sorted_result)
                st.download_button("Download as PDF", data=pdf_data, file_name="sorted.pdf", mime="application/pdf")
            with c2:
                xlsx_data = create_excel(sorted_result)
                st.download_button("Download as Excel", data=xlsx_data, file_name="sorted.xlsx", mime="application/vnd.ms-excel")
        else:
            st.warning("💎 PDF & Excel exports are for Premium members only.")
            st.info("Upgrade for **$15 initially**, then **$10/month** to unlock pro file types.")
            st.link_button("Upgrade Now", CHECKOUT_URL)
else:
    st.info("Paste your text above to start sorting!")
