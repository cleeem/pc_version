import tkinter
import tkinter.messagebox
import customtkinter
import os
import webbrowser
from PIL import Image

import dl_maps_weapons
import iksm
import s3s
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
    FONT_LABEL = ("Roboto Medium", 20) 
    
    GAME_COLOR_FRAME = "#555555"

    BUTTON_HEIGHT = 100
    WIDTH_PARAM_BUTTON = 500

    real_to_data = {
        'H-3 Nozzlenose' : 'Shooter_TripleMiddle',
        'L-3 Nozzlenose' : 'Shooter_TripleQuick',
        'L-3 Nozzlenose D' : 'Shooter_TripleQuick_01',
        'Aerospray MG' : 'Shooter_Blaze',
        'Aerospray RG' : 'Shooter_Blaze_01',
        'Splattershot Pro' : 'Shooter_Expert',
        'Forge Splattershot Pro' : 'Shooter_Expert_01',
        'Splattershot Jr.' : 'Shooter_First',
        'Custom Splattershot Jr.' : 'Shooter_First_01',
        'Squeezer' : 'Shooter_Flash',
        '.52 Gal' : 'Shooter_Gravity',
        '.96 Gal' : 'Shooter_Heavy',
        '.96 Gal Deco' : 'Shooter_Heavy_01',
        'Jet Squelcher' : 'Shooter_Long',
        'Custom Jet Squelcher' : 'Shooter_Long_01',
        'Splattershot' : 'Shooter_Normal',
        'Tentatek Splattershot' : 'Shooter_Normal_01',
        'Hero Shot Replica' : 'Shooter_Normal_H',
        'Splash-o-matic' : 'Shooter_Precision',
        'Neo Splash-o-matic' : 'Shooter_Precision_01',
        'Splattershot Nova' : 'Shooter_QuickLong',
        'N-ZAP 85' : 'Shooter_QuickMiddle',
        'N-ZAP 89' : 'Shooter_QuickMiddle_01',
        'Sploosh-o-matic' : 'Shooter_Short',
        'Neo Sploosh-o-matic' : 'Shooter_Short_01',
        'Splatana Stamper' : 'Saber_Normal',
        'Splatana Wiper' : 'Saber_Lite',
        'Rapid Blaster' : 'Blaster_Light',
        'Rapid Blaster Deco' : 'Blaster_Light_01',
        'Rapid Blaster Pro' : 'Blaster_LightLong',
        'Clash Blaster' : 'Blaster_LightShort',
        'Clash Blaster Neo' : 'Blaster_LightShort_01',
        'Range Blaster' : 'Blaster_Long',
        'Blaster' : 'Blaster_Middle',
        'Luna Blaster' : 'Blaster_Short',
        'Luna Blaster Neo' : 'Blaster_Short_01',
        'Inkbrush' : 'Brush_Mini',
        'Inkbrush Nouveau' : 'Brush_Mini_01',
        'Octobrush' : 'Brush_Normal',
        'Goo Tuber' : 'Charger_Keeper',
        'Classic Squiffer' : 'Charger_Light',
        'E-liter 4K' : 'Charger_Long',
        'E-liter 4K Scope' : 'Charger_LongScope',
        'Splat Charger' : 'Charger_Normal',
        'Z+F Splat Charger' : 'Charger_Normal_01',
        'Splatterscope' : 'Charger_NormalScope',
        'Z+F Splatterscope' : 'Charger_NormalScope_01',
        'Snipewriter 5H' : 'Charger_Pencil',
        'Bamboozler 14 Mk I' : 'Charger_Quick',
        'Dualie Squelchers' : 'Maneuver_Dual',
        'Splat Dualies' : 'Maneuver_Normal',
        'Dapple Dualies' : 'Maneuver_Short',
        'Dapple Dualies Nouveau' : 'Maneuver_Short_01',
        'Dark Tetra Dualies' : 'Maneuver_Stepper',
        'Glooga Dualies' : 'Maneuver_Gallon',
        'Carbon Roller' : 'Roller_Compact',
        'Carbon Roller Deco' : 'Roller_Compact_01',
        'Dynamo Roller' : 'Roller_Heavy',
        'Flingza Roller' : 'Roller_Hunter',
        'Splat Roller' : 'Roller_Normal',
        'Krak-On Splat Roller' : 'Roller_Normal_01',
        'Big Swig Roller' : 'Roller_Wide',
        'Tri-Stringer' : 'Stringer_Normal',
        'REEF-LUX 450' : 'Stringer_Short',
        'Undercover Brella' : 'Shelter_Compact',
        'Splat Brella' : 'Shelter_Normal',
        'Tenta Brella' : 'Shelter_Wide',
        'Bloblobber' : 'Slosher_Bathtub',
        'Tri-Slosher' : 'Slosher_Diffusion',
        'Tri-Slosher Nouveau' : 'Slosher_Diffusion_01',
        'Sloshing Machine' : 'Slosher_Launcher',
        'Slosher' : 'Slosher_Strong',
        'Slosher Deco' : 'Slosher_Strong_01',
        'Explosher' : 'Slosher_Washtub',
        'Mini Splatling' : 'Spinner_Quick',
        'Zink Mini Splatling' : 'Spinner_Quick_01',
        'Ballpoint Splatling' : 'Spinner_Downpour',
        'Hydra Splatling' : 'Spinner_Hyper',
        'Nautilus 47' : 'Spinner_Serein',
        'Heavy Splatling' : 'Spinner_Standard',
    }
    
    subs_specials_to_data = {
        'Killer Wail 5.1' : 'SpMicroLaser',
        'Tenta Missiles' : 'SpMultiMissile',
        'Booyah Bomb' : 'SpNiceBall',
        'Wave Breaker' : 'SpShockSonar',
        'Reefslider' : 'SpSkewer',
        'Zipcaster' : 'SpSuperHook',
        'Triple Inkstrike' : 'SpTripleTornado',
        'Trizooka' : 'SpUltraShot',
        'Ultra Stamp' : 'SpUltraStamp',
        'Ink Vac' : 'SpBlower',
        'Kraken Royale' : 'SpCastle',
        'Crab Tank' : 'SpChariot',
        'Tacticooler' : 'SpEnergyStand',
        'Super Chump' : 'SpFirework',
        'Big Bubbler' : 'SpGreatBarrier',
        'Ink Storm' : 'SpInkStorm',
        'Inkjet' : 'SpJetpack',
        'Squid Beakon' : 'Beacon',
        'Splat Bomb' : 'Bomb_Splash',
        'Suction Bomb' : 'Bomb_Suction',
        'Torpedo' : 'Bomb_Torpedo',
        'Angle Shooter' : 'LineMarker',
        'Splash Wall' : 'Shield',
        'Sprinkler' : 'Sprinkler',
        'Ink Mine' : 'Trap',
        'Curling Bomb' : 'Bomb_Curling',
        'Fizzy Bomb' : 'Bomb_Fizzy',
        'Burst Bomb' : 'Bomb_Quick',
        'Autobomb' : 'Bomb_Robot',
        'Toxic Mist' : 'PoisonMist',
        'Point Sensor' : 'PointSensor',
    }


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
        new_height = 0
        for img in images:
            new_height += img.height

        new_image = Image.new('RGB', (images[0].width, new_height), color="#FFFFFF")

        temp_height=0
        for img in images:
            new_image.paste(img, (0, temp_height))
            temp_height += img.height
        return new_image
    
    def get_concat_h(self, images: list):
        new_width = 0
        for img in images:
            new_width += img.width

        new_image = Image.new('RGB', (new_width, images[0].height), color="#FFFFFF")

        temp_width=0
        for img in images:
            new_image.paste(img, (temp_width, 0))
            temp_width += img.width
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

        self.update_assets_button = customtkinter.CTkButton(
            master=self.left_frame,
            text="update assets",
            font=self.FONT_BUTTON,
            command=self.callback_update_assets,
            height=self.BUTTON_HEIGHT,
        )
        self.update_assets_button.grid(row=3, column=0, pady=10, padx=20)

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
            padx=10, pady=10,
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
        self.game_frame.rowconfigure((1,2,3), weight=1)
        self.game_frame.rowconfigure(4, minsize=10)

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

    def load_ctk_image(self, path, x=25, y=25):
        """ load rectangular image with path relative to PATH """
        return customtkinter.CTkImage(Image.open(os.path.join(path)), size=(x, y))

    def load_pil_image(self, path):
        return Image.open(path).convert("RGBA").resize((64,64), Image.ANTIALIAS)

    def convert_image(self, img, x=128, y=128):
        return customtkinter.CTkImage(img, size=(x, y))

    def get_player_stuff(self, player: Splatoon3Player):

        head_gear_list = []
        clothing_gear_list = []
        shoes_gear_list = []

        for bonus in player.head_gear_abilities:
            bonus = bonus.replace(" ", "_")
            path = f"bonus/{bonus}.png"
            head_gear_list.append(self.load_pil_image(path)) 
        
        for bonus in player.clothing_gear_abilities:
            bonus = bonus.replace(" ", "_")
            path = f"bonus/{bonus}.png"
            clothing_gear_list.append(self.load_pil_image(path)) 

        for bonus in player.shoes_gear_abilities:
            bonus = bonus.replace(" ", "_")
            path = f"bonus/{bonus}.png"
            shoes_gear_list.append(self.load_pil_image(path)) 
        
        head = self.get_concat_h(head_gear_list)
        clothing = self.get_concat_h(clothing_gear_list)
        shoes = self.get_concat_h(shoes_gear_list)

        total = self.get_concat_v([head, clothing, shoes])

        return total

    def display_player(self, player: Splatoon3Player, frame):

        player_text = f"{player.name} \n{player.kill_w_assist}({player.assist_count}) / {player.death_count} / {player.special_count} \n{player.turf_point} pts"

        name_label = customtkinter.CTkLabel(
            master=frame,
            text=player_text,
            font=self.FONT_LABEL
        )
        name_label.grid(
            row=1, column=2,
            sticky="nsew"
        )

        main_weapon     = self.real_to_data[player.main_weapon]
        sub_weapon      = self.subs_specials_to_data[player.sub_weapon]
        special_weapon  = self.subs_specials_to_data[player.special_weapon]

        main_weapon_image = self.load_pil_image(f"assets/{main_weapon}.png")
        sub_weapon_image = self.load_pil_image(f"assets/{sub_weapon}.png")
        special_weapon_image = self.load_pil_image(f"assets/{special_weapon}.png")

        weapons = self.get_concat_h([main_weapon_image, sub_weapon_image, special_weapon_image])
        weapons.show()

        image_stuff = self.get_player_stuff(player)

        label_stuff = customtkinter.CTkLabel(
            master=frame,
            text="",
            image=self.convert_image(image_stuff, x=120, y=90)
        )
        label_stuff.grid(row=3, column=2)

    def display_data(self, game_data: Splatoon3Game):
        self.display_player(game_data.players["myTeam"].player_list[0], self.my_team_p1)
        self.display_player(game_data.players["myTeam"].player_list[1], self.my_team_p2)
        self.display_player(game_data.players["myTeam"].player_list[2], self.my_team_p3)
        self.display_player(game_data.players["myTeam"].player_list[3], self.my_team_p4)

        self.display_player(game_data.players["ennemy"].player_list[0], self.ennemy_p1)
        self.display_player(game_data.players["ennemy"].player_list[1], self.ennemy_p2)
        self.display_player(game_data.players["ennemy"].player_list[2], self.ennemy_p3)
        self.display_player(game_data.players["ennemy"].player_list[3], self.ennemy_p4)


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

            game_data = Splatoon3Game(s3s.main())

            label_loading.destroy()

            self.display_data(game_data)



        print("last game")

    def choose_game_callback(self):
        self.configure_frames()

        if not self.check_configuration():
            self.invalid_config()

        print("choose game")

    def callback_update_assets(self):

        self.configure_frames()

        # labels
        self.label_weapons = customtkinter.CTkLabel(
            master=self.my_team_frame,
            text="main weapons",
            font=self.FONT_LABEL
        )
        self.label_weapons.grid(
            row=1, column=1,
            padx=10, pady=10,
            columnspan=2
        )

        self.label_subs_specials = customtkinter.CTkLabel(
            master=self.ennemy_team_frame,
            text="subs and specials",
            font=self.FONT_LABEL
        )
        self.label_subs_specials.grid(
            row=1, column=1,
            padx=10, pady=10,
            columnspan=2
        )

        # progress bars
        self.weapons_progressbar = customtkinter.CTkProgressBar(
            master=self.my_team_frame,
        )
        self.weapons_progressbar.grid(
            row=2, column=1, 
            sticky="ew", 
            padx=10, pady=10,
            columnspan=2
        )
        self.weapons_progressbar.set(0)
        self.weapons_progressbar.update()

        self.subs_specials_progressbar = customtkinter.CTkProgressBar(
            master=self.ennemy_team_frame,
        )
        self.subs_specials_progressbar.grid(
            row=2, column=1, 
            sticky="ew", 
            padx=10, pady=10,
            columnspan=2
        )
        self.subs_specials_progressbar.set(0)
        self.subs_specials_progressbar.update()

        try:
            dl_maps_weapons.data_parse_all_versions.setup()
            version = dl_maps_weapons.data_parse_all_versions.last_version

            dl_maps_weapons.update_weapons(
                barre=self.weapons_progressbar,
                label=self.label_weapons
            )

            dl_maps_weapons.update_subs_specials(
                barre=self.subs_specials_progressbar,
                label=self.label_subs_specials
            )

            final_text = f"all assets have been updated to version {version}"

        except: # ConnectionError | urllib3.exceptions.MaxRetryError | NewConnectionError
            final_text = f"Connection error, please check your internet connection"


        # label fin
        self.label_weapons = customtkinter.CTkLabel(
            master=self.game_frame,
            text=final_text,
            font=self.FONT_LABEL
        )
        self.label_weapons.grid(
            row=2, column=2,
            padx=10, pady=10,
        )

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
                    text="configuration written succesfuly",
                    font=self.FONT_TITLE
                )
                label_ok.grid(
                    row=1, column=1,
                    sticky="nsew",
                    columnspan=3
                )
            
            except:
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
        #TODO gérer le systeme avec les tokens 💀


    def on_closing(self, event=0):
        print("bye")
        self.destroy()

if __name__ =="__main__":
    app = Application()
    app.mainloop()