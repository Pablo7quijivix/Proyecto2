print(f"Agregando archivo adicional en donde se alojara la parte grafica")

# =========================================================
# Archivo: Interfaz.py
# Contiene el código de PySide6, el controlador de la UI,
# y el punto de entrada de la aplicación.
# =========================================================

from PySide6.QtWidgets import (
    QMainWindow, QStackedWidget, QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox, QFrame, QHBoxLayout, QSizePolicy, QGridLayout,
    QComboBox, QSpacerItem, QTableView, QHeaderView
)

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QStandardItemModel, QStandardItem # accede y ayuda a manejar los datos de la tabla
import sys

# --- IMPORTACIÓN DE LA LÓGICA DE NEGOCIO ---
# Importamos la función de login desde el archivo Proyecto_2.py
# actualización 2, imoprtamos auditor para usar sus métodos
# añadiendo Cliente y empresa en la actualización '3'

from Proyecto_2 import inicio_sesio, Auditor, Usuario, Cliente, Empresa


# --- 1. SIMULACIÓN DE LA INTERFAZ GENERADA POR Qt Designer ---
# se añade la interfaz (para las funciones de empresa) actualización 3
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
        self.setup_gestion_empresas_ui() # nueva funcion de empresa, A3

    def setup_login_ui(self: QWidget):
        # --- Configuración Visual del Login (siguiendo PDF) ---
        # en la actualización 2, el login siguie igual (aclaración)

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
# en la actualizacion 2, el dashboard sigue siendo el mismo
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
        inicio_layout.addWidget(self.label_bienvenida, alignment = Qt.AlignCenter)

        # Layout del area de contenido para contener el stacked widget
        contenido_layout = QVBoxLayout(self.contenido_area)
        contenido_layout.addWidget(self.dashboard_stacked_widget)

        # 3. Ensamblaje Final
        dashboard_layout.addWidget(self.menu_lateral_frame)
        dashboard_layout.addWidget(self.contenido_area)

        # Iniciar mostrando la página de inicio del dashboard
        self.dashboard_stacked_widget.setCurrentIndex(0)

     # -------------------------------------------------------------
     # FUNCIÓN CLAVE: DISEÑO PARA GESTIONAR A LOS USUARIOS (pag 4 del canva)
     # -------------------------------------------------------------
     # Layout principal de la página de Gestionar Usuarios (Índice 1 del dashboard_stacked_widget)
    def setup_gestion_usuarios_ui(self):
        main_layout = QHBoxLayout(self.dashboard_usuarios_page)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 1. Menú de Usuarios (Sidebar interno)
        menu_frame = QFrame()
        menu_frame.setFixedWidth(200)  # Ancho del menú interno
        menu_frame.setStyleSheet("background-color: #F0F0F0; border-right: 1px solid #CCC;")  # Color gris claro

        menu_layout = QVBoxLayout(menu_frame)
        menu_layout.setAlignment(Qt.AlignTop)

        # titulo del submenu
        label_titulo = QLabel("Gestión de Usuarios")
        label_titulo.setStyleSheet("font-size: 16pt; font-weight: bold; padding: 20px 10px; color: #4B0082;")
        menu_layout.addWidget(label_titulo)

        # agregando botones de navegación interna (ver pagina 4 del canva)
        self.btn_crear_usuario = QPushButton("CREAR USUARIO")
        self.btn_modificar_usuarios = QPushButton("MODIFICAR USUARIOS")
        self.btn_eliminar_usuarios = QPushButton("LISTAR Y ELIMINAR")

        menu_btn_style = (
            "QPushButton { background-color: transparent; color: black; "
            "border: none; padding: 15px 5px; text-align: left; font-size: 12pt;}"
            "QPushButton:hover { background-color: #E0E0E0; border-left: 5px solid #6A1B9A; }"
        )
        self.btn_crear_usuario.setStyleSheet(menu_btn_style)
        self.btn_modificar_usuarios.setStyleSheet(menu_btn_style)
        self.btn_eliminar_usuarios.setStyleSheet(menu_btn_style)

        menu_layout.addWidget(self.btn_crear_usuario)
        menu_layout.addWidget(self.btn_modificar_usuarios)
        menu_layout.addWidget(self.btn_eliminar_usuarios)
        menu_layout.addStretch()

        # 2. Área de Contenido de Usuarios (Tercer QStackedWidget)
        self.usuarios_stacked_widget = QStackedWidget()
        self.usuarios_stacked_widget.setStyleSheet("background-color: white; padding: 10px;")

        # VISTAS INTERNAS DE USUARIOS
        self.usuarios_vacio_page = QWidget()  # Sub-página 0: Vacio/Inicial
        self.usuarios_crear_page = QWidget()  # Sub-página 1: Crear Usuario (Página 5 de CANVA)
        self.usuarios_modificar_page = QWidget()  # Sub-página 2: Modificar Usuarios (Página 6 DE CANVA)
        self.usuarios_eliminar_page = QWidget()  # Sub-página 3: Eliminar Usuarios (Página 7 de CANVA)

        self.usuarios_stacked_widget.addWidget(self.usuarios_vacio_page)
        self.usuarios_stacked_widget.addWidget(self.usuarios_crear_page)
        self.usuarios_stacked_widget.addWidget(self.usuarios_modificar_page)
        self.usuarios_stacked_widget.addWidget(self.usuarios_eliminar_page)

        # 3. Ensamblaje Final
        main_layout.addWidget(menu_frame)
        main_layout.addWidget(self.usuarios_stacked_widget)

        # Iniciar mostrando la página de crear usuario por defecto
        self.usuarios_stacked_widget.setCurrentIndex(1)  # Mostramos Crear Usuario (Página 5)

        # Diseño del formulario de Crear Usuario (Página 5 del PDF)
        self.setup_formulario_crear_usuario()
        self.setup_listar_eliminar_usuarios()  # Llamada al nuevo setup

    def setup_formulario_crear_usuario(self):
        form_layout =QVBoxLayout(self.usuarios_crear_page)
        form_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        titulo = QLabel("Crear nuevo usuario")
        titulo.setStyleSheet("font-size: 24pt; color: #4B0082; margin-bottom: 20px; font-weight: bold;")
        form_layout.addWidget(titulo, alignment=Qt.AlignCenter)

        # Usamos un QFrame para contener el formulario (simulando la "tarjeta" deL CANVA)
        formulario_frame = QFrame()
        formulario_frame.setMinimumWidth(500)
        formulario_frame.setStyleSheet("background-color: #F8F8F8; border-radius: 10px; padding: 25px;")

        grid_layout = QGridLayout(formulario_frame)
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(15)

        # ------------------ CAMPOS DE ENTRADA (QLineEdit) ------------------
        self.input_nombre_completo = QLineEdit()
        self.input_dpi = QLineEdit()
        self.input_correo = QLineEdit()
        self.input_puesto = QLineEdit()
        self.input_usuario = QLineEdit()
        self.input_contrasena = QLineEdit()
        self.input_telefono = QLineEdit()
        self.input_fecha_nacimiento = QLineEdit()  # Usaremos un QLineEdit simple por ahora

        # Campo ROL (QComboBox)
        self.combo_rol = QComboBox()
        self.combo_rol.addItems(["Admin", "Usuario"])  # Roles de tu lógica (Admin/Usuario)

        # Estilo para todos los inputs
        input_style = "QLineEdit, QComboBox { padding: 8px; border: 1px solid #CCC; border-radius: 5px; font-size: 11pt; }"
        self.input_nombre_completo.setStyleSheet(input_style)
        self.input_dpi.setStyleSheet(input_style)
        self.input_correo.setStyleSheet(input_style)
        self.input_puesto.setStyleSheet(input_style)
        self.input_usuario.setStyleSheet(input_style)
        self.input_contrasena.setStyleSheet(input_style)
        self.input_telefono.setStyleSheet(input_style)
        self.input_fecha_nacimiento.setStyleSheet(input_style)
        self.combo_rol.setStyleSheet(input_style)

        # Etiquetas de ayuda (Opcional, pero ayuda a la claridad)
        grid_layout.addWidget(QLabel("Nombre Completo:"), 0, 0)
        grid_layout.addWidget(self.input_nombre_completo, 0, 1)

        grid_layout.addWidget(QLabel("DPI:"), 1, 0)
        grid_layout.addWidget(self.input_dpi, 1, 1)

        grid_layout.addWidget(QLabel("Correo:"), 2, 0)
        grid_layout.addWidget(self.input_correo, 2, 1)

        grid_layout.addWidget(QLabel("Puesto:"), 3, 0)
        grid_layout.addWidget(self.input_puesto, 3, 1)

        grid_layout.addWidget(QLabel("Usuario (Login):"), 4, 0)
        grid_layout.addWidget(self.input_usuario, 4, 1)

        grid_layout.addWidget(QLabel("Contraseña:"), 5, 0)
        self.input_contrasena.setEchoMode(QLineEdit.Password)
        grid_layout.addWidget(self.input_contrasena, 5, 1)

        grid_layout.addWidget(QLabel("Rol:"), 6, 0)
        grid_layout.addWidget(self.combo_rol, 6, 1)

        grid_layout.addWidget(QLabel("Teléfono:"), 7, 0)
        grid_layout.addWidget(self.input_telefono, 7, 1)

        grid_layout.addWidget(QLabel("Fecha Nacimiento:"), 8, 0)
        grid_layout.addWidget(self.input_fecha_nacimiento, 8, 1)

        # Botón CREAR USUARIO
        self.btn_crear_usuario_submit = QPushButton("CREAR USUARIO")
        self.btn_crear_usuario_submit.setStyleSheet("background-color: #4CAF50; color: white; padding: 12px; font-size: 14pt; font-weight: bold; border-radius: 5px; margin-top: 20px;")

        # Agregamos el formulario a la página
        form_layout.addWidget(formulario_frame, alignment = Qt.AlignCenter)
        form_layout.addWidget(self.btn_crear_usuario_submit, alignment=Qt.AlignCenter)
        form_layout.addStretch()

    def setup_listar_eliminar_usuarios(self):
        # codigo de listar y eliminar sin cambios
        main_layout = QVBoxLayout(self.usuarios_eliminar_page)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Título
        titulo = QLabel("Listado y Eliminación de Usuarios")
        titulo.setStyleSheet("font-size: 24pt; color: #4B0082; margin-bottom: 20px; font-weight: bold;")
        main_layout.addWidget(titulo, alignment=Qt.AlignCenter)

        # Barra de Búsqueda y Control
        control_frame = QFrame()
        control_layout = QHBoxLayout(control_frame)
        control_layout.setContentsMargins(0, 0, 0, 0)

        self.input_buscar_usuario = QLineEdit()
        self.input_buscar_usuario.setPlaceholderText("Buscar por Nombre, DPI o Usuario...")
        self.input_buscar_usuario.setStyleSheet(
            "padding: 8px; border: 1px solid #CCC; border-radius: 5px; font-size: 11pt;")
        self.input_buscar_usuario.setMinimumWidth(300)

        self.btn_eliminar_seleccionado = QPushButton("Eliminar Seleccionado")
        self.btn_eliminar_seleccionado.setStyleSheet(
            "background-color: #D32F2F; color: white; padding: 10px; font-size: 12pt; font-weight: bold; border-radius: 5px;")

        control_layout.addWidget(self.input_buscar_usuario)
        control_layout.addStretch()
        control_layout.addWidget(self.btn_eliminar_seleccionado)

        main_layout.addWidget(control_frame)

        # QTableView para mostrar la lista
        self.tabla_usuarios = QTableView()
        self.tabla_usuarios.setSelectionBehavior(QTableView.SelectRows)  # Seleccionar filas completas
        self.tabla_usuarios.setSelectionMode(QTableView.SingleSelection)  # Solo una fila a la vez
        self.tabla_usuarios.setStyleSheet("QTableView { gridline-color: #CCC; font-size: 11pt; }")
        main_layout.addWidget(self.tabla_usuarios)

        main_layout.addStretch()

    # --- NUEVA IMPLEMENTACIÓN: MODIFICAR USUARIOS ---
    def setup_modificar_usuarios(self):
        main_layout = QVBoxLayout(self.usuarios_modificar_page)
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        titulo = QLabel("Modificar Información de Usuario")
        titulo.setStyleSheet("font-size: 24pt; color: #4B0082; margin-bottom: 20px; font-weight: bold;")
        main_layout.addWidget(titulo, alignment=Qt.AlignCenter)

        # 1. SECCIÓN DE BÚSQUEDA
        busqueda_frame = QFrame()
        busqueda_layout = QHBoxLayout(busqueda_frame)
        busqueda_frame.setMinimumWidth(600)
        busqueda_frame.setStyleSheet("background-color: #E0E0E0; border-radius: 10px; padding: 15px;")

        self.input_buscar_modificar = QLineEdit()
        self.input_buscar_modificar.setPlaceholderText("Ingresar DPI o Usuario a modificar...")
        self.btn_buscar_usuario_modificar = QPushButton("Buscar Usuario")

        input_style = "QLineEdit { padding: 8px; border: 1px solid #CCC; border-radius: 5px; font-size: 11pt; }"
        self.input_buscar_modificar.setStyleSheet(input_style)
        self.btn_buscar_usuario_modificar.setStyleSheet(
            "background-color: #007BFF; color: white; padding: 8px; border-radius: 5px;")

        busqueda_layout.addWidget(QLabel("DPI/Usuario:"))
        busqueda_layout.addWidget(self.input_buscar_modificar)
        busqueda_layout.addWidget(self.btn_buscar_usuario_modificar)
        main_layout.addWidget(busqueda_frame)

        # 2. SECCIÓN DE FORMULARIO DE MODIFICACIÓN
        self.form_modificar_frame = QFrame()
        self.form_modificar_frame.setMinimumWidth(600)
        self.form_modificar_frame.setStyleSheet(
            "background-color: #F8F8F8; border-radius: 10px; padding: 25px; margin-top: 20px;")
        self.form_modificar_frame.setHidden(True)  # Se oculta hasta que se encuentre un usuario

        grid_layout = QGridLayout(self.form_modificar_frame)
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(15)

        # CAMPOS DE MODIFICACIÓN (Nuevos nombres para evitar conflicto con Crear Usuario)
        self.mod_nombre_completo = QLineEdit()
        self.mod_dpi = QLineEdit()  # Campo clave
        self.mod_dpi.setReadOnly(True)  # El DPI no debe ser modificable, solo se muestra
        self.mod_correo = QLineEdit()
        self.mod_puesto = QLineEdit()
        self.mod_usuario = QLineEdit()
        self.mod_contrasena = QLineEdit()
        self.mod_telefono = QLineEdit()
        self.mod_fecha_nacimiento = QLineEdit()
        self.mod_combo_rol = QComboBox()
        self.mod_combo_rol.addItems(["Admin", "Usuario"])

        # Estilo
        mod_input_style = "QLineEdit:not([readOnly='true']), QComboBox { padding: 8px; border: 1px solid #CCC; border-radius: 5px; font-size: 11pt; } QLineEdit[readOnly='true'] { background-color: #E9ECEF; color: #6C757D; }"
        self.mod_nombre_completo.setStyleSheet(mod_input_style)
        self.mod_dpi.setStyleSheet(mod_input_style)
        self.mod_correo.setStyleSheet(mod_input_style)
        self.mod_puesto.setStyleSheet(mod_input_style)
        self.mod_usuario.setStyleSheet(mod_input_style)
        self.mod_contrasena.setStyleSheet(mod_input_style)
        self.mod_telefono.setStyleSheet(mod_input_style)
        self.mod_fecha_nacimiento.setStyleSheet(mod_input_style)
        self.mod_combo_rol.setStyleSheet(mod_input_style)

        # Etiquetas y campos en la grilla
        grid_layout.addWidget(QLabel("DPI (Clave):"), 0, 0)
        grid_layout.addWidget(self.mod_dpi, 0, 1)
        grid_layout.addWidget(QLabel("Nombre Completo:"), 1, 0)
        grid_layout.addWidget(self.mod_nombre_completo, 1, 1)
        grid_layout.addWidget(QLabel("Usuario (Login):"), 2, 0)
        grid_layout.addWidget(self.mod_usuario, 2, 1)
        grid_layout.addWidget(QLabel("Contraseña:"), 3, 0)
        self.mod_contrasena.setEchoMode(QLineEdit.Password)
        grid_layout.addWidget(self.mod_contrasena, 3, 1)
        grid_layout.addWidget(QLabel("Rol:"), 4, 0)
        grid_layout.addWidget(self.mod_combo_rol, 4, 1)
        grid_layout.addWidget(QLabel("Correo:"), 5, 0)
        grid_layout.addWidget(self.mod_correo, 5, 1)
        grid_layout.addWidget(QLabel("Puesto:"), 6, 0)
        grid_layout.addWidget(self.mod_puesto, 6, 1)
        grid_layout.addWidget(QLabel("Teléfono:"), 7, 0)
        grid_layout.addWidget(self.mod_telefono, 7, 1)
        grid_layout.addWidget(QLabel("Fecha Nacimiento:"), 8, 0)
        grid_layout.addWidget(self.mod_fecha_nacimiento, 8, 1)

        # Botón GUARDAR MODIFICACIÓN
        self.btn_guardar_modificacion = QPushButton("GUARDAR MODIFICACIÓN")
        self.btn_guardar_modificacion.setStyleSheet(
            "background-color: #FFA500; color: white; padding: 12px; font-size: 14pt; font-weight: bold; border-radius: 5px; margin-top: 20px;")
        grid_layout.addWidget(self.btn_guardar_modificacion, 9, 0, 1, 2)

        main_layout.addWidget(self.form_modificar_frame)
        main_layout.addStretch()





    def setup_listar_empresas(self):
        """CONFIGURA LA VISTA PRINCIPAL PARA VER LA LISTA DE EMPRESAS."""
        main_layout = QVBoxLayout(self.dashboard_ver_empresas_page)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Título
        titulo = QLabel("Listado de Empresas Registradas")
        titulo.setStyleSheet("font-size: 28pt; color: #4B0082; margin-bottom: 20px; font-weight: bold;")
        main_layout.addWidget(titulo, alignment=Qt.AlignCenter)

        # Barra de Búsqueda y Control
        control_frame = QFrame()
        control_layout = QHBoxLayout(control_frame)
        control_layout.setContentsMargins(0, 0, 0, 0)

        self.input_buscar_empresa = QLineEdit()
        self.input_buscar_empresa.setPlaceholderText("Buscar por Nombre de Empresa o NIT...")
        self.input_buscar_empresa.setStyleSheet(
            "padding: 8px; border: 1px solid #CCC; border-radius: 5px; font-size: 11pt;")
        self.input_buscar_empresa.setMinimumWidth(300)

        # Botón para simular la acción de VER EMPRESA (doble clic en la tabla)
        self.btn_ver_empresa_seleccionada = QPushButton("Ver Opciones (Doble Clic)")
        self.btn_ver_empresa_seleccionada.setStyleSheet(
            "background-color: #4CAF50; color: white; padding: 10px; font-size: 12pt; font-weight: bold; border-radius: 5px;")

        control_layout.addWidget(self.input_buscar_empresa)
        control_layout.addStretch()
        control_layout.addWidget(self.btn_ver_empresa_seleccionada)

        main_layout.addWidget(control_frame)










    #-------------------------------------------------------
    # AGREGANDO FUNCION DE: DISEÑO GESTIONAR EMPRESAS (PAGINA 9 DLE BOCETO DEL CANVA)
    #-------------------------------------------------------
    def setup_gestion_empresas_ui(self):
        # Layout principal de la página de Gestionar Empresas (Índice 2 del dashboard_stacked_widget)
        main_layout = QHBoxLayout(self.dashboard_empresas_page)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 1. Menú de Empresas (Sidebar interno)
        menu_frame = QFrame()
        menu_frame.setFixedWidth(200)
        menu_frame.setStyleSheet("background-color: #F0F0F0; border-right: 1px solid #CCC;")

        menu_layout = QVBoxLayout(menu_frame)
        menu_layout.setAlignment(Qt.AlignTop)

        # Título del Sub-menú
        label_titulo = QLabel("Gestión de Empresas")
        label_titulo.setStyleSheet("font-size: 16pt; font-weight: bold; padding: 20px 10px; color: #4B0082;")
        menu_layout.addWidget(label_titulo)

        # BOTONES DE NAVEGACION INTERNA (PAGINA 9 DEL BOCETO DE CANVA)
        self.btn_crear_empresa = QPushButton("CREAR EMPRESA")
        self.btn_modificar_empresa = QPushButton("MODIFICAR INFO")
        self.btn_eliminar_empresa = QPushButton("ELIMINAR EMPRESA")

        menu_btn_style = (
            "QPushButton { background-color: transparent; color: black; "
            "border: none; padding: 15px 5px; text-align: left; font-size: 12pt;}"
            "QPushButton:hover { background-color: #E0E0E0; border-left: 5px solid #6A1B9A; }"
        )
        self.btn_crear_empresa.setStyleSheet(menu_btn_style)
        self.btn_modificar_empresa.setStyleSheet(menu_btn_style)
        self.btn_eliminar_empresa.setStyleSheet(menu_btn_style)

        menu_layout.addWidget(self.btn_crear_empresa)
        menu_layout.addWidget(self.btn_modificar_empresa)
        menu_layout.addWidget(self.btn_eliminar_empresa)
        menu_layout.addStretch()

        # 2. Área de Contenido de Empresas (Tercer QStackedWidget)
        self.empresas_stacked_widget = QStackedWidget()
        self.empresas_stacked_widget.setStyleSheet("background-color: white; padding: 10px;")

        # --- VISTAS INTERNAS DE EMPRESAS ---
        self.empresas_vacio_page = QWidget()  # Sub-página 0: Vacio/Inicial
        self.empresas_crear_page = QWidget()  # Sub-página 1: Crear Empresa (Página 10 del PDF)
        self.empresas_modificar_page = QWidget()  # Sub-página 2: Modificar Empresa
        self.empresas_eliminar_page = QWidget()  # Sub-página 3: Eliminar Empresa

        self.empresas_stacked_widget.addWidget(self.empresas_vacio_page)
        self.empresas_stacked_widget.addWidget(self.empresas_crear_page)
        self.empresas_stacked_widget.addWidget(self.empresas_modificar_page)
        self.empresas_stacked_widget.addWidget(self.empresas_eliminar_page)

        # 3. Ensamblaje Final
        main_layout.addWidget(menu_frame)
        main_layout.addWidget(self.empresas_stacked_widget)

        # Iniciar mostrando la página de crear empresa por defecto
        self.empresas_stacked_widget.setCurrentIndex(1)

        # Diseño del formulario de Crear Empresa
        self.setup_formulario_crear_empresa()

    def setup_formulario_crear_empresa(self):
        '''
        Diseño del formulario de crear empresa (página 10 del boceto de canva)
        Combina los campos de cliente (dueño) y empresa.
        '''

        form_layout = QVBoxLayout(self.empresas_crear_page)
        form_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        titulo = QLabel("Crear nueva empresa")
        titulo.setStyleSheet("font-size: 24pt; color: #4B0082; margin-bottom: 20px; font-weight: bold;")
        form_layout.addWidget(titulo, alignment=Qt.AlignCenter)

        # Marco del Formulario
        formulario_frame = QFrame()
        formulario_frame.setMinimumWidth(650)
        formulario_frame.setStyleSheet("background-color: #F8F8F8; border-radius: 10px; padding: 25px;")

        grid_layout = QGridLayout(formulario_frame)
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(15)

        # Estilo común para inputs
        input_style = "QLineEdit { padding: 8px; border: 1px solid #CCC; border-radius: 5px; font-size: 11pt; }"

        #--------------------seccion de empresa columna 1 ---------------------------------------------------------
        grid_layout.addWidget(QLabel("### Datos de la Empresa", styleSheet="font-weight: bold; color: #4B0082;"), 0, 0, 1, 2)

        grid_layout.addWidget(QLabel("Nombre de la Empresa:"), 1, 0)
        self.input_nombre_empresa = QLineEdit()
        self.input_nombre_empresa.setStyleSheet(input_style)
        self.input_nombre_empresa.setPlaceholderText("Ej: Panadería El Sol")
        grid_layout.addWidget(self.input_nombre_empresa, 1, 1)

        grid_layout.addWidget(QLabel("Dirección de la Empresa:"), 2, 0)
        self.input_direccion_empresa = QLineEdit()
        self.input_direccion_empresa.setStyleSheet(input_style)
        grid_layout.addWidget(self.input_direccion_empresa, 2, 1)

        # Separador para claridad
        grid_layout.addItem(QSpacerItem(20, 20), 3, 0)


        #------------------------SECCION DE CLIENTE / PROPIETARIO (COLUMNA 2)-------------
        grid_layout.addWidget(QLabel("### Datos del Cliente/Propietario", styleSheet="font-weight: bold; color: #4B0082;"), 4, 0, 1, 2)

        grid_layout.addWidget(QLabel("NIT del Cliente:"), 5, 0)
        self.input_nit_cliente = QLineEdit()
        self.input_nit_cliente.setStyleSheet(input_style)
        self.input_nit_cliente.setPlaceholderText("NIT del dueño (Clave para empresa)")
        grid_layout.addWidget(self.input_nit_cliente, 5, 1)

        grid_layout.addWidget(QLabel("Nombre del Propietario/Jefe:"), 6, 0)
        self.input_nombre_jefe = QLineEdit()
        self.input_nombre_jefe.setStyleSheet(input_style)
        grid_layout.addWidget(self.input_nombre_jefe, 6, 1)

        grid_layout.addWidget(QLabel("DPI del Propietario:"), 7, 0)
        self.input_dpi_propietario = QLineEdit()
        self.input_dpi_propietario.setStyleSheet(input_style)
        grid_layout.addWidget(self.input_dpi_propietario, 7, 1)

        grid_layout.addWidget(QLabel("Teléfono:"), 8, 0)
        self.input_telefono_propietario = QLineEdit()
        self.input_telefono_propietario.setStyleSheet(input_style)
        grid_layout.addWidget(self.input_telefono_propietario, 8, 1)

        grid_layout.addWidget(QLabel("Correo:"), 9, 0)
        self.input_correo_propietario = QLineEdit()
        self.input_correo_propietario.setStyleSheet(input_style)
        grid_layout.addWidget(self.input_correo_propietario, 9, 1)

        grid_layout.addWidget(QLabel("Fecha de Nacimiento:"), 10, 0)
        self.input_fecha_nacimiento_propietario = QLineEdit()
        self.input_fecha_nacimiento_propietario.setStyleSheet(input_style)
        self.input_fecha_nacimiento_propietario.setPlaceholderText("AAAA-MM-DD")
        grid_layout.addWidget(self.input_fecha_nacimiento_propietario, 10, 1)

        # Botón CREAR EMPRESA
        self.btn_crear_empresa_submit = QPushButton("CREAR EMPRESA")
        self.btn_crear_empresa_submit.setStyleSheet("background-color: #4B0082; color: white; padding: 12px; font-size: 14pt; font-weight: bold; border-radius: 5px; margin-top: 20px;")

        # Agregamos el formulario a la página
        form_layout.addWidget(formulario_frame, alignment=Qt.AlignCenter)
        form_layout.addWidget(self.btn_crear_empresa_submit, alignment=Qt.AlignCenter)
        form_layout.addStretch()




