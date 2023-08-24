import customtkinter
from tkinter.messagebox import askyesno
from tkinter import END
from PIL import Image, ImageTk
import os
from dotenv import load_dotenv
from threading import Thread
from ext.Bot import *
import datetime
load_dotenv()


class UIBotApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestionnaire du bot Twitch")
        self.geometry("900x650")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.iconbitmap("imgs/twitch_small_logo.ico")
        self.logo_image = customtkinter.CTkImage(Image.open("imgs/twitch_small_logo.png"), size=(26, 26))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=f"  Gestion de {os.environ['BOT_NICK']}", image=self.logo_image,
                                                                compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_title = customtkinter.CTkLabel(self.home_frame, text="Status du bot [HORS LIGNE]", fg_color="transparent",text_color="red")
        self.home_frame_title.grid(row=1, column=0, padx=20, pady=50)

        self.textbox = customtkinter.CTkTextbox(master=self.home_frame, width=400,height=400, corner_radius=0,border_spacing=15)
        self.textbox.grid(row=2, column=0, sticky="nsew")
        self.textbox.configure(state="disabled") 

        self.home_start_button = customtkinter.CTkButton(self.home_frame, corner_radius=0, height=40, border_spacing=10, text=f"Démarrer {os.environ['BOT_NICK']}",
                                                    fg_color="transparent", text_color=("green", "green"), hover_color=("gray70", "gray30"), anchor="center", command=self.StartStopBot)
        self.home_start_button.grid(row=3, column=0, sticky="ew", padx=20, pady=50)

        self.home_loading_bar = customtkinter.CTkProgressBar(self.home_frame, orientation="horizontal", mode="indeterminate")


        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Système", "Clair", "Sombre"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=50, sticky="s")

        self.bot_started = False

        self.select_frame_by_name("Home")

    def RunTwitchBot(self):
        self.TwitchBot.Run()

    def change_appearance_mode_event(self, new_appearance_mode):
        new_appearance_mode = new_appearance_mode.replace("Clair","Light")
        new_appearance_mode = new_appearance_mode.replace("Sombre","Dark")
        new_appearance_mode = new_appearance_mode.replace("Système","System")
        customtkinter.set_appearance_mode(new_appearance_mode)
    def home_button_event(self):
        self.select_frame_by_name("Home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "Home" else "transparent")
        if name == "Home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
    def StartStopBot(self):
        if(self.bot_started):
            # self.ToggleButtonLoading(True)
            self.TwitchBot.Stop()
            self.TwitchBot = None
            self.home_frame_title.configure(text="Status du bot [HORS LIGNE]",text_color="red")
            self.home_start_button.configure(text=f"Démarrer {os.environ['BOT_NICK']}",text_color="green")
        else:
            self.ToggleButtonLoading(True)
            self.TwitchBot = TwitchBot(self)
            self.TwitchBot.Run()
        self.bot_started = not self.bot_started
    
    def ToggleButtonLoading(self,State):
        if(State):
            self.home_start_button.grid_forget()
            self.home_loading_bar.grid(row=3, column=0, sticky="ew", padx=20, pady=50)
            self.home_loading_bar.start()
        else:
            self.home_loading_bar.grid_forget()
            self.home_start_button.grid(row=3, column=0, sticky="ew", padx=20, pady=50)

    def Log(self, DATA):
        self.textbox.configure(state="normal")
        current_content = self.textbox.get("1.0", "end-1c")  # Get the current content of the textbox
        new_content = f"{current_content}{datetime.datetime.now().time().strftime('[%H:%M:%S]')}    {DATA}\n\n"  # Append the new logs
        self.textbox.delete("1.0", "end")  # Clear the textbox
        self.textbox.insert("1.0", new_content)  # Insert the updated content
        self.textbox.see(END)
        self.textbox.configure(state="disabled")

if __name__ == "__main__":
    app = UIBotApp()
    app.mainloop()