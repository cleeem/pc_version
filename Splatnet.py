import utils

def GesotownQuery(result: dict):
    res = {}

    res["dailyBrand"] = {
        "name" : result["data"]["gesotown"]["pickupBrand"]["brand"]["name"],
        "common" : result["data"]["gesotown"]["pickupBrand"]["brand"]["usualGearPower"]["name"]
    }

    res["dailyDropGears"] = []

    for gear in result["data"]["gesotown"]["pickupBrand"]["brandGears"]:
        res["dailyDropGears"].append(
            {
                "name" : gear["gear"]["name"],
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
                "ability" : gear["gear"]["primaryGearPower"]["name"],
                "price" : gear["price"],
                "endTime" : str(utils.epoch_time(gear["saleEndTime"]))[11:], # hours only 

            }
        )

    return res
