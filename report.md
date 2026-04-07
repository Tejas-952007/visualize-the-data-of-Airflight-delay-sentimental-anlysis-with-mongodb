# PROJECT REPORT: Social Media Data Analysis using MongoDB

## 1. INTRODUCTION
In the current digital era, social media platforms generate an unfathomable amount of data every second. This data is "unstructured"—it consists of text, hashtags, emojis, timestamps, and nested user profiles. Traditional relational databases (SQL) struggle to scale and adapt to this fluidity.

This project focuses on leveraging MongoDB, a NoSQL document-oriented database, to store and analyze social media streams.

## 2. ABSTRACT
The goal of this project is to build a data pipeline that ingests social media data, stores it efficiently in MongoDB, and performs analytical queries to derive business intelligence using the Aggregation Framework.

## 3. REQUIREMENT ANALYSIS
- **Functional:** Data Ingestion, NoSQL Storage, Analytical Queries, Keyword Filtering.
- **Non-Functional:** Scalability, Flexibility, Query Efficiency.
- **Tech Stack:** MongoDB, Python 3.x, pymongo, pandas.

## 4. ENTITY RELATIONSHIP DIAGRAM (Conceptual)
MongoDB uses a Document Model:
Collection: `social_media_analysis`
Fields: `_id`, `user` (Nested), `post` (Nested), `hashtags` (Array), `sentiment`.

## 5. CODE
(Implemented in main.py)

## 6. OUTPUT
Console outputs the frequency of hashtags sorted by popularity.

## 7. CONCLUSION
The project demonstrates that NoSQL databases are superior for unstructured social media data, allowing for rapid development and high-performance aggregation.

## 8. ADVANTAGE AND USES
- **Flexibility:** Schema-less nature allows easy updates.
- **Scalability:** Handles high volumes of data.
- **Use Cases:** Brand monitoring, Trend analysis, User profiling.
