import tkinter
import tkinter.messagebox
import customtkinter
import os
import webbrowser
from PIL import Image

import iksm
import s3s
import utils as SpUtils
import parse_data

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
    BIG_FONT = ("Roboto Medium", 23)
    SMALL_FONT = ("Roboto Medium", 14)
    
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

        self.init_frames()
        self.configure_frames_games()
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
            text="Welcome to splatnet3 for PC \n \nif this is your first time using the application, \nplease check the setup menu",
            font=self.FONT_TITLE,
            justify=tkinter.LEFT
        )
        self.welcome_label.grid(
            row=1, column=4,
            sticky="nsew"
        )

        self.other_menu = customtkinter.CTkLabel(
            master=self.right_frame,
            text="Other menus available : \n\n \
- last game : shows the last game you've played \n \
- setup : to setup the configuration required to use the app  ",
            font=self.FONT_LABEL,
            justify=tkinter.LEFT
        )
        self.other_menu.grid(
            row=2, column=4,
            sticky="nsew",
        )

    def init_frames(self):
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
        self.right_frame.columnconfigure((1,2,3,4,5,6,7), weight=1)
        self.right_frame.columnconfigure(8, minsize=10)

        self.right_frame.rowconfigure(0, minsize=10)
        self.right_frame.rowconfigure((1,2), weight=1)
        self.right_frame.rowconfigure(3, minsize=10)


        # buttons 
        self.last_game_button = customtkinter.CTkButton(
            master=self.left_frame,
            text="Last Game",
            font=self.FONT_BUTTON,
            command=self.last_game_callback,
            height=self.BUTTON_HEIGHT,
        )
        self.last_game_button.grid(row=0, column=0, pady=10, padx=20)
    
        self.my_stats = customtkinter.CTkButton(
            master=self.left_frame,
            text="My Stats",
            font=self.FONT_BUTTON,
            command=self.my_stats_callback,
            height=self.BUTTON_HEIGHT,
        )
        self.my_stats.grid(row=1, column=0, pady=10, padx=20)

        self.splatnet_button = customtkinter.CTkButton(
            master=self.left_frame,
            text="Splatnet \nStuffs",
            font=self.FONT_BUTTON,
            command=self.splatnet_callback,
            height=self.BUTTON_HEIGHT,
        )
        self.splatnet_button.grid(row=2, column=0, pady=10, padx=20)


        self.setup_button = customtkinter.CTkButton(
            master=self.left_frame,
            text="setup",
            font=self.FONT_BUTTON,
            command=self.setup_callback,
            height=self.BUTTON_HEIGHT,
        )
        self.setup_button.grid(row=3, column=0, pady=10, padx=20)


        self.leave_button = customtkinter.CTkButton(
            master=self.left_frame,
            text="exit",
            font=self.FONT_BUTTON,
            command=self.on_closing,
            height=self.BUTTON_HEIGHT,
        )
        self.leave_button.grid(row=11, column=0, pady=10, padx=20)

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

    def configure_my_stats_frames(self):
        try:
            self.right_frame.destroy()
        except:
            pass

        self.right_frame = customtkinter.CTkFrame(
            master=self,
            corner_radius=self.CORNER_RADIUS
        )
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.right_frame.rowconfigure(0, minsize=10)
        self.right_frame.rowconfigure((1,2), weight=1)
        self.right_frame.rowconfigure(3, minsize=10)

        self.right_frame.columnconfigure(0, minsize=10)
        self.right_frame.columnconfigure((1,2), weight=1)
        self.right_frame.columnconfigure(3, minsize=10)


        self.best_power_frame = customtkinter.CTkFrame(
            master=self.right_frame,
        )
        self.best_power_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.best_power_frame.rowconfigure(0, minsize=10)
        self.best_power_frame.rowconfigure((1,2,3,4), weight=1)
        self.best_power_frame.rowconfigure(5, minsize=10)

        self.best_power_frame.columnconfigure(0, minsize=10)
        self.best_power_frame.columnconfigure((1,2,3,4), weight=1)
        self.best_power_frame.columnconfigure(5, minsize=10)


        self.current_power_frame = customtkinter.CTkFrame(
            master=self.right_frame,
        )
        self.current_power_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        self.current_power_frame.rowconfigure(0, minsize=10)
        self.current_power_frame.rowconfigure((1,2,3,4), weight=1)
        self.current_power_frame.rowconfigure(5, minsize=10)

        self.current_power_frame.columnconfigure(0, minsize=10)
        self.current_power_frame.columnconfigure((1,2,3,4), weight=1)
        self.current_power_frame.columnconfigure(5, minsize=10)

        self.frequent_weapons = customtkinter.CTkFrame(
            master=self.right_frame,
        )
        self.frequent_weapons.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        self.weapon_usage = customtkinter.CTkFrame(
            master=self.right_frame,
        )
        self.weapon_usage.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

    def configure_frames_games(self):
        try:
            self.right_frame.destroy()
            self.setup_frame.destroy()
        except:
            pass

        self.right_frame = customtkinter.CTkFrame(
            master=self,
            corner_radius=self.CORNER_RADIUS
        )
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)


        # right frame configuration
        self.right_frame.columnconfigure(0, minsize=10)
        self.right_frame.columnconfigure((1,2,3,4,5,6,7), weight=1)
        self.right_frame.columnconfigure(8, minsize=10)

        self.right_frame.rowconfigure(0, minsize=10)
        self.right_frame.rowconfigure((1,2), weight=1)
        self.right_frame.rowconfigure(3, minsize=10)

        # Teams frames
        self.my_team_frame = customtkinter.CTkFrame(
            master=self.right_frame,
            fg_color=self.GAME_COLOR_FRAME,
            corner_radius=self.CORNER_RADIUS
        )
        self.my_team_frame.grid(row=2, column=1, 
                sticky="nsew", 
                padx=10, pady=10,
                columnspan=3)

        self.ennemy_team_frame = customtkinter.CTkFrame(
            master=self.right_frame,
            fg_color=self.GAME_COLOR_FRAME,
            corner_radius=self.CORNER_RADIUS
        )
        self.ennemy_team_frame.grid(row=2, column=5, 
                sticky="nsew", 
                padx=10, pady=10,
                columnspan=3)

        self.game_frame = customtkinter.CTkFrame(
            master=self.right_frame,
            fg_color=self.GAME_COLOR_FRAME,
            corner_radius=self.CORNER_RADIUS,
        )
        self.game_frame.grid(
            row=1, column=2, sticky="ew",
            padx=10, pady=10,
            columnspan=5
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

    def congigure_stuff_frame(self, frame: customtkinter.CTkFrame):
        frame.rowconfigure(0, minsize=10)
        frame.rowconfigure((1,2), weight=1)
        frame.rowconfigure(3, minsize=10)

        frame.columnconfigure(0, minsize=10)
        frame.columnconfigure((1,2,3), weight=1)
        frame.columnconfigure(4, minsize=10)

    def configure_frames_splatnet(self):
        try:
            self.right_frame.destroy()
        except:
            pass

        self.right_frame = customtkinter.CTkFrame(
            master=self,
            corner_radius=self.CORNER_RADIUS
        )
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.right_frame.rowconfigure(0, minsize=10)
        self.right_frame.rowconfigure(1, weight=1)
        self.right_frame.rowconfigure(2, minsize=10)

        self.right_frame.columnconfigure(0, minsize=10)
        self.right_frame.columnconfigure((1,2,3,4,5,6,7), weight=1)
        self.right_frame.columnconfigure(8, minsize=10)

        self.daily_brand_frame = customtkinter.CTkFrame(
            master=self.right_frame
        )
        self.daily_brand_frame.grid(
            row=1, column=1,
            columnspan=2,
            sticky="nsew",
            padx=10, pady=10
        )

        self.daily_brand_frame.rowconfigure(0, minsize=10)
        self.daily_brand_frame.rowconfigure((1,2,3,4,5), weight=1)
        self.daily_brand_frame.rowconfigure(6, minsize=10)

        self.daily_brand_frame.columnconfigure(0, minsize=10)
        self.daily_brand_frame.columnconfigure((1), weight=1)
        self.daily_brand_frame.columnconfigure(2, minsize=10)


        self.daily_first_gear_frame = customtkinter.CTkFrame(
            master=self.daily_brand_frame,
            height=150
        )
        self.daily_first_gear_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        self.congigure_stuff_frame(self.daily_first_gear_frame)


        self.daily_second_gear_frame = customtkinter.CTkFrame(
            master=self.daily_brand_frame,
            height=150
        )
        self.daily_second_gear_frame.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)

        self.congigure_stuff_frame(self.daily_second_gear_frame)


        self.daily_third_gear_frame = customtkinter.CTkFrame(
            master=self.daily_brand_frame,
            height=150
        )
        self.daily_third_gear_frame.grid(row=4, column=1, sticky="nsew", padx=10, pady=10)

        self.congigure_stuff_frame(self.daily_third_gear_frame)


        self.daily_gear_frames = [self.daily_first_gear_frame, self.daily_second_gear_frame, self.daily_third_gear_frame]


        self.common_bonus_frame = customtkinter.CTkFrame(
            master=self.daily_brand_frame,
            height=150
        )
        self.common_bonus_frame.grid(row=5, column=1, sticky="ew", padx=10, pady=10)
        self.common_bonus_frame.rowconfigure(0, minsize=10)
        self.common_bonus_frame.rowconfigure((1), weight=1)
        self.common_bonus_frame.rowconfigure(2, minsize=10)

        self.common_bonus_frame.columnconfigure(0, minsize=10)
        self.common_bonus_frame.columnconfigure((1,2,3), weight=1)
        self.common_bonus_frame.columnconfigure(4, minsize=10)

        self.other_stuffs_frame = customtkinter.CTkFrame(
            master=self.right_frame
        ) 
        self.other_stuffs_frame.grid(
            row=1, column=4,
            columnspan=4,
            sticky="nsew",
            padx=10, pady=10
        )

        self.other_stuffs_frame.rowconfigure(0, minsize=10)
        self.other_stuffs_frame.rowconfigure((1,2,3), weight=1)
        self.other_stuffs_frame.rowconfigure(7, minsize=10)

        self.other_stuffs_frame.columnconfigure(0, minsize=10)
        self.other_stuffs_frame.columnconfigure((1,2), weight=1)
        self.other_stuffs_frame.columnconfigure(3, minsize=10)

        self.other_frame_1 = customtkinter.CTkFrame(
            master=self.other_stuffs_frame,
            height=150
        )
        self.other_frame_1.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.congigure_stuff_frame(self.other_frame_1)

        self.other_frame_2 = customtkinter.CTkFrame(
            master=self.other_stuffs_frame,
            height=150
        )
        self.other_frame_2.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
        self.congigure_stuff_frame(self.other_frame_2)

        self.other_frame_3 = customtkinter.CTkFrame(
            master=self.other_stuffs_frame,
            height=150
        )
        self.other_frame_3.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        self.congigure_stuff_frame(self.other_frame_3)

        self.other_frame_4 = customtkinter.CTkFrame(
            master=self.other_stuffs_frame,
            height=150
        )
        self.other_frame_4.grid(row=2, column=2, sticky="nsew", padx=10, pady=10)
        self.congigure_stuff_frame(self.other_frame_4)

        self.other_frame_5 = customtkinter.CTkFrame(
            master=self.other_stuffs_frame,
            height=150
        )
        self.other_frame_5.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)
        self.congigure_stuff_frame(self.other_frame_5)

        self.other_frame_6 = customtkinter.CTkFrame(
            master=self.other_stuffs_frame,
            height=150
        )
        self.other_frame_6.grid(row=3, column=2, sticky="nsew", padx=10, pady=10)
        self.congigure_stuff_frame(self.other_frame_6)

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
            if os.path.exists(path):
                head_gear_list.append(self.load_pil_image(path))
            else:
                head_gear_list.append(self.load_pil_image("bonus/Unknown.png")) 
        
        for bonus in player.clothing_gear_abilities:
            path = f"bonus/{bonus}.png"
            if os.path.exists(path):
                clothing_gear_list.append(self.load_pil_image(path))
            else:
                head_gear_list.append(self.load_pil_image("bonus/Unknown.png")) 

        for bonus in player.shoes_gear_abilities:
            path = f"bonus/{bonus}.png"
            if os.path.exists(path):
                shoes_gear_list.append(self.load_pil_image(path))
            else:
                head_gear_list.append(self.load_pil_image("bonus/Unknown.png")) 
        
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

        main_weapon_path     = f"assets/{player.main_weapon}.png" if os.path.exists(f"assets/{player.main_weapon}.png") else "bonus/Unknown.png"
        sub_weapon_path      = f"assets/{player.sub_weapon}.png" if os.path.exists(f"assets/{player.sub_weapon}.png") else "bonus/Unknown.png"
        special_weapon_path  = f"assets/{player.special_weapon}.png" if os.path.exists(f"assets/{player.special_weapon}.png") else "bonus/Unknown.png"

        main_weapon_image = self.load_pil_image(main_weapon_path)
        sub_weapon_image = self.load_pil_image(sub_weapon_path)
        special_weapon_image = self.load_pil_image(special_weapon_path)

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

    def display_result(self, game_data: Splatoon3Game, game_id):
        if game_data.players["myTeam"].win_or_lose == "LOSE" and game_data.players["myTeam"].score != "draw":
            score = f"Ennemy Team won ({game_data.players['myTeam'].score} - {game_data.players['ennemy'].score})" 

        elif game_data.players["myTeam"].win_or_lose == "WIN" and game_data.players["myTeam"].score != "draw":
            score = f"Your Team won ({game_data.players['myTeam'].score} - {game_data.players['ennemy'].score})"

        else:
            score = "DRAW"

        if game_data.last_X_power != 0:
            x_power = f"last X power : {game_data.last_X_power}"
        else:
            x_power = "\r"

        game_res = \
