# 📊 Social Media Analysis using MongoDB

An interactive data analytics dashboard built with **Python**, **MongoDB**, and **Streamlit**. This project implements an ETL pipeline to analyze real-world Twitter sentiment data.

## 🌟 Features
- **ETL Pipeline:** Extracts data from Kaggle CSV $\rightarrow$ Transforms to BSON $\rightarrow$ Loads into MongoDB.
- **Interactive Dashboard:** Visualizes sentiment and user engagement using Plotly.
- **NoSQL Power:** Uses MongoDB for high-performance storage of unstructured social media text.

## 🛠️ Tech Stack
- **Database:** MongoDB
- **Frontend:** Streamlit
- **Language:** Python
- **Libraries:** Pandas, Pymongo, Plotly

## 🚀 How to Run
1. Clone the repo:
   ```bash
   git clone <your-repo-link>
   cd dbms_mini_project
   ```
2. Install dependencies:
   ```bash
   pip install streamlit pymongo pandas plotly
   ```
3. Start MongoDB server.
4. Run the app:
   ```bash
   streamlit run main.py
   ```

## 📊 Dataset
This project uses the **Twitter US Airline Sentiment** dataset from Kaggle.
