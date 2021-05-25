import os
from random import randint
from time import sleep
from typing import Optional, List

from fastapi import FastAPI, Depends, Response
# Dependency
from pydantic import BaseModel

from race_condition.db import SessionLocal, engine, Base, Item, Client


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if not os.path.isfile("../sql_app.db"):
    Base.metadata.create_all(bind=engine)

app = FastAPI()


class ItemIn(BaseModel):
    name: str
    quantity: int
    purchased_count: int

    class Config:
        orm_mode = True


class ItemOut(ItemIn):
    pass


@app.post("/items", response_model=List[ItemOut])
def create_items(db=Depends(get_db)):
    for i in range(10):
        item = ItemIn(name=f"Item {i + 1}", quantity=10, purchased_count=0)

        db_item = Item(**item.dict())
        db.add(db_item)
    db.commit()

    return db.query(Item).all()


def process_payement() -> bool:
    a = randint(1, 4)
    sleep(a)

    return True


@app.post("/item/buy/{item_id}", )
def buy(item_id: int, response: Response, db=Depends(get_db), ) -> bool:
    db_item: Optional[Item] = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        response.status_code = 401
        return False

    if db_item.purchased_count >= db_item.quantity:
        response.status_code = 401
        return False

    process_payement()

    db_item.purchased_count += 1

    c = Client()
    c.item = db_item
    db.add(c)
    db.commit()
    return True


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
