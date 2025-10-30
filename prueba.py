import mysql.connector
from datetime import datetime, date

# --- Funciones de ordenamiento y búsqueda ---
def busqueda_binaria(lista, indice, valor):
    inicio = 0
    fin = len(lista) - 1
    while inicio <= fin:
        medio = (inicio + fin) // 2
        if lista[medio][indice] == valor:
            return lista[medio]
        elif lista[medio][indice] < valor:
            inicio = medio + 1
        else:
            fin = medio - 1
    return -1

def busqueda_secuencial(lista, indice, valor):
    for x in lista:
        if x[indice] == valor:
            return x
    return -1

def metodo_bubble_sort(lista, indice=1):
    datos = list(lista)
    numero = len(datos)
    for i in range(numero):
        cambio = False
        for j in range(0, numero - i - 1):
            if datos[j][indice] > datos[j + 1][indice]:
                datos[j], datos[j + 1] = datos[j + 1], datos[j]
                cambio = True
        if not cambio:
            break
    return datos

def metodo_selection_sort(lista, indice=1):
    lista_ordenar = list(lista)
    for i in range(len(lista_ordenar)-1):
        menor = i
        for j in range(i+1, len(lista_ordenar)):
            if lista_ordenar[j][indice] < lista_ordenar[menor][indice]:
                menor = j
        lista_ordenar[i], lista_ordenar[menor] = lista_ordenar[menor], lista_ordenar[i]
    return lista_ordenar

# --- Conexión a la base de datos ---
class BasedeDatos:
    @staticmethod
    def conectar():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Wilson200.",
            database="mono_prueba"
        )

# --- Normalización de nombres ---
def normalizar_nombre(nombre):
    nombre_empresa = nombre.strip().lower()
    nombre_empresa = "_".join(nombre_empresa.split())
    resultado = ""
    for x in nombre_empresa:
        if x.isalnum() or x == "_":
            resultado += x
    if not resultado:
        resultado = "empresa"
    return resultado[:50]  # evitar nombres de tabla muy largos

# --- Clases principales ---
class Usuario:
    def __init__(self, nombre, dpi, correo, puesto, usuario, contrasena, rol):
        self.__nombre = nombre
        self.__dpi = dpi
        self._correo = correo
        self._puesto = puesto
        self.__usuario = usuario
        self.__contrasena = contrasena  # texto plano
        self._rol = rol

    @staticmethod
    def _conn():
        conn = BasedeDatos.conectar()
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(255) NOT NULL,
                    dpi VARCHAR(50),
                    correo VARCHAR(255),
                    puesto VARCHAR(50),
                    usuario VARCHAR(255) UNIQUE NOT NULL,
                    contrasena VARCHAR(255) NOT NULL,
                    rol VARCHAR(50) NOT NULL
                );
            """)
            conn.commit()
        return conn

    def guardar(self):
        conn = self._conn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO usuarios (nombre, dpi, correo, puesto, usuario, contrasena, rol) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (self.__nombre, self.__dpi, self._correo, self._puesto, self.__usuario, self.__contrasena, self._rol)
                )
                conn.commit()
                print(f"✅ Usuario '{self.__usuario}' guardado con éxito.")
        finally:
            conn.close()

class Cliente:
    def __init__(self, nit, nombre, telefono="", correo="", direccion="", dpi="", fecha_nacimiento=None, nombre_negocio=""):
        self._nit = nit
        self._nombre = nombre
        self._telefono = telefono
        self._correo = correo
        self._direccion = direccion
        self._dpi = dpi
        self._nombre_negocio = nombre_negocio

        # Convertir string a date si es necesario
        if isinstance(fecha_nacimiento, str):
            try:
                self._fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
            except ValueError:
                print(f"⚠ Fecha inválida '{fecha_nacimiento}', se asignará None")
                self._fecha_nacimiento = None
        else:
            self._fecha_nacimiento = fecha_nacimiento

    @staticmethod
    def _crear_tabla():
        conn = BasedeDatos.conectar()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS clientes (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nit VARCHAR(50) UNIQUE NOT NULL,
                        nombre VARCHAR(255) NOT NULL,
                        telefono VARCHAR(20),
                        correo VARCHAR(255),
                        direccion TEXT,
                        dpi VARCHAR(50),
                        fecha_nacimiento DATE,
                        nombre_negocio VARCHAR(255)
                    );
                """)
                conn.commit()
        finally:
            conn.close()

    def guardar(self):
        Cliente._crear_tabla()  # asegurarse que tabla existe
        conn = BasedeDatos.conectar()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM clientes WHERE nit=%s", (self._nit,))
                if cursor.fetchone():
                    print(f"⚠ Cliente con NIT '{self._nit}' ya existe.")
                    return False
                cursor.execute(
                    "INSERT INTO clientes (nit, nombre, telefono, correo, direccion, dpi, fecha_nacimiento, nombre_negocio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (self._nit, self._nombre, self._telefono, self._correo, self._direccion, self._dpi, self._fecha_nacimiento, self._nombre_negocio)
                )
                conn.commit()
                print(f"✅ Cliente '{self._nombre}' guardado con éxito.")
                return True
        finally:
            conn.close()

