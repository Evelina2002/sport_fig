from app import app
from flask import render_template, request
from utils import get_db_connection
from models.search_model import get_author_count, get_genre_count, get_publisher_count, get_filtered_books, get_all_authors, get_all_genres, get_all_publishers

@app.route('/search', methods=['GET', 'POST'])
def search():
    conn = get_db_connection()

    selected_authors = []
    selected_genres = []
    selected_publishers = []

    df_authors = get_author_count(conn)
    df_genres = get_genre_count(conn)
    df_publishers = get_publisher_count(conn)
    df_books = get_filtered_books(
            conn,
            get_all_authors(conn),
            get_all_genres(conn),
            get_all_publishers(conn)
        )
    
    if request.method == 'POST':
        if 'confirm' in request.form:
            selected_authors = request.form.getlist("authors")
            selected_genres = request.form.getlist("genres")
            selected_publishers = request.form.getlist("publishers")

        if 'reset' in request.form:
            selected_authors = []
            selected_genres = []
            selected_publishers = []
        
        df_books = get_filtered_books(
            conn,
            get_all_authors(conn) if not selected_authors else selected_authors,
            get_all_genres(conn) if not selected_genres else selected_genres,
            get_all_publishers(conn) if not selected_publishers else selected_publishers
        )

    html = render_template(
        'search.html',
        selected_authors=selected_authors,
        df_authors=df_authors,
        selected_genres=selected_genres,
        df_genres=df_genres,
        selected_publishers=selected_publishers,
        df_publishers=df_publishers,
        df_books=df_books
    )
    return html
