from Team import Team

class Game:

    def __init__(self, data: dict) -> None:

        self.vs_mode = data["vsMode"]["mode"]
        self.vs_rule = data["vsRule"]["name"]

        self.stage = data["vsStage"]["name"]
        self.game_date = data["playedTime"]
        minutes  = data["duration"] // 60
        secondes = data["duration"] % 60
        secondes = "0"+str(secondes) if secondes<10 else secondes
        self.duration =  f"{minutes}:{secondes}"

        if self.vs_mode == "X_MATCH":
            self.last_X_power = round(data["xMatch"]["lastXPower"], 1)
        else:
            self.last_X_power = 0

        self.players = {
            "myTeam" : Team(data["myTeam"], mode=self.vs_mode, is_my_team=True),
            "ennemy" : Team(data["otherTeams"][0], mode=self.vs_mode),
        }

    def get_discord_str(self):
        return (
            \
f"""
{self.vs_mode} {self.vs_rule} on {self.stage}
date : {self.game_date}
played for : {self.duration}

your power for this game : {self.last_X_power}

TEAM STATS
""",

str(self.players["myTeam"]),

"-------------------------------------------------",

str(self.players["ennemy"]),

        )


    def __str__(self) -> str:
        return \
f"""
{self.vs_mode} {self.vs_rule} on {self.stage}
date : {self.game_date}
played for : {self.duration}

your power for this game : {self.last_X_power}

TEAM STATS
{str(self.players["myTeam"])}

-------------------------------------------------

{str(self.players["ennemy"])}
"""
