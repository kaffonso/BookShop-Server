from json import JSONEncoder
from flask import Flask, abort, jsonify, make_response, request

class Book:
 def __init__(self, isbn, title, author, price): #inicializar 
  self.isbn = isbn
  self.title = title
  self.author = author
  self.price = price

  def __str__(self): #retornar string com infos de books
    return self.title + ' by ' + self.author + ' @ ' + str(self.price)


class Bookshop:
  def __init__(self, books): #inicianlizar
    self.books = books

  def get(self, isbn): #retornar livor por isbn
    if int(isbn) > len(self.books):
      abort(404)
    return list(filter(lambda b: b.isbn == isbn, self.books))[0]
  
  def add_book(self, book): #adicionar um livro a lista books
    self.books.append(book)

  def delete_book(self, isbn): #remover um livro po isbn
    self.books = list(filter(lambda b: b.isbn != isbn, self.books))
    

class BookJSONEncoder(JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Book):
      return {
        'isbn': obj.isbn,
        'title': obj.title,
        'author': obj.author,
        'price': obj.price
      }
    else:
      return super(BookJSONEncoder, self).default(obj)

bookshop = Bookshop([
  Book(1, 'XML', 'Gryff Smith', 10.99),
  Book(2, 'Java', 'Phoebe Cooke', 12.99),
  Book(3, 'Scala', 'Adam Davies', 11.99),
  Book(4, 'Python', 'Jasmine Byrne', 15.99)
  ])
  
def create_bookshop_service():
  app = Flask(__name__)
  app.json_encoder = BookJSONEncoder

  @app.route('/book/list', methods=['GET']) #rota para ler lista de livros
  def get_books():
    return jsonify({'books': bookshop.books})

  @app.route('/book/<int:isbn>', methods=['GET']) #rota para vre um livro
  def get_book(isbn):
    book = bookshop.get(isbn)
    return jsonify({'book': book})

  @app.route('/book/<int:isbn>', methods=['DELETE']) #rota para remover um livro
  def delete_book(isbn):
    bookshop.delete_book(isbn)
    return jsonify({'result': True})

  @app.route('/book', methods=['POST']) #rota para adicionar um livro
  def create_book():
    print('create book')
    if not request.json or not 'isbn' in request.json:
      abort(400)
    book = Book(
      request.json['isbn'],
      request.json['title'],
      request.json.get('author', ""),
      float(
        request.json['price'])
      )
    bookshop.add_book(book)
    return jsonify({'book': book}), 201

  @app.route('/book', methods=['PUT']) #rota para atualizar um livro
  def update_book():
    if not request.json or not 'isbn' in request.json:
      abort(400)
    isbn = request.json['isbn']
    book = bookshop.get(isbn)
    book.title = request.json['title']
    book.author = request.json['author']
    book.price = request.json['price']
    return jsonify({'book': book}), 201

  @app.errorhandler(400)
  def not_found(error):
    return make_response(jsonify({'book': 'Not found'}), 400)

  return app

if __name__ == '__main__':
  app = create_bookshop_service()
  app.run(debug=True)
