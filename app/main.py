from random import randrange
from pydantic import BaseModel
from fastapi import FastAPI, status, Response, HTTPException

app = FastAPI()


class Item(BaseModel):
    name: str


items = [
    {"id": 1, "name": "Foo"},
    {"id": 2, "name": "Bar"},
]

# Helper function to find item by ID
def find_item(id):
    for i in items:
        if i["id"] == id:
            return i


# Helper function to find index item
def find_index_item(id):
    for n, i in enumerate(items):
        if i["id"] == id:
            return n


# Root route
@app.get("/")
def root():
    return {"Hello": "World"}


# Get all items
@app.get("/items")
def get_items():
    return {"data": items}


# Create item
@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    item_dict = item.dict()
    item_dict["id"] = randrange(0, 1000)
    items.append(item_dict)
    return {"data": item_dict}


# Get item by ID
@app.get("/items/{id}")
def get_items(id: int):
    item = find_item(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"message: {id} was not found"
        )
    return {"item": item}


# Update item by ID
@app.put("/items/{id}")
def update_item(id: int, item: Item):
    index = find_index_item(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"item {id} does not exist"
        )
    item_dict = item.dict()
    item_dict["id"] = id
    items[index] = item_dict
    return {"data": item_dict}


# Delete item by ID
@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int):
    index = find_index_item(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"item {id} does not exist"
        )
    items.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
