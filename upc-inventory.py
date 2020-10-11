import requests, json, re, creds
from pymongo import MongoClient
client = MongoClient(creds.mongostring)
db = client.inventory
drugs = db.drugs
while True:
    upc = input("Enter UPC Code:")
    drug_in_db = drugs.find_one({'_id':upc}) #chek if it already exists in the database
    if drug_in_db:
        print("Already in database:")
        name = drug_in_db["name"]
        strength = drug_in_db["strength"]
        qty = drug_in_db["qty"]
        stock = drug_in_db["stock"]
        print(f"{name}, {strength}")
        print(qty)
        print(f"Currently {stock} in stock, would you like to change that value? (y/n)")
        change = input()
        if change == "y":
            stock = input("How many are in stock?")
            drugs.update_one({"_id": drug_in_db["_id"]}, {"$set": {"stock": stock}})
    else:
        print("Checking the FDA database")
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
                stock = input("Enter number of containers: ")
            else:
                print("Ok, add it manually")
                name = input("Name: ")
                strength = input("Strength: ")
                qty = input("How many are in each container? ")
                stock = input("Enter number of containers: ")
                print({"_id": upc, "name": name, "strength": strength, "qty": qty, "stock": stock})
            drugs.insert_one({"_id": upc, "name": name, "strength": strength, "qty": qty, "stock": stock})
            print("Added to database")
            print("\n\n")
        else:
            print("Not found in database")
            print("Add manually")
            name = input("Name: ")
            strength = input("Strength: ")
            qty = input("How many are in each container?: ")
            stock = input("Enter number of bottles: ")
            print({"_id": upc, "name": name, "strength": strength, "qty": qty, "stock": stock})
            drugs.insert_one({"_id": upc, "name": name, "strength": strength, "qty": qty, "stock": stock})
            print("Added to database")
            print("\n\n")
