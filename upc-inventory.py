import requests, json, re, creds
from pymongo import MongoClient
client = MongoClient(creds.mongostring)
db = client.inventory
drugs = db.drugs
while True:
    upc = input("Enter UPC Code:")
    response = json.loads(
        requests.get(
            f"https://api.fda.gov/drug/ndc.json?search=openfda.upc:0{upc}"
        ).text
    )
    if "results" in response:
        results = response["results"][0]
        name = results["brand_name"]
        strength = results["active_ingredients"][0]["strength"]
        qty = results["packaging"][0]["description"]

        print(f"{name}, {strength}")
        print(f"Qty: {qty}")
        print("Is this info correct? (y/n)")
        correct = input()
        if correct == "y":
            stock = input("Enter number of bottles: ")
        else:
            print("Ok, add it manually")
            name = input("Name: ")
            strength = input("Strength: ")
            stock = input("Enter number of bottles: ")

        identifier = {"_id": upc}
        product = {"name": name, "strength": strength, "qty": qty, "stock": stock}
        drugs.replace_one(identifier, product, True)
        print("Added to database")
        print("\n\n")
    else:
        print("Not found in database")