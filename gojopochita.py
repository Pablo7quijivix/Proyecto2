import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw
import os
import tkinter.messagebox as messagebox
import Proyecto_2

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- CONFIGURACIÓN DE RUTAS Y COLORES ---
COLOR_MORADO_OSCURO = "#301934"
COLOR_FONDO_PRINCIPAL = "#4b0082"
COLOR_DEGRADADO_BASE = "#28074d"
COLOR_CAMPO_CLARO = "#9c79c9"
COLOR_BOTON_REGRESAR = "#7D3C98"
COLOR_FORM_FRAME = "#5800a3"
COLOR_BOTON_EDITAR = "#E0BBE4"
COLOR_BOTON_ELIMINAR = "#DC3545"
COLOR_TEXTO_TABLA = "#301934"
COLOR_FILA_OSCURA = "#4b0082"
COLOR_FILA_CLARA = "#9c79c9"
COLOR_CABECERA = "#301934"
COLOR_FONDO_LISTA = "#eeeeee"
COLOR_CONTENIDO_BOX = "#ffffff"
COLOR_FONDO_GENERAL = "#f5f5f5"
COLOR_TEXTO_ETIQUETA = "#301934"
COLOR_BOTON_PRIMARIO = "#4b0082"

PATH_BG = "fondo_degradado.png"
PATH_LOGO = "fondo_degradado.png"
PATH_FROG = "fondo_degradado.png"


def create_default_image(width, height, color1, color2, text=""):
    image = Image.new("RGB", (width, height), color1)
    draw = ImageDraw.Draw(image)

    def hex_to_rgb(hex_color):
        if isinstance(hex_color, str) and hex_color.startswith('#'):
            return tuple(int(hex_color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        return hex_color

    color1_rgb = hex_to_rgb(color1)
    color2_rgb = hex_to_rgb(color2)

    for i in range(height):
        ratio = i / height
        r = int(color1_rgb[0] * (1 - ratio) + color2_rgb[0] * ratio)
        g = int(color1_rgb[1] * (1 - ratio) + color2_rgb[1] * ratio)
        b = int(color1_rgb[2] * (1 - ratio) + color2_rgb[2] * ratio)
        draw.line([(0, i), (width, i)], fill=(r, g, b))

    if text:
        print(f"Creando imagen por defecto: {text}")

    return image


def load_pil_image(path, default_width=800, default_height=600):
    if os.path.exists(path):
        try:
            pil_img = Image.open(path)
            print(f"[ÉXITO] Archivo '{path}' cargado correctamente. Tamaño: {pil_img.size}")
            return pil_img
        except Exception as e:
            print(f"[ERROR] Falló al procesar '{path}': {e}. Usando imagen por defecto.")
    else:
        print(f"[ADVERTENCIA] Archivo '{path}' no encontrado. Creando imagen por defecto.")
        print(f"Directorio actual: {os.getcwd()}")

    return create_default_image(
        default_width, default_height,
        COLOR_DEGRADADO_BASE, COLOR_FONDO_PRINCIPAL,
        f"Default_{os.path.basename(path)}")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        print(f"¿Existe PATH_BG ({PATH_BG})? {os.path.exists(PATH_BG)}")
        print(f"¿Existe PATH_LOGO ({PATH_LOGO})? {os.path.exists(PATH_LOGO)}")
        print(f"¿Existe PATH_FROG ({PATH_FROG})? {os.path.exists(PATH_FROG)}")
        print(f"Directorio actual: {os.getcwd()}")

        # Variables de usuario
        self.current_user = None
        self.user_role = None
        self.selected_company = None

        self.title("Aplicación de Gestión")
        self.geometry("1000x700")
        self.minsize(700, 500)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ctk.CTkFrame(self, fg_color=COLOR_FONDO_PRINCIPAL)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.original_bg_image = load_pil_image(PATH_BG, 1000, 700)
        self.original_logo_image = load_pil_image(PATH_LOGO, 50, 30)

        self.frames[LoginPage] = LoginPage(parent=container, controller=self,
                                           bg_image=self.original_bg_image, logo_image=self.original_logo_image)

        # DashboardPage se creará después de la autenticación
        self.frames[DashboardPage] = None

        self.pages = {
            LoginPage: LoginPage,
            DashboardPage: DashboardPage,
            CreateUserPage: CreateUserPage,
            ModifyUsersPage: ModifyUsersPage,
            DeleteUsersPage: DeleteUsersPage,
            CreateCompanyPage: CreateCompanyPage,
            ModifyCompanyPage: ModifyCompanyPage,
            DeleteCompanyPage: DeleteCompanyPage,
            ViewCompaniesPage: ViewCompaniesPage,
            CompanyHomePage: CompanyHomePage,
            InventoryManagementPage: InventoryManagementPage,
            CreateInvoicePage: CreateInvoicePage,
            ReportsPage: ReportsPage
        }

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        if cont == DashboardPage and self.frames[cont] is None:
            # Crear DashboardPage solo cuando sea necesario y después de la autenticación
            self.frames[DashboardPage] = DashboardPage(parent=self.frames[LoginPage].master, controller=self)

        if cont in self.frames and self.frames[cont] is not None:
            frame = self.frames[cont]
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()

    def authenticate_user(self, username, password):
        """Verifica las credenciales en la base de datos MySQL y almacena el rol"""
        try:
            resultado = Proyecto_2.inicio_sesio(username, password)

            if resultado == "salir":
                return False
            elif resultado:
                self.current_user = resultado
                self.user_role = resultado.get('rol', 'empleado')

                # Crear DashboardPage después de la autenticación
                self.frames[DashboardPage] = DashboardPage(parent=self.frames[LoginPage].master, controller=self)
                self.show_frame(DashboardPage)
                return True
            return False
        except Exception as e:
            print(f"Error en autenticación: {e}")
            return False

    def select_company_and_navigate(self, company_name):
        self.selected_company = company_name
        if self.frames[DashboardPage]:
            self.frames[CompanyHomePage] = CompanyHomePage(parent=self.frames[DashboardPage].content_container,
                                                           controller=self.frames[DashboardPage],
                                                           company_name=company_name)
            self.frames[DashboardPage].show_content(CompanyHomePage)

    def is_admin(self):
        """Verifica si el usuario actual es administrador"""
        return self.user_role and self.user_role.lower() in ['admin', 'administrador']


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
        if hasattr(self, 'original_bg_image') and self.original_bg_image:
            if event.width > 50 and event.height > 50:
                try:
                    original_width, original_height = self.original_bg_image.size
                    ratio = min(event.width / original_width, event.height / original_height)
                    new_width = int(original_width * ratio)
                    new_height = int(original_height * ratio)

                    resized_bg = self.original_bg_image.resize((new_width, new_height), Image.LANCZOS)

                    self.ctk_bg_image = ctk.CTkImage(
                        light_image=resized_bg,
                        dark_image=resized_bg,
                        size=(new_width, new_height)
                    )
                    self.background_label.configure(image=self.ctk_bg_image)

                except Exception as e:
                    print(f"Error al redimensionar fondo: {e}")

    def _setup_header(self):
        ctk.CTkLabel(self, text="Nombre empresa",
                     font=ctk.CTkFont(size=16, weight="normal"),
                     text_color="white", bg_color="transparent").place(x=20, y=10)

    def login_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not self.controller.authenticate_user(username, password):
            self.error_label.configure(text="Usuario o contraseña incorrectos.")
        else:
            self.error_label.configure(text="")


class CreateUserPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO_PRINCIPAL)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsw", padx=20, pady=20)
        left_frame.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(left_frame, text="Nombre empresa",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="white").grid(row=0, column=0, sticky="nw")

        ctk.CTkLabel(left_frame, text="Crear nuevo\nusuario",
                     font=ctk.CTkFont(size=48, weight="bold"), text_color="white",
                     justify="left").grid(row=1, column=0, sticky="nw", pady=(30, 20))

        ctk.CTkLabel(left_frame, text="Aquí puedes crear un nuevo usuario para el sistema.",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="white").grid(row=2, column=0, sticky="nw")

        ctk.CTkLabel(left_frame, text="—",
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="white",
                     justify="left").grid(row=3, column=0, sticky="nw", pady=5)

        ctk.CTkLabel(left_frame, text="Completa todos los campos requeridos.",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="white").grid(row=4, column=0, sticky="nw")

        ctk.CTkButton(left_frame, text="Regresar",
                      command=lambda: self.controller.show_default_dashboard(),
                      width=150, height=45, corner_radius=10,
                      fg_color=COLOR_BOTON_REGRESAR,
                      hover_color="#A948C9",
                      font=ctk.CTkFont(size=16, weight="normal"),
                      text_color="white").grid(row=5, column=0, sticky="sw", pady=(100, 0))

        right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nse", padx=150, pady=50)
        form_frame = ctk.CTkScrollableFrame(right_frame, corner_radius=30,
                                            fg_color=COLOR_FORM_FRAME, width=350)
        form_frame.pack(expand=False, fill="y", side="right")

        ctk.CTkLabel(form_frame, text="Usuario",
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="white").pack(pady=(40, 20), padx=40)

        fields = [
            ("DPI", "text"),
            ("NOMBRE_COMPLETO", "text"),
            ("CORREO", "text"),
            ("PUESTO", "text"),
            ("USUARIO", "text"),
            ("CONTRASEÑA", "password"),
            ("ROL", "text")
        ]

        self.entries = {}
        for field, field_type in fields:
            ctk.CTkLabel(form_frame, text=field.replace("_", " "),
                         font=ctk.CTkFont(size=12, weight="normal"), text_color="white", anchor="w").pack(fill="x",
                                                                                                          padx=40,
                                                                                                          pady=(15, 0))

            if field_type == "password":
                entry = ctk.CTkEntry(form_frame, placeholder_text="", height=40, show="•",
                                     corner_radius=10, fg_color=COLOR_CAMPO_CLARO, border_width=0, text_color="white")
            else:
                entry = ctk.CTkEntry(form_frame, placeholder_text="", height=40,
                                     corner_radius=10, fg_color=COLOR_CAMPO_CLARO, border_width=0, text_color="white")

            entry.pack(fill="x", padx=40)
            self.entries[field] = entry

        ctk.CTkButton(form_frame, text="CREAR\nUSUARIO",
                      command=self.create_user_action,
                      width=180, height=60, corner_radius=15,
                      fg_color=COLOR_MORADO_OSCURO,
                      hover_color="#5D3FD3",
                      font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(30, 40))

    def create_user_action(self):
        dpi = self.entries["DPI"].get()
        nombre = self.entries["NOMBRE_COMPLETO"].get()
        correo = self.entries["CORREO"].get()
        puesto = self.entries["PUESTO"].get()
        usuario = self.entries["USUARIO"].get()
        contrasena = self.entries["CONTRASEÑA"].get()
        rol = self.entries["ROL"].get()

        if not all([dpi, nombre, usuario, contrasena, rol, correo, puesto]):
            messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
            return

        auditor = Proyecto_2.Auditor(nombre, dpi, correo, usuario, contrasena)
        success = auditor.crear_usuario(nombre, dpi, correo, puesto, usuario, contrasena, rol)

        if success:
            messagebox.showinfo("Éxito", f"Usuario {usuario} creado correctamente")
            for entry in self.entries.values():
                entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "No se pudo crear el usuario")


class CreateCompanyPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO_PRINCIPAL)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsw", padx=20, pady=20)
        left_frame.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(left_frame, text="Nombre empresa",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="white").grid(row=0, column=0, sticky="nw")

        ctk.CTkLabel(left_frame, text="Crear nueva\nempresa",
                     font=ctk.CTkFont(size=48, weight="bold"), text_color="white",
                     justify="left").grid(row=1, column=0, sticky="nw", pady=(30, 20))

        ctk.CTkLabel(left_frame, text="Aquí puedes crear una nueva empresa.",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="white").grid(row=2, column=0, sticky="nw")

        ctk.CTkLabel(left_frame, text="—",
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="white",
                     justify="left").grid(row=3, column=0, sticky="nw", pady=5)

        ctk.CTkLabel(left_frame, text="Completa todos los campos requeridos.",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="white").grid(row=4, column=0, sticky="nw")

        ctk.CTkButton(left_frame, text="Regresar",
                      command=lambda: self.controller.show_default_dashboard(),
                      width=150, height=45, corner_radius=10,
                      fg_color=COLOR_BOTON_REGRESAR,
                      hover_color="#A948C9",
                      font=ctk.CTkFont(size=16, weight="normal"),
                      text_color="white").grid(row=5, column=0, sticky="sw", pady=(100, 0))

        right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nse", padx=20, pady=20)

        form_frame = ctk.CTkScrollableFrame(right_frame, corner_radius=30,
                                            fg_color=COLOR_FORM_FRAME, width=350)
        form_frame.pack(expand=False, fill="y", side="right")

        ctk.CTkLabel(form_frame, text="Empresa",
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="white").pack(pady=(40, 20), padx=40)

        fields = [
            "NOMBRE EMPRESA", "NIT", "DIRECCIÓN"
        ]

        self.entries = {}
        for field in fields:
            ctk.CTkLabel(form_frame, text=field,
                         font=ctk.CTkFont(size=12, weight="normal"), text_color="white", anchor="w").pack(fill="x",
                                                                                                          padx=40,
                                                                                                          pady=(15, 0))

            entry = ctk.CTkEntry(form_frame, placeholder_text="", height=40,
                                 corner_radius=10, fg_color=COLOR_CAMPO_CLARO, border_width=0, text_color="white")
            entry.pack(fill="x", padx=40)
            self.entries[field] = entry

        ctk.CTkButton(form_frame, text="CREAR\nEMPRESA",
                      command=self.create_company_action,
                      width=180, height=60, corner_radius=15,
                      fg_color=COLOR_MORADO_OSCURO,
                      hover_color="#5D3FD3",
                      font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(30, 40))

    def create_company_action(self):
        nombre_empresa = self.entries["NOMBRE EMPRESA"].get()
        nit = self.entries["NIT"].get()
        direccion = self.entries["DIRECCIÓN"].get()

        if not all([nit, nombre_empresa]):
            messagebox.showerror("Error", "Por favor complete los campos obligatorios: NIT y Nombre Empresa")
            return

        try:
            auditor = Proyecto_2.Auditor("Administrador", "123456789", "admin@empresa.com", "admin", "password")
            success = auditor.crear_empresa(nombre_empresa, nit, direccion)

            if success:
                messagebox.showinfo("Éxito", f"Empresa {nombre_empresa} creada correctamente")
                for entry in self.entries.values():
                    entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "No se pudo crear la empresa")

        except Exception as e:
            messagebox.showerror("Error", f"Error al crear la empresa: {str(e)}")


class CreateInvoicePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO_PRINCIPAL)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsw", padx=20, pady=20)
        left_frame.grid_rowconfigure(5, weight=1)

        company_name = self.controller.controller.selected_company if self.controller.controller.selected_company else "Nombre empresa"
        ctk.CTkLabel(left_frame, text=company_name,
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="white").grid(row=0, column=0, sticky="nw")

        ctk.CTkLabel(left_frame, text="Registrar\nFactura",
                     font=ctk.CTkFont(size=48, weight="bold"), text_color="white",
                     justify="left").grid(row=1, column=0, sticky="nw", pady=(30, 20))

        ctk.CTkLabel(left_frame, text=f"Aquí puedes registrar una nueva factura de {company_name}.",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="white", justify="left").grid(row=2,
                                                                                                          column=0,
                                                                                                          sticky="nw")

        ctk.CTkLabel(left_frame, text="—",
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="white",
                     justify="left").grid(row=3, column=0, sticky="nw", pady=5)

        ctk.CTkLabel(left_frame, text="Asegúrate de ingresar todos los datos requeridos.",
                     font=ctk.CTkFont(size=16, weight="normal"), text_color="white", justify="left").grid(row=4,
                                                                                                          column=0,
                                                                                                          sticky="nw")

        ctk.CTkButton(left_frame, text="Regresar",
                      command=lambda: self.controller.nav_action("REGRESAR A EMPRESA"),
                      width=150, height=45, corner_radius=10,
                      fg_color=COLOR_BOTON_REGRESAR,
                      hover_color="#A948C9",
                      font=ctk.CTkFont(size=16, weight="normal"),
                      text_color="white").grid(row=5, column=0, sticky="sw", pady=(100, 0))

        right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nse", padx=20, pady=20)

        form_frame = ctk.CTkScrollableFrame(right_frame, corner_radius=30,
                                            fg_color=COLOR_FORM_FRAME, width=350)
        form_frame.pack(expand=False, fill="y", side="right")

        ctk.CTkLabel(form_frame, text="Factura",
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="white").pack(pady=(40, 20), padx=40)

        self.entries = {}
        fields = ["NIT CLIENTE", "NOMBRE CLIENTE", "DIRECCIÓN CLIENTE", "CORREO CLIENTE", "DPI CLIENTE",
                  "NUMERO FACTURA", "TOTAL", "FECHA DE COMPRA"]

        for field in fields:
            ctk.CTkLabel(form_frame, text=field.replace("_", " "),
                         font=ctk.CTkFont(size=12, weight="normal"), text_color="white", anchor="w").pack(fill="x",
                                                                                                          padx=40,
                                                                                                          pady=(15, 0))

            if field == "FECHA DE COMPRA":
                entry = ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD", height=40,
                                     corner_radius=10, fg_color=COLOR_CAMPO_CLARO, border_width=0, text_color="white")
            else:
                entry = ctk.CTkEntry(form_frame, placeholder_text="", height=40,
                                     corner_radius=10, fg_color=COLOR_CAMPO_CLARO, border_width=0, text_color="white")

            entry.pack(fill="x", padx=40)
            self.entries[field] = entry

        ctk.CTkButton(form_frame, text="REGISTRAR\nFACTURA",
                      command=self.register_invoice_action,
                      width=180, height=60, corner_radius=15,
                      fg_color=COLOR_MORADO_OSCURO,
                      hover_color="#5D3FD3",
                      font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(30, 40))

    def register_invoice_action(self):
        nit_cliente = self.entries["NIT CLIENTE"].get()
        numero_factura = self.entries["NUMERO FACTURA"].get()
        total = self.entries["TOTAL"].get()
        fecha_compra = self.entries["FECHA DE COMPRA"].get()

        if not all([nit_cliente, numero_factura, total, fecha_compra]):
            messagebox.showerror("Error", "Por favor complete los campos obligatorios")
            return

        empresa_nombre = self.controller.controller.selected_company
        if not empresa_nombre:
            messagebox.showerror("Error", "No hay empresa seleccionada")
            return

        try:
            auditor = Proyecto_2.Auditor("Administrador", "123456789", "admin@empresa.com", "admin", "password")
            success = auditor.registrar_factura(numero_factura, nit_cliente, empresa_nombre, float(total), fecha_compra)

            if success:
                messagebox.showinfo("Éxito", f"Factura {numero_factura} registrada correctamente")
                for entry in self.entries.values():
                    entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "No se pudo registrar la factura")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar factura: {str(e)}")


