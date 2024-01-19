from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.index_model import get_reader, get_book_reader, get_new_reader, borrow_book, set_return_date

@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()

    if request.values.get('reader'):
        reader_id = int(request.values.get('reader'))
        session['reader_id'] = reader_id
    elif request.values.get('new_reader'):
        new_reader = request.values.get('new_reader')
        session['reader_id'] = get_new_reader(conn, new_reader)
        print("get_new_reader(conn, new_reader) = ", get_new_reader(conn, new_reader))
    elif request.values.get('book'):
        book_id = int(request.values.get('book'))
        borrow_book(conn, book_id, session['reader_id'])
    elif request.values.get('return_val'):
        book_reader_id = request.values.get("return_val")
        set_return_date(conn, book_reader_id)
    else:
        if "reader_id" in session.keys():
            session['reader_id'] = session['reader_id']
        else:
            session['reader_id'] = 1
    df_reader = get_reader(conn)
    df_book_reader = get_book_reader(conn, session['reader_id'])

    html = render_template(
        'index.html',
        reader_id=session['reader_id'],
        combo_box=df_reader,
        book_reader=df_book_reader,
        len=len,
    )
    return html
