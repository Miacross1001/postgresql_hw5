import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, unique=True, nullable=False)

    def __str__(self):
        return f'{self.id}: {self.name}'

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String, unique=True, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref='books')

    def __str__(self):
        return f'{self.id} | {self.title} | {self.id_publisher}'

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True, nullable=False)

    def __str__(self):
        return f'{self.id}: {self.name}'

class Stock(Base):
    __tablename__ = "stock"
    __table_args__ = (
        sq.CheckConstraint('count>=0'),
    )

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, unique=False)

    book = relationship(Book, backref='books')
    shop = relationship(Shop, backref='shops')

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float)
    date_sale = sq.Column(sq.DateTime, default=datetime.now())
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer)

    stock = relationship(Stock, backref='sales')

    def __str__(self):
        return f'{self.id} | {self.price} | {self.date_sale} | {self.id_stock} | {self.count}'

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

DSN = "postgresql://postgres@localhost:5431/postgres"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

p1 = Publisher(name='Гоголь')
p2 = Publisher(name='Пушкин')
p3 = Publisher(name='Платон')
p4 = Publisher(name='Гюго')
p5 = Publisher(name='Роулинг')
p6 = Publisher(name='Гончаров')
session.add_all([p1, p2, p3, p4, p5, p6])

sh1 = Shop(name='Буквоед')
sh2 = Shop(name='Читай город')
sh3 = Shop(name='Лабиринт')
session.add_all([sh1, sh2, sh3])
session.commit()

b1 = Book(title='Ревизор', publisher=p1)
b2 = Book(title='Евгений Онегин', publisher=p2)
b3 = Book(title='Диалоги', publisher=p3)
b4 = Book(title='Отверженные', publisher=p4)
b5 = Book(title='Гарри Поттер', publisher=p5)
b6 = Book(title='Обломов', publisher=p6)
session.add_all([b1, b2, b3, b4, b5, b6])
session.commit()

st1 = Stock(count=5, book=b2, shop=sh3)
st2 = Stock(count=10, book=b1, shop=sh2)
st3 = Stock(count=1, book=b6, shop=sh1)
st4 = Stock(count=2, book=b5, shop=sh2)
st5 = Stock(count=15, book=b3, shop=sh1)
st6 = Stock(count=7, book=b4, shop=sh3)
session.add_all([st1, st2, st3, st4, st5, st6])
session.commit()

s1 = Sale(price=300, count=3, stock=st1)
s2 = Sale(price=180, count=8, stock=st2)
s3 = Sale(price=200, count=1, stock=st3)
s4 = Sale(price=150, count=3, stock=st5)
s5 = Sale(price=210, count=1, stock=st4)
s6 = Sale(price=120, count=5, stock=st6)
session.add_all([s1, s2, s3, s4, s5, s6])
session.commit()

acction = input()
q = session.query(Book.title, Shop.name, Sale).join(Publisher, Book.id_publisher==Publisher.id).join(Stock, Stock.id_book==Book.id).join(Sale, Sale.id_stock==Stock.id).join(Shop, Stock.id_shop==Shop.id).filter(sq.or_(Book.title==acction, Publisher.name==acction))
for title, name, sale in q.all():
    print(f'{title} | {name} | {sale.price} | {sale.date_sale}')


session.close()

