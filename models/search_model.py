import pandas

def get_author_count(conn):
    return pandas.read_sql(
        '''
            WITH cte (author_name, author_count) AS (
                SELECT
                    author_name,
                    COUNT(book_id)
                FROM
                    author 
                    JOIN book_author USING (author_id)
                    JOIN book USING (book_id)
                GROUP BY
                    author_name
            )
            SELECT * FROM cte
        ''',
        conn
    )

def get_genre_count(conn):
    return pandas.read_sql(
        '''
            WITH cte (genre_name, genre_count) AS (
                SELECT
                    genre_name,
                    COUNT(book_id)
                FROM
                    genre
                    JOIN book USING (genre_id)
                GROUP BY
                    genre_name
            )
            SELECT * FROM cte
        ''',
        conn
    )

def get_publisher_count(conn):
    return pandas.read_sql(
        '''
            WITH cte (publisher_name, publisher_count) AS (
                SELECT
                    publisher_name,
                    COUNT(book_id)
                FROM
                    publisher
                    JOIN book USING (publisher_id)
                GROUP BY
                    publisher_name
            )
            SELECT * FROM cte
        ''',
        conn
    )

def get_all_authors(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT author_name FROM author")
    authors = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return authors

def get_all_genres(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT genre_name FROM genre")
    genres = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return genres

def get_all_publishers(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT publisher_name FROM publisher")
    publishers = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return publishers


def get_filtered_books(conn, selected_authors, selected_genres, selected_publishers):
    return pandas.read_sql(
        '''
            WITH get_authors (book_id, authors) AS (
                SELECT
                    book_id,
                    GROUP_CONCAT(author_name, ", ")
                FROM
                    book
                    JOIN book_author USING (book_id)
                    JOIN author USING (author_id)
                WHERE
                    author_name IN {}
                GROUP BY
                    book_id
            ),
            get_books AS (
                SELECT
                    title,
                    authors,
                    genre_name,
                    publisher_name,
                    year_publication,
                    available_numbers,
                    book_id
                FROM
                    get_authors
                    JOIN book USING (book_id)
                    JOIN publisher USING (publisher_id)
                    JOIN genre USING (genre_id)
                WHERE
                    publisher_name IN {}
                    AND genre_name IN {}
            )
            SELECT
                *
            FROM get_books
        '''.format(
                '({})'.format(', '.join([f'"{elem}"' for elem in selected_authors])), 
                '({})'.format(', '.join([f'"{elem}"' for elem in selected_publishers])), 
                '({})'.format(', '.join([f'"{elem}"' for elem in selected_genres]))
            ),
        conn
    )