from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

data = []

class Item(BaseModel):
    item: str

@app.post('/add')
def add_item(item: Item):
    if item.item:
        data.append(item.item)
        return {"message": "Item added"}
    raise HTTPException(status_code=400, detail="No item provided")

@app.get('/get')
def get_items():
    return {"items": data}

@app.post('/delete')
def delete_item(item: Item):
    if item.item in data:
        data.remove(item.item)
        return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.put('/update')
def update_item(old_item: Item, new_item: Item):
    if old_item.item in data:
        index = data.index(old_item.item)
        data[index] = new_item.item
        return {"message": "Item updated"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.get('/count')
def count_items():
    return {"count": len(data)}

@app.delete('/clear')
def clear_items():
    data.clear()
    return {"message": "All items cleared"}

@app.get('/exists')
def check_item_exists(item: str):
    return {"exists": item in data}

@app.get('/list-reversed')
def get_items_reversed():
    return {"items": list(reversed(data))}
