import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import sqlite3

# Configurações do Selenium
def configure_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa o navegador em segundo plano
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Evita detecção

    # Adicione o caminho do seu ChromeDriver aqui
    driver = webdriver.Chrome(executable_path='path/to/chromedriver', options=chrome_options)
    return driver

# Função para buscar os dados dos livros
def fetch_books():
    url = 'https://www.amazon.com.br/gp/bestsellers/books/'
    driver = configure_driver()
    driver.get(url)

    time.sleep(3)  # Aguarde o carregamento da página
    books = []

    # Tenta coletar dados dos livros
    try:
        items = driver.find_elements(By.CLASS_NAME, 'zg-item-immersion')
        for item in items:
            try:
                rank = item.find_element(By.CLASS_NAME, 'zg-badge-text').text
                title = item.find_element(By.CLASS_NAME, 'p13n-sc-truncate').text
                author = item.find_element(By.CLASS_NAME, 'a-link-child').text
            except:
                author = 'Autor desconhecido'
            
            books.append({
                "rank": rank,
                "title": title,
                "author": author
            })

    except Exception as e:
        st.write("Erro ao acessar a Amazon:", e)
    
    driver.quit()  # Fecha o navegador
    return books if books else None

# Funções do banco de dados e interface Streamlit permanecem as mesmas
def init_db():
    conn = sqlite3.connect('bestsellers.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (rank TEXT, title TEXT, author TEXT)''')
    conn.commit()
    conn.close()

def save_books_to_db(books):
    conn = sqlite3.connect('bestsellers.db')
    c = conn.cursor()
    c.execute('DELETE FROM books')  # Limpa a tabela antes de inserir novos dados
    for book in books:
        c.execute("INSERT INTO books VALUES (?, ?, ?)", (book['rank'], book['title'], book['author']))
    conn.commit()
    conn.close()

def fetch_books_from_db():
    conn = sqlite3.connect('bestsellers.db')
    c = conn.cursor()
    c.execute("SELECT rank, title, author FROM books")
    books = [{"rank": row[0], "title": row[1], "author": row[2]} for row in c.fetchall()]
    conn.close()
    return books

def display_books(books):
    for book in books:
        st.write(f"**Posição:** {book['rank']}")
        st.write(f"**Título:** {book['title']}")
        st.write(f"**Autor:** {book['author']}")
        st.write("---")

# Inicializa o banco de dados e a tabela
init_db()

# Configuração da página do Streamlit
st.title("Top 100 Livros Mais Vendidos na Amazon Brasil")
st.write("Atualizado em tempo real")

# Botão para atualizar a lista de livros
if st.button("Atualizar Lista"):
    with st.spinner('Atualizando...'):
        books = fetch_books()
        if books:
            st.success("Lista atualizada com sucesso!")
            save_books_to_db(books)
        else:
            st.warning("Não foi possível obter a lista atualizada. Carregando dados do banco de dados.")
            books = fetch_books_from_db()
        display_books(books)
