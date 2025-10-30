import mysql.connector
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
            host="190.143.186.220",
            user="root",
            password="Wilson200.",
            database="sistema_contable"
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

    @staticmethod
    def _conn():
        cursor= None
        conn= None
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
            return conn
        except mysql.connector as e:
            print(f"Ocurrio un error en la base de datos {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


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
        conn = self._conn()
        cursor = conn.cursor()
        cursor.execute(
    "INSERT INTO usuarios (nombre, dpi, correo, puesto, usuario, contrasena, rol) VALUES (%s, %s, %s, %s, %s, %s, %s)",
    (self.__nombre, self.__dpi, self._correo, self._puesto, self.__usuario, self.__contrasena, self._rol))
        conn.commit()
        print(f"Usuario '{self.__usuario}' guardado con éxito.")
        conn.close()

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

    def registrar_cliente(self):
        print("--- REGISTRAR CLIENTE ---")
        nit = input("Ingrese NIT: ")
        nombre = input("Ingrese nombre: ")
        telefono = input("Ingrese numero de teléfono: ")
        correo = input("Ingrese correo electronico: ")
        direccion = input("Ingrese diirección: ")
        dpi = input("Ingrese DPI: ")
        fecha_nacimiento = input("Ingrese fecha de nacimiento (YYYY-MM-DD): ")
        nombre_negocio = input("Ingrese nombre de negocio: ")

        cliente = Cliente(nit, nombre, telefono, correo, direccion, dpi, fecha_nacimiento, nombre_negocio)
        cliente.guardar()

    def crear_usuario(self, nombre, dpi, correo, puesto, usuario, contrasena, rol):
        u = Usuario(nombre, dpi, correo, puesto, usuario, contrasena, rol)
        return u.guardar()

    def crear_cliente(self, nit,nombre,telefono="",correo="",direccion="",dpi="",fecha_nac=None,nombre_negocio=""):
        c = Cliente(nit,nombre,telefono,correo,direccion,dpi,fecha_nac,nombre_negocio)
        return c.guardar()

    def crear_empresa(self, nombre_empresa, nit_cliente, direccion=""):
        empresa = Empresa(nombre_empresa, nit_cliente, direccion)
        guardar = empresa.guardar()
        if guardar:
            tabla = empresa.tabla_inventario

            if tabla not in reportes:
                reportes[nombre_empresa] = []
            if tabla not in facturas:
                facturas[nombre_empresa] = []
            if tabla not in inventario:
                inventario[nombre_empresa] = []
        return guardar

    def listar_empresas(self):
        return Empresa.listar()

    def listar_clientes(self):
        return Cliente.listar()

    def ver_inventario(self,nombre_empresa):
        return Empresa.listar(nombre_empresa)

    def modificar_inventario(self,nombre_empresa,producto,cantidad,precio):
        inventario=Inventario(nombre_empresa,producto,cantidad,precio)
        guardar=inventario.guardar()
        return  guardar

    def registrar_factura(self,numero_factura,nit_cliente,empresa_nombre,monto,fecha=None):
        factura = Factura(numero_factura, nit_cliente, empresa_nombre, monto, fecha)
        guardar = factura.guardar()
        if guardar:
            if empresa_nombre not in facturas:
                facturas[empresa_nombre] = []
            facturas[empresa_nombre].append(factura)
        return guardar

class Empleado(Usuario):
    def __init__(self,nombre,dpi,correo,usuario,contrasena):
        super().__init__(nombre,dpi,correo,"Empelado",usuario,"Usuario")

    def mostrar_info(self):
        pass


class Cliente:
    def __init__(self, nit, nombre, telefono="", correo="", direccion="", dpi="", fecha_nacimiento=None):
        self._nit = nit
        self._nombre = nombre
        self._telefono = telefono
        self._correo = correo
        self._direccion = direccion
        self._dpi = dpi
        self._fecha_nacimiento = fecha_nacimiento

    @staticmethod
    def _conn():
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
        return conn

    def guardar(self):
        conn = self._conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clientes (nit, nombre, telefono, correo, direccion, dpi, fecha_nacimiento, nombre_negocio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (self.__nit, self.__nombre, self._telefono, self._correo, self._direccion, self.__dpi, self.__fecha_nacimiento, self.__nombre_negocio))
        conn.commit()
        print(f"Cliente '{self.__nombre}' guardado con éxito.")
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
        self.tabla_inventario = "inventario_" + normalizar_nombre(self._nombre)

    @staticmethod
    def _crear_tabla():
        conn = BasedeDatos.conectar()
        cursor = conn.cursor()
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
        cursor.close()

    def guardar(self):
        conn= BasedeDatos.conectar()
        cursor= conn.cursor()
        cursor.execute(
            "INSERT INTO empresas (nombre,nit_cliente,direccion) VALUES (%s,%s,%s)",
            (self._nombre,self._nit_cliente,self._direccion))
        conn.commit()
        cursor.close()
        Inventario._crear_tabla(self._nombre)
        conn.commit()
        cursor.close()

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
    def __init__(self,no_factura,nit_cliente,monto,fecha,estado="Emitida"):
        self.__no_factura= no_factura
        self.__nit_cliente= nit_cliente
        self._monto= monto
        self._fecha= fecha
        self._estado= estado

    @staticmethod
    def _conn():
        conn = BasedeDatos.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS facturas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                no_factura INT NOT NULL,
                nit_cliente VARCHAR(50) NOT NULL,
                monto DECIMAL(10,2) NOT NULL,
                fecha DATE NOT NULL,
                estado VARCHAR(50) NOT NULL
            );
        """)
        conn.commit()
        return conn

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

    def guardar(self):
        conn = self._conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO facturas (no_factura, nit_cliente, monto, fecha, estado) VALUES (%s, %s, %s, %s, %s)",
            (self.__no_factura, self.__nit_cliente, self._monto, self._fecha, self._estado))
        conn.commit()
        print(f"Factura '{self.__no_factura}' guardada con éxito.")
        conn.close()

class Reporte:
    def __init__(self,total_clientes,total_facturas):
        self.total_clientes= total_clientes
        self.total_factuas= total_facturas


class Inventario:
    def __init__(self, empresa_nombre, producto, cantidad, precio):
        self._empresa_nombre = empresa_nombre
        self._producto = producto
        self._cantidad = int(cantidad)
        self._precio = float(precio)
        Inventario.crear_tabla(empresa_nombre)

    def crear_tabla(self,nombre_empresa):
        tabla = "inventario_" + normalizar_nombre(nombre_empresa)
        conn = BasedeDatos.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nit_cliente VARCHAR(60),
                producto VARCHAR(200) NOT NULL,
                cantidad INT NOT NULL,
                precio DECIMAL(12,2) NOT NULL
            );""")
        conn.commit()
        cursor.close()
        return tabla

    def guardar(self):
        tabla= "inventario_" + normalizar_nombre(self._empresa_nombre)
        conn = BasedeDatos.conectar()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {tabla} (producto,cantidad,precio) VALUES (%s,%s,%s)",
                    (self._producto, self._cantidad, self._precio))
        conn.commit()
        cursor.close()

    @staticmethod
    def listar(nombre_empresa):
        tabla = "inventario_" + normalizar_nombre(nombre_empresa)
        conn = BasedeDatos.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT producto,cantidad,precio FROM {tabla}")
        rows = cursor.fetchall()
        cursor.close()
        return rows








