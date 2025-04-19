# Main.py

import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_cohere
from mongo import store_in_mongodb
from streamlit_lottie import st_lottie
import requests
import time

# Load Lottie Animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_scrape = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_4kx2q32n.json")
lottie_parse = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_kdx6cani.json")
lottie_success = load_lottieurl("https://assets4.lottiefiles.com/private_files/lf30_t26law.json")

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    .stTextInput > div > div > input {
        border-radius: 8px;
        padding: 10px;
        background-color: #f4f4f4;
        color: black;
    }
    .stButton button {
        background-color: #00BFFF;
        color: white;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI Title and Sidebar
st.sidebar.title("🔧 AI Web Scraper Navigation")
page = st.sidebar.radio("Go to:", ["🏠 Home", "🕸 Scrape Website", "🔍 Parse Content"])

st.title("🤖 AI-powered Web Scraper & Parser")

if page == "🏠 Home":
    st_lottie(lottie_scrape, height=300)
    st.markdown("""
        Welcome to your AI Web Scraper!  
        1️⃣ Enter a website URL.  
        2️⃣ Let AI scrape and parse data based on your description.  
        3️⃣ Automatically store the parsed results into MongoDB!  
        
        ⚡ Powered by Cohere AI & Streamlit.
    """)

elif page == "🕸 Scrape Website":
    st.header("🌐 Enter the Website URL")

    url = st.text_input("Website URL")

    if st.button("🚀 Scrape Now"):
        if url:
            with st.spinner("Connecting and scraping the website..."):
                dom_content = scrape_website(url)
                body_content = extract_body_content(dom_content)
                cleaned_content = clean_body_content(body_content)

                st.session_state.dom_content = cleaned_content

                st.success("✅ Website scraped successfully!")
                st.balloons()

            with st.expander("🔎 View Cleaned DOM Content"):
                st.text_area("Cleaned DOM Content", cleaned_content, height=300)

elif page == "🔍 Parse Content":
    if "dom_content" not in st.session_state:
        st.warning("⚠️ First scrape a website before parsing!")
    else:
        st.header("✍️ Describe What You Want to Extract")

        parse_description = st.text_area("Enter your parsing instructions here:")

        if st.button("🧠 Parse Content"):
            if parse_description:
                with st.spinner("AI is parsing the content..."):
                    dom_chunks = split_dom_content(st.session_state.dom_content)

                    progress = st.progress(0)
                    for i in range(len(dom_chunks)):
                        time.sleep(0.05)
                        progress.progress((i + 1) / len(dom_chunks))

                    parsed_result = parse_with_cohere(dom_chunks, parse_description)

                st.success("🎉 Content parsed successfully!")

                st.metric("Total Chunks Parsed", len(dom_chunks))
                st.text_area("📝 Parsed Result", parsed_result, height=300)

                metadata = {"url": "URL was in the scrape phase"}
                store_in_mongodb(parsed_result, metadata)

                st.toast("✅ Parsed content stored in MongoDB!", icon="🗄️")
                st_lottie(lottie_success, height=200)

