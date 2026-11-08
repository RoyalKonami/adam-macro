import customtkinter as ctk

class App(ctk.CTk):
    menu_open = 1
    def __init__(self):
        menu().__init__()
        self.title("CustomTkinter Close Detection")
        self.geometry("400x300")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

 
 
 
 
 
    def on_closing(self):
        menu_open = 0
        print("Window close detected!")
        self.destroy() 

if __name__ == "__main__":
    app = App()
    app.mainloop()