class TableBasePage(ctk.CTkFrame):
    def __init__(self, parent, controller, action_text, action_color, action_hover_color, action_command,
                 data_type="user", title_text=""):
        super().__init__(parent, fg_color=COLOR_FONDO_PRINCIPAL)

        self.controller = controller
        self.action_text = action_text
        self.action_color = action_color
        self.action_hover_color = action_hover_color
        self.action_command = action_command
        self.data_type = data_type
        self.title_text = title_text

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        if data_type == "user":
            self.user_data = self._load_users_from_db()
        elif data_type == "company":
            self.company_data = self._load_companies_from_db()
        elif data_type == "inventory":
            self.inventory_data = self._load_inventory_from_db()

        self._setup_title()
        self._setup_top_bar()
        self._setup_table()

    def _load_users_from_db(self):
        """Carga usuarios reales desde la base de datos"""
        try:
            usuarios = Proyecto_2.Usuario.listar_todos()
            # Adaptar formato para la tabla
            formatted_users = []
            for usuario in usuarios:
                formatted_users.append({
                    "ID": usuario.get('id', ''),
                    "Nombre": usuario.get('nombre', ''),
                    "Usuario": usuario.get('usuario', ''),
                    "ROL": usuario.get('rol', ''),
                    "Puesto": usuario.get('puesto', '')
                })
            return formatted_users
        except Exception as e:
            print(f"Error cargando usuarios: {e}")
            return []

    def _load_companies_from_db(self):
        """Carga empresas reales desde la base de datos"""
        try:
            empresas = Proyecto_2.Empresa.listar()
            formatted_companies = []
            for empresa in empresas:
                formatted_companies.append({
                    "ID": empresa.get('id', ''),
                    "Nombre": empresa.get('nombre', ''),
                    "NIT": empresa.get('nit_cliente', ''),
                    "DIRECCIÓN": empresa.get('direccion', '')
                })
            return formatted_companies
        except Exception as e:
            print(f"Error cargando empresas: {e}")
            return []

    def _load_inventory_from_db(self):
        """Carga inventario real desde la base de datos"""
        try:
            empresa_nombre = self.controller.controller.selected_company
            if not empresa_nombre:
                return []

            inventario = Proyecto_2.Inventario.listar(empresa_nombre)
            formatted_inventory = []
            for item in inventario:
                formatted_inventory.append({
                    "ID_Producto": item.get('producto', ''),
                    "Nombre": item.get('producto', ''),
                    "Cantidad": item.get('cantidad', 0),
                    "Precio": item.get('precio', 0)
                })
            return formatted_inventory
        except Exception as e:
            print(f"Error cargando inventario: {e}")
            return []

    def _setup_title(self):
        ctk.CTkLabel(self, text=self.title_text,
                     font=ctk.CTkFont(size=30, weight="bold"),
                     text_color="white").grid(row=0, column=0, pady=(40, 0), sticky="n")

    def _get_data(self):
        if self.data_type == "company":
            return self.company_data
        elif self.data_type == "inventory":
            return self.inventory_data
        return self.user_data

    def _get_columns(self):
        if self.data_type == "company":
            return ["ID", "Nombre", "NIT", "DIRECCIÓN", "Acción"]
        elif self.data_type == "inventory":
            return ["PRODUCTO", "CANTIDAD", "PRECIO", "Acción"]
        return ["ID", "Nombre", "Usuario", "ROL", "Acción"]

    def _setup_top_bar(self):
        top_bar_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        top_bar_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(40, 20))
        top_bar_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(top_bar_frame, text="Ordenar",
                      width=100, height=45, corner_radius=25,
                      fg_color="transparent", border_color="white", border_width=2,
                      hover_color="#6A5ACD", text_color="white",
                      font=ctk.CTkFont(size=16, weight="bold")
                      ).grid(row=0, column=0, padx=(0, 15), sticky="w")

        ctk.CTkEntry(top_bar_frame, placeholder_text="Buscar",
                     width=500, height=50, corner_radius=25,
                     fg_color="white", text_color="black",
                     font=ctk.CTkFont(size=16)
                     ).grid(row=0, column=1, sticky="ew", padx=15)

        ctk.CTkButton(top_bar_frame, text="Regresar",
                      command=lambda: self._handle_back_action(),
                      width=100, height=45, corner_radius=25,
                      fg_color="white", hover_color="#cccccc", text_color="black",
                      font=ctk.CTkFont(size=16, weight="bold")
                      ).grid(row=0, column=2, padx=(15, 0), sticky="e")

    def _handle_back_action(self):
        if self.data_type == "inventory":
            if self.controller.controller.selected_company:
                company_name = self.controller.controller.selected_company
                self.controller.controller.select_company_and_navigate(company_name)
            else:
                self.controller.show_default_dashboard()
        else:
            self.controller.show_default_dashboard()

    def _setup_table(self):
        table_container = ctk.CTkScrollableFrame(self, fg_color="transparent", label_text=None)
        table_container.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)

        data = self._get_data()
        cols = self._get_columns()

        num_cols = len(cols)
        for i in range(num_cols):
            table_container.grid_columnconfigure(i, weight=1 if i < num_cols - 1 else 1)

        header_font = ctk.CTkFont(size=16, weight="bold")
        for i, col_name in enumerate(cols):
            header_cell = ctk.CTkLabel(table_container, text=col_name.upper(),
                                       fg_color=COLOR_CABECERA, text_color="white", font=header_font, height=50,
                                       corner_radius=0)
            header_cell.grid(row=0, column=i, sticky="nsew", padx=(1 if i > 0 else 0, 1), pady=(0, 1))

        row_font = ctk.CTkFont(size=14)
        if self.data_type == "user":
            display_keys = ["Nombre", "Usuario", "ROL"]
            id_key = "ID"
        elif self.data_type == "company":
            display_keys = ["Nombre", "NIT", "DIRECCIÓN"]
            id_key = "ID"
        elif self.data_type == "inventory":
            display_keys = ["Cantidad", "Precio"]
            id_key = "Nombre"
        else:
            display_keys = []
            id_key = ""

        for r, item in enumerate(data):
            row_index = r + 1
            bg_color = COLOR_FILA_CLARA if r % 2 == 0 else COLOR_FILA_OSCURA
            text_color = COLOR_TEXTO_TABLA if r % 2 == 0 else "white"

            ctk.CTkLabel(table_container, text=item[id_key], fg_color=bg_color, text_color=text_color,
                         font=row_font, height=60, corner_radius=0, anchor="w", padx=15).grid(row=row_index, column=0,
                                                                                              sticky="nsew",
                                                                                              padx=(1, 1), pady=(1, 1))

            current_col = 1
            for key in display_keys:
                value = item.get(key)
                if key == "Precio":
                    display_value = f"Q {float(value):.2f}" if value else "Q 0.00"
                else:
                    display_value = str(value) if value else ""
                cell = ctk.CTkLabel(table_container, text=display_value, fg_color=bg_color, text_color=text_color,
                                    font=row_font, height=60, corner_radius=0, anchor="w", padx=15)
                cell.grid(row=row_index, column=current_col, sticky="nsew", padx=(1, 1), pady=(1, 1))
                current_col += 1

            action_col_idx = num_cols - 1
            edit_button_frame = ctk.CTkFrame(table_container, fg_color=bg_color, corner_radius=0)
            edit_button_frame.grid(row=row_index, column=action_col_idx, sticky="nsew", padx=(1, 1), pady=(1, 1))
            edit_button_frame.grid_columnconfigure(0, weight=1)

            ctk.CTkButton(edit_button_frame, text=self.action_text,
                          command=lambda u=item: self.action_command(u),
                          width=80, height=35, corner_radius=10,
                          fg_color=self.action_color,
                          hover_color=self.action_hover_color,
                          text_color=COLOR_TEXTO_TABLA if bg_color == COLOR_BOTON_EDITAR else "white",
                          font=ctk.CTkFont(size=14, weight="bold")
                          ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)


class ModifyUsersPage(TableBasePage):
    def __init__(self, parent, controller):
        super().__init__(
            parent, controller,
            action_text="Editar",
            action_color=COLOR_BOTON_EDITAR,
            action_hover_color="#CBAACB",
            action_command=self.edit_user_action,
            data_type="user",
            title_text="MODIFICAR USUARIOS"
        )

    def edit_user_action(self, user):
        print(f"Editando usuario: ID={user['ID']}, Nombre={user['Nombre']}")


class DeleteUsersPage(TableBasePage):
    def __init__(self, parent, controller):
        super().__init__(
            parent, controller,
            action_text="Eliminar",
            action_color=COLOR_BOTON_ELIMINAR,
            action_hover_color="#8B0000",
            action_command=self.delete_user_action,
            data_type="user",
            title_text="ELIMINAR USUARIOS"
        )

    def delete_user_action(self, user):
        """Elimina un usuario usando Proyecto_2"""
        try:
            success = Proyecto_2.Usuario.eliminar(user['Usuario'])
            if success:
                messagebox.showinfo("Éxito", f"Usuario {user['Nombre']} eliminado correctamente")
                self.user_data = self._load_users_from_db()
                self._setup_table()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el usuario: {e}")


