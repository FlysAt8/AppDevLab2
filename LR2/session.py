from sqlalchemy import create_engine, select
from sqlalchemy.orm import selectinload
from uuid import UUID, uuid4

connect_url = "postgresql+psycopg2://postgres:postgres@localhost/my_db"

engine = create_engine(
    connect_url,
    echo=True  # Логирование SQL-запросов
)

from sqlalchemy.orm import sessionmaker
from orm.db import User, Address, Order

session_factory = sessionmaker(engine)

def insert_user():
    for i in range(1, 6):
        with session_factory() as session:
            user = User(username=f'User{i}', email=f'user{i}@example.com', addresses=[
                Address(street=f'Street {i}',
                        city=f'City {i}',
                        state=f'State {i}',
                        zip_code=f'Zip code {i}',
                        country=f'Country {i}')
            ])
            session.add(user)
            session.commit()
                

#insert_user()

def update():
    for i in range(1, 6):
        with session_factory() as session:
            user = session.query(User).filter_by(username=f'User{i}').first()
            for address in user.addresses:
                id1 = address.id 
            user.orders = [Order(address_id=id1,
                                 product=f'Product {i}')]
            session.commit()

# update()

def delete_user(name):
    with session_factory() as session:
        user = session.query(User).filter_by(username=name).first()
        session.delete(user)
        session.commit()

def zapros1():
    with session_factory() as session:
        user = select(User).options(selectinload(User.addresses))
        for user in session.execute(user).scalars():
            print(f'\n Пользователь {user.username} живет в городе {[i.city for i in user.addresses]}',
                  f'на улице {[i.street for i in user.addresses]}')
        print()

def zapros2():
    with session_factory() as session:
        order = select(Order).options(selectinload(Order.user), selectinload(Order.address))
        for order in session.execute(order).scalars():
            un = order.user
            ar = order.address
            print(f'\n Пользователь {un.username} заказал {order.product}',
                  f'на адрес {ar.street}')
        print()

zapros2()