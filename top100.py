import streamlit as st
import pandas as pd
import plotly.express as px

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
avg_rating = df_books["rating"].mean()

# Display metrics
st.sidebar.metric("Total Books", total_books)
st.sidebar.metric("Average Price", f"${avg_price:.2f}")
st.sidebar.metric("Average Rating", f"{avg_rating:.1f} / 5")

# Display filtered data table
st.write("### Filtered Books Data")
st.dataframe(df_books)

# Visualization Section
st.write("### Data Visualizations")

# 1. Books by Price Range
st.write("#### Books by Price Range")
st.write("This bar chart shows the number of books available within different price ranges.")
bins = [0, 10, 20, 30, 40, 50, price_max]
labels = ["$0-10", "$10-20", "$20-30", "$30-40", "$40-50", f"${price_max}+"]

df_books["price range"] = pd.cut(df_books["book price"], bins=bins, labels=labels)
fig_price_range = px.bar(df_books["price range"].value_counts().sort_index(),
                         title="Books by Price Range", labels={"index": "Price Range", "value": "Count"})
st.plotly_chart(fig_price_range, use_container_width=True)

# 2. Top 10 Most Expensive Books
st.write("#### Top 10 Most Expensive Books")
st.write("This bar chart lists the 10 most expensive books in the dataset.")
top_expensive_books = df_books.nlargest(10, "book price")[["book title", "book price"]]
fig_top_expensive = px.bar(top_expensive_books, x="book title", y="book price", title="Top 10 Most Expensive Books",
                           labels={"book title": "Book Title", "book price": "Price"})
st.plotly_chart(fig_top_expensive, use_container_width=True)

# 3. Books by Genre and Year
st.write("#### Books by Genre and Year")
st.write("This heatmap shows the distribution of book genres across different years.")
df_genre_year = df_books.groupby(["year of publication", "genre"]).size().reset_index(name="count")
fig_genre_year = px.density_heatmap(df_genre_year, x="year of publication", y="genre", z="count",
                                    title="Books by Genre and Year", color_continuous_scale="Viridis",
                                    labels={"year of publication": "Year", "genre": "Genre", "count": "Count"})
st.plotly_chart(fig_genre_year, use_container_width=True)

# 4. Average Rating per Genre
st.write("#### Average Rating per Genre")
st.write("This bar chart compares the average rating across different book genres.")
avg_rating_genre = df_books.groupby("genre")["rating"].mean().sort_values()
fig_avg_rating_genre = px.bar(avg_rating_genre, x=avg_rating_genre.index, y=avg_rating_genre.values,
                              labels={"x": "Genre", "y": "Average Rating"},
                              title="Average Rating per Genre")
st.plotly_chart(fig_avg_rating_genre, use_container_width=True)

# Footer with credits
st.markdown("Created with ❤️ and maintained by [Murilo Krominski](https://murilokrominski.github.io/autor.htm).")
