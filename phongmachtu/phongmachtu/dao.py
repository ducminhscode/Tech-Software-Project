import json
import hashlib
from models import *
from phongmachtu import db

def add_account(name, username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = Patient(name=name, username=username, password=password)
    db.session.add(u)
    db.session.commit()


def auth_account(username, password):

    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    return Account.query.filter(Account.username.__eq__(username),
                             Account.password.__eq__(password)).first()


def get_all_period():
    # Truy vấn tất cả các giá trị period và id từ bảng Time
    periods = Time.query.with_entities(Time.id, Time.period).all()

    # Trả về danh sách các tuple chứa (id, period)
    return periods


def get_account_by_id(user_id):
    return Account.query.get(user_id)


# def load_book_by_id(book_id):
#     with open('data/books.json', encoding='utf-8') as f:
#         books = json.load(f)
#         for p in books:
#             if p["id"] == id:
#                 return p
#
#

# def load_products(q=None, cate_id=None, page=None):
#     # with open('data/products.json', encoding='utf-8') as f:
#     #     products = json.load(f)
#     #     if q:
#     #         products = [p for p in products if p["name"].find(q)>=0]
#     #     if cate_id:
#     #         products = [p for p in products if p["category_id"].__eq__(int(cate_id))]
#     #     return products
#
#     query = Product.query
#
#     if q:
#         query = query.filter(Product.name.contains(q))
#     if cate_id:
#         query = query.filter(Product.category_id.__eq__(cate_id))
#
#     if page:
#         page_size = app.config['PAGE_SIZE']
#         start = (int(page)-1)*page_size
#         query = query.slice(start, start+page_size)
#
#     return query.all()