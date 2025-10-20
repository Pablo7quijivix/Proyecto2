class Usuario:
    def __init__(self,nombre,dpi,correo,puesto,usuario,contrasena,rol):
        self.__nombre= nombre
        self.__dpi= dpi
        self._correo= correo
        self._puesto= puesto
        self.__usuario= usuario
        self.__contrasena= contrasena
        self._rol= rol

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

    def mostrar_info(self):
        print(f"{self.nombre} ({self.puesto}) - Rol:{self.rol}")

class Auditor(Usuario):
    def __init__(self,nombre,dpi,correo,usuario,contrasena):
        super().__init__(nombre,dpi,correo,"Auditor",usuario,contrasena,"Admin")

    def mostrar_info(self):
        pass

class Empleado(Usuario):
    def __init__(self,nombre,dpi,correo,usuario,contrasena):
        super().__init__(nombre,dpi,correo,"Empelado",usuario,"Usuario")

    def mostrar_info(self):
        pass


class Cliente:
    def __init__(self,nit,nombre,telefono,correo,direccion,dpi,fecha_nacimiento,nombre_negocio):
        self.__nit=nit
        self.__nombre= nombre
        self._telefono= telefono
        self._correo= correo
        self._direccion= direccion
        self.__dpi= dpi
        self.__fecha_nacimiento= fecha_nacimiento
        self.__nombre_negocio= nombre_negocio


    def mostrar_informacion(self):
        print(f"{self.nit} - {self.nombre} ({self.nombre_negocio})")

class Factura:
    def __init__(self,no_factura,nit_cliente,monto,fecha,estado="Emitida"):
        self.__no_factura= no_factura
        self.__nit_cliente= nit_cliente
        self._monto= monto
        self._fecha= fecha
        self._estado= estado

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

class Reporte:
    def __init__(self,total_clientes,total_facturas):
        self.total_clientes= total_clientes
        self.total_factuas= total_facturas





