import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- CONFIGURACIÓN DE RUTAS Y COLORES ---
# Colores basados en el diseño de la imagen:
COLOR_MORADO_OSCURO = "#301934"  # Morado casi negro (Sidebar)
COLOR_FONDO_PRINCIPAL = "#4b0082"  # Morado oscuro (Fondo general y Hover)
COLOR_DEGRADADO_BASE = "#28074d"  # Fondo más oscuro para simular el degradado principal
COLOR_CAMPO_CLARO = "#9c79c9"  # Morado claro para campos de entrada (similar a #A38DD0)
COLOR_BOTON_REGRESAR = "#7D3C98"  # Color del botón Regresar
COLOR_FORM_FRAME = "#5800a3"  # Morado más claro para el frame del formulario
CREDENCIALES_VALIDAS = {"admin": "contador"}

# ATENCIÓN: Se asume que esta imagen existe en el mismo directorio
PATH_BG = "image_7365ba.jpg"
PATH_LOGO = "image_7365ba.jpg"
PATH_FROG = "image_7365ba.jpg"  # Imagen para el Dashboard


def create_default_image(width, height, color1, color2, text=""):
    """Crea una imagen de degradado de colores sólida como fallback."""
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
    """Carga una imagen o crea un degradado de fallback si el archivo no existe."""
    # Colores oscuros de fallback para el Login (simulando el degradado de la imagen)
    FALLBACK_COLOR_1 = COLOR_DEGRADADO_BASE
    FALLBACK_COLOR_2 = COLOR_FONDO_PRINCIPAL

    if not os.path.exists(path):
        print(f"[ADVERTENCIA] Archivo '{path}' no encontrado. Creando imagen por defecto.")
        print(f"Directorio actual: {os.getcwd()}")
        # Usar el degradado del usuario
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

        # Crear un contenedor que usará el color de fondo para la simulación del degradado
        container = ctk.CTkFrame(self, fg_color=COLOR_FONDO_PRINCIPAL)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Cargar imágenes de fondo para el LoginPage (ahora con el degradado correcto)
        self.original_bg_image = load_pil_image(PATH_BG, 1000, 700)
        self.original_logo_image = load_pil_image(PATH_LOGO, 50, 30)

        # Crear las páginas, pasando las imágenes necesarias
        self.frames[LoginPage] = LoginPage(parent=container, controller=self,
                                           bg_image=self.original_bg_image, logo_image=self.original_logo_image)
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
    def __init__(self, parent, controller, bg_image, logo_image):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.original_bg_image = bg_image
        self.original_logo_image = logo_image

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

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

        self.username_entry = ctk.CTkEntry(self.login_frame,
                                           placeholder_text="Usuario",
                                           width=250, height=40,
                                           corner_radius=10,
                                           fg_color="#f0f0f0",
                                           text_color="black",
                                           border_width=0)
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
            # Inicializa la imagen con el tamaño actual o por defecto
            initial_width = self.winfo_width() if self.winfo_width() > 1 else 1000
            initial_height = self.winfo_height() if self.winfo_height() > 1 else 700

            self.ctk_bg_image = ctk.CTkImage(
                light_image=self.original_bg_image,
                dark_image=self.original_bg_image,
                size=(initial_width, initial_height))
            self.background_label.configure(image=self.ctk_bg_image)
        else:
            self.background_label.configure(fg_color=COLOR_MORADO_OSCURO)

        # Asegura que el fondo se redimensione
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        """Redimensiona la imagen de fondo cuando cambia el tamaño de la ventana."""
        if hasattr(self, 'original_bg_image') and self.original_bg_image:
            # Solo redimensionar si el ancho/alto ha cambiado significativamente
            if event.width > 0 and event.height > 0:
                try:
                    # Usar el degradado personalizado para simular el fondo de la imagen
                    degraded_bg = create_default_image(
                        event.width, event.height,
                        COLOR_DEGRADADO_BASE, COLOR_FONDO_PRINCIPAL
                    )

                    self.ctk_bg_image = ctk.CTkImage(light_image=degraded_bg,
                                                     dark_image=degraded_bg,
                                                     size=(event.width, event.height))
                    self.background_label.configure(image=self.ctk_bg_image)

                except Exception as e:
                    print(f"Error al redimensionar fondo: {e}")

    def _setup_header(self):
        # Nombre de la empresa
        ctk.CTkLabel(self, text="Nombre empresa",
                     font=ctk.CTkFont(size=16, weight="normal"),
                     text_color="white", bg_color="transparent").place(x=20, y=10)

        if self.original_logo_image:
            pass

    def login_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not self.controller.authenticate_user(username, password):
            self.error_label.configure(text="Usuario o contraseña incorrectos.")
        else:
            self.error_label.configure(text="")



class CreateUserPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO_PRINCIPAL)  # Fondo del diseño (Morado oscuro)

        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 1. Contenedor principal centrado
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)

        # 2. Lado Izquierdo (Título, textos y Botón Regresar)
        left_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsw", padx=20, pady=20)
        left_frame.grid_rowconfigure(4, weight=1)  # El botón regresas estará en la fila 5

        # "Nombre empresa"
        ctk.CTkLabel(left_frame, text="Nombre empresa",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="white").grid(row=0, column=0, sticky="nw")

        # Título Grande
        ctk.CTkLabel(left_frame, text="Crear nuevo\nusuario",
                     font=ctk.CTkFont(size=48, weight="bold"), text_color="white",
                     justify="left").grid(row=1, column=0, sticky="nw", pady=(30, 20))

        # "texto"
        ctk.CTkLabel(left_frame, text="Ingrese infromación de usuario",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="white").grid(row=2, column=0, sticky="nw")

        ctk.CTkLabel(left_frame, text="—",
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="white",
                     justify="left").grid(row=3, column=0, sticky="nw", pady=5)

        # "wasssa"
        ctk.CTkLabel(left_frame, text=":D",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="white").grid(row=4, column=0, sticky="nw")

        # Botón Regresar
        ctk.CTkButton(left_frame, text="Regresar",
                      command=lambda: self.controller.show_default_dashboard(),
                      width=150, height=45, corner_radius=10,
                      fg_color=COLOR_BOTON_REGRESAR,
                      hover_color="#A948C9",  # Color del botón Regresar en hover
                      font=ctk.CTkFont(size=16, weight="normal"),
                      text_color="white").grid(row=5, column=0, sticky="sw", pady=(100, 0))

        # 3. Lado Derecho (Formulario de Usuario)
        right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nse", padx=20, pady=20)

        # El formulario estará en un sub-frame morado con esquinas muy redondeadas
        form_frame = ctk.CTkFrame(right_frame, corner_radius=30,
                                  fg_color=COLOR_FORM_FRAME, width=350)
        form_frame.pack(expand=False, fill="y", side="right")

        # Título del Formulario
        ctk.CTkLabel(form_frame, text="Usuario",
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="white").pack(pady=(40, 20), padx=40)

        # CAMPOS DE LA IMAGEN DE REFERENCIA:
        fields = ["NOMBRE_COMPLETO", "USUARIO", "CONTRASEÑA", "ROL", "CORREO", "TELEFONO", "FECHA DE NACIMIENTO"]

        for field in fields:
            # Etiqueta (Ejemplo del diseño: NOMBRE_COMPLETO)
            ctk.CTkLabel(form_frame, text=field.replace("_", " "),  # Reemplazar _ por espacio para mejor lectura
                         font=ctk.CTkFont(size=12, weight="normal"), text_color="white", anchor="w").pack(fill="x",
                                                                                                          padx=40,
                                                                                                          pady=(15, 0))

            # Campo de entrada
            if field == "FECHA DE NACIMIENTO":
                # Simulación de Dropdown/Combobox para Fecha
                entry = ctk.CTkEntry(form_frame, placeholder_text="Seleccionar fecha", height=40,
                                     corner_radius=10,
                                     fg_color=COLOR_CAMPO_CLARO,
                                     border_width=0,
                                     text_color="white")
                entry.pack(fill="x", padx=40)

                # Simular flecha de dropdown usando un label con el carácter unicode
                ctk.CTkLabel(entry, text="⌄", font=ctk.CTkFont(size=20, weight="bold"), text_color="white",
                             fg_color="transparent").place(relx=0.9, rely=0.5, anchor=tk.CENTER)
            else:
                entry = ctk.CTkEntry(form_frame, placeholder_text="", height=40,
                                     corner_radius=10,
                                     fg_color=COLOR_CAMPO_CLARO,
                                     border_width=0,
                                     text_color="white")
                entry.pack(fill="x", padx=40)

            # Placeholder/Ejemplo (Solo para el primer campo como en la imagen)
            if field == "NOMBRE_COMPLETO":
                entry.insert(0, "Francois Mercer")

        # Botón Crear Usuario (Color morado oscuro)
        ctk.CTkButton(form_frame, text="Crear\nusuario",
                      command=self.create_user_action,
                      width=180, height=60, corner_radius=15,
                      fg_color=COLOR_MORADO_OSCURO,
                      hover_color="#5D3FD3",  # Un color más claro para el hover
                      font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(30, 40))

    def create_user_action(self):
        # Lógica para crear el usuario
        print("Intentando crear nuevo usuario...")
        # Aquí iría la lógica de validación y guardado


