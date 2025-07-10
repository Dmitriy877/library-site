import argparse
import json
import math
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def rebuild(books):
    env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html', 'xml'])
        )
    template = env.get_template('template.html')

    os.makedirs('pages', exist_ok=True)

    books_on_page_amount = 20
    book_pages_amount = list(chunked(books, books_on_page_amount))
    books_columns_amount = 2

    for page, book_page in enumerate(book_pages_amount, start=1):

        pages_amount = math.ceil(len(book_pages_amount))
        chunked_books_columns = list(chunked(book_page, books_columns_amount))

        rendered_page = template.render(
            chunked_books=chunked_books_columns,
            pages_amount=pages_amount,
            current_page_number=page,
        )

        with open(Path('.')/'pages'/f'index{page}.html', 'w', encoding='utf8') as file:
            file.write(rendered_page)


def main():
    parser = argparse.ArgumentParser(
        description='Скрипт для запуска библиотеки'
    )
    parser.add_argument(
        '-p',
        '--path',
        help='Путь до библиотеки json',
        default=Path('.')/'media'/'meta_data.json'
    )
    args = parser.parse_args()

    with open(args.path, 'r', encoding='utf-8') as file:
        books = json.load(file)

    rebuild(books)

    server = Server()

    server.watch('template.html', rebuild)

    server.serve(root='.')


if __name__ == '__main__':
    main()
