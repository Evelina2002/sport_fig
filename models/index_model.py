import pandas

def get_reader(conn):
    return pandas.read_sql(
    '''
        SELECT * FROM reader
    ''', 
    conn
    )

def get_book_reader(conn, reader_id):
    return pandas.read_sql('''
        WITH get_authors(book_id, authors_name)
        AS (
            SELECT book_id, GROUP_CONCAT(author_name)
            FROM author JOIN book_author USING(author_id)
            GROUP BY book_id
        )
        SELECT 
            authors_name AS Тренеры,
            publisher_name AS Тип_тренировки,
            title AS Время,
            genre_name AS Место_проведения,
            borrow_date AS Дата_записи, 
            return_date AS Отмена_занятий,
            book_reader_id
        FROM
        reader
        JOIN book_reader USING(reader_id)
        JOIN book USING(book_id)
        JOIN get_authors USING(book_id)
        JOIN publisher USING(publisher_id)
        JOIN genre USING(genre_id)
        WHERE reader.reader_id = :id
        ORDER BY 3
    ''', 
    conn, 
    params={"id": reader_id}
    )

def get_new_reader(conn, new_reader):
    cur = conn.cursor()
    cur.execute(
        '''
            INSERT INTO reader (reader_name)
            VALUES (:new_reader)
        ''',
        {"new_reader": new_reader}
    )
    conn.commit()
    return cur.lastrowid

def borrow_book(conn, book_id, reader_id):
    cur = conn.cursor()
    cur.executescript(
        f'''
            INSERT INTO book_reader (book_id, reader_id, borrow_date, return_date)
            VALUES ({book_id}, {reader_id}, DATE("NOW"), NULL);

            UPDATE book
            SET available_numbers = available_numbers - 1
            WHERE book_id = {book_id}
        ''',
    )
    conn.commit()

def set_return_date(conn, book_reader_id):
    cur = conn.cursor()
    cur.execute(
        f'''
            UPDATE book_reader
            SET return_date = DATE('NOW')
            WHERE book_reader_id = {book_reader_id}
        '''
    )
    cur.execute(
        f'''
            UPDATE book
            SET available_numbers = available_numbers + 1
            WHERE book_id = (SELECT book_id FROM book_reader WHERE book_reader_id = {book_reader_id})
        '''
    )
    conn.commit()