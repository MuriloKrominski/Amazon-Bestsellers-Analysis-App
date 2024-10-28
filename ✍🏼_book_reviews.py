import streamlit as st  # Imports Streamlit to create the web app
import pandas as pd  # Imports pandas for data manipulation

# Sets the Streamlit page layout to "wide" (more horizontal space)
st.set_page_config(layout="wide")

# Loads the customer reviews dataset and the top 100 trending books dataset
df_reviews = pd.read_csv("dataset/customer reviews.csv")
df_top100_books = pd.read_csv("dataset/Top-100 Trending Books.csv")

# Gets the list of unique book titles, sorted in reverse order for display
books = df_top100_books["book title"].unique()[::-1]

# Creates a dropdown (selectbox) in the sidebar for users to choose a book title
book = st.sidebar.selectbox("Books", books)

# Filters the main books dataframe to only include the selected book
df_book = df_top100_books[df_top100_books["book title"] == book]

# Filters the reviews dataframe to only include reviews for the selected book
df_reviews_f = df_reviews[df_reviews["book name"] == book]

# Extracts details of the selected book: title, genre, price, rating, and year of publication
book_title = df_book["book title"].iloc[0]
book_genre = df_book["genre"].iloc[0]
book_price = f"$ {df_book['book price'].iloc[0]}"
book_rating = df_book['rating'].iloc[0]
book_year = df_book['year of publication'].iloc[0]

# Displays the book's title as the main heading and the genre as a subheading
st.title(book_title)
st.subheader(book_genre)

# Creates three columns to display key metrics: Price, Rating, and Year of Publication
col1, col2, col3 = st.columns([1, 1, 3])
col1.metric("Price", book_price)  # Shows the book price in the first column
col2.metric("Rating", book_rating)  # Shows the book rating in the second column
col3.metric("Year of Publication", book_year)  # Shows the publication year in the third column

# Adds a divider to visually separate sections on the page
st.divider()

# Iterates over each review for the selected book and displays them as chat messages
for row in df_reviews_f.values:
    # Each review is displayed with the reviewer's name and the review title
    message = st.chat_message(f"{row[4]}")
    message.markdown(f"#### {row[2]}")  # Displays the review title in markdown
    message.write(row[5])  # Displays the review text