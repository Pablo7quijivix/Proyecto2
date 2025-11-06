#----------------------------------------------------------------------------------------
import customtkinter as ctk
from tkinter import messagebox
import mysql.connector

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
DB_CONFIG = {
    'host':'localhost',
    'user':'root',
    'password':'rufisbb7',
    'database':'prueba2',
    'port': '3306'
}
# ------------------------------------------

# Configuración inicial de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
MORADO_FONDO = "#4B0082"
COLOR_BOTON_GUARDAR = "#008000"  # Verde


# =======================================================
# 1. GESTOR DE BASE DE DATOS (MySQLConnector)
# =======================================================

class MySQLConnector:
    """Clase para manejar las operaciones CRUD de la base de datos."""

    def __init__(self, config):
        self.config = config
        self.columnas_db = ["nombre", "dpi", "correo", "puesto", "usuario", "contrasena", "rol"]
        self.tabla = "personal"
        self.conn = None
        self.cursor = None
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Conexión a MySQL", f"No se pudo conectar a la base de datos: {err}")

    def actualizar_registro_por_id(self, registro_id, nuevos_datos):
        """Actualiza un solo registro por su ID."""
        if not self.conn: return 0

        campos_a_actualizar = [f"{col} = %s" for col in self.columnas_db]
        set_clause = ', '.join(campos_a_actualizar)
        query = f"UPDATE {self.tabla} SET {set_clause} WHERE ID = %s"

        # El orden de los datos debe ser: [nombre, dpi, ..., rol] + [ID]
        datos_para_sql = nuevos_datos + [registro_id]

        try:
            self.cursor.execute(query, datos_para_sql)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            messagebox.showerror("Error de Actualización", f"Error al actualizar registro {registro_id}: {e}")
            self.conn.rollback()
            return 0


# =======================================================
# 2. VENTANA MODAL DE EDICIÓN (CTkToplevel)
# =======================================================

class UserEditDialog(ctk.CTkToplevel):
    """Ventana modal para editar un solo usuario."""

    def __init__(self, parent_window, user_data, db_connector):
        super().__init__(parent_window)
        self.parent_window = parent_window
        self.user_data = user_data  # Diccionario con las llaves: 'ID', 'NOMBRE', 'DPI', ...
        self.db = db_connector

        self.title(f"Editar Usuario: {self.user_data['nombre']}")
        self.geometry("450x550")
        self.configure(fg_color="white")

        # Configurar como modal
        self.transient(parent_window)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.close_window)  # Manejar el cierre de la ventana

        self.column_names = list(self.user_data.keys())[1:]  # Excluir 'ID'
        self.entries = {}

        self._setup_form()

    def _setup_form(self):
        """Crea las etiquetas y campos de entrada para el formulario."""
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(padx=20, pady=20, fill="both", expand=True)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=3)

        # Mostrar ID de forma fija
        ctk.CTkLabel(form_frame, text=f"ID: {self.user_data['ID']}",
                     font=ctk.CTkFont(weight="bold"), text_color=MORADO_FONDO).grid(row=0, column=0, columnspan=2,
                                                                                    pady=(0, 15))

        # Crear campos de entrada para los datos
        for i, key in enumerate(self.column_names):
            # Usar 'nombre' de la columna en minúsculas para mapear a la base de datos.
            db_key = key.lower()
            current_value = self.user_data[key]

            ctk.CTkLabel(form_frame, text=f"{key.capitalize()}:", anchor="w",
                         text_color="black").grid(row=i + 1, column=0, padx=5, pady=(5, 0), sticky="w")

            entry = ctk.CTkEntry(form_frame, placeholder_text=f"Ingrese nuevo {db_key}")
            entry.insert(0, str(current_value))
            entry.grid(row=i + 1, column=1, padx=5, pady=(5, 0), sticky="ew")
            self.entries[db_key] = entry

        # Botón Guardar
        btn_save = ctk.CTkButton(self, text="GUARDAR CAMBIOS",
                                 command=self.save_changes,
                                 fg_color=COLOR_BOTON_GUARDAR,
                                 hover_color="#006400")
        btn_save.pack(pady=(0, 20), padx=20, fill="x")

    def save_changes(self):
        """Recopila los datos y llama a la función de actualización de la base de datos."""
        # Recopilar datos en el orden de las columnas de la BD (nombre, dpi, correo, ...)
        columnas_db_orden = self.db.columnas_db
        nuevos_datos_ordenados = [self.entries[col].get() for col in columnas_db_orden]

        if not all(nuevos_datos_ordenados):
            messagebox.showwarning("Advertencia", "Todos los campos deben estar llenos.")
            return

        registro_id = self.user_data['id']

        # 1. Llamar al método de la BD para actualizar
        actualizados = self.db.actualizar_registro_por_id(registro_id, nuevos_datos_ordenados)

        # 2. Mostrar resultado y cerrar
        if actualizados > 0:
            messagebox.showinfo("Éxito", f"Usuario '{self.user_data['nombre']}' actualizado correctamente.")
        else:
            # Puede ser 0 si no hubo cambios o si hubo un error de conexión
            if self.db.conn:
                messagebox.showinfo("Información", "No se detectaron cambios, o el registro no existe.")

        self.close_window()

    def close_window(self):
        """Cierra la ventana modal y libera el bloqueo."""
        self.grab_release()
        self.destroy()


# =======================================================
# 3. FUNCIÓN DE ENTRADA PÚBLICA (LLamada desde Dashboard)
# =======================================================

# Conexión Global (se inicializa solo una vez al importar el módulo)
db_connector = MySQLConnector(DB_CONFIG)


def abrir_ventana_edicion(parent_window, user_data):
    """
    Función llamada desde ModifyUsersPage para abrir la ventana de edición.
    :param parent_window: La instancia de ModifyUsersPage (self)
    :param user_data: Diccionario con los datos del usuario a editar.
    """
    if not db_connector.conn:
        messagebox.showerror("Error", "No se puede editar, la conexión a la base de datos falló al iniciar.")
        return

    # Crear y mostrar la ventana modal
    dialog = UserEditDialog(parent_window, user_data, db_connector)

    # Bloquea el resto de la aplicación hasta que se cierre
    parent_window.wait_window(dialog)

    # La página principal (ModifyUsersPage) debe recargar la tabla después de que la ventana se cierra
    # Esto ya está manejado en tu ModifyUsersPage.edit_user_action con self._setup_table()

# Opcional: Bloque de ejecución principal para pruebas
if __name__ == "__main__":
     class MockApp(ctk.CTk):
         def __init__(self):
            super().__init__()
            self.title("Ventana Principal de Prueba")
            self.geometry("300x200")
            btn = ctk.CTkButton(self, text="Abrir Edición", command=self.test_edit)
            btn.pack(pady=50)

         def test_edit(self):
             user = {'id': 5, 'nombre': 'Test User', 'dpi': '1234', 'correo': 'test@mail.com', 'puesto': 'Manager', 'usuario': 'testuser', 'contrasna': 'pass', 'rol': 'Admin'}
             abrir_ventana_edicion(self, user)

     if db_connector.conn:
         app = MockApp()
         app.mainloop()
     else:
        print("Conexión a BD fallida, la aplicación de prueba no se ejecutará.")