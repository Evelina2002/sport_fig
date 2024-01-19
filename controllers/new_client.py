from app import app
from flask import render_template

@app.route('/new_reader', methods=['GET'])
def new_reader():
    html = render_template(
        'new_reader.html',
    )
    return html
