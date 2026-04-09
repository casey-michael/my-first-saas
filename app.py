import streamlit as st
import requests
import re
import pandas as pd
from fpdf import FPDF
from io import BytesIO
from collections import Counter # New import for counting words

# --- CONFIGURATION ---
CHECK_LINK = "https://your-store.lemonsqueezy.com/checkout/..."
FREE_LIMIT = 10

def is_premium(license_key):
    if not license_key:
        return False
    
    # We use the 'activate' link to turn the key from Inactive to Active
    url = "https://api.lemonsqueezy.com/v1/licenses/activate"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {st.secrets['LEMON_API_KEY']}"
    }
    
    # Lemon Squeezy requires 'instance_name' to track which device is using the key
    payload = {
        "license_key": license_key,
        "instance_name": "User_Laptop"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        # This will show the real reason for failure in your black CMD window
        print(f"Lemon Squeezy Response: {data}")

        # Success Case 1: Key just became active
        if data.get("activated") == True:
            return True
        
        # Success Case 2: Key was already active from a previous session
        if data.get("error") == "license_key_already_active":
            return True

        # Failure Case: Show the specific error in the sidebar for debugging
        if "error" in data:
            st.sidebar.error(f"Issue: {data['error']}")
            
        return False
    except Exception as e:
        st.sidebar.error(f"Connection Error: {e}")
        return False

# --- EXPORT HELPERS ---
def create_pdf(word_list, counts):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Word Sorter Pro - Results", ln=1, align='C')
    for i, word in enumerate(word_list, 1):
        txt = f"{i}. {word} (Occurrences: {counts[word]})"
        pdf.cell(200, 10, txt=txt, ln=1)
    return pdf.output(dest='S').encode('latin-1')

def create_excel(word_list, counts):
    df = pd.DataFrame({
        "No.": list(range(1, len(word_list) + 1)),
        "Word": word_list,
        "Occurrences": [counts[w] for w in word_list]
    })
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
text_input = st.text_area("Paste your text here:", height=200, placeholder="Type or paste your story...")

if text_input:
    # Extract all words and clean them to lowercase for accurate counting
    all_words_raw = re.findall(r'\b\w+\b', text_input.lower())
    total_count = len(all_words_raw)
    
    # Create a frequency map of ALL words first
    word_counts = Counter(all_words_raw)
    
    # Get unique words to avoid sorting the same word twice (optional, but cleaner)
    unique_words = sorted(list(set(all_words_raw)))

    # 1. Alert for Word Count Limit
    if not has_premium and len(unique_words) > FREE_LIMIT:
        st.warning(f"⚠️ **Limit Detected:** You have {len(unique_words)} unique words. Only the first {FREE_LIMIT} are shown in Free Mode.")
    
    # Process Slicing
    display_list = unique_words if has_premium else unique_words[:FREE_LIMIT]
    
    col1, col2 = st.columns(2)
    sorted_result = None

    if col1.button("Sort A-Z"):
        display_list.sort() # Already lowercased
        sorted_result = display_list
    if col2.button("Sort Z-A"):
        display_list.sort(reverse=True)
        sorted_result = display_list

    if sorted_result:
        st.divider()
        
        # Display results with numbering AND occurrence count
        # Example: 1. apple (Occurrences: 3)
        output_text = "\n".join([f"{i}. {w} (Occurrences: {word_counts[w]})" for i, w in enumerate(sorted_result, 1)])
        st.text_area("Sorted List with Counts:", value=output_text, height=250)
        
        # --- THE DOWNLOAD PAYWALL ---
        st.subheader("📥 Save Your Results")
        
        if has_premium:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.download_button("Text (.txt)", data=output_text, file_name="sorted.txt")
            with c2:
                pdf_data = create_pdf(sorted_result, word_counts)
                st.download_button("PDF (.pdf)", data=pdf_data, file_name="sorted.pdf")
            with c3:
                xlsx_data = create_excel(sorted_result, word_counts)
                st.download_button("Excel (.xlsx)", data=xlsx_data, file_name="sorted.xlsx")
        else:
            st.error("🔒 **Download Feature Locked**")
            st.info("💡 **Premium Benefit:** Sort unlimited words and download as **TXT, PDF, and Excel**!")
            st.link_button("🚀 Get Premium Now", CHECK_LINK)
else:
    st.info("Input a paragraph to begin.")