# --- DashboardPage Modificada ---

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        # El dashboard usa fondo blanco/claro
        super().__init__(parent, fg_color="white")
        self.controller = controller

        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.grid(row=0, column=1, sticky="nsew")
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

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

        ctk.CTkLabel(self.nav_frame, text="BIENVENIDO!",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="white").pack(pady=(20, 30), padx=10, anchor="w")

        self._setup_navigation()

        # Botón Cerrar Sesión (Se pega al fondo de la barra lateral)
        ctk.CTkButton(self.sidebar_frame, text="Cerrar Sesión",
                      command=lambda: controller.show_frame(LoginPage),
                      fg_color="red", hover_color="#8B0000").grid(row=2, column=0, sticky="s", padx=20, pady=20)

        # --- Columna 1: Área de Contenido Principal (Derecha) ---
        self.current_content = None
        self.show_default_dashboard()

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
        """Función auxiliar para crear botones de submenú."""
        return ctk.CTkButton(
            parent_frame, text=f"• {sub_item_text}",
            command=lambda val=sub_item_text: self.nav_action(val),
            fg_color="transparent", hover_color="#6A5ACD",
            anchor="w", font=ctk.CTkFont(size=12),
            height=30, corner_radius=0,
            text_color="white"
        )

    def _setup_navigation(self):
        """Configura los botones de navegación y los menús desplegables."""
        # 1. Botones Principales
        self.btn_usuarios = self._create_nav_button("GESTIONAR USUARIOS ▾", lambda: self.toggle_menu('user'))
        self.btn_empresa = self._create_nav_button("GESTIONAR EMPRESA ▾", lambda: self.toggle_menu('company'))
        self.btn_ver = self._create_nav_button("VER EMPRESAS", lambda: self.nav_action("VER EMPRESAS"))

        # 2. Submenu Frame USUARIOS
        self.user_menu_frame = ctk.CTkFrame(self.nav_frame, fg_color="#4B0082", corner_radius=0)
        user_submenu_items = ["CREAR USUARIO", "MODIFICAR USUARIOS", "ELIMINAR USUARIOS"]
        for sub_item in user_submenu_items:
            self._create_sub_menu(self.user_menu_frame, sub_item).pack(fill="x", padx=(20, 0), pady=1)

        # 3. Submenu Frame EMPRESA
        self.company_menu_frame = ctk.CTkFrame(self.nav_frame, fg_color="#4B0082", corner_radius=0)
        company_submenu_items = ["CREAR EMPRESA", "MODIFICAR INFORMACIÓN EMPRESA", "ELIMINAR EMPRESA"]
        for sub_item in company_submenu_items:
            self._create_sub_menu(self.company_menu_frame, sub_item).pack(fill="x", padx=(20, 0), pady=1)

        # 4. Empaquetar los botones principales
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

    def show_content(self, content_frame_class):
        """Destruye el contenido actual y muestra la nueva página."""
        if self.current_content:
            self.current_content.destroy()

        if content_frame_class != DashboardPage:
            self.current_content = content_frame_class(self.content_container, self)
        else:
            self.current_content = ctk.CTkFrame(self.content_container, fg_color="transparent")

        self.current_content.grid(row=0, column=0, sticky="nsew")

    def show_default_dashboard(self):
        """Muestra la vista por defecto (la imagen de la rana o placeholder)."""

        if self.current_content:
            self.current_content.destroy()

        # Frame que contiene la rana (para heredar el estilo blanco/compacto)
        main_content_frame = ctk.CTkFrame(self.content_container, fg_color="white")
        main_content_frame.grid(row=0, column=0, sticky="nsew")
        main_content_frame.grid_columnconfigure(0, weight=1)
        main_content_frame.grid_rowconfigure(0, weight=1)

        self.current_content = main_content_frame  # Asignar el nuevo frame como contenido actual

        # Carga la imagen (Sigue siendo la imagen de Doraemon si PATH_FROG no existe)
        FROG_SIZE = (300, 150)  # TAMAÑO MODIFICADO: Más ancho (300) y menos largo (150)
        frog_image = load_pil_image(PATH_FROG, FROG_SIZE[0], FROG_SIZE[1])

        # Contenedor de la rana (más compacto)
        content_wrapper = ctk.CTkFrame(main_content_frame, fg_color="white",
                                       width=FROG_SIZE[0] + 40, height=FROG_SIZE[1] + 40)
        # Centrar el wrapper
        content_wrapper.grid(row=0, column=0, padx=20, pady=20)

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
        """Maneja la acción de navegación (imprime por ahora y cambia de pantalla)."""
        print(f"Navegando a: {action}")

        if action == "CREAR USUARIO":
            self.show_content(CreateUserPage)
        else:
            self.show_default_dashboard()


if __name__ == "__main__":
    print(f"\n--- INICIO DE APLICACIÓN ---")
    print(f"Directorio de trabajo: {os.getcwd()}")

    app = App()
    app.mainloop()
