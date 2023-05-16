from Player import Player

class Team:

    player_unknown_dict = {
        "name" : "?",
        "paint" : 0,
        "result" : None,
        "weapon" : {
            "name" : "Unknown",
            "specialWeapon" : {
                "name" : "Unknown",
            },
            "subWeapon" : {
                "name" : "Unknown",
            },
        },
        "headGear" : {
            "primaryGearPower" : {
                "name" : "Unknown",
            },
            "additionalGearPowers" : []
        },
        "clothingGear" : {
            "primaryGearPower" : {
                "name" : "Unknown",
            },
            "additionalGearPowers" : []
        },
        "shoesGear" : {
            "primaryGearPower" : {
                "name" : "Unknown",
            },
            "additionalGearPowers" : []
        },

    }

    def __init__(self, data: dict, mode, is_my_team = False) -> None:


        self.is_my_team = is_my_team

        self.win_or_lose = data["judgement"]
        
        if mode in ("REGULAR", "FEST"):
            self.score = "draw" if data["result"] is None else str(data["result"]["paintRatio"] * 100)[:4] + "%"
        else:
            self.score = "draw" if data["result"] is None else round(data["result"]["score"], 1) 

        self.player_list = []

        for player_data in data["players"]:
            
            self.player_list.append(
                Player(player_data)
            )
        
        if len(self.player_list) < 4:
            for i in range(4 - len(self.player_list)):
                self.player_list.append(Player(self.player_unknown_dict))


    def __str__(self) -> str:
        res_player = ""
        for player in self.player_list:
            res_player = res_player + str(player)
        return \
f"""
{self.win_or_lose}
score : {self.score}

player stats 
{res_player}
"""