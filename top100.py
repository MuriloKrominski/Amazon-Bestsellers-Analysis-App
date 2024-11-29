# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Set initial Streamlit configuration
st.set_page_config(layout="wide")

# Load the dataset of the 100 most popular books
df_top100_books = pd.read_csv("dataset/Top-100 Trending Books.csv")

# Get the maximum and minimum publication years for slider control
year_max = df_top100_books["year of publication"].max()
year_min = df_top100_books["year of publication"].min()

# Sidebar slider for selecting the publication year range
selected_year_range = st.sidebar.slider(
    "Year of Publication Range",
    int(year_min),
    int(year_max),
    (int(year_min), int(year_max))
)

# Filter dataset based on the selected publication year range
df_books = df_top100_books[
    (df_top100_books["year of publication"] >= selected_year_range[0]) &
    (df_top100_books["year of publication"] <= selected_year_range[1])
]

# Key metrics calculations
total_books = len(df_books)
average_price = df_books["book price"].mean()
average_rating = df_books["rating"].mean()

# Display main metrics
st.header("📚📊Amazon Bestsellers Analysis Web App [1947 - 2023]")
st.markdown("By [Murilo Krominski](https://murilokrominski.github.io/autor.htm).")
st.write(f"**Total Books**: {total_books}")
st.write(f"**Average Price**: ${average_price:.2f}")
st.write(f"**Average Rating**: {average_rating:.2f}")

# Display filtered dataframe
st.dataframe(df_books)

# Function to generate a word cloud of book titles
def plot_wordcloud():
    # Join all titles into a single string
    all_titles = " ".join(title for title in df_books["book title"].astype(str) if title)
    
    # Check if there is content to generate the word cloud
    if all_titles.strip():  # Ensures all_titles is not empty or whitespace
        # Generate the word cloud
        wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="viridis").generate(all_titles)
        
        # Display the word cloud with matplotlib and Streamlit
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.write("No titles available to generate a word cloud.")

# Function to plot price vs. ranking position scatter plot
def plot_price_vs_ranking():
    fig = px.scatter(df_books, x="Rank", y="book price", title="Price vs. Ranking Position",
                     labels={"Rank": "Ranking Position", "book price": "Price ($)"})
    st.plotly_chart(fig)

# Function to plot genre popularity and pricing heatmap
def plot_genre_popularity_pricing():
    fig = px.density_heatmap(df_books, x="genre", y="rating", z="book price", histfunc="avg",
                             title="Average Price and Popularity by Genre",
                             labels={"genre": "Genre", "rating": "Popularity", "book price": "Average Price ($)"})
    st.plotly_chart(fig)

# Function to plot author ratings and book volume scatter plot
def plot_author_rating_volume():
    df_filtered = df_books.dropna(subset=["author", "rating"])
    fig = px.scatter(df_filtered, x="author", y="rating", size="rating",
                     title="Average Rating and Book Volume by Author",
                     labels={"author": "Author", "rating": "Average Rating"})
    st.plotly_chart(fig)

# Function to perform clustering by genre and rating for segmentation
def plot_genre_rating_clusters():
    # Filter out rows with NaN values in required columns
    df_filtered = df_books.dropna(subset=["genre", "rating", "book price"])
    
    # Check if there are enough samples for clustering
    if len(df_filtered) >= 4:  # Ensure at least 4 samples for 4 clusters
        # Prepare data for clustering
        genre_data = df_filtered[["genre", "rating", "book price"]]
        scaler = StandardScaler()
        genre_data_scaled = scaler.fit_transform(genre_data[["rating", "book price"]])

        # Apply KMeans clustering
        kmeans = KMeans(n_clusters=4, random_state=0).fit(genre_data_scaled)
        df_filtered["Cluster"] = kmeans.labels_

        # Create a scatter plot to display clusters
        fig = px.scatter(df_filtered, x="rating", y="book price", color="Cluster", hover_data=["genre"],
                         title="Clustering Genres and Ratings for Audience Segmentation",
                         labels={"rating": "Rating", "book price": "Price ($)"})
        st.plotly_chart(fig)
    else:
        # Display a message if clustering cannot be performed
        st.write("Not enough data points to perform clustering. Please adjust the filter criteria.")


