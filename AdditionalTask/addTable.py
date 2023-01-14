import json
import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, nullable=False, unique=True)

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String, unique=True, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="books")

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, unique=True, nullable=False)

class Stock(Base):
    __tablename__ = "stock"
    __table_args__ = (
        sq.CheckConstraint("count>=0"),
    )

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref="stocks")
    shop = relationship(Shop, backref="stocks")

class Sale(Base):
    __tablename__ = "sale"
    __table_args__ = (
        sq.CheckConstraint("count>=0"),
    )

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DateTime, default=datetime.datetime.now())
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref="sales")

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

DSN = "postgresql://postgres@localhost:5431/postgres"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open("tests_data.json", 'r') as f:
    data = json.load(f)

table_obj = {
    'publisher': Publisher,
    'shop': Shop,
    'book': Book,
    'stock': Stock,
    'sale': Sale,
}

for t in data:
    table = table_obj[t.get('model')]
    session.add(table(id=t.get('pk'), **t.get('fields')))

session.commit()
q = session.query(Publisher)
for a in q.all():
    print(a.name)
session.close()