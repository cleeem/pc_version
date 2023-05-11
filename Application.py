import tkinter
import tkinter.messagebox
import customtkinter
import os
import webbrowser
from PIL import Image

import iksm
import s3s
import utils as SpUtils
from Game import Game as Splatoon3Game
from Team import Team as Splatoon3Team
from Player import Player as Splatoon3Player





class Application(customtkinter.CTk):
    MIN_WIDTH = 1080
    MIN_HEIGHT = 720

    MAX_WIDTH = 1920
    MAX_HEIGHT = 1080

    CORNER_RADIUS = 15
    
    FONT_TITLE = ("Roboto Medium", 30) 
    FONT_BUTTON = ("Roboto Medium", 15) 
    FONT_LABEL = ("Roboto Medium", 18) 
    
    GAME_COLOR_FRAME = "#555555"

    BUTTON_HEIGHT = 100
    WIDTH_PARAM_BUTTON = 500

    def __init__(self):
        super().__init__()

        self.title("Splatnet 3 for PC")
        self.geometry(f"{Application.MIN_WIDTH}x{Application.MIN_HEIGHT}")
        self.minsize(width=Application.MIN_WIDTH, height=Application.MIN_HEIGHT)
        self.maxsize(width=Application.MAX_WIDTH, height=Application.MAX_HEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        self.configure_frames()
        self.my_team_frame.destroy()
        self.ennemy_team_frame.destroy()
        self.game_frame.destroy()

        self.right_frame.columnconfigure(0, minsize=10)
        self.right_frame.columnconfigure((1,2,3), weight=1)
        self.right_frame.columnconfigure(4, minsize=10)

        self.right_frame.rowconfigure(0, minsize=10)
        self.right_frame.rowconfigure((1,2,3), weight=1)
        self.right_frame.rowconfigure(4, minsize=10)

        self.welcome_label = customtkinter.CTkLabel(
            master=self.right_frame,
            text="Welcome on splatnet3 for PC \n \nif this is your first time using the application, \nplease check the setup menu",
            font=self.FONT_TITLE,
            justify=tkinter.LEFT
        )
        self.welcome_label.grid(
            row=1, column=2,
            sticky="nsew"
        )

        self.other_menu = customtkinter.CTkLabel(
            master=self.right_frame,
            text="Other menus available : \n\n \
    - last game : shows the last game you've played \n \
    - game (index) : select a game to see (from 1 to 50) \n \
    - setup : to setup the configuration required to use the app \n \
    - update assets : update all the game assets to latest version",
            font=self.FONT_LABEL,
            justify=tkinter.LEFT
        )
        self.other_menu.grid(
            row=2, column=2,
            sticky="nsew",
        )

    def get_concat_v(self, images: list):
        new_height = 64*len(images)

        new_image = Image.new('RGBA', (images[0].width, new_height))

        temp_height=0
        for img in images:
            new_image.paste(img, (0, temp_height))
            temp_height += 64

        return new_image
    
    def get_concat_h(self, images: list):
        new_width = 64*len(images)

        new_image = Image.new('RGBA', (new_width, images[0].height))

        temp_width=0
        for img in images:
            new_image.paste(img, (temp_width, 0))
            temp_width += 64
        
        return new_image

    def configure_frames(self):

        try:
            self.right_frame.destroy()
        except:
            pass

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.left_frame = customtkinter.CTkFrame(
            master=self,
            width=200,
            corner_radius=0
        )
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.right_frame = customtkinter.CTkFrame(
            master=self,
            corner_radius=self.CORNER_RADIUS
        )
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)


        # left frame configuration
        self.left_frame.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.left_frame.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.left_frame.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.left_frame.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        # right frame configuration
        self.right_frame.columnconfigure(0, minsize=10)
        self.right_frame.columnconfigure((1,2), weight=1)
        self.right_frame.columnconfigure(3, minsize=10)

        self.right_frame.rowconfigure(0, minsize=10)
        self.right_frame.rowconfigure((1,2), weight=1)
        self.right_frame.rowconfigure(3, minsize=10)


        # buttons 
        self.last_game_button = customtkinter.CTkButton(
            master=self.left_frame,
            text="last game",
            font=self.FONT_BUTTON,
            command=self.last_game_callback,
            height=self.BUTTON_HEIGHT,
        )
        self.last_game_button.grid(row=0, column=0, pady=10, padx=20)
        
        self.choose_game_button = customtkinter.CTkButton(
            master=self.left_frame,
            text="game (index)",
            font=self.FONT_BUTTON,
            command=self.choose_game_callback,
            height=self.BUTTON_HEIGHT,
        )
        self.choose_game_button.grid(row=1, column=0, pady=10, padx=20)

        self.setup_button = customtkinter.CTkButton(
            master=self.left_frame,
            text="setup",
            font=self.FONT_BUTTON,
            command=self.setup_callback,
            height=self.BUTTON_HEIGHT,
        )
        self.setup_button.grid(row=2, column=0, pady=10, padx=20)


        self.leave_button = customtkinter.CTkButton(
            master=self.left_frame,
            text="exit",
            font=self.FONT_BUTTON,
            command=self.on_closing,
            height=self.BUTTON_HEIGHT,
        )
        self.leave_button.grid(row=11, column=0, pady=10, padx=20)


        # Teams frames
        self.my_team_frame = customtkinter.CTkFrame(
            master=self.right_frame,
            fg_color=self.GAME_COLOR_FRAME,
            corner_radius=self.CORNER_RADIUS
        )
        self.my_team_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.ennemy_team_frame = customtkinter.CTkFrame(
            master=self.right_frame,
            fg_color=self.GAME_COLOR_FRAME,
            corner_radius=self.CORNER_RADIUS
        )
        self.ennemy_team_frame.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        self.game_frame = customtkinter.CTkFrame(
            master=self.right_frame,
            fg_color=self.GAME_COLOR_FRAME,
            corner_radius=self.CORNER_RADIUS
        )
        self.game_frame.grid(
            row=2, column=1, sticky="nsew",
            padx=10, #pady=10,
            columnspan=3
        )

        # Team frames configuration
        self.my_team_frame.rowconfigure(0, minsize=10)
        self.my_team_frame.rowconfigure((1,2), weight=1)
        self.my_team_frame.rowconfigure(3, minsize=10)

        self.my_team_frame.columnconfigure(0, minsize=10)
        self.my_team_frame.columnconfigure((1,2), weight=1)
        self.my_team_frame.columnconfigure(3, minsize=10)

        self.ennemy_team_frame.rowconfigure(0, minsize=10)
        self.ennemy_team_frame.rowconfigure((1,2), weight=1)
        self.ennemy_team_frame.rowconfigure(3, minsize=10)

        self.ennemy_team_frame.columnconfigure(0, minsize=10)
        self.ennemy_team_frame.columnconfigure((1,2), weight=1)
        self.ennemy_team_frame.columnconfigure(3, minsize=10)

        self.game_frame.rowconfigure(0, minsize=10)
        self.game_frame.rowconfigure((1), weight=1)
        self.game_frame.rowconfigure(2, minsize=10)

        self.game_frame.columnconfigure(0, minsize=10)
        self.game_frame.columnconfigure((1,2,3), weight=1)
        self.game_frame.columnconfigure(4, minsize=10)

    def row_column_configure_frame(self, frame):
        frame.columnconfigure(0, minsize=10)
        frame.columnconfigure((1,2,3), weight=1)
        frame.columnconfigure(4, minsize=10)

        frame.rowconfigure(0, minsize=10)
        frame.rowconfigure((1,2,3), weight=1)
        frame.rowconfigure(4, minsize=10)

    def configure_player_frames(self):
        self.my_team_p1 = customtkinter.CTkFrame(master=self.my_team_frame)
        self.my_team_p2 = customtkinter.CTkFrame(master=self.my_team_frame)
        self.my_team_p3 = customtkinter.CTkFrame(master=self.my_team_frame)
        self.my_team_p4 = customtkinter.CTkFrame(master=self.my_team_frame)

        self.ennemy_p1 = customtkinter.CTkFrame(master=self.ennemy_team_frame)
        self.ennemy_p2 = customtkinter.CTkFrame(master=self.ennemy_team_frame)
        self.ennemy_p3 = customtkinter.CTkFrame(master=self.ennemy_team_frame)
        self.ennemy_p4 = customtkinter.CTkFrame(master=self.ennemy_team_frame)

        self.my_team_p1.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.my_team_p2.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
        self.my_team_p3.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        self.my_team_p4.grid(row=2, column=2, sticky="nsew", padx=10, pady=10)

        self.ennemy_p1.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.ennemy_p2.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
        self.ennemy_p3.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        self.ennemy_p4.grid(row=2, column=2, sticky="nsew", padx=10, pady=10)

        self.row_column_configure_frame(self.my_team_p1)
        self.row_column_configure_frame(self.my_team_p2)
        self.row_column_configure_frame(self.my_team_p3)
        self.row_column_configure_frame(self.my_team_p4)
        self.row_column_configure_frame(self.ennemy_p1)
        self.row_column_configure_frame(self.ennemy_p2)
        self.row_column_configure_frame(self.ennemy_p3)
        self.row_column_configure_frame(self.ennemy_p4)

    def check_configuration(self):
        return os.path.exists("config.txt")
    
    def invalid_config(self):
        self.invalid_config_label = customtkinter.CTkLabel(
            master=self.game_frame,
            text="Config file was not found, \nplease go on the setup menu and follow the steps",
            font=self.FONT_TITLE,
            justify=tkinter.CENTER,
        )
        self.invalid_config_label.grid(row=2, column=2, padx=10, pady=10)        

    def load_ctk_image(self, path, x=40, y=40):
        """ load rectangular image with path relative to PATH """
        return customtkinter.CTkImage(Image.open(os.path.join(path)), size=(x, y))

    def load_pil_image(self, path):
        return Image.open(path).convert("RGBA")

    def convert_image(self, img, x=40, y=40):
        return customtkinter.CTkImage(img, size=(x, y))

    def get_player_stuff(self, player: Splatoon3Player):

        head_gear_list = []
        clothing_gear_list = []
        shoes_gear_list = []

        for bonus in player.head_gear_abilities:
            path = f"bonus/{bonus}.png"
            head_gear_list.append(self.load_pil_image(path)) 
        
        for bonus in player.clothing_gear_abilities:
            path = f"bonus/{bonus}.png"
            clothing_gear_list.append(self.load_pil_image(path)) 

        for bonus in player.shoes_gear_abilities:
            path = f"bonus/{bonus}.png"
            shoes_gear_list.append(self.load_pil_image(path)) 
        
        head = self.get_concat_h(head_gear_list)
        clothing = self.get_concat_h(clothing_gear_list)
        shoes = self.get_concat_h(shoes_gear_list)

        total = self.get_concat_v([head, clothing, shoes])

        return total

    def display_player(self, player: Splatoon3Player, frame):

        player_text = f"{player.name}\n{player.turf_point} pts \n{player.kill_w_assist}({player.assist_count}) / {player.death_count} / {player.special_count}"

        name_label = customtkinter.CTkLabel(
            master=frame,
            text=player_text,
            font=self.FONT_LABEL
        )
        name_label.grid(
            row=1, column=1, columnspan=3, 
            sticky="nsew"
        )

        main_weapon     = player.main_weapon
        sub_weapon      = player.sub_weapon
        special_weapon  = player.special_weapon

        main_weapon_image = self.load_pil_image(f"assets/{main_weapon}.png")
        sub_weapon_image = self.load_pil_image(f"assets/{sub_weapon}.png")
        special_weapon_image = self.load_pil_image(f"assets/{special_weapon}.png")

        weapons = self.get_concat_h([main_weapon_image, sub_weapon_image, special_weapon_image])
        # weapons.show()

        label_weapon = customtkinter.CTkLabel(
            master=frame,
            text="",
            image=self.convert_image(weapons, x=120, y=40)
        )
        label_weapon.grid(row=2, column=2)


        image_stuff = self.get_player_stuff(player)

        label_stuff = customtkinter.CTkLabel(
            master=frame,
            text="",
            image=self.convert_image(image_stuff, x=120, y=90)
        )
        label_stuff.grid(row=3, column=1, columnspan=3)

    def display_result(self, game_data: Splatoon3Game):
        if game_data.players["myTeam"].win_or_lose == "LOSE" and game_data.players["myTeam"].score != "draw":
            score = f"Ennemy Team won ({game_data.players['myTeam'].score} - {game_data.players['ennemy'].score})" 

        elif game_data.players["myTeam"].win_or_lose == "WIN" and game_data.players["myTeam"].score != "draw":
            score = f"Your Team won ({game_data.players['myTeam'].score} - {game_data.players['ennemy'].score})"

        else:
            score = "DRAW"

        game_res = \
