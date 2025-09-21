import streamlit as st
import pandas as pd
import urllib.parse

# Load data
def load_data():
    df = pd.read_csv("data/cleaned_data.csv")
    df.dropna(subset=["Price", "Area"], inplace=True)

    return df

df = load_data()

# Page config
st.set_page_config(page_title="SmartRent", layout="wide")

st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #0f1117 !important;
            color: #eaeef2 !important;
            font-family: 'Segoe UI', sans-serif;
        }

        .smartrent-header {
            background: linear-gradient(135deg, #121820, #1e2a38);
            padding: 36px;
            border-radius: 14px;
            text-align: center;
            box-shadow: inset 0 0 0 1px #2a3b4d, 0 0 20px rgba(255, 255, 255, 0.05);
            margin-bottom: 48px;
        }

        .smartrent-header h1 {
            color: #f8fbff;
            font-size: 3em;
            margin-bottom: 10px;
            letter-spacing: 0.5px;
        }

        .smartrent-header p {
            color: #cfd8e3;
            font-size: 1.2em;
            margin-top: 0;
        }

        .scorecard {
            text-align: center;
            padding: 16px;
            border-radius: 12px;
            background: linear-gradient(145deg, #1a1f27, #232a35);
            box-shadow: inset 0 0 0 1px #2e3a4d, 0 4px 12px rgba(7, 55, 91, 0.3);
            color: #f0f2f5;
            margin-bottom: 24px;
        }

        .scorecard h3 {
            margin-bottom: 6px;
            font-size: 1.2em;
            color: #d0d6dd;
        }

        .scorecard p {
            font-size: 1.1em;
            font-weight: bold;
            color: #ffffff;
        }

        .contact-button {
            background-color: #062a44;
            color: #ffffff !important;
            padding: 10px 20px;
            border-radius: 6px;
            text-decoration: none !important;
            font-weight: bold;
            display: inline-block;
            margin-top: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.4);
        }

        .contact-button:hover {
            background-color: #01406b;
        }

        .footer {
            margin-top: 60px;
            padding: 20px;
            text-align: center;
            font-size: 0.9em;
            color: #777;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class='smartrent-header'>
        <h1>🏠 SmartRent</h1>
        <p>Discover the pulse of the rental market — clean data, smart insights, and backend precision.</p>
    </div>
""", unsafe_allow_html=True)

st.image('./assets/image.png',use_container_width=True)
# Scorecards
col1, col2, col3 = st.columns(4)
with col1:
    st.markdown(f"<div class='scorecard'><h3>Price Range</h3><p>₹{int(df['Price'].min())} – ₹{int(df['Price'].max())}</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='scorecard'><h3>Locations Covered</h3><p>{len(df['Location'].unique())}</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='scorecard'><h3>Total Listings</h3><p>{len(df)}</p></div>", unsafe_allow_html=True)
st.divider()

# FAQs Section
st.subheader("❓ Frequently Asked Questions")

with st.expander("What is SmartRent?"):
    st.write(
        "SmartRent aggregates and analyzes rental listings from OLX Delhi using automated scraping and cleaning pipelines. "
        "It delivers clean, deduplicated, and structured rental data for backend-driven dashboards and analytics."
    )

with st.expander("How often is the data updated?"):
    st.write(
        "Our GitHub Actions workflow runs weekly, fetching fresh listings, cleaning them, and appending them to the existing dataset. "
        "This ensures continuity, reproducibility, and minimal manual intervention."
    )

with st.expander("Can I filter listings?"):
    st.write(
        "Yes. The dashboard supports filtering by price, BHK count, and area. You can also extend it to include location, furnishing status, or amenities."
    )

with st.expander("Can I integrate this with my own backend?"):
    st.write(
        "Absolutely. SmartRent is designed with modular scraping, cleaning, and CI/CD logic. You can plug it into your own database, API, or dashboard stack."
    )

st.divider()

# Contact Us Section
st.subheader("📬 Contact Us")

with st.form("contact_form"):
    user_email = st.text_input("Your Email", placeholder="you@example.com")
    user_message = st.text_area("Your Message", placeholder="Type your query or feedback here...")
    submitted = st.form_submit_button("Create Email")

    if submitted and user_email and user_message:
        subject = "SmartRent Inquiry"
        body = f"From: {user_email}\n\n{user_message}"
        mailto_link = f"mailto:smartrent@example.com?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
        st.info('Your email is created successfully !!!')
        st.markdown(f"<a href='{mailto_link}' class='contact-button'>📨 Click to Send   </a>", unsafe_allow_html=True)
    elif submitted:
        st.warning("Please fill in both your email and message before composing.")

st.markdown("""
    <style>
        .chatbot-button {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background-color: #062a44;
            color: white !important;
            padding: 12px 20px;
            border-radius: 30px;
            font-weight: bold;
            text-decoration: none !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 9999;
        }

        .chatbot-button:hover {
            background-color: #01406b;
        }
    </style>

    <a href="/AI_Assistant✨" class="chatbot-button">Chat ✨</a>
""", unsafe_allow_html=True)
# Footer
st.markdown("<div class='footer'>© 2025 SmartRent • Built with precision by HANNI</div>", unsafe_allow_html=True)