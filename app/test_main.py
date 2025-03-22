from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_add_item():
    response = client.post("/add", json={"item": "test_item"})
    assert response.status_code == 200
    assert response.json() == {"message": "Item added"}

def test_get_items():
    response = client.get("/get")
    assert response.status_code == 200
    assert "items" in response.json()

def test_delete_item():
    client.post("/add", json={"item": "delete_me"})
    response = client.post("/delete", json={"item": "delete_me"})
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted"}

def test_update_item():
    client.post("/add", json={"item": "old_item"})
    response = client.put("/update", json={"old_item": {"item": "old_item"}, "new_item": {"item": "new_item"}})
    assert response.status_code == 200
    assert response.json() == {"message": "Item updated"}

def test_count_items():
    response = client.get("/count")
    assert response.status_code == 200
    assert "count" in response.json()

def test_clear_items():
    response = client.delete("/clear")
    assert response.status_code == 200
    assert response.json() == {"message": "All items cleared"}

def test_check_item_exists():
    client.post("/add", json={"item": "exists_check"})
    response = client.get("/exists", params={"item": "exists_check"})
    assert response.status_code == 200
    assert response.json() == {"exists": True}

def test_get_items_reversed():
    response = client.delete("/clear")
    client.post("/add", json={"item": "first"})
    client.post("/add", json={"item": "second"})
    response = client.get("/list-reversed")
    assert response.status_code == 200
    assert response.json()["items"] == ["second", "first"]
