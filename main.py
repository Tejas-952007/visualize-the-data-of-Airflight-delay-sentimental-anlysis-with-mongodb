import streamlit as st
import pymongo
from pymongo import MongoClient
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import re
from collections import Counter

# Page Configuration
st.set_page_config(page_title="Enterprise Social Intelligence", page_icon="🏢", layout="wide")

# --- DATABASE CONNECTION ---
@st.cache_resource
def init_connection():
    return MongoClient("mongodb://localhost:27017/").SocialMedia_Enterprise

client = init_connection()
collection = client["airline_insights"]

# --- DATA LOADING & ENRICHMENT ---
def load_data_to_mongo():
    csv_path = os.path.expanduser("~/dbms_mini_project/Tweets.csv")
    if not os.path.exists(csv_path):
        st.error(f"CSV file not found at {csv_path}.")
        return False
    
    df = pd.read_csv(csv_path)
    
    # Enterprise Enrichment: Define Categories for "Actionable Insights"
    categories = {
        'delay': ['delay', 'late', 'waiting', 'hours', 'schedule'],
        'staff': ['staff', 'rude', 'attitude', 'employee', 'service'],
        'money': ['refund', 'money', 'charge', 'price', 'expensive'],
        'baggage': ['bag', 'luggage', 'lost', 'suitcase']
    }

    def categorize_tweet(text):
        text = str(text).lower()
        for cat, keywords in categories.items():
            if any(k in text for k in keywords):
                return cat
        return 'other'

    json_records = []
    for _, row in df.iterrows():
        json_records.append({
            "tweet_id": row['tweet_id'],
            "user": {"name": row['name']},
            "content": row['text'],
            "sentiment": row['airline_sentiment'],
            "category": categorize_tweet(row['text']),
            "impact_score": len(str(row['text']).split()) * 1.5 
        })
    
    collection.delete_many({})
    collection.insert_many(json_records)
    return True

# --- UI LAYOUT ---
st.title("🏢 Enterprise Social Intelligence Dashboard")
st.markdown("### Turning Noise into Actionable Business Decisions")

# Sidebar
st.sidebar.header("⚙️ System Controls")
if st.sidebar.button("🚀 Run Enterprise Pipeline"):
    with st.spinner("Processing High-Value Insights..."):
        if load_data_to_mongo():
            st.sidebar.success("Intelligence Loaded!")
        else:
            st.sidebar.error("Pipeline Failed!")

# Fetch data
data = list(collection.find({}, {"_id": 0}))
df = pd.DataFrame(data)

if not df.empty:
    # --- FIX: Flatten the user dictionary to a column 'user_name' ---
    if 'user' in df.columns:
        df['user_name'] = df['user'].apply(lambda x: x.get('name', 'Unknown') if isinstance(x, dict) else 'Unknown')

    # --- ROW 1: THE CRISIS CENTER ---
    neg_rate = (len(df[df['sentiment'] == 'negative']) / len(df)) * 100
    
    if neg_rate > 50:
        st.error(f"🚨 CRISIS ALERT: Negativity Rate is {neg_rate:.1f}%! Immediate PR Intervention Required.")
    else:
        st.success(f"✅ Brand Health Stable: Negativity Rate at {neg_rate:.1f}%")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Brand Mentions", f"{len(df):,}")
    c2.metric("Critical Issues", len(df[df['sentiment'] == 'negative']))
    c3.metric("Unique Customers", df['user_name'].nunique())

    st.divider()

    # --- ROW 2: ACTIONABLE INSIGHTS (THE "WHY") ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🎯 Departmental Problem Map")
        cat_counts = df[df['sentiment'] == 'negative']['category'].value_counts()
        fig_cat = px.bar(cat_counts, 
                         labels={'index':'Issue Category', 'value':'Count'},
                         color=cat_counts.values, 
                         color_continuous_scale='Reds')
        fig_cat.update_layout(xaxis_title="Department", yaxis_title="Number of Complaints")
        st.plotly_chart(fig_cat, use_container_width=True)
        st.info("💡 **Insight:** Use this to allocate resources to the failing department.")

    with col_right:
        st.subheader("🎭 Sentiment vs. Impact")
        fig_impact = px.scatter(df, x='sentiment', y='impact_score', 
                               color='sentiment', 
                               size='impact_score',
                               hover_data=['content'],
                               color_discrete_map={'positive':'green', 'neutral':'gray', 'negative':'red'})
        st.plotly_chart(fig_impact, use_container_width=True)
        st.info("💡 **Insight:** Largest red bubbles are high-priority tickets.")

    st.divider()

    # --- ROW 3: PRIORITY LIST ---
    st.subheader("🚩 High-Priority Intervention List")
    # Corrected the column names here to use 'user_name' instead of 'user.name'
    priority_list = df[df['sentiment'] == 'negative'].sort_values(by='impact_score', ascending=False).head(10)
    st.table(priority_list[['user_name', 'content', 'category', 'impact_score']])

else:
    st.info("👈 Please click 'Run Enterprise Pipeline' in the sidebar to begin.")
