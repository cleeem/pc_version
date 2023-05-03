import tkinter
import tkinter.messagebox
import customtkinter
import os


class Application(customtkinter.CTk):
    MIN_WIDTH = 1080
    MIN_HEIGHT = 720

    MAX_WIDTH = 1920
    MAX_HEIGHT = 1080

    CORNER_RADIUS = 15
    
    FONT_TITLE = ("Roboto Medium", 20) 
    FONT_BUTTON = ("Roboto Medium", 15) 
    FONT_LABEL = ("Roboto Medium", 15) 
    
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

        self.last_game_callback()
    
    def configure_frames(self):

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
            text_font=self.FONT_BUTTON,
            command=self.last_game_callback,
            height=self.BUTTON_HEIGHT,
        )
        self.last_game_button.grid(row=0, column=0, pady=10, padx=20)
        
        self.choose_game_button = customtkinter.CTkButton(
            master=self.left_frame,
            text=r"game {index}",
            text_font=self.FONT_BUTTON,
            command=self.choose_game_callback,
            height=self.BUTTON_HEIGHT,
        )
        self.choose_game_button.grid(row=1, column=0, pady=10, padx=20)


        self.setup_button = customtkinter.CTkButton(
            master=self.left_frame,
            text="setup",
            text_font=self.FONT_BUTTON,
            command=self.setup_callback,
            height=self.BUTTON_HEIGHT,
        )
        self.setup_button.grid(row=2, column=0, pady=10, padx=20)

        self.leave_button = customtkinter.CTkButton(
            master=self.left_frame,
            text="exit",
            text_font=self.FONT_BUTTON,
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

    

    def check_configuration(self):
        return os.path.exists("config.txt")
    
    def invalid_config(self):
        self.invalid_config_label = customtkinter.CTkLabel(
            master=self.game_frame,
            text="Config file was not found, \nplease go on the setup menu and follow the steps",
            text_font=self.FONT_TITLE,
            justify=tkinter.CENTER,
        )
        self.invalid_config_label.grid(row=2, column=2, padx=10, pady=10)

    def last_game_callback(self):
        self.configure_frames()

        if not self.check_configuration():
            self.invalid_config()
            
        
        else:
            ...
            #TODO afficher les infos de chaque team et de la game

        print("last game")

    def choose_game_callback(self):
        if not self.check_configuration():
            self.invalid_config()

        print("choose game")

    def setup_callback(self):
        print("setup")
        #TODO gérer le systeme avec les tokens 💀


    def on_closing(self, event=0):
        print("bye")
        self.destroy()

if __name__ =="__main__":
    app = Application()
    app.mainloop()