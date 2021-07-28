import pymysql
from pymysql.err import Error


def abrir_conexion():
    try:
        conexion = pymysql.connect(host='localhost',
                                    user='root',
                                    password='',
                                    db='abm_socios')
        print("La conexión a la base de datos fue correcta")
        return conexion 
    except (Exception, Error) as error_capturado: 
        print("Ocurrió el siguiente error en la conexión a la base de datos: ",
                error_capturado) 

def cerrar_conexion(conexion):
    try: 
        conexion.close() 
        print("La conexión a la base de datos cerrada de forma correcta")
    except (Exception, Error) as error_capturado: 
        print("Ocurrió el siguiente error al cerrar la conexión a la base de datos: ", error_capturado) 

def buscar_socio_x_Id(id_buscar):
    try: 
        conexion = abrir_conexion() 
        cursor =  conexion.cursor()
        query = 'SELECT id_socio, nombres_socio, apellidos_socio, dni_socio, \
                cant_grupo_familiar, cant_menores18, cuota \
                FROM socios WHERE id_socio = %s;'
        cursor.execute(query, id_buscar)
        socio = cursor.fetchone()
        return socio
    except:
        return False
    finally: 
        cerrar_conexion(conexion)


def modificacion_socio(socio):
    try:
        conexion = abrir_conexion()
        cursor =  conexion.cursor()
        query = 'UPDATE socios SET nombres_socio = %s, apellidos_socio = %s, \
            dni_socio = %s, cant_grupo_familiar = %s,\
            cant_menores18 = %s, cuota = %s, menores_18 = %s WHERE id_socio = %s;'  #agregamos la columna menores_18
        values = (socio[1], socio[2], socio[3], socio[4], socio[5], socio[6], socio[7], socio[0]) #aca se le agrega el value correspondiente
        cursor.execute(query, values)
        conexion.commit()
        return True
    except:
        return False
    finally: 
        cerrar_conexion(conexion)


def baja_socio(id_eliminar): 
    try:
        conexion = abrir_conexion()
        cursor =  conexion.cursor()
        query = 'DELETE FROM socios WHERE id_socio = %s;'
        cursor.execute(query, id_eliminar)
        conexion.commit()
        return True
    except:
        return False
    finally: 
        cerrar_conexion(conexion)


def alta_socio(socio):
    try:
        conexion = abrir_conexion()
        cursor =  conexion.cursor()
        query = 'INSERT INTO socios(nombres_socio, apellidos_socio, dni_socio,\
             cant_grupo_familiar, cant_menores18, cuota, menores_18) VALUES (%s, %s, %s, %s, %s, %s, %s);' #y por ultimo se agrega al insert el menores_18 con su respectivo value
        cursor.execute(query, socio[1:])
        conexion.commit()
        query = 'SELECT * FROM socios WHERE id_socio = \
                                (SELECT MAX(id_socio) FROM socios)'
        cursor.execute(query)
        socio = cursor.fetchone()
        return socio 
    except:
        return False
    finally: 
        cerrar_conexion(conexion)
 