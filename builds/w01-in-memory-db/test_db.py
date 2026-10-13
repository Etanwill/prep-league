from db import InMemoryDB


def test_in_memory_db():
    memory = InMemoryDB()
    memory.set( "01", "name", "etan")
    memory.set( "01", "age", 22)
    assert "01" in memory.data
    assert "name" in memory.data["01"]
    assert memory.get("01", "age") == 22
    assert memory.get("01", "city") == None
    assert memory.get("02", "city") == None
    assert memory.delete("01", "name") == True
    assert memory.delete("01", "name") == False
    assert memory.delete("01", "city") == False
    memory.set( "001", "name", "will")
    memory.set( "001", "city", "yaounde")
    memory.set( "001", "age", 22)
    assert memory.scan("001") == ["age(22)", "city(yaounde)", "name(will)"]
    assert memory.scan("11") == []
    memory.set( "001", "address", "emana")
    assert memory.scan_by_prefix("001", "name") == ["name(will)"]
    assert memory.scan_by_prefix("001", "a") == ["age(22)", "address(emana)"]

    memory.set("user1", "name", "Etan")
    assert memory.get("user1", "name") == "Etan"
    assert memory.get("user1", "age") is None

    assert memory.delete("user1", "name") is True
    assert memory.get("user1", "name") is None
    assert memory.delete("user1", "name") is False

    
