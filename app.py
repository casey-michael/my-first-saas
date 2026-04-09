import streamlit as st
import requests
import re
import pandas as pd
from fpdf import FPDF
from io import BytesIO

# --- CONFIGURATION ---
CHECK_LINK = "https://your-store.lemonsqueezy.com/checkout/..."
FREE_LIMIT = 10

def is_premium(license_key):
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

# --- EXPORT HELPERS ---
def create_pdf(word_list):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Word Sorter Pro - Results", ln=1, align='C')
    for i, word in enumerate(word_list, 1):
        pdf.cell(200, 10, txt=f"{i}. {word}", ln=1)
    return pdf.output(dest='S').encode('latin-1')

def create_excel(word_list):
    df = pd.DataFrame({"No.": list(range(1, len(word_list) + 1)), "Sorted Words": word_list})
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# --- APP UI ---
st.set_page_config(page_title="Word Sorter Pro", page_icon="📝")
st.title("📝 Word Sorter Pro")

# --- SIDEBAR ---
st.sidebar.title("Settings")
user_key = st.sidebar.text_input("Enter License Key", type="password")
has_premium = is_premium(user_key)

if has_premium:
    st.sidebar.success("Premium Active ✅")
else:
    st.sidebar.warning("Free Tier: 10 Word Limit")

# --- CORE LOGIC ---
text_input = st.text_area("Paste your text here:", height=200, placeholder="Once upon a time...")

if text_input:
    all_words = re.findall(r'\b\w+\b', text_input)
    total_count = len(all_words)
    
    # 1. Alert for Word Count Limit
    if not has_premium and total_count > FREE_LIMIT:
        st.warning(f"⚠️ **Limit Detected:** You have {total_count} words. Only the first {FREE_LIMIT} will be sorted in Free Mode. Upgrade to sort the full text!")
    
    # Process Slicing
    words_to_sort = all_words if has_premium else all_words[:FREE_LIMIT]
    
    col1, col2 = st.columns(2)
    sorted_result = None

    if col1.button("Sort A-Z"):
        words_to_sort.sort(key=str.lower)
        sorted_result = words_to_sort
    if col2.button("Sort Z-A"):
        words_to_sort.sort(key=str.lower, reverse=True)
        sorted_result = words_to_sort

    if sorted_result:
        st.divider()
        
        # Display results with numbering
        output_text = "\n".join([f"{i}. {w}" for i, w in enumerate(sorted_result, 1)])
        st.text_area("Sorted List:", value=output_text, height=250)
        
        # --- THE DOWNLOAD PAYWALL & ALERT ---
        st.subheader("📥 Save Your Results")
        
        if has_premium:
            st.write("Choose your format below:")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.download_button("Text (.txt)", data=output_text, file_name="sorted.txt")
            with c2:
                pdf_data = create_pdf(sorted_result)
                st.download_button("PDF (.pdf)", data=pdf_data, file_name="sorted.pdf")
            with c3:
                xlsx_data = create_excel(sorted_result)
                st.download_button("Excel (.xlsx)", data=xlsx_data, file_name="sorted.xlsx")
        else:
            # High-visibility alert about downloading
            st.error("🔒 **Download Feature Locked**")
            st.info("💡 **Premium Benefit:** Subscribers can download results as professional **TXT, PDF, and Excel** files with one click!")
            st.write("To unlock downloads and sort more than 10 words, subscribe for **$15 initially** (then $10/month).")
            st.link_button("🚀 Get Premium Now", CHECK_LINK)
else:
    st.info("Input a paragraph to begin.")
