import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


COLOR_MORADO_OSCURO = "#301934"
CREDENCIALES_VALIDAS = {"admin": "contador"}


PATH_BG = "fondo_degradado.png"
PATH_LOGO = "doraemon.jpeg"
PATH_FROG = "doraemon.jpeg"


def create_default_image(width, height, color1, color2, text=""):
    image = Image.new("RGB", (width, height), color1)
    draw = ImageDraw.Draw(image)

    # Convertir a tuplas RGB
    def hex_to_rgb(hex_color):
        if isinstance(hex_color, str) and hex_color.startswith('#'):
            return tuple(int(hex_color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        return hex_color

    color1_rgb = hex_to_rgb(color1)
    color2_rgb = hex_to_rgb(color2)

    for i in range(height):
        ratio = i / height
        # Interpolación lineal entre los colores
        r = int(color1_rgb[0] * (1 - ratio) + color2_rgb[0] * ratio)
        g = int(color1_rgb[1] * (1 - ratio) + color2_rgb[1] * ratio)
        b = int(color1_rgb[2] * (1 - ratio) + color2_rgb[2] * ratio)
        draw.line([(0, i), (width, i)], fill=(r, g, b))

    if text:
        print(f"Creando imagen por defecto: {text}")

    return image


def load_pil_image(path, default_width=800, default_height=600):
    FALLBACK_COLOR_1 = "#2c2130"
    FALLBACK_COLOR_2 = "#4b0082"

    if not os.path.exists(path):
        print(f"[ADVERTENCIA] Archivo '{path}' no encontrado. Creando imagen por defecto.")
        print(f"Directorio actual: {os.getcwd()}")
        return create_default_image(
            default_width, default_height,
            FALLBACK_COLOR_1, FALLBACK_COLOR_2,
            f"Default_{os.path.basename(path)}")
    try:
        pil_img = Image.open(path)
        print(f"[ÉXITO] Archivo '{path}' cargado correctamente.")
        return pil_img
    except Exception as e:
        print(f"[ERROR] Falló al procesar '{path}': {e}. Usando imagen por defecto.")
        return create_default_image(
            default_width, default_height,
            FALLBACK_COLOR_1, FALLBACK_COLOR_2,
            f"Error_{os.path.basename(path)}")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación de Gestión")
        self.geometry("1000x700")
        self.minsize(700, 500)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Crear las páginas
        self.frames[LoginPage] = LoginPage(parent=container, controller=self)
        self.frames[DashboardPage] = DashboardPage(parent=container, controller=self)

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        """Muestra el frame (pantalla) solicitado."""
        frame = self.frames[cont]
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def authenticate_user(self, username, password):
        """Verifica las credenciales y navega."""
        if CREDENCIALES_VALIDAS.get(username) == password:
            self.show_frame(DashboardPage)
            return True
        return False

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Cargar imágenes
        self.original_bg_image = load_pil_image(PATH_BG, 1000, 700)
        self.original_logo_image = load_pil_image(PATH_LOGO, 50, 30)

        self.background_label = ctk.CTkLabel(self, text="")
        self.background_label.grid(row=0, column=0, sticky="nsew")

        self.setup_background()

        self._setup_header()
        self.login_frame = ctk.CTkFrame(
            self, width=350, height=350, corner_radius=15,
            fg_color="white", bg_color="transparent", border_width=0)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Login Título
        ctk.CTkLabel(self.login_frame, text="Inicio de Sesión",
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=COLOR_MORADO_OSCURO).pack(pady=(40, 30), padx=10)

        self.username_entry = ctk.CTkEntry(self.login_frame,placeholder_text="Usuario",width=250, height=40,corner_radius=10,fg_color="#f0f0f0",text_color="black",border_width=0)
        self.username_entry.pack(pady=10)
        self.username_entry.insert(0, "admin")

        self.password_entry = ctk.CTkEntry(self.login_frame,
                                           placeholder_text="Contraseña",
                                           show="•",
                                           width=250, height=40,
                                           corner_radius=10,
                                           fg_color="#f0f0f0",
                                           text_color="black",
                                           border_width=0)
        self.password_entry.pack(pady=10)
        self.password_entry.insert(0, "contador")
        # Botón Ingresar
        ctk.CTkButton(self.login_frame, text="Ingresar",
                      command=self.login_action,
                      width=200, height=40,
                      corner_radius=10,
                      fg_color=COLOR_MORADO_OSCURO,
                      hover_color="#4B0082").pack(pady=(30, 20))

        self.error_label = ctk.CTkLabel(self.login_frame, text="", text_color="red")
        self.error_label.pack()

        self.password_entry.bind("<Return>", lambda e: self.login_action())

    def setup_background(self):
        """Configura la imagen de fondo y el listener de redimensionamiento."""
        if self.original_bg_image:

            initial_width = self.winfo_width() if self.winfo_width() > 1 else 1000
            initial_height = self.winfo_height() if self.winfo_height() > 1 else 700

            self.ctk_bg_image = ctk.CTkImage(
                light_image=self.original_bg_image,
                dark_image=self.original_bg_image,
                size=(initial_width, initial_height))
            self.background_label.configure(image=self.ctk_bg_image)
        else:
            self.background_label.configure(fg_color=COLOR_MORADO_OSCURO)

        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        """Redimensiona la imagen de fondo cuando cambia el tamaño de la ventana."""
        if hasattr(self, 'original_bg_image') and self.original_bg_image:

            if event.width > 0 and event.height > 0:
                try:
                    resized_image = self.original_bg_image.resize((event.width, event.height))
                    self.ctk_bg_image.configure(light_image=resized_image,
                                                dark_image=resized_image,
                                                size=(event.width, event.height))
                except Exception as e:
                    print(f"Error al redimensionar fondo: {e}")

    def _setup_header(self):
        # Nombre de la empresa
        ctk.CTkLabel(self, text="Empres SK",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="white", bg_color="transparent").place(x=20, y=10)

        # Logo
        if self.original_logo_image:
            ctk_logo_image = ctk.CTkImage(
                light_image=self.original_logo_image,
                dark_image=self.original_logo_image,
                size=(50, 30)
            )
            logo_label = ctk.CTkLabel(self, text="", image=ctk_logo_image,
                                      compound="center", bg_color="transparent")
            logo_label.place(relx=1.0, x=-20, y=10, anchor=tk.NE)
        else:
            ctk.CTkLabel(self, text="LOGO",
                         font=ctk.CTkFont(size=14, weight="bold"),
                         text_color="white", bg_color="transparent").place(relx=1.0, x=-20, y=10, anchor=tk.NE)

    def login_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not self.controller.authenticate_user(username, password):
            self.error_label.configure(text="Usuario o contraseña incorrectos.")
        else:
            self.error_label.configure(text="")


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="white")
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Inicializar estado de los menús
        self.user_menu_open = False
        self.company_menu_open = False

        # --- Columna 0: Barra Lateral (Izquierda) ---
        self.sidebar_frame = ctk.CTkFrame(
            self, width=200, corner_radius=0, fg_color=COLOR_MORADO_OSCURO
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.sidebar_frame, text="☰ LOGOTIPO",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="white").grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.nav_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.nav_frame.grid(row=1, column=0, sticky="nwe", padx=0, pady=(0, 20))

        # El nav_frame usará 'pack' para que los botones y submenús fluyan
        ctk.CTkLabel(self.nav_frame, text="BIENVENIDO!",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="white").pack(pady=(20, 30), padx=10, anchor="w")


        self._setup_navigation()


        ctk.CTkButton(self.sidebar_frame, text="Cerrar Sesión",
                      command=lambda: controller.show_frame(LoginPage),
                      fg_color="red", hover_color="#8B0000").grid(row=2, column=0, sticky="s", padx=20, pady=20)

        self.main_content_frame = ctk.CTkFrame(self, fg_color="white")
        self.main_content_frame.grid(row=0, column=1, sticky="nsew")

        self.main_content_frame.grid_columnconfigure(0, weight=1)

        self._setup_main_content()

    def _create_nav_button(self, text, command):
        """Función auxiliar para crear botones de navegación con estilo uniforme."""
        return ctk.CTkButton(
            self.nav_frame, text=text,
            command=command,
            fg_color="transparent",
            hover_color="#4B0082",
            anchor="w", font=ctk.CTkFont(size=14, weight="bold"),
            height=40, corner_radius=0,
            text_color="white"
        )

    def _create_sub_menu(self, parent_frame, sub_item_text):
        return ctk.CTkButton(
            parent_frame, text=f"• {sub_item_text}",
            command=lambda val=sub_item_text: self.nav_action(val),
            fg_color="transparent", hover_color="#6A5ACD",
            anchor="w", font=ctk.CTkFont(size=12),
            height=30, corner_radius=0,
            text_color="white"
        )

    def _setup_navigation(self):
        # 1. Botones Principales
        self.btn_usuarios = self._create_nav_button("GESTIONAR USUARIOS ▾", lambda: self.toggle_menu('user'))
        self.btn_empresa = self._create_nav_button("GESTIONAR EMPRESA ▾", lambda: self.toggle_menu('company'))
        self.btn_ver = self._create_nav_button("VER EMPRESAS", lambda: self.nav_action("VER EMPRESAS"))

        # 2. Submenu Frame USUARIOS
        self.user_menu_frame = ctk.CTkFrame(self.nav_frame, fg_color="#4B0082", corner_radius=0)
        user_submenu_items = ["CREAR USUARIO", "MODIFICAR USUARIOS", "ELIMINAR USUARIOS"]
        for sub_item in user_submenu_items:
            self._create_sub_menu(self.user_menu_frame, sub_item).pack(fill="x", padx=(20, 0), pady=1)


        self.company_menu_frame = ctk.CTkFrame(self.nav_frame, fg_color="#4B0082", corner_radius=0)
        company_submenu_items = ["CREAR EMPRESA", "MODIFICAR INFORMACIÓN EMPRESA", "ELIMINAR EMPRESA"]
        for sub_item in company_submenu_items:
            self._create_sub_menu(self.company_menu_frame, sub_item).pack(fill="x", padx=(20, 0), pady=1)

        self.repack_navigation()

    def repack_navigation(self):
        """Reordena todos los elementos del nav_frame en función del estado de los menús."""

        for widget in self.nav_frame.winfo_children():

            if widget.winfo_class() != 'CTkLabel' or widget.cget('text') != "BIENVENIDO!":
                widget.pack_forget()

        self.btn_usuarios.pack(fill="x", padx=0, pady=0)
        if self.user_menu_open:
            self.user_menu_frame.pack(fill="x", padx=0, pady=0)

        self.btn_empresa.pack(fill="x", padx=0, pady=0)
        if self.company_menu_open:
            self.company_menu_frame.pack(fill="x", padx=0, pady=0)

        self.btn_ver.pack(fill="x", padx=0, pady=0)

    def toggle_menu(self, menu_type):
        """Muestra u oculta el submenú solicitado y cierra el otro."""


        if menu_type == 'user':
            self.user_menu_open = not self.user_menu_open
            if self.user_menu_open:
                # Si se abre, cerrar el otro
                self.company_menu_open = False
                self.btn_usuarios.configure(text="GESTIONAR USUARIOS ▴")
                self.btn_empresa.configure(text="GESTIONAR EMPRESA ▾")
            else:
                self.btn_usuarios.configure(text="GESTIONAR USUARIOS ▾")

        elif menu_type == 'company':
            self.company_menu_open = not self.company_menu_open
            if self.company_menu_open:

                self.user_menu_open = False
                self.btn_empresa.configure(text="GESTIONAR EMPRESA ▴")
                self.btn_usuarios.configure(text="GESTIONAR USUARIOS ▾")
            else:
                self.btn_empresa.configure(text="GESTIONAR EMPRESA ▾")


        self.repack_navigation()

        self.nav_action(self.btn_usuarios.cget("text") if menu_type == 'user' else self.btn_empresa.cget("text"))

    def _setup_main_content(self):

        FROG_SIZE = (200, 200)
        frog_image = load_pil_image(PATH_FROG, FROG_SIZE[0], FROG_SIZE[1])

        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        # Contenedor para centrar la imagen
        content_wrapper = ctk.CTkFrame(self.main_content_frame, fg_color="white", height=300,
                                       width=400)
        content_wrapper.grid(row=0, column=0, padx=20, pady=20)

        # Centrar el content_wrapper dentro del main_content_frame
        self.main_content_frame.grid_rowconfigure(0, weight=1)
        self.main_content_frame.grid_columnconfigure(0, weight=1)

        if frog_image:
            ctk_frog_image = ctk.CTkImage(light_image=frog_image, dark_image=frog_image, size=FROG_SIZE)
            image_label = ctk.CTkLabel(content_wrapper, text="", image=ctk_frog_image, fg_color="white")
            image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        else:
            ctk.CTkLabel(content_wrapper,
                         text="Área de Contenido Principal\n\nBienvenido al Dashboard",
                         text_color="black",
                         font=ctk.CTkFont(size=16, weight="bold")).place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def nav_action(self, action):
        """Maneja la acción de navegación (imprime por ahora)."""
        print(f"Navegando a: {action}")



if __name__ == "__main__":
    print(f"\n--- INICIO DE APLICACIÓN ---")
    print(f"Directorio de trabajo: {os.getcwd()}")

    app = App()
    app.mainloop()
