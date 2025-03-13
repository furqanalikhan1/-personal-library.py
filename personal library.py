import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Initialize session state for books if it doesn't exist
if 'books' not in st.session_state:
    st.session_state.books = []

def save_books():
    """Save books to a JSON file"""
    with open('books.json', 'w') as f:
        json.dump(st.session_state.books, f)

def load_books():
    """Load books from JSON file"""
    if os.path.exists('books.json'):
        with open('books.json', 'r') as f:
            st.session_state.books = json.load(f)

# Page config
st.set_page_config(page_title="Personal Library", page_icon="📚")

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("📚 Personal Library Management")

# Load existing books
load_books()

# Sidebar for adding new books
with st.sidebar:
    st.header("Add New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "Technology", 
                                  "History", "Biography", "Self-Help", "Other"])
    status = st.selectbox("Reading Status", ["To Read", "Currently Reading", "Completed"])
    rating = st.slider("Rating", 1, 5, 3)
    notes = st.text_area("Notes")
    
    if st.button("Add Book"):
        if title and author:
            new_book = {
                "title": title,
                "author": author,
                "genre": genre,
                "status": status,
                "rating": rating,
                "notes": notes,
                "date_added": datetime.now().strftime("%Y-%m-%d")
            }
            st.session_state.books.append(new_book)
            save_books()
            st.success("Book added successfully!")
        else:
            st.error("Title and Author are required!")

# Main content
tab1, tab2, tab3 = st.tabs(["All Books", "Statistics", "Search"])

with tab1:
    if st.session_state.books:
        for i, book in enumerate(st.session_state.books):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.subheader(book["title"])
                st.write(f"By: {book['author']}")
                st.write(f"Genre: {book['genre']}")
                st.write(f"Status: {book['status']}")
                st.write(f"Rating: {'⭐' * book['rating']}")
                if book["notes"]:
                    with st.expander("Notes"):
                        st.write(book["notes"])
            with col2:
                if st.button("Edit", key=f"edit_{i}"):
                    st.session_state.editing = i
            with col3:
                if st.button("Delete", key=f"delete_{i}"):
                    st.session_state.books.pop(i)
                    save_books()
                    st.rerun()
    else:
        st.info("No books in your library yet. Add some books using the sidebar!")

with tab2:
    if st.session_state.books:
        df = pd.DataFrame(st.session_state.books)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Books by Genre")
            genre_counts = df['genre'].value_counts()
            st.bar_chart(genre_counts)
        
        with col2:
            st.subheader("Reading Status")
            status_counts = df['status'].value_counts()
            st.pie_chart(status_counts)
        
        st.subheader("Average Rating by Genre")
        avg_ratings = df.groupby('genre')['rating'].mean()
        st.bar_chart(avg_ratings)
    else:
        st.info("Add some books to see statistics!")

with tab3:
    search_term = st.text_input("Search books by title or author")
    if search_term:
        results = [book for book in st.session_state.books 
                  if search_term.lower() in book['title'].lower() 
                  or search_term.lower() in book['author'].lower()]
        if results:
            for book in results:
                st.subheader(book["title"])
                st.write(f"By: {book['author']}")
                st.write(f"Genre: {book['genre']}")
                st.write(f"Status: {book['status']}")
                st.write(f"Rating: {'⭐' * book['rating']}")
        else:
            st.warning("No matching books found!")