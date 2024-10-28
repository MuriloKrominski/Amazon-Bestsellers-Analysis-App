import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

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

# Updated Visualization 1: Average Price and Rating per Year
st.write("#### Average Price and Rating per Year")
st.write("This combined line and bar chart shows the trend in average price and rating over the years of publication.")
avg_data_year = df_books.groupby("year of publication").agg({"book price": "mean", "rating": "mean"})
fig_avg_year = go.Figure()
fig_avg_year.add_trace(go.Bar(x=avg_data_year.index, y=avg_data_year["book price"],
                              name="Average Price", marker_color="blue"))
fig_avg_year.add_trace(go.Scatter(x=avg_data_year.index, y=avg_data_year["rating"], 
                                  name="Average Rating", mode="lines+markers", marker_color="red"))
fig_avg_year.update_layout(title="Average Price and Rating per Year", 
                           xaxis_title="Year", yaxis_title="Value")
st.plotly_chart(fig_avg_year, use_container_width=True)

# 2. Book Price Distribution
st.write("#### Book Price Distribution")
st.write("This histogram displays the distribution of book prices within the selected range.")
fig_price = px.histogram(df_books, x="book price", title="Book Price Distribution")
st.plotly_chart(fig_price, use_container_width=True)

# 3. Distribution of Ratings
st.write("#### Distribution of Ratings")
st.write("This pie chart shows the proportion of books within each rating level.")
fig_ratings = px.pie(df_books, names="rating", title="Distribution of Ratings")
st.plotly_chart(fig_ratings, use_container_width=True)

# 4. Price vs Rating Scatter Plot
st.write("#### Price vs. Rating")
st.write("This scatter plot shows the relationship between book price and average rating, with bubble sizes representing book rank.")
fig_scatter = px.scatter(df_books, x="book price", y="rating", 
                         size="Rank", color="rating",
                         title="Price vs. Rating Scatter Plot")
st.plotly_chart(fig_scatter, use_container_width=True)

# 5. Top Authors by Book Count
st.write("#### Top Authors by Book Count")
st.write("This bar chart highlights the authors with the most books in the top 100 list.")
top_authors = df_books["author"].value_counts().head(10)
fig_authors = px.bar(top_authors, x=top_authors.index, y=top_authors.values, 
                     labels={"x": "Author", "y": "Number of Books"}, 
                     title="Top Authors by Book Count")
st.plotly_chart(fig_authors, use_container_width=True)

# 6. Genre Distribution
st.write("#### Genre Distribution")
st.write("This pie chart displays the distribution of different genres in the top 100 books.")
fig_genre = px.pie(df_books, names="genre", title="Genre Distribution")
st.plotly_chart(fig_genre, use_container_width=True)

# 7. Top Genres by Average Rating
st.write("#### Top Genres by Average Rating")
st.write("This bar chart shows the average rating across different genres.")
avg_rating_genre = df_books.groupby("genre")["rating"].mean().sort_values(ascending=False)
fig_avg_rating_genre = px.bar(avg_rating_genre, x=avg_rating_genre.index, y=avg_rating_genre.values,
                              labels={"x": "Genre", "y": "Average Rating"},
                              title="Top Genres by Average Rating")
st.plotly_chart(fig_avg_rating_genre, use_container_width=True)

# 8. Correlation Matrix Heatmap
st.write("#### Correlation Matrix")
st.write("This heatmap displays the correlation between numerical variables, showing relationships between price, rating, and rank.")
corr_matrix = df_books[["book price", "rating", "Rank"]].corr()
fig_corr = plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap="Blues", fmt=".2f", square=True)
st.pyplot(fig_corr)

# Footer with credits
st.markdown("Created with ❤️ and maintained by [Murilo Krominski](https://murilokrominski.github.io/autor.htm).")
