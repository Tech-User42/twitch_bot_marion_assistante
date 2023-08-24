import customtkinter
import os
from PIL import Image, ImageTk
from ext.quizz_manager import *

from tkinter.messagebox import askyesno

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.QuizzManager = QuizzManager()
        self.title("Gestionnaire de questions du bot Twitch")
        self.geometry("900x650")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.iconbitmap('imgs/twitch_small_logo.ico')
        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "twitch_small_logo.png")), size=(26, 26))
    
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Gestion des questions du bot Twitch", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Ajout de questions",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Suppression de questions",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Système", "Clair", "Sombre"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_title = customtkinter.CTkLabel(self.home_frame, text="Ajouter une question au Quizz", fg_color="transparent")
        self.home_frame_title.grid(row=1, column=0, padx=20, pady=50)

        self.home_frame_question = customtkinter.CTkEntry(self.home_frame, height=75, width=500, placeholder_text="La question qui sera posée.")
        self.home_frame_question.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.home_frame_question.bind('<KeyRelease>',command=self.CheckSaveButtonDisplaying)

        self.home_frame_response = customtkinter.CTkEntry(self.home_frame, height=75, width=500, placeholder_text="La réponse à la question.")
        self.home_frame_response.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        self.home_frame_response.bind('<KeyRelease>',command=self.CheckSaveButtonDisplaying)

        self.home_frame_save_button = customtkinter.CTkButton(self.home_frame, text="Enregistrer", command=self.TriggerAddQuestion, height=75, width=500)
        self.home_frame_save_button.grid(row=4, column=0, padx=20, pady=50, sticky="nsew")
        self.home_frame_save_button.configure(state="disabled")
        self.ReloadQuizzData()
        self.select_frame_by_name("Ajout de questions")

    def ReloadQuizzData(self):
        self.SelectedQuestionToDelete = -1
        self.QA_Delete_Buttons_List = []
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_rowconfigure(0, weight=1)
        self.second_frame.grid_columnconfigure(0, weight=1)
        self.scroll_frame = customtkinter.CTkScrollableFrame(self.second_frame,height=500)
        self.scroll_frame.grid(row=0, column=0, padx=20, pady=10,sticky="nsew")
        self.delete_question_button = customtkinter.CTkButton(self.second_frame, text="Supprimer", command=self.TriggerDeleteQuestion, height=75, width=300)
        self.delete_question_button.grid(row=1, column=0, padx=20, pady=10,sticky="ew")
        self.delete_question_button.configure(state="disabled")
        def delete_button_click(index):
            return lambda: self.SelectQuestionToDelete(index)
        for index, faq_item in enumerate(self.QuizzManager.QuizzData):
            question_button = customtkinter.CTkButton(self.scroll_frame, corner_radius=0, height=40,width=500, border_spacing=10, text=faq_item["Question"],
                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w",command=delete_button_click(int(index)))
            question_button.pack()
            self.QA_Delete_Buttons_List.append(question_button)    

    def SelectQuestionToDelete(self,id):
        self.delete_question_button.configure(state="enabled")
        button = self.QA_Delete_Buttons_List[id]
        for buttons in self.QA_Delete_Buttons_List:
            buttons.configure(fg_color=("transparent"))
        button.configure(fg_color=("gray75", "gray25"))
        self.SelectedQuestionToDelete = id        
        #QuizzManager.DeleteQuestion(id)


    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "Ajout de questions" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "Suppression de questions" else "transparent")

        if name == "Ajout de questions":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "Suppression de questions":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("Ajout de questions")

    def frame_2_button_event(self):
        self.select_frame_by_name("Suppression de questions")

    def TriggerAddQuestion(self):
        if askyesno(title='Confirmation',
                    message="Êtes vous sur de vouloir ajouter cette question ?"):
            self.QuizzManager.AddQuestion(self.home_frame_question.get(),self.home_frame_response.get())
            self.home_frame_question.delete(0,len(self.home_frame_question.get()))
            self.home_frame_response.delete(0,len(self.home_frame_response.get()))
            self.home_frame_question.focus()
            self.ReloadQuizzData()

    def TriggerDeleteQuestion(self):
        if askyesno(title='Confirmation',
                    message="Êtes vous sur de vouloir supprimer cette question ?"):
            self.QuizzManager.DeleteQuestion(self.SelectedQuestionToDelete)
            self.select_frame_by_name("Ajout de questions")
            self.ReloadQuizzData()
            self.select_frame_by_name("Suppression de questions")


    def change_appearance_mode_event(self, new_appearance_mode):
        new_appearance_mode = new_appearance_mode.replace("Clair","Light")
        new_appearance_mode = new_appearance_mode.replace("Sombre","Dark")
        new_appearance_mode = new_appearance_mode.replace("Système","System")
        customtkinter.set_appearance_mode(new_appearance_mode)

    def CheckSaveButtonDisplaying(self,event):
        if(self.home_frame_response.get() != "" and self.home_frame_question.get() != ""):
            self.home_frame_save_button.configure(state="enabled")
        else:
            self.home_frame_save_button.configure(state="disabled")

if __name__ == "__main__":
    app = App()
    app.mainloop()