class ModifyCompanyPage(TableBasePage):
    def __init__(self, parent, controller):
        super().__init__(
            parent, controller,
            action_text="Editar",
            action_color=COLOR_BOTON_EDITAR,
            action_hover_color="#CBAACB",
            action_command=self.edit_company_action,
            data_type="company",
            title_text="MODIFICAR EMPRESAS"
        )

    def edit_company_action(self, company):
        print(f"Editando empresa: ID={company['ID']}, Nombre={company['Nombre']}")


class DeleteCompanyPage(TableBasePage):
    def __init__(self, parent, controller):
        super().__init__(
            parent, controller,
            action_text="Eliminar",
            action_color=COLOR_BOTON_ELIMINAR,
            action_hover_color="#8B0000",
            action_command=self.delete_company_action,
            data_type="company",
            title_text="ELIMINAR EMPRESAS"
        )

    def delete_company_action(self, company):
        """Elimina una empresa usando Proyecto_2"""
        try:
            success = Proyecto_2.Empresa.eliminar(company['Nombre'])
            if success:
                messagebox.showinfo("Éxito", f"Empresa {company['Nombre']} eliminada correctamente")
                self.company_data = self._load_companies_from_db()
                self._setup_table()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la empresa")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la empresa: {e}")


class InventoryManagementPage(TableBasePage):
    def __init__(self, parent, controller):
        super().__init__(
            parent, controller,
            action_text="Editar",
            action_color=COLOR_BOTON_EDITAR,
            action_hover_color="#CBAACB",
            action_command=self.edit_inventory_action,
            data_type="inventory",
            title_text="GESTIÓN DE INVENTARIO"
        )
        self._setup_inventory_top_bar()

    def _setup_inventory_top_bar(self):
        for widget in self.grid_slaves():
            if int(widget.grid_info()["row"]) == 1:
                widget.destroy()

        top_bar_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        top_bar_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(40, 20))
        top_bar_frame.grid_columnconfigure(2, weight=1)

        ctk.CTkButton(top_bar_frame, text="Agregar", command=self.add_inventory_action,
                      width=100, height=45, corner_radius=25,
                      fg_color=COLOR_MORADO_OSCURO,
                      hover_color="#5D3FD3",
                      text_color="white",
                      font=ctk.CTkFont(size=16, weight="bold")
                      ).grid(row=0, column=0, padx=(0, 15), sticky="w")

        ctk.CTkButton(top_bar_frame, text="Ordenar",
                      width=100, height=45, corner_radius=25,
                      fg_color="transparent", border_color="white", border_width=2,
                      hover_color="#6A5ACD", text_color="white",
                      font=ctk.CTkFont(size=16, weight="bold")
                      ).grid(row=0, column=1, padx=(0, 15), sticky="w")

        ctk.CTkEntry(top_bar_frame, placeholder_text="Buscar",
                     width=500, height=50, corner_radius=25,
                     fg_color="white", text_color="black",
                     font=ctk.CTkFont(size=16)
                     ).grid(row=0, column=2, sticky="ew", padx=15)

        ctk.CTkButton(top_bar_frame, text="Regresar",
                      command=lambda: self._handle_back_action(),
                      width=100, height=45, corner_radius=25,
                      fg_color="white", hover_color="#cccccc", text_color="black",
                      font=ctk.CTkFont(size=16, weight="bold")
                      ).grid(row=0, column=3, padx=(15, 0), sticky="e")

    def add_inventory_action(self):
        dialog = AddInventoryDialog(self)
        self.wait_window(dialog)

    def edit_inventory_action(self, item):
        print(f"Editando ítem de inventario: Producto={item['Nombre']}")

    def delete_inventory_action(self, item):
        """Elimina un ítem del inventario usando Proyecto_2"""
        try:
            empresa_nombre = self.controller.controller.selected_company
            if not empresa_nombre:
                messagebox.showerror("Error", "No hay empresa seleccionada")
                return

            success = Proyecto_2.Inventario.eliminar_de_inventario(empresa_nombre, item['Nombre'])
            if success:
                messagebox.showinfo("Éxito", f"Producto {item['Nombre']} eliminado correctamente")
                self.inventory_data = self._load_inventory_from_db()
                self._setup_table()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")

    def _setup_table(self):
        table_container = ctk.CTkScrollableFrame(self, fg_color="transparent", label_text=None)
        table_container.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)

        data = self._get_data()
        cols = self._get_columns()
        cols.append("Eliminar")

        num_cols = len(cols)
        for i in range(num_cols):
            table_container.grid_columnconfigure(i, weight=1)

        header_font = ctk.CTkFont(size=16, weight="bold")
        for i, col_name in enumerate(cols):
            header_cell = ctk.CTkLabel(table_container, text=col_name.upper(),
                                       fg_color=COLOR_CABECERA, text_color="white", font=header_font, height=50,
                                       corner_radius=0)
            header_cell.grid(row=0, column=i, sticky="nsew", padx=(1 if i > 0 else 0, 1), pady=(0, 1))

        row_font = ctk.CTkFont(size=14)
        display_keys = ["Cantidad", "Precio"]
        id_key = "Nombre"

        for r, item in enumerate(data):
            row_index = r + 1
            bg_color = COLOR_FILA_CLARA if r % 2 == 0 else COLOR_FILA_OSCURA
            text_color = COLOR_TEXTO_TABLA if r % 2 == 0 else "white"

            ctk.CTkLabel(table_container, text=item[id_key], fg_color=bg_color, text_color=text_color,
                         font=row_font, height=60, corner_radius=0, anchor="w", padx=15).grid(row=row_index, column=0,
                                                                                              sticky="nsew",
                                                                                              padx=(1, 1), pady=(1, 1))

            current_col = 1
            for key in display_keys:
                value = item.get(key)
                if key == "Precio":
                    display_value = f"Q {float(value):.2f}" if value else "Q 0.00"
                else:
                    display_value = str(value) if value else ""
                cell = ctk.CTkLabel(table_container, text=display_value, fg_color=bg_color, text_color=text_color,
                                    font=row_font, height=60, corner_radius=0, anchor="w", padx=15)
                cell.grid(row=row_index, column=current_col, sticky="nsew", padx=(1, 1), pady=(1, 1))
                current_col += 1

            action_col_idx = current_col
            edit_button_frame = ctk.CTkFrame(table_container, fg_color=bg_color, corner_radius=0)
            edit_button_frame.grid(row=row_index, column=action_col_idx, sticky="nsew", padx=(1, 1), pady=(1, 1))
            edit_button_frame.grid_columnconfigure(0, weight=1)

            ctk.CTkButton(edit_button_frame, text="Editar",
                          command=lambda u=item: self.edit_inventory_action(u),
                          width=70, height=35, corner_radius=10,
                          fg_color=COLOR_BOTON_EDITAR,
                          hover_color="#CBAACB",
                          text_color=COLOR_TEXTO_TABLA,
                          font=ctk.CTkFont(size=14, weight="bold")
                          ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            delete_col_idx = action_col_idx + 1
            delete_button_frame = ctk.CTkFrame(table_container, fg_color=bg_color, corner_radius=0)
            delete_button_frame.grid(row=row_index, column=delete_col_idx, sticky="nsew", padx=(1, 1), pady=(1, 1))
            delete_button_frame.grid_columnconfigure(0, weight=1)

            ctk.CTkButton(delete_button_frame, text="Eliminar",
                          command=lambda u=item: self.delete_inventory_action(u),
                          width=80, height=35, corner_radius=10,
                          fg_color=COLOR_BOTON_ELIMINAR,
                          hover_color="#8B0000",
                          text_color="white",
                          font=ctk.CTkFont(size=14, weight="bold")
                          ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)


class AddInventoryDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Agregar Producto al Inventario")
        self.geometry("400x400")
        self.resizable(False, False)

        self.parent = parent

        main_frame = ctk.CTkFrame(self, fg_color=COLOR_FORM_FRAME, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text="AGREGAR PRODUCTO",
                     font=ctk.CTkFont(size=20, weight="bold"), text_color="white").pack(pady=(20, 30))

        self.entries = {}
        fields = ["PRODUCTO", "CANTIDAD", "PRECIO"]

        for field in fields:
            ctk.CTkLabel(main_frame, text=field,
                         font=ctk.CTkFont(size=12, weight="normal"), text_color="white", anchor="w").pack(fill="x",
                                                                                                          padx=40,
                                                                                                          pady=(10, 0))

            entry = ctk.CTkEntry(main_frame, placeholder_text="", height=35,
                                 corner_radius=10, fg_color=COLOR_CAMPO_CLARO, border_width=0, text_color="white")
            entry.pack(fill="x", padx=40, pady=(5, 10))
            self.entries[field] = entry

        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=40, pady=20)

        ctk.CTkButton(button_frame, text="Cancelar", command=self.destroy,
                      width=120, height=40, corner_radius=10,
                      fg_color=COLOR_BOTON_ELIMINAR,
                      hover_color="#8B0000").pack(side="left", padx=(0, 10))

        ctk.CTkButton(button_frame, text="Agregar", command=self.add_product,
                      width=120, height=40, corner_radius=10,
                      fg_color=COLOR_MORADO_OSCURO,
                      hover_color="#5D3FD3").pack(side="right")

    def add_product(self):
        producto = self.entries["PRODUCTO"].get()
        cantidad = self.entries["CANTIDAD"].get()
        precio = self.entries["PRECIO"].get()

        if not all([producto, cantidad, precio]):
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return

        empresa_nombre = self.parent.controller.controller.selected_company
        if not empresa_nombre:
            messagebox.showerror("Error", "No hay empresa seleccionada")
            return

        try:
            inventario = Proyecto_2.Inventario(empresa_nombre, producto, int(cantidad), float(precio))
            success = inventario.guardar()

            if success:
                messagebox.showinfo("Éxito", f"Producto {producto} agregado correctamente")
                self.destroy()
                self.parent.inventory_data = self.parent._load_inventory_from_db()
                self.parent._setup_table()
            else:
                messagebox.showerror("Error", "No se pudo agregar el producto")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")


class ViewCompaniesPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO_PRINCIPAL)
        self.controller = controller.controller

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.companies = self._load_companies_from_db()
        self._setup_header()
        self._setup_company_list()

    def _load_companies_from_db(self):
        """Carga empresas reales desde la base de datos"""
        try:
            empresas = Proyecto_2.Empresa.listar()
            return [empresa['nombre'] for empresa in empresas] if empresas else []
        except Exception as e:
            print(f"Error cargando empresas: {e}")
            return []

    def _setup_header(self):
        header_frame = ctk.CTkFrame(self, fg_color=COLOR_MORADO_OSCURO, corner_radius=0, height=60)
        header_frame.grid(row=0, column=0, sticky="new")
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(header_frame, text="LOGOTIPO", font=ctk.CTkFont(size=18, weight="bold"), text_color="white").grid(
            row=0, column=0, padx=20, pady=10, sticky="w")

        ctk.CTkEntry(header_frame, placeholder_text="Buscar",
                     width=250, height=35, corner_radius=15,
                     fg_color="white", text_color="black",
                     font=ctk.CTkFont(size=14)
                     ).grid(row=0, column=1, padx=20, sticky="e")

        ctk.CTkLabel(self, text="EMPRESAS", font=ctk.CTkFont(size=30, weight="bold"), text_color="white").grid(row=1,
                                                                                                               column=0,
                                                                                                               pady=(40,
                                                                                                                     30),
                                                                                                               sticky="n")

    def _setup_company_list(self):
        list_frame = ctk.CTkFrame(self, fg_color=COLOR_FONDO_LISTA, corner_radius=15)
        list_frame.grid(row=2, column=0, sticky="nsew", padx=100, pady=50)
        list_frame.grid_columnconfigure(0, weight=1)

        scrollable_list = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        scrollable_list.pack(fill="both", expand=True, padx=40, pady=40)
        scrollable_list.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(scrollable_list, text="LISTA DE EMPRESAS",
                     font=ctk.CTkFont(family="Courier", size=24, weight="bold"), text_color="black").grid(row=0,
                                                                                                          column=0,
                                                                                                          pady=(20, 30),
                                                                                                          sticky="n")
        list_font = ctk.CTkFont(family="Courier", size=20)
        for i, company_name in enumerate(self.companies):
            company_button = ctk.CTkButton(scrollable_list,
                                           text=f"{i + 1}. {company_name}",
                                           command=lambda name=company_name: self.select_company(name),
                                           fg_color="transparent",
                                           hover_color="#cccccc",
                                           anchor="w",
                                           font=list_font,
                                           height=40,
                                           text_color="black")
            company_button.grid(row=i + 1, column=0, sticky="ew", pady=5, padx=20)

    def select_company(self, company_name):
        print(f"Empresa seleccionada: {company_name}")
        self.controller.select_company_and_navigate(company_name)


