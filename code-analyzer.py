import re
import requests, json

combined_regex = r"(01(?P<GTIN>\d{14}))?21(?P<serial>\w{1,20})\W?(17(?P<exp>\d{6}))?(15(?P<bestbefore>\d{6}))?10(?P<batch>\w{1,20})\W?"


def lookup():
    print("GS1 Data Matrix Code")
    code = input()
    match = re.search(combined_regex, code)
    GTIN = match.group("GTIN")
    serial = match.group("serial")
    best_before = match.group("bestbefore")
    exp = match.group("exp")
    batch = match.group("batch")
    if GTIN == None:
        print("Error, no gtin")
        lookup()

    if exp:
        use_by = exp
    elif best_before:
        use_by = best_before
    else:
        use_by = "None"

    ndc = GTIN[3:11]
    results = None
    i = 1
    while results is None and i < 16:
        try:
            ndc = GTIN[3:11]
            if i > 7: #No results yet
                ndc = GTIN[3:12] #Add more digits
            ndc = ndc[:i%8] + "-" + ndc[i%8:]  # openFDA needs a hyphen there
            print(f"NDC: {ndc}")
            response = json.loads(
                requests.get(
                    f"https://api.fda.gov/drug/ndc.json?search=product_ndc:{ndc}"
                ).text
            )
            results = response["results"][0]
        except:
            i=i+1

    name = results["brand_name"]
    strength = results["active_ingredients"][0]["strength"]
    description = results["packaging"][0]["description"]
    qty = re.findall(r"(\d*) TABLET", description)[0]

    print(f"{name}, {strength}")
    print(f"Qty: {qty}")
    print(f"S/N {serial}")
    print(f"Lot/Batch #{batch}")
    print(f"Use By {use_by}")

    lookup()


lookup()
