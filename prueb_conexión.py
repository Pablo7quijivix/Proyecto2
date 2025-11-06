import mysql.connector
from mysql.connector import Error


def conexion_segura():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Wilson200.",
            database="nueva_prueba",
            auth_plugin='mysql_native_password'  # ¡Importante!
        )

        if conexion.is_connected():
            print("✅ Conexión exitosa")

            # Hacer alguna operación simple
            cursor = conexion.cursor()
            cursor.execute("SELECT 1")
            resultado = cursor.fetchone()
            print(f"✅ Test query: {resultado}")

            cursor.close()
            conexion.close()
            print("✅ Conexión cerrada correctamente")

    except Error as e:
        print(f"❌ Error de MySQL: {e}")
    except Exception as e:
        print(f"❌ Error general: {e}")


# Ejecutar
if __name__ == "__main__":
    conexion_segura()