class CompanyHomePage(ctk.CTkFrame):
    def __init__(self, parent, controller, company_name):
        super().__init__(parent, fg_color=COLOR_FONDO_PRINCIPAL)
        self.controller = controller
        self.company_name = company_name

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._setup_header()
        self._setup_options_list()

    def _setup_header(self):
        header_frame = ctk.CTkFrame(self, fg_color=COLOR_MORADO_OSCURO, corner_radius=0, height=60)
        header_frame.grid(row=0, column=0, sticky="new")
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(header_frame, text="LOGOTIPO", font=ctk.CTkFont(size=18, weight="bold"), text_color="white").grid(
            row=0, column=0, padx=20, pady=10, sticky="w")

        ctk.CTkEntry(header_frame, placeholder_text="Buscar",
                     width=250, height=35, corner_radius=15,
                     fg_color="white", text_color="black",
                     font=ctk.CTkFont(size=14)
                     ).grid(row=0, column=1, padx=20, sticky="e")

        title_text = f"{self.company_name} CONTA"
        ctk.CTkLabel(self, text=title_text, font=ctk.CTkFont(size=30, weight="bold"), text_color="white").grid(row=1,
                                                                                                               column=0,
                                                                                                               pady=(40,
                                                                                                                     30),
                                                                                                               sticky="n")

    def _setup_options_list(self):
        list_frame = ctk.CTkFrame(self, fg_color=COLOR_FONDO_LISTA, corner_radius=15)
        list_frame.grid(row=2, column=0, sticky="nsew", padx=100, pady=50)
        list_frame.grid_columnconfigure(0, weight=1)

        scrollable_list = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        scrollable_list.pack(fill="both", expand=True, padx=40, pady=40)
        scrollable_list.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(scrollable_list, text="OPCIONES", font=ctk.CTkFont(family="Courier", size=24, weight="normal"),
                     text_color="black").grid(row=0, column=0, pady=(20, 30), sticky="n")

        options = ["GESTIONAR INVENTARIO", "VER REPORTES", "REGISTRAR FACTURA"]

        list_font_normal = ctk.CTkFont(family="Courier", size=20)
        for i, option_name in enumerate(options):
            command = lambda name=option_name: self.controller.nav_action(name)

            option_button = ctk.CTkButton(scrollable_list,
                                          text=f"{i + 1}. {option_name}",
                                          command=command,
                                          fg_color="transparent",
                                          hover_color="#cccccc",
                                          anchor="w",
                                          font=list_font_normal,
                                          height=40,
                                          text_color="black")
            option_button.grid(row=i + 1, column=0, sticky="ew", pady=5, padx=20)


class ReportsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=COLOR_FONDO_PRINCIPAL)
        self.controller = controller
        self.company_name = self.controller.controller.selected_company

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._setup_header()
        self._setup_reports()

    def _setup_header(self):
        header_frame = ctk.CTkFrame(self, fg_color=COLOR_MORADO_OSCURO, corner_radius=0, height=60)
        header_frame.grid(row=0, column=0, sticky="new")
        header_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(header_frame, text=f"REPORTES - {self.company_name}",
                     font=ctk.CTkFont(size=18, weight="bold"), text_color="white").grid(
            row=0, column=0, padx=20, pady=10)

        ctk.CTkButton(header_frame, text="Regresar",
                      command=lambda: self.controller.nav_action("REGRESAR A EMPRESA"),
                      width=100, height=35, corner_radius=10,
                      fg_color="white", hover_color="#cccccc", text_color="black"
                      ).grid(row=0, column=1, padx=20, sticky="e")

    def _setup_reports(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=50, pady=30)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # Botones de tipos de reportes
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        report_types = ["FACTURAS EMITIDAS", "FACTURAS CANCELADAS", "VENTAS TOTALES"]
        for i, report_type in enumerate(report_types):
            ctk.CTkButton(button_frame, text=report_type,
                          command=lambda rt=report_type: self.show_report(rt),
                          width=150, height=40, corner_radius=10,
                          fg_color=COLOR_BOTON_PRIMARIO,
                          hover_color="#5D3FD3").grid(row=0, column=i, padx=10)

        # Área de reportes
        self.report_frame = ctk.CTkScrollableFrame(main_frame, fg_color=COLOR_CONTENIDO_BOX)
        self.report_frame.grid(row=1, column=0, sticky="nsew")

        # Mostrar reporte por defecto
        self.show_report("FACTURAS EMITIDAS")

    def show_report(self, report_type):
        # Limpiar frame anterior
        for widget in self.report_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.report_frame, text=report_type,
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=COLOR_TEXTO_ETIQUETA).pack(pady=20)

        try:
            if report_type == "FACTURAS EMITIDAS":
                data = Proyecto_2.Reporte.facturas_emitidas(self.company_name)
            elif report_type == "FACTURAS CANCELADAS":
                data = Proyecto_2.Reporte.facturas_anuladas(self.company_name)
            elif report_type == "VENTAS TOTALES":
                data = Proyecto_2.Reporte.total_ventas_empresa(self.company_name)
            else:
                data = []

            if not data:
                ctk.CTkLabel(self.report_frame, text="No hay datos disponibles",
                             font=ctk.CTkFont(size=16), text_color=COLOR_TEXTO_ETIQUETA).pack(pady=50)
                return

            # Crear tabla simple
            for i, item in enumerate(data):
                report_text = ""
                for key, value in item.items():
                    report_text += f"{key}: {value}\n"

                frame = ctk.CTkFrame(self.report_frame, fg_color=COLOR_FILA_CLARA if i % 2 == 0 else COLOR_FILA_OSCURA)
                frame.pack(fill="x", padx=10, pady=5)

                ctk.CTkLabel(frame, text=report_text.strip(),
                             font=ctk.CTkFont(size=12),
                             text_color=COLOR_TEXTO_TABLA if i % 2 == 0 else "white",
                             justify="left").pack(padx=10, pady=5)

        except Exception as e:
            ctk.CTkLabel(self.report_frame, text=f"Error al cargar reporte: {str(e)}",
                         font=ctk.CTkFont(size=16), text_color="red").pack(pady=50)


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
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

        self.sidebar_frame = ctk.CTkFrame(
            self, width=200, corner_radius=0,
            fg_color=COLOR_MORADO_OSCURO
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.sidebar_frame, text="☰ LOGOTIPO", font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="white").grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.nav_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.nav_frame.grid(row=1, column=0, sticky="nwe", padx=0, pady=(0, 20))

        # Mostrar información del usuario de forma segura
        user_role = self.controller.user_role if self.controller.user_role else "USUARIO"
        user_info = f"BIENVENIDO!\n({user_role.upper()})"
        ctk.CTkLabel(self.nav_frame, text=user_info, font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="white", justify="left").pack(pady=(20, 30), padx=10, anchor="w")

        self._setup_navigation()

        ctk.CTkButton(self.sidebar_frame, text="Cerrar Sesión", command=self.logout_action,
                      fg_color="red", hover_color="#8B0000").grid(row=2, column=0, sticky="s", padx=20, pady=20)

        self.current_content = None
        self.show_default_dashboard()

    def logout_action(self):
        # Limpiar datos de usuario al cerrar sesión
        self.controller.current_user = None
        self.controller.user_role = None
        self.controller.selected_company = None
        self.controller.show_frame(LoginPage)

    def _create_nav_button(self, text, command):
        return ctk.CTkButton(
            self.nav_frame,
            text=text,
            command=command,
            fg_color="transparent",
            hover_color="#4B0082",
            anchor="w",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=0,
            text_color="white"
        )

    def _create_sub_menu(self, parent_frame, sub_item_text):
        return ctk.CTkButton(
            parent_frame,
            text=f"• {sub_item_text}",
            command=lambda val=sub_item_text: self.nav_action(val),
            fg_color="transparent",
            hover_color="#6A5ACD",
            anchor="w",
            font=ctk.CTkFont(size=12),
            height=30,
            corner_radius=0,
            text_color="white"
        )

    def _setup_navigation(self):
        # Solo mostrar gestión de usuarios si es administrador
        if self.controller.is_admin():
            self.btn_usuarios = self._create_nav_button("GESTIONAR USUARIOS ▾",
                                                        lambda: self.toggle_menu('user'))
            self.btn_usuarios.pack(fill="x", padx=0, pady=(10, 0))
            self.user_menu_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
            self._create_sub_menu(self.user_menu_frame, "CREAR USUARIO").pack(fill="x")
            self._create_sub_menu(self.user_menu_frame, "MODIFICAR USUARIOS").pack(fill="x")
            self._create_sub_menu(self.user_menu_frame, "ELIMINAR USUARIOS").pack(fill="x")

        # Solo mostrar gestión de empresa si es administrador
        if self.controller.is_admin():
            self.btn_empresa = self._create_nav_button("GESTIONAR EMPRESA ▾",
                                                       lambda: self.toggle_menu('company'))
            self.btn_empresa.pack(fill="x", padx=0, pady=(10, 0))
            self.company_menu_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
            self._create_sub_menu(self.company_menu_frame, "CREAR EMPRESA").pack(fill="x")
            self._create_sub_menu(self.company_menu_frame, "MODIFICAR INFORMACIÓN EMPRESA").pack(fill="x")
            self._create_sub_menu(self.company_menu_frame, "ELIMINAR EMPRESA").pack(fill="x")

        # Todos los usuarios pueden ver empresas
        self.btn_view_companies = self._create_nav_button("VER EMPRESAS",
                                                          lambda: self.nav_action("VER EMPRESAS"))
        self.btn_view_companies.pack(fill="x", padx=0, pady=(10, 0))

        self.repack_navigation()

    def repack_navigation(self):
        # Limpiar todos los widgets
        for widget in self.nav_frame.winfo_children():
            widget.pack_forget()

        # Mostrar información del usuario de forma segura
        user_role = self.controller.user_role if self.controller.user_role else "USUARIO"
        user_info = f"BIENVENIDO!\n({user_role.upper()})"
        ctk.CTkLabel(self.nav_frame, text=user_info, font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="white", justify="left").pack(pady=(20, 30), padx=10, anchor="w")

        # Reconstruir navegación según permisos
        if self.controller.is_admin() and hasattr(self, 'btn_usuarios'):
            self.btn_usuarios.pack(fill="x", padx=0, pady=(10, 0))
            if self.user_menu_open:
                self.user_menu_frame.pack(fill="x", padx=20, pady=(0, 10))

        if self.controller.is_admin() and hasattr(self, 'btn_empresa'):
            self.btn_empresa.pack(fill="x", padx=0, pady=(10, 0))
            if self.company_menu_open:
                self.company_menu_frame.pack(fill="x", padx=20, pady=(0, 10))

        if hasattr(self, 'btn_view_companies'):
            self.btn_view_companies.pack(fill="x", padx=0, pady=(10, 0))

        self.nav_frame.update_idletasks()

    def toggle_menu(self, menu_type):
        if menu_type == 'user' and self.controller.is_admin():
            self.user_menu_open = not self.user_menu_open
            if self.user_menu_open:
                self.company_menu_open = False
                self.btn_usuarios.configure(text="GESTIONAR USUARIOS ▴")
                if hasattr(self, 'btn_empresa'):
                    self.btn_empresa.configure(text="GESTIONAR EMPRESA ▾")
            else:
                self.btn_usuarios.configure(text="GESTIONAR USUARIOS ▾")
        elif menu_type == 'company' and self.controller.is_admin():
            self.company_menu_open = not self.company_menu_open
            if self.company_menu_open:
                self.user_menu_open = False
                self.btn_empresa.configure(text="GESTIONAR EMPRESA ▴")
                if hasattr(self, 'btn_usuarios'):
                    self.btn_usuarios.configure(text="GESTIONAR USUARIOS ▾")
            else:
                self.btn_empresa.configure(text="GESTIONAR EMPRESA ▾")

        self.repack_navigation()

    def show_content(self, content_frame_class):
        if self.current_content:
            self.current_content.destroy()

        if content_frame_class == CompanyHomePage:
            self.current_content = self.controller.frames.get(CompanyHomePage)
        elif content_frame_class == ViewCompaniesPage:
            self.current_content = ViewCompaniesPage(self.content_container, self)
        else:
            page_class = self.controller.pages.get(content_frame_class) or content_frame_class
            self.current_content = page_class(self.content_container, self)

        if self.current_content:
            self.current_content.grid(row=0, column=0, sticky="nsew")

    def show_default_dashboard(self):
        if self.current_content:
            self.current_content.destroy()

        default_frame = ctk.CTkFrame(self.content_container, fg_color="white")
        default_frame.grid(row=0, column=0, sticky="nsew")

        user_role = self.controller.user_role if self.controller.user_role else "USUARIO"
        welcome_text = f"Bienvenido al menu \nRol: {user_role.upper()}"
        ctk.CTkLabel(default_frame, text=welcome_text,
                     font=ctk.CTkFont(size=40, weight="bold"),
                     text_color=COLOR_MORADO_OSCURO).pack(pady=100)

        self.current_content = default_frame

    def nav_action(self, action):
        print(f"Navegando a: {action}")

        # Verificar permisos para acciones de administrador
        if action in ["CREAR USUARIO", "MODIFICAR USUARIOS", "ELIMINAR USUARIOS",
                      "CREAR EMPRESA", "MODIFICAR INFORMACIÓN EMPRESA", "ELIMINAR EMPRESA"]:
            if not self.controller.is_admin():
                messagebox.showwarning("Acceso Denegado",
                                       "No tienes permisos para acceder a esta función.")
                return

        if action == "CREAR USUARIO":
            self.show_content(CreateUserPage)
        elif action == "MODIFICAR USUARIOS":
            self.show_content(ModifyUsersPage)
        elif action == "ELIMINAR USUARIOS":
            self.show_content(DeleteUsersPage)
        elif action == "CREAR EMPRESA":
            self.show_content(CreateCompanyPage)
        elif action == "MODIFICAR INFORMACIÓN EMPRESA":
            self.show_content(ModifyCompanyPage)
        elif action == "ELIMINAR EMPRESA":
            self.show_content(DeleteCompanyPage)
        elif action == "VER EMPRESAS":
            self.show_content(ViewCompaniesPage)
        elif action == "GESTIONAR INVENTARIO":
            self.show_content(InventoryManagementPage)
        elif action == "REGISTRAR FACTURA":
            self.show_content(CreateInvoicePage)
        elif action == "VER REPORTES":
            company_name = self.controller.selected_company if self.controller.selected_company else "EMPRESA"
            reports_page = ReportsPage(self.content_container, self)
            reports_page.grid(row=0, column=0, sticky="nsew")
            self.current_content = reports_page
        elif action == "REGRESAR A EMPRESA":
            company_name = self.controller.selected_company
            if company_name:
                self.controller.select_company_and_navigate(company_name)
            else:
                self.show_default_dashboard()
        else:
            self.show_default_dashboard()


if __name__ == "__main__":
    print(f"\n--- INICIO DE APLICACIÓN ---")
    app = App()
    app.mainloop()