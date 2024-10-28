import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit page configuration
st.set_page_config(page_title="Top 100 Best-Selling Books on Amazon", layout="wide")

# Title and Introduction
st.title("Amazon's Top 100 Best-Selling Books")
st.subheader("Explore data on Amazon's top 100 best-selling books and customer reviews.")
st.markdown("**Data Reference**: [Top 200 Trending Books Dataset on Kaggle](https://www.kaggle.com/datasets/anshtanwar/top-200-trending-books-with-reviews)")
st.markdown("**Project by [Murilo Krominski](https://murilokrominski.github.io/autor.htm)**")

# Load datasets
df_reviews = pd.read_csv("dataset/customer reviews.csv")
df_top100_books = pd.read_csv("dataset/Top-100 Trending Books.csv")

# Filter parameters
price_min, price_max = df_top100_books["book price"].min(), df_top100_books["book price"].max()
selected_price = st.sidebar.slider("Price Range", price_min, price_max, price_max, format="$%f")

# Filter dataset by price and display general metrics
df_books = df_top100_books[df_top100_books["book price"] <= selected_price]
total_books = len(df_books)
avg_price = df_books["book price"].mean()
avg_rating = df_books["average rating"].mean()

# Display metrics
st.sidebar.metric("Total Books", total_books)
st.sidebar.metric("Average Price", f"${avg_price:.2f}")
st.sidebar.metric("Average Rating", f"{avg_rating:.1f} / 5")

# Display filtered data table
st.write("### Filtered Books Data")
st.dataframe(df_books)

# Graphs: book count by year and price distribution
fig_year = px.bar(df_books, x="year of publication", title="Books Count by Year of Publication")
fig_price = px.histogram(df_books, x="book price", title="Book Price Distribution")

# Ratings distribution pie chart
fig_ratings = px.pie(df_books, names="average rating", title="Distribution of Ratings")

# Price vs Rating scatter plot
fig_scatter = px.scatter(df_books, x="book price", y="average rating", 
                         size="number of reviews", color="average rating",
                         title="Price vs. Rating Scatter Plot")

# Display charts in columns
st.write("### Data Visualizations")
col1, col2 = st.columns(2)
col1.plotly_chart(fig_year, use_container_width=True)
col2.plotly_chart(fig_price, use_container_width=True)

col3, col4 = st.columns(2)
col3.plotly_chart(fig_ratings, use_container_width=True)
col4.plotly_chart(fig_scatter, use_container_width=True)

# Footer with credits
st.markdown("Created with ❤️ and maintained by [Murilo Krominski](https://murilokrominski.github.io/autor.htm).")
