print(f"Agregando archivo adicional en donde se alojara la parte grafica")

# =========================================================
# Archivo: Interfaz.py
# Contiene el código de PySide6, el controlador de la UI,
# y el punto de entrada de la aplicación.
# =========================================================

from PySide6.QtWidgets import (
    QMainWindow, QStackedWidget, QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox, QFrame, QHBoxLayout, QSizePolicy, QGridLayout,
    QComboBox, QSpacerItem
)

from PySide6.QtCore import Qt, QSize
import sys

# --- IMPORTACIÓN DE LA LÓGICA DE NEGOCIO ---
# Importamos la función de login desde el archivo Proyecto_2.py
# actualización 2, imoprtamos auditor para usar sus métodos
from Proyecto_2 import inicio_sesio, Auditor, Usuario


# --- 1. SIMULACIÓN DE LA INTERFAZ GENERADA POR Qt Designer ---
# Esta clase simula lo que se generaría a partir de tu archivo .ui
class Ui_MainWindow(object):
    """
    Clase de simulación de la interfaz generada por PySide6-uic.
    Contiene la estructura base de la ventana y el QStackedWidget.
    """

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)

        # El QStackedWidget será el corazón de la navegación
        self.stackedWidget = QStackedWidget()
        MainWindow.setCentralWidget(self.stackedWidget)

        #paginas
        # Widgets principales (los diseñaremos individualmente después)
        self.login_page = QWidget()  # Página 0: Login (Diseño de la Página 1 y 2 del PDF) \ indice 0
        self.dashboard_page = QWidget()  # Página 1: Menú Principal (Diseño de la Página 3 y 8 del PDF) \ indice 1

        # Agregar las páginas al Stacked Widget
        self.stackedWidget.addWidget(self.login_page)
        self.stackedWidget.addWidget(self.dashboard_page)

        # Configurar el diseño inicial de la página de Login
        self.setup_login_ui()
        self.setup_dashboard_ui() # AGREGANDO NUEVA FUNCIÓN
        self.setup_gestion_usuarios_ui() # AGREGAMOS NUEVA FUNCIÓN EN ACTUALIZACIÓN 2

    def setup_login_ui(self):
        # --- Configuración Visual del Login (siguiendo PDF) ---

        # Widgets de entrada
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("padding: 10px; font-size: 14pt; border: 1px solid #ccc; border-radius: 5px;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 10px; font-size: 14pt; border: 1px solid #ccc; border-radius: 5px;")

        self.btn_ingresar = QPushButton("Ingresar")
        self.btn_ingresar.setStyleSheet(
            "background-color: #4B0082; color: white; padding: 10px; font-size: 16pt; border-radius: 5px;")

        self.label_titulo = QLabel("Log in")
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 24pt; color: #4B0082; margin-bottom: 20px;")

        # QFrame para simular la tarjeta blanca centrada
        card_frame = QFrame(self.login_page)
        card_frame.setStyleSheet("background-color: white; border-radius: 15px; padding: 20px;")
        card_layout = QVBoxLayout(card_frame)

        # Agregar elementos a la tarjeta
        card_layout.addWidget(self.label_titulo)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(self.btn_ingresar)

        # Fondo y Centrado (Fondo Morado del PDF)
        self.login_page.setStyleSheet("background-color: #6A1B9A;")
        main_layout = QVBoxLayout(self.login_page)
        main_layout.addStretch()
        main_layout.addWidget(card_frame, alignment=Qt.AlignCenter)
        main_layout.addStretch()


