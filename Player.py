class Player:

    def __init__(self, data: dict) -> None:
        
        self.name = data["name"]
        
        # if the player was disconnected from the game
        if data.get("result", None) == None:
            self.kill_w_assist = "-"
            self.death_count   = "-"
            self.assist_count  = "-"
            self.special_count = "-"
            self.turf_point    = 0 

        else:
            self.kill_w_assist = data["result"]["kill"]
            self.death_count   = data["result"]["death"]
            self.assist_count  = data["result"]["assist"]
            self.special_count = data["result"]["special"]
            self.turf_point    = data["paint"] 
        
        self.main_weapon = data["weapon"]["name"]
        self.special_weapon = data["weapon"]["specialWeapon"]["name"]
        self.sub_weapon = data["weapon"]["subWeapon"]["name"]

        self.head_gear_abilities = [data["headGear"]["primaryGearPower"]["name"]]
        for sub in data["headGear"]["additionalGearPowers"]:
            self.head_gear_abilities.append(sub["name"])

        if len(self.head_gear_abilities) != 4:
            for i in range(4 - len(self.head_gear_abilities)):
                self.head_gear_abilities.append("Unknown")


        self.clothing_gear_abilities = [data["clothingGear"]["primaryGearPower"]["name"]]
        for sub in data["clothingGear"]["additionalGearPowers"]:
            self.clothing_gear_abilities.append(sub["name"])

        if len(self.clothing_gear_abilities) != 4:
            for i in range(4 - len(self.clothing_gear_abilities)):
                self.clothing_gear_abilities.append("Unknown")


        self.shoes_gear_abilities = [data["shoesGear"]["primaryGearPower"]["name"]]
        for sub in data["shoesGear"]["additionalGearPowers"]:
            self.shoes_gear_abilities.append(sub["name"])

        if len(self.shoes_gear_abilities) != 4:
            for i in range(4 - len(self.shoes_gear_abilities)):
                self.shoes_gear_abilities.append("Unknown")

    
    def __str__(self) -> str:
        return \
f"""
player name : {self.name}
stats : {self.kill_w_assist} ({self.assist_count}) / {self.death_count} / {self.special_count}
weapon : {self.main_weapon}  {self.sub_weapon}  {self.special_weapon}
stuff : 
    head {self.head_gear_abilities}
clothing {self.clothing_gear_abilities}
   shoes {self.shoes_gear_abilities}
"""