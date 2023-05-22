import utils, requests, os

def GesotownQuery(result: dict):

    res = {}

    res["dailyBrand"] = {
        "name" : result["data"]["gesotown"]["pickupBrand"]["brand"]["name"],
        "common" : result["data"]["gesotown"]["pickupBrand"]["brand"]["usualGearPower"]["name"]
    }

    res["dailyDropGears"] = []

    for gear in result["data"]["gesotown"]["pickupBrand"]["brandGears"]:

        name = gear["gear"]["name"]
        gear_type = gear["gear"]["__typename"]
        gear_type = gear_type[0].lower() + gear_type[1:]

        if not os.path.exists(f"gears/{gear_type}/{name}.png"):
            url = gear["gear"]["image"]["url"]
            with open(f"gears/{gear_type}/{name}.png", "wb") as file:
                file.write(requests.get(url=url).content)

                print("download done")

        res["dailyDropGears"].append(
            {
                "name" : name,
                "ability" : gear["gear"]["primaryGearPower"]["name"],
                "price" : gear["price"]
            }
        )
    
    # return res
    res["gearsOnSale"] = []

    for gear in result["data"]["gesotown"]["limitedGears"]:
        res["gearsOnSale"].append(
            {
                "name" : gear["gear"]["name"],
                "type" : gear["gear"]["__typename"],
                "ability" : gear["gear"]["primaryGearPower"]["name"],
                "price" : gear["price"],
                "endTime" : str(utils.epoch_time(gear["saleEndTime"]))[11:], # hours only 

            }
        )

    return res
