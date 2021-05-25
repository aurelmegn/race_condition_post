from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_POSTGRES_DATABASE_URL = "postgresql://aurel:shift@localhost:5432/lab"

engine = create_engine(
    SQLALCHEMY_POSTGRES_DATABASE_URL,  # connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer, )
    purchased_count = Column(Integer, )

    clients = relationship("Client", back_populates="item")


class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True, index=True)
    at = Column(DateTime, default=datetime.now)

    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship("Item", back_populates="clients")
