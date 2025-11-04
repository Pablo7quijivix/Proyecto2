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
COLOR_BOTON_EDITAR = "#E0BBE4"  # Botón Editar (Morado claro del ejemplo)
COLOR_BOTON_ELIMINAR = "#DC3545"  # Rojo para el botón Eliminar
COLOR_TEXTO_TABLA = "#301934"  # Texto oscuro para las celdas claras de la tabla
COLOR_FILA_OSCURA = "#4b0082"  # Fondo de las filas oscuras
COLOR_FILA_CLARA = "#9c79c9"  # Fondo de las filas claras (similar al input)
COLOR_CABECERA = "#301934"  # Color de la cabecera de la tabla
COLOR_FONDO_LISTA = "#eeeeee"  # Color de fondo de la lista de empresas
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

        # Configuración del Fondo (usando el degradado de fallback)
        self.background_label = ctk.CTkLabel(self, text="")
        self.background_label.grid(row=0, column=0, sticky="nsew")

        self.setup_background()

        self._setup_header()

        # El frame de login ahora debe ser blanco para contrastar con el fondo
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

        # Logo (oculto en el Login de la imagen de referencia)
        if self.original_logo_image:
            pass  # No mostrar logo en la esquina superior derecha del Login

    def login_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not self.controller.authenticate_user(username, password):
            self.error_label.configure(text="Usuario o contraseña incorrectos.")
        else:
            self.error_label.configure(text="")


