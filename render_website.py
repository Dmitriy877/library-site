from jinja2 import Environment, FileSystemLoader, select_autoescape
import json

from livereload import Server
from more_itertools import chunked

def rebuild():

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open('.\media\meta_data.json', encoding='utf-8') as file:
        books_json = file.read()
    books = json.loads(books_json)
    chunked_books = list(chunked(books, 2))

    # print(chunked_books)
    
    # for book in chunked_books:
    #     for i in book:
    #         print(i)

    rendered_page = template.render(
        chunked_books=chunked_books
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


rebuild()

server = Server()

server.watch('template.html', rebuild)

server.serve(root='.')