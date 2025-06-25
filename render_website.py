from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import os

from livereload import Server
from more_itertools import chunked


def rebuild():

    os.makedirs('pages', exist_ok=True)

    with open(os.path.join('media', 'meta_data.json'), encoding='utf-8') as file:
        books_json = file.read()
    books = json.loads(books_json)

    book_pages = list(chunked(books, 20))

    for i, book_page in enumerate(book_pages):

        chunked_books = list(chunked(book_page, 2))

        env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html', 'xml'])
        )

        template = env.get_template('./pages/template.html')

        rendered_page = template.render(
            chunked_books=chunked_books
        )

        with open(os.path.join('pages', f'index{i}.html'), 'w', encoding="utf8") as file:
            file.write(rendered_page)


rebuild()

server = Server()

server.watch('template.html', rebuild)

server.serve(root='./pages')