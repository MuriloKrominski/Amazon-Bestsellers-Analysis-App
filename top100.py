import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Configuração da página
st.set_page_config(page_title="Amazon's Top 100 Best-Selling Books", layout="wide")

# Título e Introdução
st.title("Amazon's Top 100 Best-Selling Books Analysis")
st.subheader("Explore Amazon's top 100 best-selling books and customer reviews.")
st.markdown("**Data Reference**: [Top 200 Trending Books Dataset on Kaggle](https://www.kaggle.com/datasets/anshtanwar/top-200-trending-books-with-reviews)")
st.markdown("**Project by [Murilo Krominski](https://murilokrominski.github.io/autor.htm)**")

# Carregamento dos datasets
df_reviews = pd.read_csv("dataset/customer reviews.csv")
df_top100_books = pd.read_csv("dataset/Top-100 Trending Books.csv")

# Parâmetros de filtro
price_min, price_max = df_top100_books["book price"].min(), df_top100_books["book price"].max()
selected_price = st.sidebar.slider("Price Range", price_min, price_max, price_max, format="$%f")

# Filtrar dataset pelo preço e exibir métricas gerais
df_books = df_top100_books[df_top100_books["book price"] <= selected_price]
total_books = len(df_books)
avg_price = df_books["book price"].mean()
avg_rating = df_books["rating"].mean()

# Display das métricas
st.sidebar.metric("Total Books", total_books)
st.sidebar.metric("Average Price", f"${avg_price:.2f}")
st.sidebar.metric("Average Rating", f"{avg_rating:.1f} / 5")

# Tabela dos dados filtrados
st.write("### Filtered Books Data")
st.dataframe(df_books)

# Visualizações
st.write("### Data Visualizations")

### 1. Average Price and Rating per Year ###
st.write("#### Average Price and Rating per Year")
avg_data_year = df_books.groupby("year of publication").agg({"book price": "mean", "rating": "mean"})
fig_avg_year = go.Figure()
fig_avg_year.add_trace(go.Bar(x=avg_data_year.index, y=avg_data_year["book price"], name="Average Price", marker_color="blue"))
fig_avg_year.add_trace(go.Scatter(x=avg_data_year.index, y=avg_data_year["rating"], name="Average Rating", mode="lines+markers", marker_color="red"))
fig_avg_year.update_layout(title="Average Price and Rating per Year", xaxis_title="Year", yaxis_title="Value")
st.plotly_chart(fig_avg_year, use_container_width=True)

### 2. Genre Distribution ###
st.write("#### Genre Distribution")
fig_genre = px.pie(df_books, names="genre", title="Genre Distribution")
st.plotly_chart(fig_genre, use_container_width=True)

### 3. Top Genres by Average Rating ###
st.write("#### Top Genres by Average Rating")
avg_rating_genre = df_books.groupby("genre")["rating"].mean().sort_values(ascending=False)
fig_avg_rating_genre = px.bar(avg_rating_genre, x=avg_rating_genre.index, y=avg_rating_genre.values,
                              labels={"x": "Genre", "y": "Average Rating"},
                              title="Top Genres by Average Rating")
st.plotly_chart(fig_avg_rating_genre, use_container_width=True)

### 4. Top Authors by Book Count ###
st.write("#### Top Authors by Book Count")
top_authors = df_books["author"].value_counts().head(10)
fig_authors = px.bar(top_authors, x=top_authors.index, y=top_authors.values, 
                     labels={"x": "Author", "y": "Number of Books"}, 
                     title="Top Authors by Book Count")
st.plotly_chart(fig_authors, use_container_width=True)

### 5. Word Cloud of Book Titles ###
st.write("#### Word Cloud of Book Titles")
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(df_books["book title"]))
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
st.pyplot(plt)

### 6. Price Distribution Histogram ###
st.write("#### Book Price Distribution")
fig_price = px.histogram(df_books, x="book price", title="Book Price Distribution")
st.plotly_chart(fig_price, use_container_width=True)

### 7. Price vs. Rating Scatter Plot ###
st.write("#### Price vs. Rating Scatter Plot")
fig_scatter = px.scatter(df_books, x="book price", y="rating", size="Rank", color="rating",
                         title="Price vs. Rating Scatter Plot")
st.plotly_chart(fig_scatter, use_container_width=True)

### 8. Rating Distribution ###
st.write("#### Rating Distribution")
fig_ratings = px.pie(df_books, names="rating", title="Distribution of Ratings")
st.plotly_chart(fig_ratings, use_container_width=True)

### 9. Top Genres by Average Price ###
st.write("#### Top Genres by Average Price")
avg_price_genre = df_books.groupby("genre")["book price"].mean().sort_values(ascending=False)
fig_avg_price_genre = px.bar(avg_price_genre, x=avg_price_genre.index, y=avg_price_genre.values,
                              labels={"x": "Genre", "y": "Average Price"},
                              title="Top Genres by Average Price")
st.plotly_chart(fig_avg_price_genre, use_container_width=True)

### 10. Correlation Matrix Heatmap ###
st.write("#### Correlation Matrix")
corr_matrix = df_books[["book price", "rating", "Rank"]].corr()
fig_corr = plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap="Blues", fmt=".2f", square=True)
st.pyplot(fig_corr)

# Mensagem de rodapé
st.markdown("Created with ❤️ and maintained by [Murilo Krominski](https://murilokrominski.github.io/autor.htm).")
