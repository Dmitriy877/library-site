from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import os
import math

from livereload import Server
from more_itertools import chunked


def rebuild():

    with open(os.path.join('media', 'meta_data.json'), encoding='utf-8') as file:
        books_json = file.read()
    books = json.loads(books_json)

    book_pages = list(chunked(books, 20))

    for page, book_page in enumerate(book_pages):

        pages_amount = math.ceil(len(book_pages))
        chunked_books = list(chunked(book_page, 2))
        current_page_number = page + 1

        env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html', 'xml'])
        )

        template = env.get_template('template.html')

        rendered_page = template.render(
            chunked_books=chunked_books,
            pages_amount=pages_amount,
            current_page_number=current_page_number
        )

        if current_page_number == 1:
            with open('index.html', 'w', encoding="utf8") as file:
                file.write(rendered_page)
        else:
            with open(f'index{current_page_number}.html', 'w', encoding="utf8") as file:
                file.write(rendered_page)


def main():

    rebuild()

    server = Server()

    server.watch('template.html', rebuild)

    server.serve(root='.')


if __name__ == '__main__':
    main()
