import customtkinter

macro_state = 0

def start_macro():
    macro_state = 1
    print("Macro started")

def stop_macro():
    macro_state = 0
    print("Macro stopped")

class menu(customtkinter.CTk):
    menu_open = 1

    def __init__(self):
        super().__init__()
        self.title("Adams Macro Nuke")
        self.geometry("400x300")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        start_button = customtkinter.CTkButton(self, text="start", command=start_macro)
        start_button.grid(row=0, column=0, padx=20, pady=20)

        stop_button = customtkinter.CTkButton(self, text="stop", command=stop_macro)
        stop_button.grid(row=0, column=1, padx=20, pady=20)

    def on_closing(self):
        self.menu_open = 0
        print("Window close detected!")
        self.destroy()

if __name__ == "__main__":
    app = menu()
    app.mainloop()