# --- PANTALLA: CreateUserPage ---

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
        left_frame.grid_rowconfigure(5, weight=1)  # Ajustar el peso para el botón Regresar

        # "Nombre empresa"
        ctk.CTkLabel(left_frame, text="Nombre empresa",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="white").grid(row=0, column=0, sticky="nw")

        # Título Grande
        ctk.CTkLabel(left_frame, text="Crear nuevo\nusuario",
                     font=ctk.CTkFont(size=48, weight="bold"), text_color="white",
                     justify="left").grid(row=1, column=0, sticky="nw", pady=(30, 20))

        # "olaa"
        ctk.CTkLabel(left_frame, text="olaa",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="white").grid(row=2, column=0, sticky="nw")

        # Separador (simulado con un CTkLabel con guiones)
        ctk.CTkLabel(left_frame, text="—",
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="white",
                     justify="left").grid(row=3, column=0, sticky="nw", pady=5)

        # "wasssa"
        ctk.CTkLabel(left_frame, text="wasssa",
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


# --- PANTALLA: CreateCompanyPage ---

class CreateCompanyPage(ctk.CTkFrame):
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
        left_frame.grid_rowconfigure(5, weight=1)  # Ajustar el peso para el botón Regresar

        # "Nombre empresa"
        ctk.CTkLabel(left_frame, text="Nombre empresa",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="white").grid(row=0, column=0, sticky="nw")

        # Título Grande
        ctk.CTkLabel(left_frame, text="Crear nueva\nempresa",  # Texto actualizado
                     font=ctk.CTkFont(size=48, weight="bold"), text_color="white",
                     justify="left").grid(row=1, column=0, sticky="nw", pady=(30, 20))

        # "olaa"
        ctk.CTkLabel(left_frame, text="olaa",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="white").grid(row=2, column=0, sticky="nw")

        # Separador (simulado con un CTkLabel con guiones)
        ctk.CTkLabel(left_frame, text="—",
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="white",
                     justify="left").grid(row=3, column=0, sticky="nw", pady=5)

        # "wasssa"
        ctk.CTkLabel(left_frame, text="wasssa",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="white").grid(row=4, column=0, sticky="nw")

        # Botón Regresar
        ctk.CTkButton(left_frame, text="Regresar",
                      command=lambda: self.controller.show_default_dashboard(),
                      width=150, height=45, corner_radius=10,
                      fg_color=COLOR_BOTON_REGRESAR,
                      hover_color="#A948C9",  # Color del botón Regresar en hover
                      font=ctk.CTkFont(size=16, weight="normal"),
                      text_color="white").grid(row=5, column=0, sticky="sw", pady=(100, 0))

        # 3. Lado Derecho (Formulario de Empresa)
        right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nse", padx=20, pady=20)

        # El formulario estará en un sub-frame morado con esquinas muy redondeadas
        # Usamos CTkScrollableFrame ya que hay muchos campos para evitar que se salga de pantalla
        form_frame = ctk.CTkScrollableFrame(right_frame, corner_radius=30,
                                            fg_color=COLOR_FORM_FRAME, width=350)
        form_frame.pack(expand=False, fill="y", side="right")

        # Título del Formulario
        ctk.CTkLabel(form_frame, text="Empresa",  # Título actualizado
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="white").pack(pady=(40, 20), padx=40)

        # CAMPOS DE LA IMAGEN DE REFERENCIA (Crear nueva empresa):
        fields = ["NIT", "NOMBRE JEFE", "TELEFONO", "CORREO", "DIRECCIÓN", "DPI", "FECHA DE NACIMIENTO",
                  "NOMBRE EMPRESA"]

        for field in fields:
            # Etiqueta
            ctk.CTkLabel(form_frame, text=field,
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
            if field == "NIT":
                entry.insert(0, "NIT de Empresa SA")  # Placeholder de la imagen

        # Botón Crear Empresa (Color morado oscuro)
        ctk.CTkButton(form_frame, text="CREAR\nEMPRESA",  # Texto actualizado
                      command=self.create_company_action,
                      width=180, height=60, corner_radius=15,
                      fg_color=COLOR_MORADO_OSCURO,
                      hover_color="#5D3FD3",  # Un color más claro para el hover
                      font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(30, 40))

    def create_company_action(self):
        # Lógica para crear la empresa
        print("Intentando crear nueva empresa...")
        # Aquí iría la lógica de validación y guardado


# --- PANTALLA BASE PARA TABLAS: TableBasePage ---

class TableBasePage(ctk.CTkFrame):
    def __init__(self, parent, controller, action_text, action_color, action_hover_color, action_command,
                 data_type="user"):
        super().__init__(parent, fg_color=COLOR_FONDO_PRINCIPAL)  # Fondo degradado oscuro

        self.controller = controller
        self.action_text = action_text
        self.action_color = action_color
        self.action_hover_color = action_hover_color
        self.action_command = action_command
        self.data_type = data_type

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Datos de ejemplo para Usuarios
        self.user_data = [
            {"ID": "DPI1", "Nombre": "HOLAAA", "Teléfono": "12345678", "ROL": "ENCARGADO CONTA DE BIMBO"},
            {"ID": "DPI2", "Nombre": "Maria Garcia", "Teléfono": "87654321", "ROL": "ADMINISTRADOR"},
            {"ID": "DPI3", "Nombre": "Pedro Lopez", "Teléfono": "11223344", "ROL": "CONTADOR"},
            {"ID": "DPI4", "Nombre": "Ana Martinez", "Teléfono": "44332211", "ROL": "GESTOR DE VENTAS"},
            {"ID": "DPI5", "Nombre": "Juan Pérez", "Teléfono": "55551234", "ROL": "OPERADOR"},
        ]

        # Datos de ejemplo para Empresas (Mismos datos usados en ViewCompaniesPage)
        self.company_data = [
            {"ID": "NIT1", "Nombre": "Tecno Soluciones SA", "Teléfono": "99887766", "DIRECCIÓN": "Av. Principal 123"},
            {"ID": "NIT2", "Nombre": "Inversiones del Sur", "Teléfono": "22334455", "DIRECCIÓN": "Calle Falsa 456"},
            {"ID": "NIT3", "Nombre": "Comercializadora Zeta", "Teléfono": "12121212", "DIRECCIÓN": "Zona Industrial 7"},
        ]

        self._setup_top_bar()
        self._setup_table()

    def _get_data(self):
        """Retorna los datos apropiados (usuarios o empresas)."""
        if self.data_type == "company":
            return self.company_data
        return self.user_data

    def _get_columns(self):
        """Retorna las columnas apropiadas para el tipo de dato."""
        if self.data_type == "company":
            return ["NIT", "Nombre", "Teléfono", "DIRECCIÓN", "Acción"]
        return ["DPI", "Nombre", "Teléfono", "ROL", "Acción"]

    def _setup_top_bar(self):
        """Configura la barra superior con Ordenar, Buscar y Volver."""
        top_bar_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        top_bar_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(40, 20))
        top_bar_frame.grid_columnconfigure(1, weight=1)  # Columna del buscador se expande

        # Botón Ordenar (Forma de pastilla, borde blanco)
        ctk.CTkButton(top_bar_frame, text="Ordenar",
                      width=100, height=45, corner_radius=25,
                      fg_color="transparent", border_color="white", border_width=2,
                      hover_color="#6A5ACD", text_color="white",
                      font=ctk.CTkFont(size=16, weight="bold")
                      ).grid(row=0, column=0, padx=(0, 15), sticky="w")

        # Barra de Búsqueda (Forma de pastilla, fondo blanco)
        ctk.CTkEntry(top_bar_frame, placeholder_text="Buscar",
                     width=500, height=50, corner_radius=25,
                     fg_color="white", text_color="black",
                     font=ctk.CTkFont(size=16)
                     ).grid(row=0, column=1, sticky="ew", padx=15)

        # Botón Volver (Forma de pastilla, fondo blanco)
        ctk.CTkButton(top_bar_frame, text="Volver",
                      command=lambda: self.controller.show_default_dashboard(),
                      width=100, height=45, corner_radius=25,
                      fg_color="white", hover_color="#cccccc", text_color="black",
                      font=ctk.CTkFont(size=16, weight="bold")
                      ).grid(row=0, column=2, padx=(15, 0), sticky="e")

    def _setup_table(self):
        """Configura la tabla con los datos (usuarios o empresas)."""
        table_container = ctk.CTkScrollableFrame(self, fg_color="transparent", label_text=None)
        table_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        data = self._get_data()
        cols = self._get_columns()

        # Configuración de las columnas de la tabla (ajustar pesos)
        for i in range(len(cols)):
            # Distribuir el espacio de manera uniforme
            table_container.grid_columnconfigure(i, weight=1 if i < len(cols) - 1 else 1)

            # --- Cabecera de la Tabla ---
        header_font = ctk.CTkFont(size=16, weight="bold")
        for i, col_name in enumerate(cols):
            # Usar color de cabecera oscuro
            header_cell = ctk.CTkLabel(table_container, text=col_name.upper(),
                                       fg_color=COLOR_CABECERA, text_color="white",
                                       font=header_font, height=50, corner_radius=0)
            header_cell.grid(row=0, column=i, sticky="nsew", padx=(1 if i > 0 else 0, 1), pady=(0, 1))

        # --- Filas de Datos ---
        row_font = ctk.CTkFont(size=14)

        # Determinar las claves para extraer los valores de cada fila
        # Excluimos "Acción" que es el botón, e "ID" que es la clave interna
        display_keys = [c for c in cols if c not in ["Acción", "DPI", "NIT"]]

        # La primera columna siempre es el ID visible (DPI o NIT)
        id_key = "DPI" if self.data_type == "user" else "NIT"

        for r, item in enumerate(data):
            row_index = r + 1
            # Alternar colores de fondo (claro/oscuro)
            bg_color = COLOR_FILA_CLARA if r % 2 == 0 else COLOR_FILA_OSCURA
            text_color = COLOR_TEXTO_TABLA if r % 2 == 0 else "white"

            # 1. Columna ID (DPI o NIT)
            ctk.CTkLabel(table_container, text=item["ID"],
                         fg_color=bg_color, text_color=text_color,
                         font=row_font, height=60, corner_radius=0,
                         anchor="w", padx=15).grid(row=row_index, column=0, sticky="nsew", padx=(1, 1), pady=(1, 1))

            # 2. Las otras columnas de datos
            data_values = [item.get(key) for key in display_keys]

            # Recorrer las columnas de datos a partir de la segunda columna (índice 1)
            for c, value in enumerate(data_values):
                col_idx = c + 1
                cell = ctk.CTkLabel(table_container, text=str(value),
                                    fg_color=bg_color, text_color=text_color,
                                    font=row_font, height=60, corner_radius=0,
                                    anchor="w", padx=15)
                cell.grid(row=row_index, column=col_idx, sticky="nsew", padx=(1, 1), pady=(1, 1))

            # 3. Columna de Acción (Botón) - Última columna
            action_col_idx = len(cols) - 1
            edit_button_frame = ctk.CTkFrame(table_container, fg_color=bg_color, corner_radius=0)
            edit_button_frame.grid(row=row_index, column=action_col_idx, sticky="nsew", padx=(1, 1), pady=(1, 1))
            edit_button_frame.grid_columnconfigure(0, weight=1)

            ctk.CTkButton(edit_button_frame, text=self.action_text,
                          command=lambda u=item: self.action_command(u),
                          width=80, height=35, corner_radius=10,
                          fg_color=self.action_color,
                          hover_color=self.action_hover_color,
                          text_color=COLOR_TEXTO_TABLA if bg_color == COLOR_BOTON_EDITAR else "white",
                          # Ajuste de color de texto
                          font=ctk.CTkFont(size=14, weight="bold")
                          ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Centrar el botón


# --- PANTALLA: ModifyUsersPage (Hereda de TableBasePage) ---

class ModifyUsersPage(TableBasePage):
    def __init__(self, parent, controller):
        super().__init__(
            parent,
            controller,
            action_text="EditaR",
            action_color=COLOR_BOTON_EDITAR,
            action_hover_color="#CBAACB",
            action_command=self.edit_user_action,
            data_type="user"
        )

    def edit_user_action(self, user):
        """Simula la acción de editar un usuario."""
        print(f"Editando usuario: ID={user['ID']}, Nombre={user['Nombre']}")
        # Aquí se implementaría la navegación a la página de edición


# --- PANTALLA: DeleteUsersPage (Hereda de TableBasePage) ---

class DeleteUsersPage(TableBasePage):
    def __init__(self, parent, controller):
        super().__init__(
            parent,
            controller,
            action_text="EliminaR",  # Texto de acción cambiado
            action_color=COLOR_BOTON_ELIMINAR,  # Color de acción cambiado a rojo
            action_hover_color="#B22222",  # Hover más oscuro para el rojo
            action_command=self.delete_user_action,
            data_type="user"
        )

    def delete_user_action(self, user):
        """Simula la acción de eliminar un usuario."""
        # Se podría pedir una confirmación aquí
        print(f"!!! ELIMINANDO USUARIO: ID={user['ID']}, Nombre={user['Nombre']}")
        # Lógica de eliminación...


# --- PANTALLA: ModifyCompanyPage (Hereda de TableBasePage) ---

class ModifyCompanyPage(TableBasePage):
    def __init__(self, parent, controller):
        super().__init__(
            parent,
            controller,
            action_text="EditaR",
            action_color=COLOR_BOTON_EDITAR,
            action_hover_color="#CBAACB",
            action_command=self.edit_company_action,
            data_type="company"  # Especifica que debe usar los datos de empresa
        )

    def edit_company_action(self, company):
        """Simula la acción de editar una empresa."""
        print(f"Editando empresa: ID={company['ID']}, Nombre={company['Nombre']}")
        # Aquí se implementaría la navegación a la página de edición de empresa


# --- PANTALLA: DeleteCompanyPage (Hereda de TableBasePage) ---

class DeleteCompanyPage(TableBasePage):
    def __init__(self, parent, controller):
        super().__init__(
            parent,
            controller,
            action_text="EliminaR",
            action_color=COLOR_BOTON_ELIMINAR,
            action_hover_color="#B22222",
            action_command=self.delete_company_action,
            data_type="company"  # Especifica que debe usar los datos de empresa
        )

    def delete_company_action(self, company):
        """Simula la acción de eliminar una empresa."""
        # Se podría pedir una confirmación aquí
        print(f"!!! ELIMINANDO EMPRESA: ID={company['ID']}, Nombre={company['Nombre']}")
        # Lógica de eliminación...


# --- NUEVA PANTALLA: ViewCompaniesPage (Lista simple de empresas) ---

class ViewCompaniesPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO_PRINCIPAL)  # Fondo degradado oscuro

        self.controller = controller
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Datos de ejemplo específicos para esta lista (incluye las de la imagen)
        self.companies = ["BIMBO", "PANADERIA HOLA MUNDO", "PAW PATROL", "Tecno Soluciones SA", "Inversiones del Sur"]

        self._setup_header()
        self._setup_company_list()

    def _setup_header(self):
        """Configura el encabezado (LOGOTIPO, Buscar, EMPRESAS)."""

        # --- Barra Superior ---
        header_frame = ctk.CTkFrame(self, fg_color=COLOR_MORADO_OSCURO, corner_radius=0, height=60)
        header_frame.grid(row=0, column=0, sticky="new")
        header_frame.grid_columnconfigure(0, weight=1)  # LOGOTIPO a la izquierda
        header_frame.grid_columnconfigure(1, weight=1)  # Barra de búsqueda a la derecha

        ctk.CTkLabel(header_frame, text="LOGOTIPO",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="white").grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Barra de Búsqueda (Similar a la barra superior del Dashboard)
        ctk.CTkEntry(header_frame, placeholder_text="Buscar",
                     width=250, height=35, corner_radius=15,
                     fg_color="white", text_color="black",
                     font=ctk.CTkFont(size=14)
                     ).grid(row=0, column=1, padx=20, sticky="e")

        # --- Título EMPRESAS ---
        ctk.CTkLabel(self, text="EMPRESAS",
                     font=ctk.CTkFont(size=30, weight="bold"),
                     text_color="white").grid(row=1, column=0, pady=(40, 30), sticky="n")

    def _setup_company_list(self):
        """Configura el contenedor central con la lista de empresas."""

        # Contenedor central (Color claro de la imagen)
        list_frame = ctk.CTkFrame(self, fg_color=COLOR_FONDO_LISTA, corner_radius=15)
        list_frame.grid(row=2, column=0, sticky="nsew", padx=100,
                        pady=50)  # Padding amplio para centrar y reducir el tamaño
        list_frame.grid_columnconfigure(0, weight=1)

        # Contenedor para el Scrollbar (dentro del list_frame)
        scrollable_list = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        scrollable_list.pack(fill="both", expand=True, padx=40, pady=40)
        scrollable_list.grid_columnconfigure(0, weight=1)

        # Título de la lista
        ctk.CTkLabel(scrollable_list, text="LISTA DE EMPRESAS",
                     font=ctk.CTkFont(family="Courier", size=24, weight="bold"),
                     text_color="black").grid(row=0, column=0, pady=(20, 30), sticky="n")

        # Listado de empresas
        list_font = ctk.CTkFont(family="Courier", size=20)
        for i, company_name in enumerate(self.companies):
            # Formato "1. EMPRESA"

            # Usar 'BIMBO' en negrita como se muestra en la imagen de referencia.
            if company_name == "BIMBO":
                text_display = f"{i + 1}. {company_name}"
                label = ctk.CTkLabel(scrollable_list, text=text_display,
                                     font=ctk.CTkFont(family="Courier", size=20, weight="bold"),
                                     text_color="black", anchor="w")
            else:
                text_display = f"{i + 1}. {company_name}"
                label = ctk.CTkLabel(scrollable_list, text=text_display,
                                     font=list_font,
                                     text_color="black", anchor="w")

            label.grid(row=i + 1, column=0, padx=20, pady=5, sticky="w")


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
        self.btn_ver = self._create_nav_button("VER EMPRESAS",
                                               lambda: self.nav_action("VER EMPRESAS"))  # Este ahora tiene un mapeo

        # 2. Submenu Frame USUARIOS
        self.user_menu_frame = ctk.CTkFrame(self.nav_frame, fg_color="#4B0082", corner_radius=0)
        user_submenu_items = ["CREAR USUARIO", "MODIFICAR USUARIOS", "ELIMINAR USUARIOS"]
        for sub_item in user_submenu_items:
            self._create_sub_menu(self.user_menu_frame, sub_item).pack(fill="x", padx=(20, 0), pady=1)

        # 3. Submenu Frame EMPRESA
        self.company_menu_frame = ctk.CTkFrame(self.nav_frame, fg_color="#4B0082", corner_radius=0)
        # ITEMS DE EMPRESA ACTUALIZADOS:
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

        # Las páginas de creación, modificación y eliminación manejan su propio fondo
        if content_frame_class in [ModifyUsersPage, CreateUserPage, DeleteUsersPage, CreateCompanyPage,
                                   ModifyCompanyPage, DeleteCompanyPage,
                                   ViewCompaniesPage]:  # ViewCompaniesPage añadida
            self.current_content = content_frame_class(self.content_container, self)
        elif content_frame_class != DashboardPage:
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
        elif action == "MODIFICAR USUARIOS":
            self.show_content(ModifyUsersPage)
        elif action == "ELIMINAR USUARIOS":
            self.show_content(DeleteUsersPage)  # Nueva página de eliminación
        elif action == "CREAR EMPRESA":
            self.show_content(CreateCompanyPage)
        elif action == "MODIFICAR INFORMACIÓN EMPRESA":
            self.show_content(ModifyCompanyPage)
        elif action == "ELIMINAR EMPRESA":
            self.show_content(DeleteCompanyPage)
        elif action == "VER EMPRESAS":  # NUEVA ACCIÓN
            self.show_content(ViewCompaniesPage)
        else:
            self.show_default_dashboard()


# ==================================================================
## 🏃 Ejecución
# ==================================================================

if __name__ == "__main__":
    print(f"\n--- INICIO DE APLICACIÓN ---")
    print(f"Directorio de trabajo: {os.getcwd()}")

    app = App()
    app.mainloop()