class Empresa:
    def __init__(self, nombre, nit_cliente, direccion=""):
        self._nombre = nombre
        self._nit_cliente = nit_cliente
        self._direccion = direccion
        self.tabla_inventario = "inventario_" + normalizar_nombre(self._nombre)
        self.tabla_facturas = "facturas_" + normalizar_nombre(self._nombre)

    @staticmethod
    def _crear_tabla():
        Cliente._crear_tabla()  # Asegurarse que clientes existe
        conn = BasedeDatos.conectar()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS empresas (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nombre VARCHAR(200) NOT NULL,
                        nit_cliente VARCHAR(60),
                        direccion VARCHAR(255),
                        FOREIGN KEY (nit_cliente) REFERENCES clientes(nit) ON DELETE SET NULL
                    );
                """)
                conn.commit()
        finally:
            conn.close()

    def guardar(self):
        Empresa._crear_tabla()  # asegurarse que tabla existe
        conn = BasedeDatos.conectar()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO empresas (nombre, nit_cliente, direccion) VALUES (%s, %s, %s)",
                    (self._nombre, self._nit_cliente, self._direccion)
                )
                conn.commit()

                # Crear tabla de inventario propia
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.tabla_inventario} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        producto VARCHAR(100) NOT NULL,
                        cantidad INT NOT NULL,
                        precio FLOAT NOT NULL
                    );
                """)

                # Crear tabla de facturas propia
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.tabla_facturas} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        no_factura VARCHAR(50),
                        nit_cliente VARCHAR(50),
                        monto FLOAT,
                        fecha DATE
                    );
                """)
                conn.commit()
                print(f"✅ Empresa '{self._nombre}' registrada y tablas creadas.")
                return True
        finally:
            conn.close()

class Auditor(Usuario):
    def __init__(self, nombre, dpi, correo, usuario, contrasena):
        super().__init__(nombre, dpi, correo, "Auditor", usuario, contrasena, "Admin")

    def crear_cliente(self, nit, nombre, telefono="", correo="", direccion="", dpi="", fecha_nac=None, nombre_negocio=""):
        cliente = Cliente(nit, nombre, telefono, correo, direccion, dpi, fecha_nac, nombre_negocio)
        return cliente.guardar()

    def crear_empresa(self, nombre_empresa, nit_cliente, direccion=""):
        empresa = Empresa(nombre_empresa, nit_cliente, direccion)
        return empresa.guardar()

    def registrar_factura(self, empresa_nombre, no_factura, nit_cliente, monto, fecha=None):
        if not fecha:
            fecha = date.today()
        elif isinstance(fecha, str):
            try:
                fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
            except ValueError:
                print(f"⚠ Fecha inválida '{fecha}', se usará fecha de hoy.")
                fecha = date.today()

        tabla_facturas = "facturas_" + normalizar_nombre(empresa_nombre)
        conn = BasedeDatos.conectar()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO {tabla_facturas} (no_factura, nit_cliente, monto, fecha) VALUES (%s, %s, %s, %s)",
                    (no_factura, nit_cliente, monto, fecha)
                )
                conn.commit()
                print(f"✅ Factura '{no_factura}' registrada en {tabla_facturas}.")
                return True
        finally:
            conn.close()

# --- Ejemplo de funcionamiento ---
if __name__ == "__main__":
    print("=== SIMULACIÓN DEL SISTEMA CONTABLE ===")

    auditor = Auditor("Carlos", "123456789", "carlos@gmail.com", "admin", "admin123")

    # 1️⃣ Crear cliente
    auditor.crear_cliente(
        "5678",
        "Juan Pérez",
        "5555-5555",
        "juan@gmail.com",
        "Zona 1",
        "987654321",
        "1990-05-10",
        "El Super"
    )

    # 2️⃣ Crear empresa del cliente
    auditor.crear_empresa("Ferretería La Esperanza", "5678", "Zona 10")

    # 3️⃣ Registrar una factura para esa empresa
    auditor.registrar_factura("Ferretería La Esperanza", "F001", "5678", 2500.75)

    print("✅ Todo funcionando correctamente.")


