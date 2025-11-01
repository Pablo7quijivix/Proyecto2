import mysql.connector
from datetime import date

DB_Sistema= "sistema_empresa.db"
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

def busqueda_secuencial(lista,indice,valor):
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

def metodo_quick_sort(lista, indice=1):
    if len(lista) <= 1:
        return list(lista)
    pivote = lista[len(lista)//2][indice]
    menores = [x for x in lista if x[indice] < pivote]
    iguales = [x for x in lista if x[indice] == pivote]
    mayores = [x for x in lista if x[indice] > pivote]
    return metodo_quick_sort(menores, indice) + iguales + metodo_quick_sort(mayores, indice)

def meotod_selection_sort(lista, indice=1):
    lista_ordenar = list(lista)
    for i in range(len(lista_ordenar)-1):
        menor = i
        for j in range(i+1, len(lista_ordenar)):
            if lista_ordenar[j][indice] < lista_ordenar[menor][indice]:
                menor = j
        aux = lista_ordenar[i]
        lista_ordenar[i] = lista_ordenar[menor]
        lista_ordenar[menor] = aux
    return lista_ordenar

Conexion= ()
class BasedeDatos():
    @staticmethod
    def conectar():
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Wilson200.",
            database="prueba_10"
        )
        return conn
class Usuario:
    def __init__(self,nombre,dpi,correo,puesto,usuario,contrasena,rol):
        self.__nombre= nombre
        self.__dpi= dpi
        self._correo= correo
        self._puesto= puesto
        self.__usuario= usuario
        self.__contrasena= contrasena
        self._rol= rol
        Usuario._conn()

    @staticmethod
    def _conn():
        cursor = None
        conn = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor()
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
        except mysql.connector.Error as e:
            print(f"Ocurrio un error en la base de datos {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @property
    def nombre(self):
        return self.__nombre

    def puesto(self):
        return self._puesto

    @property
    def correo(self):
        return self._correo
    @correo.setter
    def correo(self,correo_nuevo):
        if "@" in correo_nuevo:
            self._correo = correo_nuevo
        else:
            print("Correo no valido..")

    @property
    def rol(self):
        return self._rol

    def guardar(self):
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE usuario=%s", (self.__usuario,))
            if cursor.fetchone():
                print(f"Usuario {self.__usuario} ya existe.")
                return False
            cursor.execute("""INSERT INTO usuarios (nombre, dpi, correo, puesto, usuario, contrasena, rol) VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (self.__nombre, self.__dpi, self._correo, self._puesto, self.__usuario, self.__contrasena, self._rol))
            conn.commit()
            print(f"Usuario {self.__usuario} guardado.")
            return True
        except mysql.connector.Error as e:
            print(f"Error al guardar usuario: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def mostrar_info(self):
        print(f"{self.nombre} ({self.puesto}) - Rol:{self.rol}")

reportes = {}
facturas = {}
inventario={}

class Auditor(Usuario):
    def __init__(self,nombre,dpi,correo,usuario,contrasena):
        super().__init__(nombre,dpi,correo,"Auditor",usuario,contrasena,"Admin")

    def mostrar_info(self):
        pass

    def crear_usuario(self, nombre, dpi, correo, puesto, usuario, contrasena, rol):
        u = Usuario(nombre, dpi, correo, puesto, usuario, contrasena, rol)
        return u.guardar()

    def crear_cliente(self, nit, nombre, telefono="", correo="", direccion="", dpi="", fecha_nacimiento="",nombre_negocio=""):
        cliente = Cliente(nit, nombre, telefono, correo, direccion, dpi, fecha_nacimiento, nombre_negocio)
        return cliente.guardar()

    def crear_empresa(self, nombre_empresa, nit_cliente, direccion=""):
        empresa = Empresa(nombre_empresa, nit_cliente, direccion)
        guardar = empresa.guardar()
        if guardar:
            if nombre_empresa not in reportes:
                reportes[nombre_empresa] = []
            if nombre_empresa not in facturas:
                facturas[nombre_empresa] = []
            if nombre_empresa not in inventario:
                inventario[nombre_empresa] = []
        return guardar

    def listar_empresas(self):
        return Empresa.listar()

    def listar_clientes(self):
        return Cliente.listar()

    def ver_inventario(self,nombre_empresa):
        return Inventario.listar(nombre_empresa)

    def modificar_inventario(self,nombre_empresa,producto,cantidad,precio):
        inventario = Inventario(nombre_empresa,producto,cantidad,precio)
        guardar = inventario.guardar()
        return guardar

    def registrar_factura(self, numero_factura, nit_cliente, empresa_nombre, monto, fecha=None):
        factura = Factura(numero_factura, nit_cliente, monto, fecha)
        guardar = factura.guardar(empresa_nombre)
        if guardar:
            if empresa_nombre not in facturas:
                facturas[empresa_nombre] = []
            facturas[empresa_nombre].append(factura)
        return guardar

class Empleado(Usuario):
    def __init__(self,nombre,dpi,correo,usuario,contrasena):
        super().__init__(nombre, dpi, correo, "Empleado", usuario, contrasena,"Usuario")

    def mostrar_info(self):
        pass


class Cliente:
    def __init__(self, nit, nombre, telefono="", correo="", direccion="", dpi="", fecha_nacimiento=None,nombre_negocio=""):
        self._nit = nit
        self._nombre = nombre
        self._telefono = telefono
        self._correo = correo
        self._direccion = direccion
        self._dpi = dpi
        self._fecha_nacimiento = fecha_nacimiento
        self.__nombre_negocio = nombre_negocio
        self._conn()

    @staticmethod
    def _conn():
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor()
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
        except mysql.connector.Error as e:
            print(f"Error al crear la tabla clientes: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    @property
    def nit(self):
        return self._nit

    @property
    def nombre(self):
        return self._nombre

    @property
    def nombre_negocio(self):
        return self.__nombre_negocio

    def guardar(self):
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clientes WHERE nit=%s", (self._nit,))
            if cursor.fetchone():
                print(f"⚠ Cliente con NIT {self._nit} ya existe.")
                return False
            cursor.execute("""INSERT INTO clientes (nit, nombre, telefono, correo, direccion, dpi, fecha_nacimiento, nombre_negocio)VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
             """, (self._nit, self._nombre, self._telefono, self._correo, self._direccion, self._dpi,
                   self._fecha_nacimiento,
                   self.__nombre_negocio))
            conn.commit()
            print(f"Cliente {self._nombre} guardado.")
            return True
        except mysql.connector.Error as e:
            print(f"Error al guardar cliente: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def listar():
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def mostrar_informacion(self):
        print(f"{self.nit} - {self.nombre} ({self.nombre_negocio})")

def normalizar_nombre(nombre):
    nombre_empresa = nombre.strip().lower()
    nombre_empresa = "_".join(nombre_empresa.split())
    resultado = ""
    for x in nombre_empresa:
        if ("a" <= x <= "z") or ("0" <= x <= "9") or x == "_":
            resultado += x
    if not resultado:
        resultado = "empresa"
    return resultado[:50]

class Empresa:
    def __init__(self, nombre, nit_cliente, direccion=""):
        self._nombre = nombre
        self._nit_cliente = nit_cliente
        self._direccion = direccion
        self.tabla_inventario = "inventario_" + normalizar_nombre(nombre)
        self.tabla_facturas = "facturas_" + normalizar_nombre(nombre)
        self._crear_tabla()

    def _crear_tabla(self):
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS empresas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(200) UNIQUE NOT NULL,
                    nit_cliente VARCHAR(60),
                    direccion VARCHAR(255),
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (nit_cliente) REFERENCES clientes(nit) ON DELETE SET NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventario_general (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    empresa_nombre VARCHAR(200) NOT NULL,
                    producto VARCHAR(200) NOT NULL,
                    cantidad INT NOT NULL,
                    precio DECIMAL(10,2) NOT NULL,
                    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_empresa (empresa_nombre),
                    INDEX idx_producto (producto)
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS facturas_general (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    empresa_nombre VARCHAR(200) NOT NULL,
                    no_factura VARCHAR(50) NOT NULL,
                    nit_cliente VARCHAR(50) NOT NULL,
                    monto DECIMAL(10,2) NOT NULL,
                    fecha DATE NOT NULL,
                    estado VARCHAR(20) DEFAULT 'Emitida',
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE KEY uk_factura_empresa (empresa_nombre, no_factura),
                    INDEX idx_empresa (empresa_nombre),
                    INDEX idx_fecha (fecha),
                    INDEX idx_cliente (nit_cliente)
                );
            """)
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error al crear tablas unificadas: {e}")
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def guardar(self):
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM empresas WHERE nombre=%s", (self._nombre,))
            if cursor.fetchone():
                print(f"Empresa {self._nombre} ya existe.")
                return False
            cursor.execute("INSERT INTO empresas (nombre, nit_cliente, direccion) VALUES (%s,%s,%s)",
                           (self._nombre, self._nit_cliente, self._direccion))
            conn.commit()
            print(f"Empresa {self._nombre} guardada.")
            return True
        except mysql.connector.Error as e:
            print(f"Error al guardar empresa: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def listar(nit_cliente=None):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        if nit_cliente:
            cursor.execute(
                "SELECT id, nombre, nit_cliente, direccion FROM empresas WHERE nit_cliente=%s",
                (nit_cliente,))
        else:
            cursor.execute(
                "SELECT id, nombre, nit_cliente, direccion FROM empresas")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

class Factura:
    def __init__(self,no_factura,nit_cliente,monto,fecha=None,estado="Emitida"):
        self.__no_factura = no_factura
        self.__nit_cliente = nit_cliente
        self._monto = monto
        self._fecha = fecha if fecha else date.today()
        self._estado = estado

    def informacion(self):
        print(f"Factura: {self.no_factura} | Clinte: {self.nit_cliente} | Monto: {self.monto} | fecha: {self.fecha} | Estado:{self.estado}")

    def guardar(self, empresa_nombre):
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO facturas_general (empresa_nombre, no_factura, nit_cliente, monto, fecha, estado) VALUES (%s, %s, %s, %s, %s, %s)""",
                           (empresa_nombre, self.__no_factura, self.__nit_cliente, self._monto, self._fecha, self._estado))
            conn.commit()
            print(f"Factura {self.__no_factura} guardada")
            return True
        except mysql.connector.Error as e:
            print("Ocurrio un error en base de datos", e)
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @property
    def estado(self):
        return self._estado

    def cambiar_estado(self,nuevo_estado):
        self._estado =nuevo_estado

    @property
    def no_factura(self):
        return self.__no_factura

    @property
    def nit_cliente(self):
        return self.__nit_cliente
    @property
    def monto(self):
        return self._monto

    @property
    def fecha(self):
        return self._fecha

class Reporte:
    def __init__(self, total_clientes, total_facturas):
        self.total_clientes = total_clientes
        self.total_facturas = total_facturas

class Inventario:
    def __init__(self, empresa_nombre, producto, cantidad, precio):
        self._empresa_nombre = empresa_nombre
        self._producto = producto
        self._cantidad = cantidad
        self._precio = precio

    def guardar(self):
        conn = None
        cursor = None
        try:
            conn = BasedeDatos.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO inventario_general (empresa_nombre, producto, cantidad, precio) VALUES (%s, %s, %s, %s)""",
                           (self._empresa_nombre, self._producto, self._cantidad, self._precio))
            conn.commit()
            print(f"Producto {self._producto} agregado a inventario de {self._empresa_nombre}")
            return True
        except mysql.connector.Error as e:
            print("Error al guardar inventario", e)
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def listar(nombre_empresa):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT producto, cantidad, precio 
            FROM inventario_general 
            WHERE empresa_nombre = %s
            ORDER BY producto""", (nombre_empresa,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows


# EJEMPLOS DE USO DEL SISTEMA

def main():
    print("=== EJEMPLOS DE USO DEL SISTEMA ===")

    # 1. CREAR UN AUDITOR/ADMINISTRADOR
    print("\n1. CREANDO AUDITOR...")
    auditor = Auditor("Carlos Lopez", "1234567890101", "carlos@empresa.com", "clopez", "clave123")

    # 2. CREAR CLIENTES
    print("\n2. CREANDO CLIENTES...")
    auditor.crear_cliente(
        nit="CF123456789",
        nombre="Juan Pérez",
        telefono="1234-5678",
        correo="juan@negocio.com",
        direccion="Zona 1, Ciudad",
        dpi="1234567890101",
        fecha_nacimiento="1990-05-15",
        nombre_negocio="Super Tienda Juan"
    )

    auditor.crear_cliente(
        nit="CF987654321",
        nombre="María García",
        telefono="8765-4321",
        correo="maria@empresa.com",
        nombre_negocio="Distribuidora María"
    )

    # 3. CREAR EMPRESAS PARA LOS CLIENTES
    print("\n3. CREANDO EMPRESAS...")
    auditor.crear_empresa(
        nombre_empresa="Tienda Central",
        nit_cliente="CF123456789",
        direccion="Centro Comercial MegaPlaza, Local 5"
    )

    auditor.crear_empresa(
        nombre_empresa="Almacén Express",
        nit_cliente="CF987654321",
        direccion="Zona Industrial, Bodega 12"
    )

    # 4. AGREGAR PRODUCTOS AL INVENTARIO
    print("\n4. AGREGANDO PRODUCTOS AL INVENTARIO...")
    auditor.modificar_inventario("Tienda Central", "Laptop HP", 10, 4500.00)
    auditor.modificar_inventario("Tienda Central", "Mouse Inalámbrico", 50, 85.50)
    auditor.modificar_inventario("Tienda Central", "Teclado Mecánico", 25, 250.00)

    auditor.modificar_inventario("Almacén Express", "Silla Oficina", 15, 350.00)
    auditor.modificar_inventario("Almacén Express", "Escritorio Ejecutivo", 8, 1200.00)
    auditor.modificar_inventario("Almacén Express", "Archivador Metal", 30, 180.75)

    # 5. REGISTRAR FACTURAS
    print("\n5. REGISTRANDO FACTURAS...")
    auditor.registrar_factura("F001", "CF123456789", "Tienda Central", 4550.00)
    auditor.registrar_factura("F002", "CF123456789", "Tienda Central", 1275.50)
    auditor.registrar_factura("F003", "CF987654321", "Almacén Express", 2400.00)

    # 6. LISTAR INFORMACIÓN
    print("\n6. LISTANDO INFORMACIÓN...")

    print("\n--- CLIENTES REGISTRADOS ---")
    clientes = auditor.listar_clientes()
    for cliente in clientes:
        print(f"NIT: {cliente['nit']} | Nombre: {cliente['nombre']} | Negocio: {cliente['nombre_negocio']}")

    print("\n--- EMPRESAS REGISTRADAS ---")
    empresas = auditor.listar_empresas()
    for empresa in empresas:
        print(f"Empresa: {empresa['nombre']} | Cliente: {empresa['nit_cliente']} | Dirección: {empresa['direccion']}")

    print("\n--- INVENTARIO TIENDA CENTRAL ---")
    inventario_tienda = auditor.ver_inventario("Tienda Central")
    for producto in inventario_tienda:
        print(f"Producto: {producto['producto']} | Cantidad: {producto['cantidad']} | Precio: Q{producto['precio']}")

    print("\n--- INVENTARIO ALMACÉN EXPRESS ---")
    inventario_almacen = auditor.ver_inventario("Almacén Express")
    for producto in inventario_almacen:
        print(f"Producto: {producto['producto']} | Cantidad: {producto['cantidad']} | Precio: Q{producto['precio']}")

    # 7. EJEMPLOS DE BÚSQUEDAS
    print("\n7. EJEMPLOS DE BÚSQUEDAS...")

    # Buscar cliente por NIT (búsqueda secuencial)
    print("\n--- BUSCAR CLIENTE POR NIT ---")
    datos_clientes = [(c['nombre'], c['nit'], c['telefono'], c['correo']) for c in clientes]
    resultado = busqueda_secuencial(datos_clientes, 1, "CF123456789")  # Buscar por NIT (índice 1)
    if resultado != -1:
        print(f"Cliente encontrado: {resultado}")

    # Ordenar clientes por nombre
    print("\n--- CLIENTES ORDENADOS POR NOMBRE ---")
    clientes_ordenados = metodo_quick_sort(datos_clientes, 0)  # Ordenar por nombre (índice 0)
    for cliente in clientes_ordenados:
        print(f"Nombre: {cliente[0]} | NIT: {cliente[1]}")

    # 8. EJEMPLOS DE ORDENAMIENTO
    print("\n8. EJEMPLOS DE ORDENAMIENTO...")

    # Ordenar inventario por precio (Bubble Sort)
    print("\n--- INVENTARIO ORDENADO POR PRECIO (BUBBLE SORT) ---")
    datos_inventario = [(p['producto'], p['cantidad'], p['precio']) for p in inventario_tienda]
    inventario_ordenado = metodo_bubble_sort(datos_inventario, 2)  # Ordenar por precio (índice 2)
    for producto in inventario_ordenado:
        print(f"Producto: {producto[0]} | Precio: Q{producto[2]}")

    # 9. CREAR MÁS USUARIOS
    print("\n9. CREANDO MÁS USUARIOS...")
    auditor.crear_usuario(
        nombre="Ana Martinez",
        dpi="9876543210101",
        correo="ana@empresa.com",
        puesto="Empleado",
        usuario="amartinez",
        contrasena="ana123",
        rol="Usuario"
    )

    # 10. DEMOSTRACIÓN DE PROPIEDADES
    print("\n10. DEMOSTRACIÓN DE PROPIEDADES...")
    empleado = Empleado("Pedro Ramirez", "5556667770101", "pedro@empresa.com", "pramirez", "pedro123")

    # Usando propiedades
    print(f"Nombre: {empleado.nombre}")
    print(f"Rol: {empleado.rol}")

    # Cambiando correo (con validación)
    empleado.correo = "nuevoemail@empresa.com"  # Válido
    empleado.correo = "correoinvalido"  # Mostrará error

    print("\n✅ DEMOSTRACIÓN COMPLETADA!")


def ejemplos_busquedas_avanzadas():
    """Ejemplos adicionales de búsquedas y ordenamientos"""
    print("\n=== BÚSQUEDAS Y ORDENAMIENTOS AVANZADOS ===")

    # Datos de ejemplo
    productos = [
        ("Laptop", 10, 4500.00),
        ("Mouse", 50, 85.50),
        ("Teclado", 25, 250.00),
        ("Monitor", 15, 800.00),
        ("Impresora", 8, 1200.00)
    ]

    print("Productos originales:")
    for prod in productos:
        print(f"  {prod[0]} - Cant: {prod[1]} - Precio: Q{prod[2]}")

    # Búsqueda binaria (requiere datos ordenados)
    print("\n--- BÚSQUEDA BINARIA ---")
    productos_ordenados = metodo_quick_sort(productos, 0)  # Ordenar por nombre
    resultado_bin = busqueda_binaria(productos_ordenados, 0, "Monitor")
    if resultado_bin != -1:
        print(f"Producto encontrado (binaria): {resultado_bin}")

    # Búsqueda secuencial
    print("\n--- BÚSQUEDA SECUENCIAL ---")
    resultado_sec = busqueda_secuencial(productos, 2, 250.00)  # Buscar por precio
    if resultado_sec != -1:
        print(f"Producto encontrado (secuencial): {resultado_sec}")

    # Diferentes métodos de ordenamiento
    print("\n--- COMPARACIÓN DE MÉTODOS DE ORDENAMIENTO ---")

    print("Ordenado por precio (Quick Sort):")
    quick_sorted = metodo_quick_sort(productos, 2)
    for prod in quick_sorted:
        print(f"  {prod[0]} - Q{prod[2]}")

    print("\nOrdenado por cantidad (Bubble Sort):")
    bubble_sorted = metodo_bubble_sort(productos, 1)
    for prod in bubble_sorted:
        print(f"  {prod[0]} - Cant: {prod[1]}")

    print("\nOrdenado por nombre (Selection Sort):")
    selection_sorted = meotod_selection_sort(productos, 0)
    for prod in selection_sorted:
        print(f"  {prod[0]}")


# Ejecutar los ejemplos
if __name__ == "__main__":
    try:
        main()
        ejemplos_busquedas_avanzadas()

        print("\n" + "=" * 50)
        print("🎉 TODOS LOS EJEMPLOS EJECUTADOS EXITOSAMENTE")
        print("=" * 50)

    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")

    input("\nPresiona Enter para salir...")

