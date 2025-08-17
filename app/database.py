# import json
import sqlite3
from typing import Any
from .schemas import ShipmentCreate, ShipmentUpdate

# shipments = {}
# with open("shipments.json", "r") as file:
#     data = json.load(file)
#     print(data)
#     for item in data:
#         print(item)
#         shipments[item["id"]] = item
#         print(shipments)


# def save_to_database():
#     with open("shipments.json", "w") as json_file:
#         json.dump(list(shipments.values()), json_file)


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("sqlite.db", check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS shipment (id INTEGER PRIMARY KEY, content TEXT, weight REAL, status TEXT)",
        )

    def create(self, shipment:ShipmentCreate)-> int:
        self.cursor.execute("SELECT MAX(id) FROM shipment")
        result = self.cursor.fetchone()
        new_id = result[0] + 1
        self.cursor.execute("INSERT INTO shipment VALUES(:id, :content,:weight, :status)",{
            "id": new_id,
            **shipment.model_dump(),
            "status": "placed"
        })
        self.connection.commit()
        return new_id
    
    def get(self, id:int)-> dict[str,Any]|None:
        self.cursor.execute("SELECT * FROM shipment WHERE id=?",(id,))
        row = self.cursor.fetchone()
        return {
            "id": row[0],
            "content": row[1],
            "weight": row[2],
            "status": row[3]
        } if row else None
    def update(self,id:int, shipment:ShipmentUpdate) -> dict[str, Any]:
        self.cursor.execute("UPDATE shipment SET status=:status WHERE id=:id",{"id": id, **shipment.model_dump()})
        self.connection.commit()
        return self.get(id)
    
    def delete(self, id:int):
        self.cursor.execute("DELETE FROM shipment WHERE id=?",(id,))
        self.connection.commit()
    
    def close(self):
        self.connection.close()


# make a connection to the database
# connection = sqlite3.connect("sqlite.db")
# cursor = connection.cursor()
# create a table if it does not exist
# cursor.execute(
#     "CREATE TABLE IF NOT EXISTS shipment (id INTEGER PRIMARY KEY, content TEXT, weight REAL, status TEXT)"
# )
# insert data into the table
# cursor.execute("INSERT INTO shipment VALUES(12702, 'Books', 3, 'in_transit')")
# commit the changes
# connection.commit()
# fetch all data from the table
# cursor.execute("SELECT * FROM shipment")
# cursor.execute("SELECT * FROM shipment where id=12702")
# rows = cursor.fetchall()
# rows2= cursor.fetchone()
# print(rows)
# Delete all data from the table
# cursor.execute("DELETE FROM shipment where id=12702")
# commit the changes
# connection.commit()
# Drop the table
# cursor.execute("DROP TABLE shipment")
# update data in the table
# id = "0 OR TRUE"
# status = "delivered"
# # cursor.execute("UPDATE shipment SET status=? WHERE id=?", (status, id))
# cursor.execute(
#     "UPDATE shipment SET status=:status WHERE id=:id", {"status": status, "id": id}
# )
# connection.commit()
# # close the connection
# connection.close()