# -------------------------------------------------------------------
# AGREGANDO FUNCIÓN CLAVE: DISEÑO DEL DASHBOARD
# -------------------------------------------------------------------
    def setup_dashboard_ui(self):
        '''
        Configurando la pagina del Dashboard con un Menú Lateral y un area de contenido
        (siguiendo el boceto del canva PDF de la pag 3-8....)
        '''
        # Estructura Principa: Horizontal (agregando el Menú lateral \ Contenido)
        dashboard_layout = QHBoxLayout(self.dashboard_page)
        dashboard_layout.setContentsMargins(0, 0, 0, 0)

        #Ménu lateral 1(side menu)
        self.menu_lateral_frame =QFrame()
        self.menu_lateral_frame.setFixedWidth(250)  # Ancho fijo para el menú
        self.menu_lateral_frame.setStyleSheet("background-color: #4B0082; color: white;")  # Morado intenso

        #Layout del Menú
        menu_layout = QVBoxLayout(self.menu_lateral_frame)
        menu_layout.setAlignment(Qt.AlignTop)

        #Logo / Titulo
        self.label_logo = QLabel("LOGO DE EMPRESA")
        self.label_logo.setStyleSheet("font-size: 18pt; font-weight: bold; margin: 20px 0;")
        self.label_logo.setAlignment(Qt.AlignCenter)

        menu_layout.addWidget(self.label_logo)

        #Creacion de botones de navegación de las paginas del PDF (boceto canva) del 3 y 8
        # btn = significa 'BOTON'
        self.btn_gestionar_usuarios = QPushButton("GESTIONAR USUARIOS")
        self.btn_gestionar_empresa = QPushButton("GESTIONAR EMPRESA")
        self.btn_ver_empresas = QPushButton("VER EMPRESAS")

        #Estilo comun para los botones del menu  o esperar que sean modificados
        menu_btn_style =(
            "QPushButton { background-color: transparent; color: white; "
            "border: none; padding: 15px 10px; text-align: left; font-size: 14pt;}"
            "QPushButton:hover { background-color: #6A1B9A; }"
        )

        self.btn_gestionar_usuarios.setStyleSheet(menu_btn_style)
        self.btn_gestionar_empresa.setStyleSheet(menu_btn_style)
        self.btn_ver_empresas.setStyleSheet(menu_btn_style)

        #agregar botones al layout del menu
        menu_layout.addWidget(self.btn_gestionar_usuarios)
        menu_layout.addWidget(self.btn_gestionar_empresa)
        menu_layout.addWidget(self.btn_ver_empresas)
        menu_layout.addStretch() #este método sirve para que los arroje hacia arriba #

        #area de contenido principal
        self.contenido_area =QWidget()
        self.contenido_area.setStyleSheet("background-color: white;")

        # Usaremos otro QStackedWidget aquí para las sub-vistas del dashboard
        self.dashboard_stacked_widget = QStackedWidget(self.contenido_area)

        #-------sub-paginas del dashboard------------------------------
        self.dashboard_inicio_page = QWidget() # sub pagina de bienvenida / inicio
        self.dashboard_usuarios_page = QWidget()  # Sub-página 1: Gestionar Usuarios
        self.dashboard_empresas_page = QWidget()  # Sub-página 2: Gestionar Empresa
        self.dashboard_ver_empresas_page = QWidget()  # Sub-página 3: Ver Empresas (Listado)

        self.dashboard_stacked_widget.addWidget(self.dashboard_inicio_page)
        self.dashboard_stacked_widget.addWidget(self.dashboard_usuarios_page)
        self.dashboard_stacked_widget.addWidget(self.dashboard_empresas_page)
        self.dashboard_stacked_widget.addWidget(self.dashboard_ver_empresas_page)

        # simmulacion de la pagina del Dashboard
        inicio_layout = QVBoxLayout(self.dashboard_inicio_page)
        self.label_bienvenida = QLabel("Bienvenido al Panel de Administrador")
        self.label_bienvenida.setStyleSheet("font-size: 30pt; color: #4B0082;")
        inicio_layout.addWidget(self.label_bienvenida, alignment=Qt.AlignCenter)

        # Layout del area de contenido para contener el stacked widget
        contenido_layout = QVBoxLayout(self.contenido_area)
        contenido_layout.addWidget(self.dashboard_stacked_widget)

        # 3. Ensamblaje Final
        dashboard_layout.addWidget(self.menu_lateral_frame)
        dashboard_layout.addWidget(self.contenido_area)

        # Iniciar mostrando la página de inicio del dashboard
        self.dashboard_stacked_widget.setCurrentIndex(0)



# --- 2. CLASE CONTROLADORA PRINCIPAL ---
class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Sistema de Gestión Contable - PySide6")

        # Atributos para guardar la sesión
        self.usuario_activo = None
        self.rol_activo = None

        # Conexiones: Conectar el botón 'Ingresar' a la función de validación
        # nos referimos al login
        self.ui.btn_ingresar.clicked.connect(self.handle_login)

        # Nuevas conexiones de navegacion del Dashboard, agregamos nuevas conexiones
        self.ui.btn_gestionar_usuarios.clicked.connect(lambda: self.navigate_dashboard(1))
        self.ui.btn_gestionar_empresa.clicked.connect(lambda: self.navigate_dashboard(2))
        self.ui.btn_ver_empresas.clicked.connect(lambda: self.navigate_dashboard(3))

        # Establecer la primera vista: Login
        self.ui.stackedWidget.setCurrentIndex(0)


        # agregando nuevo método de navegacion
    def navigate_dashboard(self, index):
        """
        Cambia la sub-página visible dentro del QStackedWidget del Dashboard.
        """
        self.ui.dashboard_stacked_widget.setCurrentIndex(index)


    def handle_login(self):
        """
        Maneja el evento del botón Ingresar, llama a la lógica y gestiona la transición de la UI.
        """
        username = self.ui.username_input.text()
        password = self.ui.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error de Entrada", "Por favor, ingrese usuario y contraseña.")
            return

        # Llama a tu función de lógica (importada de Proyecto_2.py)
        resultado = inicio_sesio(username, password)

        if resultado and resultado != "salir":
            # Login exitoso
            self.usuario_activo = resultado
            self.rol_activo = resultado.get("rol", "Usuario")

            # Limpia y Transiciona
            self.ui.username_input.clear()
            self.ui.password_input.clear()

            #actualización del texto de bienvenida
            self.ui.label_bienvenida.setTex(f"Bienvenido/a, {self.usuario_activo.get('nombre', 'Admin')}!")

            # Muestra la página principal (Dashboard)
            self.ui.stackedWidget.setCurrentIndex(1)

        elif resultado == "salir":
            QMessageBox.information(self, "Sesión", "Comando de salida detectado.")
            self.close()

        else:
            # Login fallido
            QMessageBox.critical(self, "Error de Acceso", "Usuario o contraseña incorrectos.")
            self.ui.password_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
# Fin del archivo Interfaz.py