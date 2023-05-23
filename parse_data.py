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
        name = gear["gear"]["name"]
        gear_type = gear["gear"]["__typename"]
        gear_type = gear_type[0].lower() + gear_type[1:]

        ab = gear["gear"]["primaryGearPower"]["name"]
        price = gear["price"]

        if not os.path.exists(f"gears/{gear_type}/{name}.png"):
            url = gear["gear"]["image"]["url"]
            with open(f"gears/{gear_type}/{name}.png", "wb") as file:
                file.write(requests.get(url=url).content)

                print("download done")

        res["gearsOnSale"].append(
            {
                "name" : name,
                "type" : gear_type,
                "ability" : ab,
                "price" : price,
                "endTime" : str(utils.epoch_time(gear["saleEndTime"]))[11:], # hours only 

            }
        )

    return res



def HistoryRecordQuery(result: dict):
    res = {}

    res["bestPowers"] = {
        "Splat Zones" :   {
            "power" : result["data"]["playHistory"]["xMatchMaxAr"]["power"],
            "date" :  result["data"]["playHistory"]["xMatchMaxAr"]["powerUpdateTime"],
        },
        "Tower Control" : {
            "power" : result["data"]["playHistory"]["xMatchMaxLf"]["power"],
            "date" :  result["data"]["playHistory"]["xMatchMaxLf"]["powerUpdateTime"],
        },
        "Rainmaker" :     {
            "power" : result["data"]["playHistory"]["xMatchMaxGl"]["power"],
            "date" :  result["data"]["playHistory"]["xMatchMaxGl"]["powerUpdateTime"],
        },
        "Clam Blitz" :    {
            "power" : result["data"]["playHistory"]["xMatchMaxCl"]["power"],
            "date" :  result["data"]["playHistory"]["xMatchMaxCl"]["powerUpdateTime"],
        },
    }

    current_key = "winCountTotal"
    res[current_key] = result["data"]["playHistory"][current_key]


    res["seasons"] = {}
    for season in result["data"]["playHistory"]["xMatchSeasonHistory"]["edges"]:
        temp = season["node"]

        power_rank_dict = {
            "Splat Zones" :   {},
            "Tower Control" : {},
            "Rainmaker" :     {},
            "Clam Blitz" :    {},
        } 

        for key in list(temp.keys())[1:]:
            if "Ar" in key:
                power_rank_dict["Splat Zones"][key] = temp[key]
            elif "Lf" in key:
                power_rank_dict["Tower Control"][key] = temp[key]
            elif "Gl" in key:
                power_rank_dict["Rainmaker"][key] = temp[key]
            elif "Cl" in key:
                power_rank_dict["Clam Blitz"][key] = temp[key]

        res["seasons"][temp["xRankingSeason"]["name"]] = power_rank_dict

    current_key = "frequentlyUsedWeapons"
    res[current_key] = []
    for weapon in result["data"]["playHistory"][current_key]:
        res[current_key].append(weapon["name"])

    current_key = "weaponHistory"
    res[current_key] = {}
    for season_data in result["data"]["playHistory"][current_key]["nodes"]:
        season_name = season_data["seasonName"]
        res[current_key][season_name] = {}
        for weapon_class in season_data["weaponCategories"]:
            cate = weapon_class["weaponCategory"]["name"]
            res[current_key][season_name][cate] = {}
            # print(weapon_class["weaponCategory"]["name"])

            for weapon in weapon_class["weapons"]:
                weap = weapon["weapon"]["name"]
                ratio = weapon["utilRatio"]
                res[current_key][season_name][cate][weap] = ratio
            
    # print(len(result["data"]["playHistory"]["allBadges"]))
        
    return res
