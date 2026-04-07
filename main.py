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
    try:
        # Reduced timeout to catch errors faster
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        # Trigger an early check
        client.admin.command('ping')
        return client.SocialMedia_Enterprise
    except Exception as e:
        return None

client = init_connection()

# --- DATA LOADING & ENRICHMENT ---
def load_data_to_mongo():
    if client is None:
        st.sidebar.error("❌ MongoDB Error: Is the server running?")
        return False
        
    collection = client["airline_insights"]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "Tweets.csv")
    
    if not os.path.exists(csv_path):
        st.error(f"CSV file not found at {csv_path}.")
        return False
    
    try:
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
    except Exception as e:
        st.error(f"Error processing pipeline: {e}")
        return False

# --- UI LAYOUT ---
st.title("🏢 Enterprise Social Intelligence Dashboard")
st.markdown("### Turning Noise into Actionable Business Decisions")

# Sidebar
st.sidebar.header("⚙️ System Controls")
if client is None:
    st.sidebar.error("❌ MongoDB is NOT available.")
    st.sidebar.info("Please start MongoDB using: `sudo systemctl start mongod` if available.")

if st.sidebar.button("🚀 Run Enterprise Pipeline"):
    with st.spinner("Processing High-Value Insights..."):
        if load_data_to_mongo():
            st.sidebar.success("Intelligence Loaded!")
        else:
            st.sidebar.error("Pipeline Failed!")

# Fetch data if possible
if client is not None:
    try:
        collection = client["airline_insights"]
        data = list(collection.find({}, {"_id": 0}))
        df = pd.DataFrame(data)
    except Exception as e:
        st.error(f"Database error: {e}")
        df = pd.DataFrame()
else:
    df = pd.DataFrame()

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
        neg_df = df[df['sentiment'] == 'negative']
        if not neg_df.empty:
            cat_counts = neg_df['category'].value_counts()
            fig_cat = px.bar(cat_counts, 
                             labels={'index':'Issue Category', 'value':'Count'},
                             color=cat_counts.values, 
                             color_continuous_scale='Reds')
            fig_cat.update_layout(xaxis_title="Department", yaxis_title="Number of Complaints")
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.info("No negative sentiment detected today.")
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
    priority_list = df[df['sentiment'] == 'negative'].sort_values(by='impact_score', ascending=False).head(10)
    if not priority_list.empty:
        st.table(priority_list[['user_name', 'content', 'category', 'impact_score']])
    else:
        st.success("No high-priority issues at this moment.")

else:
    if client is not None:
        st.info("👈 Please click 'Run Enterprise Pipeline' in the sidebar to begin.")
    else:
        st.warning("⚠️ Application is in offline mode because MongoDB is not reachable.")

