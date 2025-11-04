import customtkinter as ctk
import tkinter as tk
from PIL import Image

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class InicioSesión(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login Personalizado")
        self.geometry("800x600")
        self.min_width = 700
        self.min_height = 500
        self.minsize(self.min_width, self.min_height)

        self.original_bg_image = None
        self.ctk_bg_image = None
        try:
            self.original_bg_image = Image.open("fondo_degradado.png")
            resized_image = self.original_bg_image.resize((800, 600))
            self.ctk_bg_image = ctk.CTkImage(light_image=resized_image,dark_image=resized_image,size=(800, 600))
        except FileNotFoundError:
            print("fondo_degradado.png no encontrado.")

        self.background_label = ctk.CTkLabel(
            self,
            text="",
            image=self.ctk_bg_image if self.ctk_bg_image else None)

        if self.ctk_bg_image:
            self.background_label.pack(fill="both", expand=True)
        else:
            self.background_label.configure(fg_color="#301934")
            self.background_label.pack(fill="both", expand=True)

        self.bind("<Configure>", self.on_resize)


        self.ctk_logo_image = None
        try:
            logo_image = Image.open("doraemon.jpeg")
            self.ctk_logo_image = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(50, 30))
        except FileNotFoundError:
            print("doraemon.jpeg no encontrado.")

        self.company_name = ctk.CTkLabel(self,
            text="Doraemon",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white", justify="left")
        self.company_name.place(x=20, y=10)

        if self.ctk_logo_image:
            self.logo_label = ctk.CTkLabel(
                self,
                text="", image=self.ctk_logo_image, compound="center")
            self.logo_label.place(relx=1.0, x=-20, y=10, anchor=tk.NE)
        else:
            self.logo_label = ctk.CTkLabel(
                self, text="LOGO", font=ctk.CTkFont(size=14, weight="bold"), text_color="white")
            self.logo_label.place(relx=1.0, x=-20, y=10, anchor=tk.NE)

        self.login_frame = ctk.CTkFrame(
            self,
            width=350,
            height=350,
            corner_radius=15,
            fg_color="white",
            bg_color="transparent",
            border_width=0  )
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        #Login
        self.login_title = ctk.CTkLabel(
            self.login_frame, text="Inicio de Sesión", font=ctk.CTkFont(size=24, weight="bold"), text_color="#301934")
        self.login_title.pack(pady=(40, 30), padx=10)

        self.username_entry = ctk.CTkEntry(
            self.login_frame, placeholder_text="Usario", width=250, height=40,
            corner_radius=10, fg_color="#f0f0f0", text_color="black", border_width=0)
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            self.login_frame, placeholder_text="Contraseña", show="•", width=250, height=40,
            corner_radius=10, fg_color="#f0f0f0", text_color="black", border_width=0)
        self.password_entry.pack(pady=10)

        # Botón Ingresar
        self.login_button = ctk.CTkButton(
            self.login_frame, text="Ingresar", command=self.login_action,
            width=200, height=40, corner_radius=10,
            fg_color="#301934", hover_color="#4B0082"
        )
        self.login_button.pack(pady=(30, 40))

    def on_resize(self, event):
        if self.original_bg_image and event.widget == self:
            new_width = self.winfo_width()
            new_height = self.winfo_height()


            if new_width > 0 and new_height > 0:
                resized_image = self.original_bg_image.resize((new_width, new_height))
                self.ctk_bg_image_resized = ctk.CTkImage(light_image=resized_image,dark_image=resized_image,size=(new_width, new_height))
                self.background_label.configure(image=self.ctk_bg_image_resized)

    def login_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(f"Intento de Login: Usuario={username}, Contraseña={password}")


if __name__ == "__main__":
    app = InicioSesión()
    app.mainloop()