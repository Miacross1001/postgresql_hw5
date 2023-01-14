import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, unique=True)

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'))

    publisher = relationship("Publisher", backref="books")

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

class Stock(Base):
    __tablename__ = "stock"
    __table_args__ = (
        sq.CheckConstraint('count>=0'),
    )

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref='stocks')
    shop = relationship(Shop, backref='stocks')

class Sale(Base):
    __tablename__ = "sale"
    __table_args__ = (
        sq.CheckConstraint('count>=0'),
        sq.CheckConstraint('price>=0.0'),
    )

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float)
    date_sale = sq.Column(sq.DateTime, default=datetime.now)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'))
    count = sq.Column(sq.Integer)

    stock = relationship(Stock, backref='sales')

def create_table(engine):
    Base.metadata.create_all(engine)

DNS = "postgresql://postgres@localhost:5431/netology_db"
engine = sqlalchemy.create_engine(DNS)
create_table(engine)

Session = sessionmaker(bind=engine)
session = Session()

p1 = Publisher(name="Гоголь")
print(p1.id)
sh1 = Shop(name="Лабиринт")
print(sh1.id)
b1 = Book(title="Ревизор", publisher=p1)
print(b1.id)
st1 = Stock(count=100, book=b1, shop=sh1)
print(st1.id)
s1 = Sale(price=300, count=2, stock=st1)
print(s1.id)
session.add_all([p1, sh1, b1, st1, s1])
session.commit()

p2 = Publisher(name="Гюго")
sh2 = Shop(name="Читай город")
b2 = Book(title="Отверженные", publisher=p2)
st2 = Stock(count=200, book=b2, shop=sh2)
s2 = Sale(price=180, count=1, stock=st2)
session.add_all([p2, sh2, b2, st2, s2])
session.commit()
print(s2.id)

p3 = Publisher(name="Гончаров")
sh3 = Shop(name="Буквоед")
b3 = Book(title="Обломов", publisher=p3)
st3 = Stock(count=150, book=b3, shop=sh3)
s3 = Sale(price=230, count=5, stock=st3)
session.add_all([p3, sh3, b3, st3, s3])
session.commit()
print(s3.id)

p4 = Publisher(name="Джек Лондон")
sh4 = Shop(name="Лабиринт")
b4 = Book(title="Белый клык", publisher=p4)
st4 = Stock(count=300, book=b4, shop=sh4)
s4 = Sale(price=210, count=4, stock=st4)
session.add_all([p4, sh4, b4, st4, s4])
session.commit()
print(s4.id)

p5 = Publisher(name="Роулинг")
sh5 = Shop(name="Лабиринт")
b5 = Book(title="Гарри Поттер", publisher=p5)
st5 = Stock(count=50, book=b5, shop=sh5)
s5 = Sale(price=300, count=7, stock=st5)
session.add_all([p5, sh5, b5, st5, s5])
session.commit()
print(s5.id)

p6 = Publisher(name="Платон")
sh6 = Shop(name="Чиатй город")
b6 = Book(title="Диалоги", publisher=p6)
st6 = Stock(count=100, book=b6, shop=sh6)
s6 = Sale(price=280, count=10, stock=st6)
session.add_all([p6, sh6, b6, st6, s6])
session.commit()
print(s6.id)






