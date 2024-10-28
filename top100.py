
import streamlit as st  # Importing the Streamlit library for creating web applications
import pandas as pd     # Importing pandas for data manipulation and analysis
import plotly.express as px  # Importing Plotly Express for data visualization
import plotly.graph_objects as go  # Importing Plotly Graph Objects for more customizable plots

# Page configuration for a minimal style and title "Trending Books"
st.set_page_config(page_title="Trending Books", page_icon="📚", layout="wide")

# Applying a custom dark theme configuration for Streamlit app
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
        }
        /* Header title styling */
        .css-18e3th9 {
            color: #FFF;
            font-size: 2rem;
        }
    </style>
"", unsafe_allow_html=True)

# Title for the Streamlit app displayed at the top of the page
st.title("Top 100 Trending Books")

# Uploading a CSV file containing data about books
uploaded_file = st.file_uploader("Choose a file", type="csv")

# Checking if the file is uploaded
if uploaded_file is not None:
    # Reading the uploaded CSV file into a pandas DataFrame
    df = pd.read_csv(uploaded_file)

    # Displaying the first 10 rows of the DataFrame in the app
    st.write("Preview of the data:")
    st.write(df.head(10))

    # Checking if the DataFrame has necessary columns for analysis
    if 'Rating' in df.columns and 'Price' in df.columns:
        # Creating a scatter plot with Plotly Express
        fig = px.scatter(df, x="Rating", y="Price", color="Genre", title="Rating vs Price by Genre")
        # Displaying the scatter plot in the app
        st.plotly_chart(fig)

    # If required columns are missing, display an error message
    else:
        st.error("The file must contain 'Rating' and 'Price' columns.")

# HTML for author information and social links
st.markdown("""
    <center>
    <a href="https://murilokrominski.github.io/autor.htm">
    <img src="https://murilokrominski.github.io/media/avatar.jpeg" alt="autor" style="max-width: 160px; max-height: 160px; width: auto; height: auto;">
    </a>
    <br>
    By <a href="https://murilokrominski.github.io/autor.htm">Murilo Krominski</a>
    <br>
    <a href="https://murilokrominski.github.io/autor.htm">
    <img src="https://img.shields.io/badge/https://murilokrominski.github.io/autor.htm-blue.svg" alt="Autor">
    </a>
    <a href="https://murilokrominski.github.io/">
    <img src="https://img.shields.io/badge/Projects - Repository β(PUBLIC)-orange.svg" alt="Repository β(PUBLIC)">
    </a>
    <br>
    <a href="https://t.me/murilokrominski">
    <img src="https://img.shields.io/badge/Telegram-1D9BF0?style=for-the-badge&logo=telegram&logoColor=E5F3FF" height="20">
    </a>
    <a href="https://wa.me/+5511970388634">
    <img src="https://img.shields.io/badge/WhatsApp-22BB78?style=for-the-badge&logo=whatsapp&logoColor=E8F6EE" height="20">
    </a>
    <a href="https://www.threads.net/@murilokrominski">
    <img src="https://img.shields.io/badge/Threads-565656?style=for-the-badge&logo=threads&logoColor=D8D8D8" height="20">
    </a>
    <a href="https://www.instagram.com/murilokrominski">
    <img src="https://img.shields.io/badge/Instagram-D74476?style=for-the-badge&logo=instagram&logoColor=FCE3EC" height="20">
    </a>
    <a href="mailto:murilokr@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-DC4E41?style=for-the-badge&logo=gmail&logoColor=FDEAE8" height="20">
    </a>
    <br>
    <p><strong>Hello World!</strong><img src="media/Hi.gif?raw=true" width="30px"></p>
    </center>
"", unsafe_allow_html=True)
