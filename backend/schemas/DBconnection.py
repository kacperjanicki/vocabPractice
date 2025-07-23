from sqlalchemy import text,Table,Column,Integer,String,MetaData,create_engine,insert,select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
import os

DATABASE_URL = os.getenv("DATABASE_URL")
db = create_engine(DATABASE_URL)
metadata = MetaData()

from schemas.User import User
from schemas.Book import Book

class DBconnection:
    # Book actions --------------------
    @staticmethod
    def insertBook(bk: Book) -> Book | None:
        with Session(db) as session:
            session.add(bk)
            try:
                session.commit()
                session.refresh(bk) # to be able to use __repr__ in endpoint response
                return bk
            except IntegrityError as err:
                session.rollback()
                print("Integrity err:", err)
                return None
       

    # User actions --------------------
    @staticmethod
    def insertUser(usr: User):
        with Session(db) as session:
            session.add(usr)
            try:
                session.commit()
                session.refresh(usr)
                return usr
            except IntegrityError:
                session.rollback()

    @staticmethod
    def getUsers() -> list[dict]:
        with Session(db) as session:
            users = session.query(User).all()
            return users

    @staticmethod
    def getUserByUsername(username: str) -> User | None:
        with Session(db) as session:
            return session.query(User).filter(User.username==username).first()