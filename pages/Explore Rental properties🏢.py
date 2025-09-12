import streamlit as st
import pandas as pd

# Load cleaned rental data
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_data.csv")
    df.dropna(subset=["Title", "Location", "Price", "Link", "Image", "BHK"], inplace=True)
    return df

df = load_data()

# Page config
st.set_page_config(page_title="SmartRent Listings", layout="wide")

st.title("🏙️ Delhi Rental Listings")
st.write("Browse rental properties across Delhi. Filter by location to explore listings and pricing trends.")

# Location filter with default "All"
locations = sorted(df["Location"].unique())
locations.insert(0, "All")
selected_location = st.selectbox("📍 Select a location in Delhi", locations)

# Filtered data
if selected_location == "All":
    filtered_df = df.copy()
    avg_price = int(df["Price"].mean())
    location_label = "Delhi"
else:
    filtered_df = df[df["Location"] == selected_location]
    avg_price = int(filtered_df["Price"].mean())
    location_label = selected_location

# Average price card
st.markdown(f"""
    <div style="
        background: linear-gradient(to right, #1a1f27, #2c3e50);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 0 12px rgba(255, 255, 255, 0.05);
        text-align: center;
        margin-bottom: 30px;
    ">
        <h3 style="color:#f0f4f8;">📊 Average Price in {location_label}</h3>
        <p style="font-size:1.5em; font-weight:bold; color:#ffffff;">₹{avg_price:,}</p>
    </div>
""", unsafe_allow_html=True)

# Listings display
for _, row in filtered_df.iterrows():
    st.markdown(f"""
        <div style="
            background: linear-gradient(to right, #1a1f27, #2c3e50);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 0 12px rgba(255, 255, 255, 0.05);
            margin-bottom: 30px;
        ">
            <div style="display: flex; gap: 20px; align-items: center;">
                <div style="flex: 1;">
                    <img src="{row['Image']}" style="height:200px; width:auto; border-radius:8px;" />
                </div>
                <div style="flex: 2; color: #f0f4f8;">
                    <h3 style="margin-bottom: 8px;">{row['Title']}</h3>
                    <p style="margin: 4px 0;"><strong>📍 Location:</strong> {row['Location']}</p>
                    <p style="margin: 4px 0;"><strong>💰 Price:</strong> ₹{int(row['Price']):,}</p>
                    <p style="margin: 4px 0;"><strong>🛏️ BHK:</strong> {row['BHK']}</p>
                    <a href="{row['Link']}" target="_blank" style="
                        display: inline-block;
                        margin-top: 10px;
                        padding: 8px 16px;
                        background-color: #07375b;
                        color: white;
                        text-decoration: none;
                        border-radius: 6px;
                        font-weight: bold;
                    ">🔗 Visit Listing</a>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)