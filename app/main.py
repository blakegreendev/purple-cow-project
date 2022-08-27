from pydantic import BaseModel
from fastapi import FastAPI, status, Response, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Item(BaseModel):
    name: str


# Root route
@app.get("/")
def root():
    return {"Hello": "World"}


# Get all items
@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return {"data": items}


# Create item
@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item, db: Session = Depends(get_db)):
    new_item = models.Item(name=item.name)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"data": new_item}


# Get item by ID
@app.get("/items/{id}")
def get_items(id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"message: {id} was not found"
        )
    return {"item": item}


# Update item by ID
@app.put("/items/{id}")
def update_item(id: int, updated_item: Item, db: Session = Depends(get_db)):
    item_query = db.query(models.Item).filter(models.Item.id == id)
    item = item_query.first()
    if item == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"item {id} does not exist"
        )
    item_query.update(updated_item.dict(), synchronize_session=False)
    db.commit()
    return {"data": item_query.first()}


# Delete item by ID
@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == id)

    if item.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"item {id} does not exist"
        )
    item.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
