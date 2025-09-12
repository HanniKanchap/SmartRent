import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_data.csv")
    df.dropna(subset=["Title", "Location", "Price", "Link", "Image", "BHK", "Area"], inplace=True)
    return df

df = load_data()

# Page config
st.set_page_config(page_title="SmartRent Data Insights", layout="wide")

st.title("📊 Rental Market Insights")
st.write("Explore rental trends across Delhi using clean, backend-driven visualizations.")

st.markdown("<hr style='margin-top:20px; margin-bottom:30px;'>", unsafe_allow_html=True)

# 📍 Chart 1: Listings per Location (Top 15)
location_counts = df["Location"].value_counts().nlargest(15).reset_index()
location_counts.columns = ["Location", "Count"]
fig1 = px.bar(
    location_counts,
    x="Location",
    y="Count",
    color="Location",
    title="Number of Listings per Location",
    template="plotly_dark",
    text="Count"
)
fig1.update_traces(textposition="outside")
fig1.update_layout(margin=dict(t=40, b=40), height=500)

st.markdown("""
    <div style="
        background: linear-gradient(to right, #1a1f27, #2c3e50);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 0 12px rgba(255,255,255,0.05);
        margin-bottom: 40px;
    ">
        <h3 style="color:#f0f4f8;">📍 Top 15 Locations by Listing Volume</h3>
    </div>
""", unsafe_allow_html=True)
st.plotly_chart(fig1, use_container_width=True)

# 💰 Chart 2: Price Distribution by Location (Top 15)
top_locations = location_counts["Location"].tolist()
filtered_df = df[df["Location"].isin(top_locations)]
fig2 = px.box(
    filtered_df,
    x="Location",
    y="Price",
    color="Location",
    title="Price Distribution by Location",
    template="plotly_dark",
    points="all"
)
fig2.update_layout(margin=dict(t=40, b=40), height=500)

st.markdown("""
    <div style="
        background: linear-gradient(to right, #1a1f27, #2c3e50);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 0 12px rgba(255,255,255,0.05);
        margin-bottom: 40px;
    ">
        <h3 style="color:#f0f4f8;">💰 Price Spread Across Top 15 Locations</h3>
    </div>
""", unsafe_allow_html=True)
st.plotly_chart(fig2, use_container_width=True)

# 📈 Chart 3: Average Price per Location (unsorted)
avg_price_df = df.groupby("Location")["Price"].mean().reset_index()
fig3 = px.line(
    avg_price_df,
    x="Location",
    y="Price",
    markers=True,
    title="Average Price Trend Across Delhi",
    template="plotly_dark"
)
fig3.update_layout(margin=dict(t=40, b=40), height=500)

st.markdown("""
    <div style="
        background: linear-gradient(to right, #1a1f27, #2c3e50);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 0 12px rgba(255,255,255,0.05);
        margin-bottom: 40px;
    ">
        <h3 style="color:#f0f4f8;">📈 Average Price per Location</h3>
    </div>
""", unsafe_allow_html=True)
st.plotly_chart(fig3, use_container_width=True)

# 🛏️ Chart 4: BHK Distribution (unsorted)
fig4 = px.histogram(
    df,
    x="BHK",
    nbins=10,
    title="Distribution of BHKs",
    template="plotly_dark",
    color_discrete_sequence=["#0078D4"]
)
fig4.update_layout(margin=dict(t=40, b=40), height=400)

st.markdown("""
    <div style="
        background: linear-gradient(to right, #1a1f27, #2c3e50);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 0 12px rgba(255,255,255,0.05);
        margin-bottom: 40px;
    ">
        <h3 style="color:#f0f4f8;">🛏️ BHK Distribution</h3>
    </div>
""", unsafe_allow_html=True)
st.plotly_chart(fig4, use_container_width=True)

# 📐 Chart 5: Price vs. Area (unsorted)
fig5 = px.scatter(
    df,
    x="Area",
    y="Price",
    color="Location",
    hover_data=["Title", "BHK"],
    title="Price vs. Area",
    template="plotly_dark"
)
fig5.update_layout(margin=dict(t=40, b=40), height=500)

st.markdown("""
    <div style="
        background: linear-gradient(to right, #1a1f27, #2c3e50);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 0 12px rgba(255,255,255,0.05);
        margin-bottom: 40px;
    ">
        <h3 style="color:#f0f4f8;">📐 Price vs. Area</h3>
    </div>
""", unsafe_allow_html=True)
st.plotly_chart(fig5, use_container_width=True)