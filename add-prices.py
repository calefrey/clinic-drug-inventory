import creds
from pymongo import MongoClient
from bson.decimal128 import Decimal128 as decimal
client = MongoClient(creds.mongostring)
db = client.inventory
drugs = db.drugs
data = drugs.find({"price": {"$exists": False}}).sort("name")
for doc in data:
    name = doc["name"]
    strength = doc["strength"]
    qty = doc["qty"]
    print(f"Price for {name}, {strength}")
    print(qty)
    price = input("$")
    drugs.update_one({"_id": doc["_id"]}, {"$set": {"price": decimal(price)}})
print("All records have prices")