# Link to the dataset used as a reference
# https://www.kaggle.com/datasets/anshtanwar/top-200-trending-books-with-reviews
# Reference date: Nov 23

import streamlit as st  # Imports Streamlit for creating the web app
import pandas as pd  # Imports pandas for data manipulation
import plotly.express as px  # Imports Plotly Express for creating visualizations

# Sets the Streamlit page layout to "wide" (more horizontal space)
st.set_page_config(layout="wide")

# Loads the customer reviews dataset and the top 100 trending books dataset
df_reviews = pd.read_csv("dataset/customer reviews.csv")
df_top100_books = pd.read_csv("dataset/Top-100 Trending Books.csv")

# Gets the maximum and minimum book prices from the dataset
price_max = df_top100_books["book price"].max()
price_min = df_top100_books["book price"].min()

# Creates a slider in the sidebar to let the user select a price range
max_price = st.sidebar.slider("Price Range", price_min, 
                              price_max, price_max, format="$%f")

# Filters the dataframe to include only books within the selected price range
df_books = df_top100_books[df_top100_books["book price"] <= max_price]

# Displays the filtered dataframe in an interactive table within Streamlit
st.dataframe(df_books)

# Creates a bar chart to visualize the count of books by year of publication
fig = px.bar(df_books["year of publication"].value_counts().sort_index())

# Creates a histogram to show the distribution of book prices
fig2 = px.histogram(df_books["book price"])

# Splits the page into two columns and displays one chart in each column
col1, col2 = st.columns(2)
col1.plotly_chart(fig)  # Displays the bar chart in the first column
col2.plotly_chart(fig2)  # Displays the histogram in the second column