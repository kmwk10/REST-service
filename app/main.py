from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List

class DataStore:
    def __init__(self):
        self.items = []
    
    def add(self, item: str):
        self.items.append(item)
    
    def get_all(self) -> List[str]:
        return self.items
    
    def delete(self, item: str):
        if item in self.items:
            self.items.remove(item)
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    
    def update(self, old_item: str, new_item: str):
        if old_item in self.items:
            index = self.items.index(old_item)
            self.items[index] = new_item
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    
    def count(self) -> int:
        return len(self.items)
    
    def clear(self):
        self.items.clear()
    
    def exists(self, item: str) -> bool:
        return item in self.items
    
    def get_reversed(self) -> List[str]:
        return list(reversed(self.items))

def get_data_store():
    return store

store = DataStore()
app = FastAPI()

class Item(BaseModel):
    item: str

class UpdateItem(BaseModel):
    old_item: Item
    new_item: Item

@app.post('/add')
def add_item(item: Item, store: DataStore = Depends(get_data_store)):
    store.add(item.item)
    return {"message": "Item added"}

@app.get('/get')
def get_items(store: DataStore = Depends(get_data_store)):
    return {"items": store.get_all()}

@app.post('/delete')
def delete_item(item: Item, store: DataStore = Depends(get_data_store)):
    store.delete(item.item)
    return {"message": "Item deleted"}

@app.put('/update')
def update_item(update: UpdateItem, store: DataStore = Depends(get_data_store)):
    store.update(update.old_item.item, update.new_item.item)
    return {"message": "Item updated"}

@app.get('/count')
def count_items(store: DataStore = Depends(get_data_store)):
    return {"count": store.count()}

@app.delete('/clear')
def clear_items(store: DataStore = Depends(get_data_store)):
    store.clear()
    return {"message": "All items cleared"}

@app.get('/exists')
def check_item_exists(item: str, store: DataStore = Depends(get_data_store)):
    return {"exists": store.exists(item)}

@app.get('/list-reversed')
def get_items_reversed(store: DataStore = Depends(get_data_store)):
    return {"items": store.get_reversed()}

