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
            database="prueba_100",
            port= 3306
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

    def reporte_facturas_emitidas(self,empresa):
        return Reporte.facturas_emitidas(empresa)

    def reporte_facturas_canceladas(self,empresa):
        return Reporte.facturas_anuladas(empresa)

    def reporte_ventas(self,empresa):
        return Reporte.total_ventas_empresa(empresa)

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

    @staticmethod
    def listar_por_empresa(empresa_nombre):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT 
                facturas_general.no_factura,
                facturas_general.nit_cliente,
                clientes.nombre as nombre_cliente,
                facturas_general.monto,
                facturas_general.fecha,
                facturas_general.estado
            FROM facturas_general
            INNER JOIN clientes ON facturas_general.nit_cliente = clientes.nit
            WHERE facturas_general.empresa_nombre = %s
            ORDER BY facturas_general.fecha DESC""",
            (empresa_nombre,))
        datos_filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return datos_filas

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

    @staticmethod
    def facturas_emitidas(empresa):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT no_factura, nit_cliente, monto, fecha, empresa_nombre
            FROM facturas_general 
            WHERE estado = 'Emitida' AND empresa_nombre = %s""",
                (empresa,))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

    @staticmethod
    def facturas_anuladas(empresa):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT no_factura, nit_cliente, monto, fecha, empresa_nombre
            FROM facturas_general 
            WHERE estado = 'Anulada' AND empresa_nombre = %s""", (empresa,))
        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultado

    @staticmethod
    def total_ventas_empresa(empresa):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT empresa_nombre, COUNT(*) as facturas, SUM(monto) as total
            FROM facturas_general 
            WHERE estado = 'Emitida' AND empresa_nombre = %s
            GROUP BY empresa_nombre""",
                       (empresa,))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

    @staticmethod
    def facturas_por_mes(empresa, año_deseado=None):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)

        if año_deseado:
            cursor.execute("""
                SELECT 
                    MONTH(fecha) as mes,
                    COUNT(*) as cuantas_facturas,
                    SUM(monto) as cuanto_dinero
                FROM facturas_general 
                WHERE empresa_nombre = %s AND YEAR(fecha) = %s
                GROUP BY MONTH(fecha)
                ORDER BY mes
            """, (empresa, año_deseado))
        else:
            cursor.execute("""SELECT 
                    YEAR(fecha) as año,
                    MONTH(fecha) as mes,
                    COUNT(*) as cuantas_facturas,
                    SUM(monto) as cuanto_dinero
                FROM facturas_general 
                WHERE empresa_nombre = %s
                GROUP BY YEAR(fecha), MONTH(fecha)
                ORDER BY año, mes
            """, (empresa,))

        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultado

    @staticmethod
    def facturas_emitidas_mes(empresa, año=None):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)

        if año:
            cursor.execute("""SELECT 
                    MONTH(fecha) as mes,
                    COUNT(*) as cantidad,
                    SUM(monto) as total
                FROM facturas_general 
                WHERE estado = 'Emitida' AND empresa_nombre = %s AND YEAR(fecha) = %s
                GROUP BY MONTH(fecha)
                ORDER BY mes
            """,
                           (empresa, año))
        else:
            cursor.execute("""SELECT 
                    YEAR(fecha) as año,
                    MONTH(fecha) as mes,
                    COUNT(*) as cantidad,
                    SUM(monto) as total
                FROM facturas_general 
                WHERE estado = 'Emitida' AND empresa_nombre = %s
                GROUP BY YEAR(fecha), MONTH(fecha)
                ORDER BY año, mes
            """, (empresa,))
        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultado

    @staticmethod
    def facturas_canceladas_mes(empresa, año=None):
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        if año:
            cursor.execute("""SELECT 
                    MONTH(fecha) as mes,
                    COUNT(*) as cantidad,
                    SUM(monto) as total
                FROM facturas_general 
                WHERE estado = 'Anulada' AND empresa_nombre = %s AND YEAR(fecha) = %s
                GROUP BY MONTH(fecha)
                ORDER BY mes""",
                           (empresa, año))
        else:
            cursor.execute("""
                SELECT 
                    YEAR(fecha) as año,
                    MONTH(fecha) as mes,
                    COUNT(*) as cantidad,
                    SUM(monto) as total
                FROM facturas_general 
                WHERE estado = 'Anulada' AND empresa_nombre = %s
                GROUP BY YEAR(fecha), MONTH(fecha)
                ORDER BY año, mes
            """, (empresa,))
        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultado

    @staticmethod
    def hacer_reporte_emitidas(empresa, año_seleccionado=None):
        datos = Reporte.facturas_emitidas_por_mes(empresa, año_seleccionado)
        if not datos:
            return "No hay facturas emitidas"

        nombres_meses = {
            1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL",
            5: "MAYO", 6: "JUNIO", 7: "JULIO", 8: "AGOSTO",
            9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"
        }

        reporte = "FACTURAS EMITIDAS\n"
        reporte += "=" * 30 + "\n\n"

        for dato in datos:
            año = dato.get('año', '2024')
            mes_num = dato['mes']
            mes_nombre = nombres_meses.get(mes_num, f"MES {mes_num}")

            reporte += f"{mes_nombre}: {dato['cantidad']}\n"

        return reporte



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
            WHERE empresa_nombre = %s""",
            (nombre_empresa,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows


def inicio_sesio(usuario,contrasena):
    try:
        if usuario == "contador" and contrasena == "contador123":
            return {"rol": "Contador", "nombre": "Administrador"}

        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s",
                       (usuario, contrasena))
        usuario_db = cursor.fetchone()
        cursor.close()
        conn.close()

        if usuario_db:
            return usuario_db
        elif usuario == "0" and contrasena == "0":
            return "salir"
        else:
            return None

    except Exception as e:
        print(f"Ocurrio un error inesperado: {e}")
        return None