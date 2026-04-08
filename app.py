import streamlit as st

st.set_page_config(page_title="TextInsight SaaS", page_icon="📈")

st.title("📈 TextInsight: Instant Character Analytics")
st.write("Businesses use this to analyze customer feedback trends!")

# The Input
user_text = st.text_area("Paste your text here (e.g., customer reviews):")

if user_text:
    # The Logic (Using your Dictionary Comprehension skills!)
    # This counts how many times each character appears
    char_count = {char: user_text.count(char) for char in set(user_text) if char.strip()}
    
    st.subheader("Your Analysis Results:")
    
    # Displaying the data in a nice way
    st.bar_chart(char_count)
    
    st.write("Detailed Breakdown:")
    st.json(char_count)

    # The "Premium" Hook
    st.info("💡 Upgrade to Pro to export this data to Excel and analyze 10,000+ words!")