# --- 2. CLASE CONTROLADORA PRINCIPAL --- (Se conecta la lógica de navegación y formulario) ---
class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Sistema de Gestión Contable - PySide6")

        # Atributos para guardar la sesión
        self.usuario_activo = None
        self.rol_activo = None
        self.auditor = None # objeto que sirve para interactuar con la lógica de negocio
        self.user_model = None # modelo de datos para la tabla de usuarios

        # Conexiones: Conectar el botón 'Ingresar' a la función de validación
        # nos referimos al login
        self.ui.btn_ingresar.clicked.connect(self.handle_login)

        # Nuevas conexiones de navegacion del Dashboard, agregamos nuevas conexiones
        self.ui.btn_gestionar_usuarios.clicked.connect(lambda: self.navigate_dashboard(1))
        self.ui.btn_gestionar_empresa.clicked.connect(lambda: self.navigate_dashboard(2))
        self.ui.btn_ver_empresas.clicked.connect(lambda: self.navigate_dashboard(3))

        # NUEVAS CONEXIONES --->Conexiones de Navegación del MÓDULO USUARIOS
        self.ui.btn_crear_usuario.clicked.connect(lambda: self.navigate_usuarios(1))
        self.ui.btn_modificar_usuarios.clicked.connect(lambda: self.navigate_usuarios(2))
        #self.ui.btn_eliminar_usuarios.clicked.connect(lambda: self.navigate_usuarios(3))

        #conexion especial: navegar y listar usuarios
        self.ui.btn_eliminar_usuarios.clicked.connect(self.handle_listar_usuarios)


        # CONEXION DEL FORMULARIO DE CREAR EMPRESA, CONEXION NUEVA EN LA ACTUALIZACION 3
        self.ui.btn_crear_usuario_submit.clicked.connect(self.handle_crear_usuario)

        # conexion de lsitar / eliminar usuarios
        self.ui.btn_eliminar_seleccionado.clicked.connect(self.handle_eliminar_usuario)

        # --- CONEXIONES NUEVAS DE MODIFICAR USUARIOS ---
        self.ui.btn_buscar_usuario_modificar.clicked.connect(self.handle_buscar_usuario)
        self.ui.btn_guardar_modificacion.clicked.connect(self.handle_guardar_modificacion)

        # Conexiones de Navegación del MÓDULO EMPRESAS <--- NUEVAS CONEXIONES
        self.ui.btn_crear_empresa.clicked.connect(lambda: self.navigate_empresas(1))
        self.ui.btn_modificar_empresa.clicked.connect(lambda: self.navigate_empresas(2))
        self.ui.btn_eliminar_empresa.clicked.connect(lambda: self.navigate_empresas(3))

        # conexion del formulario CREAR USUARIO <---  APLICANDO CONEXION DE LÓGICA
        self.ui.btn_crear_empresa_submit.clicked.connect(self.handle_crear_empresa)

        # Establecer la primera vista: Login
        self.ui.stackedWidget.setCurrentIndex(0)


    # AGREGANDO NUEVO MÉTODO NAVEGACION INTERNA DE LAS EMPRESAS---------------
    def navigate_empresas(self, index):
        # Cambia la sub-página visible dentro del QStackedWidget de Gestión de Empresas.
        self.ui.empresas_stacked_widget.setCurrentIndex(index)

    # CREANDO  METODO RESPECTIVO QUE CONECTA EL FORMULARIO DE EMPRESA A LA LOGICA EN PROYECTO_2.PY
    def handle_crear_empresa(self):
        if not self.auditor:
            QMessageBox.critical(self, "Error de Permisos", "Operación no permitida. Inicie sesión como Administrador.")
            return

        # 1. Recolección de datos del CLIENTE/PROPIETARIO (Lógica 1)
        nit_cliente = self.ui.input_nit_cliente.text().strip()
        nombre_jefe = self.ui.input_nombre_jefe.text().strip()
        telefono = self.ui.input_telefono_propietario.text().strip()
        correo = self.ui.input_correo_propietario.text().strip()
        dpi = self.ui.input_dpi_propietario.text().strip()
        fecha_nacimiento = self.ui.input_fecha_nacimiento_propietario.text().strip()

        # 2. Recolección de datos de la EMPRESA (Lógica 2)
        nombre_empresa = self.ui.input_nombre_empresa.text().strip()
        direccion_empresa = self.ui.input_direccion_empresa.text().strip()

        # Validación mínima
        if not all([nombre_empresa, nit_cliente, nombre_jefe]):
            QMessageBox.warning(self, "Error de Entrada","El Nombre de Empresa, NIT del Cliente y Nombre del Propietario son obligatorios.")
            return

        try:
            # PRIMER PASO: Crear el cliente/propietario (si no existe)
            # Nota: El método crear_cliente en la parte lógica de (Proyecto_2.py) retorna False si ya existe.
            cliente_creado = self.auditor.crear_cliente(
                nit=nit_cliente,
                nombre=nombre_jefe,
                telefono=telefono,
                correo=correo,
                dpi=dpi,
                fecha_nacimiento=fecha_nacimiento
            )

            if not cliente_creado:
                # Si no se creó, asumimos que ya existe, lo cual es válido si se quiere usar un cliente existente.
                QMessageBox.information(self, "Advertencia",f"El cliente con NIT {nit_cliente} ya existía en la base de datos. Se procederá a crear la empresa con este NIT.")

            # SEGUNDO PASO: Crear la empresa, vinculándola al NIT del cliente
            empresa_creada = self.auditor.crear_empresa(
                nombre_empresa=nombre_empresa,
                nit_cliente=nit_cliente,
                direccion=direccion_empresa
            )

            if empresa_creada:
                QMessageBox.information(self, "Éxito",f"Empresa '{nombre_empresa}' creada y vinculada al cliente NIT {nit_cliente} correctamente.")
                # Limpiar el formulario
                self.ui.input_nombre_empresa.clear()
                self.ui.input_direccion_empresa.clear()
                self.ui.input_nit_cliente.clear()
                self.ui.input_nombre_jefe.clear()
                self.ui.input_dpi_propietario.clear()
                self.ui.input_telefono_propietario.clear()
                self.ui.input_correo_propietario.clear()
                self.ui.input_fecha_nacimiento_propietario.clear()
            else:
                QMessageBox.critical(self, "Error",f"La empresa '{nombre_empresa}' ya existe o hubo un error al vincularla a la DB.")
        except Exception as e:
            QMessageBox.critical(self, "Error de Lógica", f"Ocurrió un error general: {e}")




    # --- MÉTODO PARA CONECTAR EL FORMULARIO A LA LÓGICA (Auditor) ---
    # Recoge datos del formulario y llama al método crear_usuario del Auditor.
    # Verificación de auditor activo (esto solo debería ejecutarse si el rol es Admin)
    def handle_crear_usuario(self):
        if not self.auditor:
            QMessageBox.critical(self, "Error de Permisos","Operación no permitida. Inicie sesión como Administrador.")
            return

        # REcoleccion de datos
        nombre = self.ui.input_nombre_completo.text()
        dpi = self.ui.input_dpi.text()
        correo = self.ui.input_correo.text()
        puesto = self.ui.input_puesto.text()
        usuario = self.ui.input_usuario.text()
        contrasena = self.ui.input_contrasena.text()
        rol = self.ui.combo_rol.currentText()
        telefono = self.ui.input_telefono.text()
        fecha_nacimiento = self.ui.input_fecha_nacimiento.text()  # Nota: La validación de formato debe ser implementada

        # Simple validación de campos obligatorios
        if not all([nombre, dpi, usuario, contrasena]):
            QMessageBox.warning(self, "Error de Entrada","Los campos Nombre, DPI, Usuario y Contraseña son obligatorios.")
            return

        # Llama a tu lógica de negocio
        try:
            exito = self.auditor.crear_usuario(nombre=nombre, dpi=dpi, correo=correo, puesto=puesto, usuario=usuario,contrasena=contrasena, rol=rol)
            # Tu clase Auditor requiere 5 argumentos en el init. Para crear un usuario,
            # llamamos al método crear_usuario que ya definiste en tu lógica.

            # La lógica de PySide no necesita una instancia de Auditor real, solo una
            # si la usamos para todas las operaciones. En tu código, la clase Auditor
            # hereda de Usuario y tiene un constructor.
            # Como ya tenemos una instancia (self.auditor), la usamos:

            if exito:
                QMessageBox.information(self, "Éxito", f"Usuario '{usuario}' creado correctamente.")
                # Limpiar el formulario después del éxito
                self.ui.input_nombre_completo.clear()
                self.ui.input_dpi.clear()
                self.ui.input_correo.clear()
                self.ui.input_puesto.clear()
                self.ui.input_usuario.clear()
                self.ui.input_contrasena.clear()
                self.ui.input_telefono.clear()
                self.ui.input_fecha_nacimiento.clear()

            else:
                QMessageBox.warning(self, "Error", "El usuario ya existe o hubo un error en la base de datos.")

        except Exception as e:
            QMessageBox.critical(self, "Error de Lógica", f"Ocurrió un error al intentar crear el usuario: {e}")


    def handle_listar_usuarios(self):
        # muestra la lista de usuarios en el QTableview y navega a la pagina
        self.navigate_usuarios(3)

        if not self.auditor:
            QMessageBox.critical(self, "Error", "Debe iniciar sesión como Admin para ver esta lista.")
            return

        try:
            # Asumimos que listar_usuarios() devuelve una lista de diccionarios.
            lista_usuarios = self.auditor.listar_usuarios()
        except AttributeError:
            QMessageBox.critical(self, "Error de Lógica","El método listar_usuarios() no está implementado en la clase Auditor.")
            return
        except Exception as e:
            QMessageBox.critical(self, "Error de Lógica", f"Error al obtener usuarios: {e}")
            return

        if not lista_usuarios:
            self.ui.tabla_usuarios.setModel(None)
            QMessageBox.information(self, "Información", "No hay usuarios registrados en el sistema.")
            return

        # 1. Setup/Clear el Modelo
        if not self.user_model:
            self.user_model = QStandardItemModel()
            self.ui.tabla_usuarios.setModel(self.user_model)

        self.user_model.clear()

        # Define cabeceras
        headers = ["DPI", "Nombre Completo", "Usuario", "Rol", "Correo"]
        self.user_model.setHorizontalHeaderLabels(headers)

        # 2. Poblar el modelo
        for user_data in lista_usuarios:
            row_items = []
            row_items.append(QStandardItem(str(user_data.get('dpi', 'N/A'))))
            row_items.append(QStandardItem(str(user_data.get('nombre', 'N/A'))))
            row_items.append(QStandardItem(str(user_data.get('usuario', 'N/A'))))
            row_items.append(QStandardItem(str(user_data.get('rol', 'N/A'))))
            row_items.append(QStandardItem(str(user_data.get('correo', 'N/A'))))
            self.user_model.appendRow(row_items)

        # 3. Ajustar vista de la tabla
        self.ui.tabla_usuarios.horizontalHeader().setStretchLastSection(True)
        self.ui.tabla_usuarios.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tabla_usuarios.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)


    def handle_eliminar_usuario(self):
        if not self.auditor:
            QMessageBox.critical(self,"Error", "Debe iniciar sesión con Admin.")
            return

        # obtener el indice de la fila seleccionada
        selected_indexes = self.ui.tabla_usuarios.selectionModel().selectedRows()

        if not selected_indexes:
            QMessageBox.warning(self,"Advertencia", "Por favor seleccione un usuario de la lista para eliminar.")
            return

        # Obtener el DPI del usuario seleccionado (columna 0)
        selected_row = selected_indexes[0].row()
        dpi_item = self.user_model.item(selected_row, 0)
        dpi_a_eliminar = dpi_item.text()

        # Diálogo de confirmación
        reply = QMessageBox.question(
            self,
        'Confirmar Eliminación',
        f"¿Está seguro que desea eliminar al usuario con DPI: {dpi_a_eliminar}? Esta acción es irreversible.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            #
            #llamamos a la logica de negocio
            try:
                exito = self.auditor.eliminar_usuario(dpi_a_eliminar)

                if exito:
                    QMessageBox.information(self, "Exito",
                                            f"Usuario con DPI: {dpi_a_eliminar}, eliminado correctamente.")
                    # recargamos la lista
                    self.handle_listar_usuarios()
                else:
                    QMessageBox.critical(self, "Error", "No se pudo eliminar el usuario. El DPI no fue encontrado.")
            except AttributeError:
                QMessageBox.critical(self, "Error de logica",
                                     "El método eliminar_usuario(dpi) no está implementado en la clase Auditor.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar: {e}")



    def handle_buscar_usuario(self):
        if not self.auditor:
            QMessageBox.critical(self, "Error", "Debe iniciar sesión como Admin.")
            return

        busqueda = self.ui.input_buscar_modificar.text().strip()
        if not busqueda:
            QMessageBox.warning(self, "Advertencia", "Ingrese el DPI o Nombre de Usuario a buscar.")
            return

        try:
            # Asume que buscar_usuario devuelve un diccionario con los datos del usuario
            datos_usuario = self.auditor.buscar_usuario(busqueda)
        except AttributeError:
            QMessageBox.critical(self, "Error de Lógica",
                                 "El método buscar_usuario() no está implementado en la clase Auditor.")
            return
        except Exception as e:
            QMessageBox.critical(self, "Error de Búsqueda", f"Ocurrió un error: {e}")
            return

        if datos_usuario:
            self.dpi_usuario_modificando = datos_usuario.get("dpi")

            # Rellenar formulario
            self.ui.mod_dpi.setText(datos_usuario.get("dpi", ""))
            self.ui.mod_nombre_completo.setText(datos_usuario.get("nombre", ""))
            self.ui.mod_correo.setText(datos_usuario.get("correo", ""))
            self.ui.mod_puesto.setText(datos_usuario.get("puesto", ""))
            self.ui.mod_usuario.setText(datos_usuario.get("usuario", ""))
            self.ui.mod_contrasena.setText(datos_usuario.get("contrasena", ""))
            self.ui.mod_telefono.setText(datos_usuario.get("telefono", ""))
            self.ui.mod_fecha_nacimiento.setText(datos_usuario.get("fecha_nacimiento", ""))

            # Seleccionar el ROL
            rol = datos_usuario.get("rol", "Usuario")
            index = self.ui.mod_combo_rol.findText(rol, Qt.MatchFixedString)
            if index >= 0:
                self.ui.mod_combo_rol.setCurrentIndex(index)

            self.ui.form_modificar_frame.setHidden(False)
            QMessageBox.information(self, "Éxito", f"Usuario {datos_usuario.get('nombre')} cargado para modificación.")
        else:
            self.ui.form_modificar_frame.setHidden(True)
            QMessageBox.information(self, "No Encontrado",f"No se encontró ningún usuario con el DPI/Usuario: {busqueda}")


    def handle_guardar_modificacion(self):
        # recoge los datos del formulario de modificaciones y llama a la logica del negocio
        if not self.auditor or not self.dpi_usuario_modificando:
            QMessageBox.critical(self,"Error", "No hay un usuario cargado o no tiene permisos.")
            return

        # parte de recoleccion de datos para guardar la modificacion hecha por el ususairo
        datos_a_modificar = {
            "dpi_original": self.dpi_usuario_modificando,  # Clave para la modificación
            "nombre": self.ui.mod_nombre_completo.text(),
            "correo": self.ui.mod_correo.text(),
            "puesto": self.ui.mod_puesto.text(),
            "usuario": self.ui.mod_usuario.text(),
            "contrasena": self.ui.mod_contrasena.text(),
            "rol": self.ui.mod_combo_rol.currentText(),
            "telefono": self.ui.mod_telefono.text(),
            "fecha_nacimiento": self.ui.mod_fecha_nacimiento.text(),
        }

        # validacion simlple (nombre, usuario y contraseña)
        if not all([datos_a_modificar["nombre", datos_a_modificar]["usuario"],datos_a_modificar["contrasena"]]):
            QMessageBox.warning(self, "Error de Entrada", "Nombre, Usuario y Contraseña son obligatorios.")
            return

        try:
            exito = self.auditor.modificar_usuario(
                datos_a_modificar)  # Asume que modifica_usuario recibe el diccionario

            if exito:
                QMessageBox.information(self, "Éxito",
                                        f"Usuario con DPI {self.dpi_usuario_modificando} modificado correctamente.")
                self.handle_navigate_modificar_usuarios()  # Limpia y vuelve al estado inicial
            else:
                QMessageBox.critical(self, "Error",
                                     "Error al intentar guardar la modificación. El usuario pudo no existir.")
        except AttributeError:
            QMessageBox.critical(self, "Error de Lógica","El método modificar_usuario() no está implementado en la clase Auditor.")
        except Exception as e:
            QMessageBox.critical(self, "Error de Lógica", f"Ocurrió un error al modificar el usuario: {e}")



        # agregando nuevo método de navegacion DE USUARIOS
        # MÉTODO PARA CONECTAR EL FORMULARIO A LA LÓGICA (AUDITOR)
        #  Cambia la sub-página visible dentro del QStackedWidget de Gestión de Usuarios.

    def navigate_usuarios(self, index):
        self.ui.usuarios_stacked_widget.setCurrentIndex(index)

    def navigate_dashboard(self, index):
        #Cambia la sub-página visible dentro del QStackedWidget del Dashboard.
        self.ui.dashboard_stacked_widget.setCurrentIndex(index)

    def handle_login(self):
        #Maneja el evento del botón Ingresar, llama a la lógica y gestiona la transición de la UI.
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

            # Si el login es exitoso y es Admin, creamos una instancia del Auditor
            if self.rol_activo.lower() in ["admin", "auditor"]:
                # Nota: Necesitas datos (nombre, dpi, correo, usuario, contrasena) para Auditor.__init__
                # Usaremos datos dummy del login por ahora, o buscaríamos el objeto completo.
                # Asumimos que el usuario 'contador' es el administrador principal:
                if username == "contador":
                    self.auditor = Auditor("Administrador", "0000000000000", "admin@app.com", "contador", "contador123")
                else:
                    # En un sistema real, buscarías todos los datos del usuario_activo
                    self.auditor = Auditor(
                        self.usuario_activo.get("nombre", "Usuario"),
                        self.usuario_activo.get("dpi", ""),
                        self.usuario_activo.get("correo", ""),
                        self.usuario_activo.get("usuario", ""),
                        self.usuario_activo.get("contrasena", "")
                    )
            self.ui.username_input.clear()
            self.ui.password_input.clear()

            self.ui.label_bienvenida.setText(f"Bienvenido/a, {self.usuario_activo.get('nombre', 'Admin')}!")
            self.ui.stackedWidget.setCurrentIndex(1)

        elif resultado == "salir":
            QMessageBox.information(self, "Sesión", "Comando de salida detectado.")
            self.close()

        else:
            QMessageBox.critical(self, "Error de Acceso", "Usuario o contraseña incorrectos.")
            self.ui.password_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
# Fin del archivo Interfaz.py