from Player import Player

class Team:

    def __init__(self, data: dict, mode, is_my_team = False) -> None:


        self.is_my_team = is_my_team

        self.win_or_lose = data["judgement"]
        
        if mode == "REGULAR":
            self.score = "draw" if data["result"] is None else str(data["result"]["paintRatio"] * 100) + "%"
        else:
            self.score = "draw" if data["result"] is None else data["result"]["score"] 

        self.player_list = []

        for player_data in data["players"]:
            self.player_list.append(
                Player(player_data)
            )

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