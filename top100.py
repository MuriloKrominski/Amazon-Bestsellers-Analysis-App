import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration for minimal style
st.set_page_config(page_title="Trending Books", page_icon="📚", layout="wide")

# Apply dark theme configuration
st.markdown("""
    <style>
        /* Background color for the main container */
        .main {
            background-color: #222;
            color: #e0e0e0;
            font-family: Arial, sans-serif;
        }
        /* Sidebar style */
        .sidebar .sidebar-content {
            background-color: #333;
            color: #e0e0e0;
        }
        /* Style for tables and dataframes */
        .dataframe {
            background-color: #1e1e1e;
            color: #d3d3d3;
        }
        /* Style for text and headers */
        h1, h2, h3, h4, h5, h6 {
            color: #e0e0e0;
        }
    </style>
    """, unsafe_allow_html=True)

# Load datasets
df_reviews = pd.read_csv("dataset/customer reviews.csv")
df_top100_books = pd.read_csv("dataset/Top-100 Trending Books.csv")

# Slider settings for book price range
price_max = df_top100_books["book price"].max()
price_min = df_top100_books["book price"].min()

# Sidebar for filters
st.sidebar.title("Filters")
max_price = st.sidebar.slider("Maximum Price", float(price_min), float(price_max), float(price_max), format="$ %.2f")

# Filter the dataset based on price
df_books = df_top100_books[df_top100_books["book price"] <= max_price]

# Display the filtered dataframe
st.markdown("### Books within the selected price range")
st.dataframe(df_books.style.set_properties(**{'background-color': '#1e1e1e', 'color': '#d3d3d3'}))

# Bar chart: Count of books by publication year
fig_bar = go.Figure(data=[
    go.Bar(x=df_books["year of publication"].value_counts().sort_index().index,
           y=df_books["year of publication"].value_counts().sort_index(),
           marker_color="#4CAF50")
])
fig_bar.update_layout(title="Count of Books by Year of Publication",
                      paper_bgcolor="#222", plot_bgcolor="#222",
                      font_color="#e0e0e0", xaxis_title="Year of Publication", yaxis_title="Number of Books")

# Histogram: Distribution of book prices
fig_hist = px.histogram(df_books, x="book price", nbins=20, title="Distribution of Book Prices")
fig_hist.update_layout(paper_bgcolor="#222", plot_bgcolor="#222",
                       font_color="#e0e0e0", xaxis_title="Book Price", yaxis_title="Count")

# Column layout for charts
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.plotly_chart(fig_hist, use_container_width=True)

# Sidebar with highlighted metrics
st.sidebar.markdown("### Key Data")
st.sidebar.metric("Average Book Price", f"$ {df_books['book price'].mean():.2f}")
st.sidebar.metric("Total Number of Books", df_books.shape[0])

# Footer with dataset reference
st.markdown("""
    <hr style="border:1px solid #555;">
    <footer style="text-align: center; color: #888;">
        Built with Streamlit by MuriloKrominski | Dataset: <a href="https://www.kaggle.com/datasets/anshtanwar/top-200-trending-books-with-reviews" target="_blank" style="color: #4CAF50;">Kaggle - Top 200 Trending Books</a>
    </footer>
    """, unsafe_allow_html=True)