f"""
Score : {score}
{game_data.vs_rule} on {game_data.stage} 
{SpUtils.epoch_time(str(game_data.game_date))} ({game_data.duration})

{f"last X power : {game_data.last_X_power}" if game_data.last_X_power != 0 else ""}
"""

        label_result = customtkinter.CTkLabel(
            master=self.game_frame,
            text=game_res,
            font=self.FONT_LABEL,
        )
        label_result.grid(row=1, column=1)

        map_image = self.load_ctk_image(f"map/{game_data.stage}.png", x=200, y=100)

        label_map = customtkinter.CTkLabel(
            master=self.game_frame,
            text="",
            image=map_image,
        )
        label_map.grid(row=1, column=2)

    def display_data(self, game_data: Splatoon3Game):
        self.display_player(game_data.players["myTeam"].player_list[0], self.my_team_p1)
        self.display_player(game_data.players["myTeam"].player_list[1], self.my_team_p2)
        self.display_player(game_data.players["myTeam"].player_list[2], self.my_team_p3)
        self.display_player(game_data.players["myTeam"].player_list[3], self.my_team_p4)

        self.display_player(game_data.players["ennemy"].player_list[0], self.ennemy_p1)
        self.display_player(game_data.players["ennemy"].player_list[1], self.ennemy_p2)
        self.display_player(game_data.players["ennemy"].player_list[2], self.ennemy_p3)
        self.display_player(game_data.players["ennemy"].player_list[3], self.ennemy_p4)


        self.display_result(game_data)

    def last_game_callback(self):
        self.configure_frames()
        self.configure_player_frames()
        

        if not self.check_configuration():
            self.invalid_config()

        else:
            label_loading = customtkinter.CTkLabel(
                master=self.game_frame,
                text="loading data, it may take some time",
                font=self.FONT_LABEL
            )
            label_loading.grid(
                row=1, column=2
            )

            self.update()

            game_data = Splatoon3Game(s3s.main(game_index=2, dict_key="VsHistoryDetailQuery")["data"]["vsHistoryDetail"])

            label_loading.destroy()

            self.display_data(game_data)



        print("last game")

    def choose_game_callback(self):
        self.configure_frames()

        if not self.check_configuration():
            self.invalid_config()

        print("choose game")

    def setup_callback(self):
        self.configure_frames()
        
        s3s.setup()

        url_login, auth_code = iksm.get_login_url(s3s.APP_USER_AGENT)

        self.label_url = customtkinter.CTkLabel(
            master=self.my_team_frame,
            text=f"please click on the button, \nyou will be redirected to nintendo's website, \ncopy the adress link of the red button \nand paste it below",
            font=self.FONT_TITLE
        )
        self.label_url.grid(
            row=1, column=1,
            sticky="nsew",
            columnspan=2
        )

        def open_link():
            webbrowser.open(url=url_login)

        self.button_link = customtkinter.CTkButton(
            master=self.my_team_frame,
            text="click to go on nintendo's website",
            font=self.FONT_TITLE,
            command=open_link
        )
        self.button_link.grid(
            row=2, column=1,
            sticky="nsew",
            columnspan=2
        )

        self.session_token_entry = customtkinter.CTkEntry(
            self.game_frame,
            fg_color="#444444",
            font=self.FONT_TITLE,
            text_color="#FFFFFF",
            placeholder_text_color="#FFFFFF",
            placeholder_text="paste here"
        )
        self.session_token_entry.grid(
            row=2, column=1,
            sticky="nsew",
            columnspan=3
        )

        def get_entry():
            use_account = self.session_token_entry.get()
            ver = s3s.A_VERSION
            try:
                new_token = iksm.log_in(ver=ver, auth_code_verifier=auth_code, use_account_url=use_account)

                s3s.CONFIG_DATA["session_token"] = new_token
                s3s.write_config(s3s.CONFIG_DATA)

                self.session_token_entry.destroy()

                label_ok = customtkinter.CTkLabel(
                    master=self.game_frame,
                    text="configuration written succesfuly, now getting you player id",
                    font=self.FONT_TITLE
                )
                label_ok.grid(
                    row=1, column=1,
                    sticky="nsew",
                    columnspan=3
                )
                self.update()

                pid = s3s.main(dict_key="VsHistoryDetailQuery")["data"]["vsHistoryDetail"]["player"]["id"]
                # print(pid)
                with open("pid.txt", "w") as file:
                    file.write(pid)

            
            except Exception:
                
                label_error = customtkinter.CTkLabel(
                    master=self.game_frame,
                    text="an error has occured while doing the configuration, \nPlease try again later ",
                    font=self.FONT_TITLE
                )
                label_error.grid(
                    row=1, column=1,
                    sticky="nsew",
                    columnspan=3
                )
                if os.path.exists("config.txt"):
                    os.remove("config.txt")
            
        self.button_validation = customtkinter.CTkButton(
            master=self.ennemy_team_frame,
            text="confirm",
            font=self.FONT_TITLE,
            command=get_entry
        )
        self.button_validation.grid(
            row=1, column=1,
            sticky="nsew",
            rowspan=2, columnspan=2
        )

        print("setup")



    def on_closing(self, event=0):
        print("bye")
        self.destroy()

if __name__ =="__main__":
    app = Application()
    app.mainloop()