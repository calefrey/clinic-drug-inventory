import creds
from pymongo import MongoClient
from bson.decimal128 import Decimal128 as decimal

print("To skip entering a price, set the it to 0 and we'll come back to it next time")
client = MongoClient(creds.mongostring)
db = client.inventory
drugs = db.drugs
data = drugs.find({"$or": [{"price": {"$exists": False}}, {"price": 0}]}).sort("name")
for doc in data:
    name = doc["name"]
    strength = doc["strength"]
    qty = doc["qty"]
    print(f"Price for {name}, {strength}")
    print(qty)
    price = input("$")
    try: #make sure it's a number
        float(price)
    except ValueError:
        print("Careful, that's not a number!")
        price = input("$")
    drugs.update_one({"_id": doc["_id"]}, {"$set": {"price": decimal(price)}})
print("All records have prices")