# Additional visualization functions for different data insights
def plot_publication_year_price_ranking():
    fig = px.scatter(df_books, x="year of publication", y="book price", size="Rank",
                     title="Publication Year vs. Price and Ranking Position",
                     labels={"year of publication": "Year of Publication", "book price": "Price ($)"})
    st.plotly_chart(fig)

# Function to plot average popularity (rating) by genre
def plot_genre_popularity():
    # Calculate the average rating for each genre
    avg_popularity_genre = df_books.groupby("genre")["rating"].mean().sort_values(ascending=False)
    
    # Create a bar plot to show average popularity by genre
    fig = px.bar(avg_popularity_genre, x=avg_popularity_genre.index, y=avg_popularity_genre.values,
                 labels={"x": "Genre", "y": "Average Popularity (Rating)"},
                 title="Average Popularity by Genre")
    st.plotly_chart(fig)

# Display various plots in Streamlit
plot_wordcloud()
plot_price_vs_ranking()
plot_genre_popularity_pricing()
plot_author_rating_volume()
plot_genre_rating_clusters()
plot_publication_year_price_ranking()
plot_genre_popularity()

### Average Price and Rating per Year ###
st.write("#### Average Price and Rating per Year")
avg_data_year = df_books.groupby("year of publication").agg({"book price": "mean", "rating": "mean"})
fig_avg_year = go.Figure()
fig_avg_year.add_trace(go.Bar(x=avg_data_year.index, y=avg_data_year["book price"], name="Average Price", marker_color="blue"))
fig_avg_year.add_trace(go.Scatter(x=avg_data_year.index, y=avg_data_year["rating"], name="Average Rating", mode="lines+markers", marker_color="red"))
fig_avg_year.update_layout(title="Average Price and Rating per Year", xaxis_title="Year", yaxis_title="Value")
st.plotly_chart(fig_avg_year, use_container_width=True)

### Genre Distribution ###
st.write("#### Genre Distribution")
fig_genre = px.pie(df_books, names="genre", title="Genre Distribution")
st.plotly_chart(fig_genre, use_container_width=True)

### Top Authors by Book Count ###
st.write("#### Top Authors by Book Count")
top_authors = df_books["author"].value_counts().head(10)
fig_authors = px.bar(top_authors, x=top_authors.index, y=top_authors.values,
                     labels={"x": "Author", "y": "Number of Books"},
                     title="Top Authors by Book Count")
st.plotly_chart(fig_authors, use_container_width=True)

### Average Rating by Genre ###
st.write("#### Average Rating by Genre")
avg_rating_genre = df_books.groupby("genre")["rating"].mean().sort_values(ascending=False)
fig_avg_rating_genre = px.bar(avg_rating_genre, x=avg_rating_genre.index, y=avg_rating_genre.values,
                              labels={"x": "Genre", "y": "Average Rating"},
                              title="Average Rating by Genre")
st.plotly_chart(fig_avg_rating_genre, use_container_width=True)

### Top 10 Highest Rated Books ###
st.write("#### Top 10 Highest Rated Books")
top_rated_books = df_books.nlargest(10, "rating")
fig_top_rated = px.bar(top_rated_books, x="book title", y="rating",
                       labels={"book title": "Book Title", "rating": "Rating"},
                       title="Top 10 Highest Rated Books")
st.plotly_chart(fig_top_rated, use_container_width=True)

### Book Price Distribution Histogram ###
st.write("#### Book Price Distribution")
fig_price = px.histogram(df_books, x="book price", title="Book Price Distribution")
st.plotly_chart(fig_price, use_container_width=True)

### Ratings Distribution ###
st.write("#### Ratings Distribution")
fig_ratings = px.histogram(df_books, x="rating", title="Ratings Distribution")
st.plotly_chart(fig_ratings, use_container_width=True)

### Yearly Publication Trends ###
st.write("#### Yearly Publication Trends")
pub_trends = df_books["year of publication"].value_counts().sort_index()
fig_pub_trends = px.line(x=pub_trends.index, y=pub_trends.values,
                         labels={"x": "Year", "y": "Number of Books"},
                         title="Yearly Publication Trends")
st.plotly_chart(fig_pub_trends, use_container_width=True)

### Footer ###
st.markdown("---")
st.markdown("Created with ❤️ and maintained by [Murilo Krominski](https://murilokrominski.github.io/autor.htm).")