f"""
GAME n°{game_id}
{score}
{game_data.vs_rule} on {game_data.stage} 
{SpUtils.epoch_time(str(game_data.game_date))} ({game_data.duration})
{x_power}"""

        self.label_result = customtkinter.CTkLabel(
            master=self.game_frame,
            text=game_res,
            font=self.FONT_LABEL,
        )
        self.label_result.grid(row=1, column=2)

    def display_data(self, game_data: Splatoon3Game, game_id):
        my_team_frame = [self.my_team_p1, self.my_team_p2, self.my_team_p3, self.my_team_p4]
        ennemy_frame = [self.ennemy_p1, self.ennemy_p2, self.ennemy_p3, self.ennemy_p4]

        for i, player in enumerate(game_data.players["myTeam"].player_list):
            self.display_player(player, my_team_frame[i])

        for i, player in enumerate(game_data.players["ennemy"].player_list):
            self.display_player(player, ennemy_frame[i])


        self.display_result(game_data, game_id)

    def get_game_data(self, game_id):
        # try:
        pulled_data = s3s.main(
            bar=self.progress_bar, 
            game_index=game_id, 
            dict_key="VsHistoryDetailQuery"
        )

        return Splatoon3Game(pulled_data["data"]["vsHistoryDetail"])
        # except: # Connection Error
        #     self.label_connection_erreor = customtkinter.CTkLabel(
        #         master=self.game_frame,
        #         text="An error as ocurred, \nplease check your connection",
        #         font=self.FONT_LABEL
        #     )
        #     self.label_connection_erreor.grid(
        #         row=1, column=2
        #     )

    def load_data(self):
        if not self.check_configuration():
            self.invalid_config()

        else:

            label_loading = customtkinter.CTkLabel(
                master=self.game_frame,
                text="Loading data, it may take some time",
                font=self.FONT_LABEL
            )
            label_loading.grid(
                row=1, column=2, sticky="nsew",
                pady=30
            )

            self.progress_bar = customtkinter.CTkProgressBar(
                master=self.game_frame
            )
            self.progress_bar.grid(row=2, column=2, sticky="nsew", pady=20)
            self.progress_bar.set(0)

            self.update()

            game_data = self.get_game_data(self.game_id)

            label_loading.destroy()
            self.progress_bar.destroy()

            self.display_data(game_data, self.game_id)

    def previous_game(self):
        if not self.game_id >= 50:
            try:
                self.label_result.destroy()
            except:
                pass
            self.game_id += 1

            self.load_data()

        self.create_next_previous()
        
        self.update()

    def next_game(self):
        if not self.game_id <=1:
            try:
                self.label_result.destroy()
            except:
                pass
            self.game_id -= 1

            self.load_data()
            
        self.create_next_previous()

        self.update()

    def create_next_previous(self):
        try:
            self.next_game_button.destroy()
            self.previous_game_button.destroy()
        except:
            pass

        self.next_game_button = customtkinter.CTkButton(
            master=self.next_previous_frame,
            text="Load next game",
            font=self.FONT_BUTTON,
            command=self.next_game,
        )
        self.next_game_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.previous_game_button = customtkinter.CTkButton(
            master=self.next_previous_frame,
            text="Load previous game",
            font=self.FONT_BUTTON,
            command=self.previous_game,
        )
        self.previous_game_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        if self.game_id <= 1:
            self.next_game_button.configure(state="disabled")
        else:
            self.next_game_button.configure(state="enabled")

        if self.game_id >= 50:
            self.previous_game_button.configure(state="disabled")
        else:
            self.previous_game_button.configure(state="enabled")

        self.update()

    def last_game_callback(self):
        self.configure_frames_games()
        self.configure_player_frames()

        self.game_id = 0

        def change_game():
            try:
                self.label_result.destroy()
            except:
                pass

            game_id_temp = int(self.game_id_entry.get()) if self.game_id_entry.get() != "" else 0
            if game_id_temp <= 0:
                game_id_temp = 1

            elif game_id_temp >= 50:
                game_id_temp = 50

            self.game_id = game_id_temp

            self.create_next_previous()

            self.load_data()
   
        self.frame_chose_game = customtkinter.CTkFrame(
            master=self.right_frame,
            corner_radius=self.CORNER_RADIUS,
            # height=200
        )
        self.frame_chose_game.grid(row=1, column=1, pady=10)

        self.frame_chose_game.rowconfigure(0, minsize=10)
        self.frame_chose_game.rowconfigure((1,2), weight=1)
        self.frame_chose_game.rowconfigure(3, minsize=10)

        self.frame_chose_game.columnconfigure(0, minsize=10)
        self.frame_chose_game.columnconfigure((1), weight=1)
        self.frame_chose_game.columnconfigure(2, minsize=10)

        self.game_id_entry = customtkinter.CTkEntry(
            self.frame_chose_game,
            fg_color="#444444",
            font=self.FONT_LABEL,
            text_color="#FFFFFF",
            placeholder_text_color="#FFFFFF",
            placeholder_text="game : 1-50",
            
            justify = tkinter.CENTER
        )
        self.game_id_entry.grid(row=1, column=1, padx=10, pady=10)

        self.search_button = customtkinter.CTkButton(
            master=self.frame_chose_game,
            text="Confirm \nand load",
            font=self.FONT_BUTTON,
            command=change_game,
        )
        self.search_button.grid(row=2, column=1, padx=10, pady=10)
        

        self.next_previous_frame = customtkinter.CTkFrame(
            master=self.right_frame,
            corner_radius=self.CORNER_RADIUS,
            # height=200
        )
        self.next_previous_frame.grid(row=1, column=7, pady=10)

        self.next_previous_frame.rowconfigure(0, minsize=10)
        self.next_previous_frame.rowconfigure((1,2), weight=1)
        self.next_previous_frame.rowconfigure(3, minsize=10)

        self.next_previous_frame.columnconfigure(0, minsize=10)
        self.next_previous_frame.columnconfigure((1), weight=1)
        self.next_previous_frame.columnconfigure(2, minsize=10)

        self.create_next_previous()


        print("last game")

    def get_gear_path(self, gear_name):
        if os.path.exists(f"gears/headGear/{gear_name}.png"):
            return f"gears/headGear/{gear_name}.png"
        
        elif os.path.exists(f"gears/clothingGear/{gear_name}.png"):
            return f"gears/clothingGear/{gear_name}.png"
        
        elif os.path.exists(f"gears/shoesGear/{gear_name}.png"):
            return f"gears/shoesGear/{gear_name}.png"

    def display_daily_stuff(self, gear, i):
        gear_type = ["headGear", "clothingGear", "shoesGear"][i]
        name = gear["name"] 
        price = gear["price"]
        new_bonus = gear["ability"]
        gear_image = self.load_ctk_image(path=f"gears/{gear_type}/{name}.png", x=64, y=64)
        new_bonus_image = self.load_ctk_image(path=f"bonus/{new_bonus}.png", x=64, y=64)

        frame = self.daily_gear_frames[i]

        change_name = ""
        for word in name.split(" "):
            change_name += word + "\n"

        gear_image_label = customtkinter.CTkLabel(
            master=frame,
            text="",
            image=gear_image
        )
        gear_image_label.grid(row=1, column=1)
        new_bonus_image_label = customtkinter.CTkLabel(
            master=frame,
            text="",
            image=new_bonus_image
        )
        new_bonus_image_label.grid(row=1, column=2)
        name_label = customtkinter.CTkLabel(
            master=frame,
            text=f"{change_name}\n{price} $",
            font=self.FONT_LABEL
        )
        name_label.grid(row=1, column=3)
    
    def display_other_gears(self, gear, frame):
        name = gear["name"]
        gear_type = gear["type"]
        price = gear["price"]
        new_bonus = gear["ability"]
        end_time = gear["endTime"]
        gear_image = self.load_ctk_image(path=f"gears/{gear_type}/{name}.png", x=64, y=64)
        new_bonus_image = self.load_ctk_image(path=f"bonus/{new_bonus}.png", x=64, y=64)

        change_name = ""
        for word in name.split(" "):
            change_name += word + "\n"

        gear_image_label = customtkinter.CTkLabel(
            master=frame,
            text="",
            image=gear_image
        )
        gear_image_label.grid(row=1, column=1)
        new_bonus_image_label = customtkinter.CTkLabel(
            master=frame,
            text="",
            image=new_bonus_image
        )
        new_bonus_image_label.grid(row=1, column=2)
        name_label = customtkinter.CTkLabel(
            master=frame,
            text=f"{change_name}\n{price} $",
            font=self.FONT_LABEL
        )
        name_label.grid(row=1, column=3)

        end_time_label = customtkinter.CTkLabel(
            master=frame,
            text=f"Gear available until {end_time}",
            font=self.FONT_LABEL
        )
        end_time_label.grid(row=2, column=1, columnspan=3)

    def display_splatnet(self, splatnet_data: dict):
        brand_name = splatnet_data["dailyBrand"]["name"]
        common_bonus = splatnet_data["dailyBrand"]["common"]

        common_bonus_image = self.load_ctk_image(f"bonus/{common_bonus}.png", x=64, y=64)

        self.daily_drop_brand_label.configure(text=f"Brand : {brand_name}")

        common_bonus_image_label = customtkinter.CTkLabel(
            master=self.common_bonus_frame,
            text="",
            image=common_bonus_image,
        )
        common_bonus_image_label.grid(row=1, column=2)


        for i, gear in enumerate(splatnet_data["dailyDropGears"]):
            self.display_daily_stuff(gear, i)

        self.display_other_gears(splatnet_data["gearsOnSale"][0], self.other_frame_1)
        self.display_other_gears(splatnet_data["gearsOnSale"][1], self.other_frame_2)
        self.display_other_gears(splatnet_data["gearsOnSale"][2], self.other_frame_3)
        self.display_other_gears(splatnet_data["gearsOnSale"][3], self.other_frame_4)
        self.display_other_gears(splatnet_data["gearsOnSale"][4], self.other_frame_5)
        self.display_other_gears(splatnet_data["gearsOnSale"][5], self.other_frame_6)
       
    def load_splatnet_data(self):
        stuffs = parse_data.GesotownQuery(s3s.main(dict_key="GesotownQuery"))
        return stuffs

    def splatnet_callback(self):
        self.configure_frames_splatnet()
        self.daily_drop_brand_label = customtkinter.CTkLabel(
            master=self.daily_brand_frame,
            text="Brand : ",
            font=self.FONT_LABEL,
        )
        self.daily_drop_brand_label.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        common_bonus_label = customtkinter.CTkLabel(
            master=self.common_bonus_frame,
            text="Common Bonus : ",
            font=self.FONT_LABEL,
        )
        common_bonus_label.grid(row=1, column=1, sticky="nsew")

        loading_label = customtkinter.CTkLabel(
            master=self,
            text="Pulling data from Online\nmight take some time",
            font=self.FONT_TITLE,
            justify=tkinter.LEFT
        )
        loading_label.grid(row=0, column=1, columnspan=2)

        self.update()

        try:
            splatnet_data = self.load_splatnet_data()
            loading_label.destroy()

            self.update()

            self.display_splatnet(splatnet_data)
        except:
            loading_label.configure(text="Connection error, \nplease try again later")

    def display_best_power(self, stats):
        best_power_label = customtkinter.CTkLabel(
            master=self.best_power_frame,
            text="Best Power",
            font=self.FONT_LABEL
        )
        best_power_label.grid(row=1, column=2, columnspan=2)

        for i,mode in enumerate(stats["bestPowers"]):
            power = stats["bestPowers"][mode]["power"]
            date = stats["bestPowers"][mode]["date"]

            mode_label = customtkinter.CTkLabel(
                master=self.best_power_frame,
                text=mode,
                font=self.SMALL_FONT
            )
            mode_label.grid(row=2, column=i+1)
            power_label = customtkinter.CTkLabel(
                master=self.best_power_frame,
                text=round(power, 1),
                font=self.SMALL_FONT
            )
            power_label.grid(row=3, column=i+1)
            date_label = customtkinter.CTkLabel(
                master=self.best_power_frame,
                text=date[:10],
                font=self.SMALL_FONT
            )
            date_label.grid(row=4, column=i+1)

    def display_season(self, season_name: dict):
        translate_mode = {
            "Splat Zones" : "Ar",
            "Tower Control" : "Lf",
            "Rainmaker" : "Gl",
            "Clam Blitz" : "Cl",
        }

        stats = self.seasons_stats["seasons"][season_name]
        for i,mode in enumerate(list(stats.keys())):
            key = translate_mode[mode]
            power = stats[mode]["power"+key]
            rank = stats[mode]["rank"+key]

            mode_label = customtkinter.CTkLabel(
                master=self.current_power_frame,
                text=mode,
                font=self.SMALL_FONT
            )
            mode_label.grid(row=2, column=i+1)
            power_label = customtkinter.CTkLabel(
                master=self.current_power_frame,
                text=round(power, 1),
                font=self.SMALL_FONT
            )
            power_label.grid(row=3, column=i+1)
            rank_label = customtkinter.CTkLabel(
                master=self.current_power_frame,
                text=rank,
                font=self.SMALL_FONT
            )
            rank_label.grid(row=4, column=i+1)

    def display_my_stats(self, stats: dict):
        self.configure_my_stats_frames()

        self.display_best_power(stats)
        best_power_label = customtkinter.CTkLabel(
            master=self.current_power_frame,
            text="Chose a Season",
            font=self.FONT_LABEL
        )
        seasons_name = list(stats["seasons"].keys())

        self.seasons_stats = stats

        best_power_label.grid(row=1, column=1, columnspan=2)
        self.seasons_option = customtkinter.CTkOptionMenu(
            master=self.current_power_frame, 
            dynamic_resizing=True,
            values=seasons_name,
            command=self.callback_seasons
        )
        self.seasons_option.grid(row=1, column=3, columnspan=2)
        self.callback_seasons(seasons_name[0])

    def callback_seasons(self, arg):
        self.display_season(arg)

    def load_my_stats(self):
        stats =  parse_data.HistoryRecordQuery(s3s.main(dict_key="HistoryRecordQuery"))
        return stats

    def my_stats_callback(self):
        loading_label = customtkinter.CTkLabel(
            master=self,
            text="Pulling data from Online\nmight take some time",
            font=self.FONT_TITLE,
            justify=tkinter.LEFT
        )
        loading_label.grid(row=0, column=1, columnspan=2)

        self.update()

        try:
            stats = self.load_my_stats()
            loading_label.destroy()

            self.update()

            self.display_my_stats(stats)

        except:
            loading_label.configure(text="Connection error, \nplease try again later")


    def setup_callback(self):
        try:
            self.right_frame.destroy()
        except:
            pass

        self.setup_frame = customtkinter.CTkFrame(
            master=self,
        )
        self.setup_frame.grid(row=0, column=1, sticky="nsew")

        self.setup_frame.rowconfigure(0, minsize=10)
        self.setup_frame.rowconfigure((1,2,3,4), weight=1)
        self.setup_frame.rowconfigure(5, minsize=10)

        self.setup_frame.columnconfigure(0, minsize=10)
        self.setup_frame.columnconfigure(1, weight=1)
        self.setup_frame.columnconfigure(2, minsize=10)

        self.update()

        s3s.setup()

        url_login, auth_code = iksm.get_login_url(s3s.APP_USER_AGENT)

        self.label_url = customtkinter.CTkLabel(
            master=self.setup_frame,
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
            master=self.setup_frame,
            text="click to go on nintendo's website",
            font=self.FONT_TITLE,
            command=open_link
        )
        self.button_link.grid(
            row=2, column=1,
        )

        self.session_token_entry = customtkinter.CTkEntry(
            self.setup_frame,
            fg_color="#444444",
            font=self.FONT_TITLE,
            text_color="#FFFFFF",
            placeholder_text_color="#FFFFFF",
            placeholder_text="paste here",
            height=100
        )
        self.session_token_entry.grid(
            row=3, column=1,
            sticky="ew",
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
                    master=self.setup_frame,
                    text="configuration written succesfuly,\nnow getting your player id",
                    font=self.FONT_TITLE
                )
                label_ok.grid(
                    row=1, column=1,
                    sticky="nsew",
                    columnspan=3
                )
                self.update()

                temp_bar = customtkinter.CTkProgressBar(master=self)

                pid = s3s.main(bar=temp_bar, dict_key="VsHistoryDetailQuery")["data"]["vsHistoryDetail"]["player"]["id"]
                with open("pid.txt", "w") as file:
                    file.write(pid)

                label_ok.configure(text="Everything was done succesfuly \nYou can use the application")
            
            except Exception:
                
                label_error = customtkinter.CTkLabel(
                    master=self.setup_frame,
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
            master=self.setup_frame,
            text="confirm",
            font=self.FONT_TITLE,
            command=get_entry
        )
        self.button_validation.grid(
            row=4, column=1,
        )

        print("setup")


    def on_closing(self, event=0):
        print("bye")
        self.destroy()

if __name__ =="__main__":
    app = Application()
    app.mainloop()