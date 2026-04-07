# PROJECT REPORT: Social Media Data Analysis using MongoDB

## 1. INTRODUCTION
In the current digital era, social media platforms generate an unfathomable amount of data every second. This data is "unstructured"—it consists of text, hashtags, emojis, timestamps, and nested user profiles. Traditional relational databases (SQL) struggle to scale and adapt to this fluidity.

This project focuses on leveraging MongoDB, a NoSQL document-oriented database, to store and analyze social media streams.

## 2. ABSTRACT
The goal of this project is to build an interactive data pipeline that ingests social media data from Kaggle, stores it in MongoDB, and visualizes business intelligence through a Streamlit dashboard.

## 3. REQUIREMENT ANALYSIS
- **Functional:** Data Ingestion (ETL), NoSQL Storage, Sentiment Visualization, Categorization of complaints.
- **Non-Functional:** Real-time feedback, Interactive charts, Robust error handling for database connection.
- **Tech Stack:** MongoDB, Python 3.x, Streamlit, pymongo, pandas, plotly.

## 4. DATABASE MODEL (Document-Oriented)
MongoDB uses a Document Model:
- **Database:** `SocialMedia_Enterprise`
- **Collection:** `airline_insights`
- **Fields:** `tweet_id`, `user` (Object), `content`, `sentiment`, `category`, `impact_score`.

## 5. DASHBOARD FEATURES
- **ETL Pipeline:** One-click data ingestion from CSV to MongoDB.
- **Crisis Center:** Real-time negativity rate monitor with crisis alerts.
- **Problem Mapping:** Departmental breakdown of complaints (Delay, Staff, Money, Baggage).
- **Sentiment vs. Impact:** Interactive scatter plot to identify high-priority customer tickets.

## 6. OUTPUT
The dashboard provides a visual interface for airline PR and operations teams to monitor brand health and prioritize customer service interventions.

## 7. CONCLUSION
The project demonstrates that NoSQL databases like MongoDB are ideally suited for unstructured social media data, providing the flexibility needed for rapid data ingestion and complex analytical visualization.

## 8. ADVANTAGE AND USES
- **Flexibility:** Schema-less nature allows easy updates to data fields.
- **Scalability:** Handles high volumes of social data efficiently.
- **Use Cases:** Brand monitoring, Crisis management, Operational resource allocation.
