import socios_model


class Socio:
    
    CUOTA_SOCIO = 100.0
    DESCUENTO_MENORES = 0.5
    DESCUENTO_FAMILIA_NUMEROSA6 = 0.2
    DESCUENTO_FAMILIA_NUMEROSA10 = 0.3

    def __init__(self, id_socio, nombre_socio, apellido_socio, DNI_socio, 
                    cant_grupo_familiar, cant_menores18, cuota=0.0, menores_18=''): #aca agregamos un parametro adicional y le damos por defecto el valor de una str vacia
        self.id_socio = int(id_socio)
        self.apellido_socio = apellido_socio
        self.nombre_socio = nombre_socio
        self.DNI_socio = DNI_socio
        self.cant_grupo_familiar = int(cant_grupo_familiar)
        self.cant_menores18 = int(cant_menores18)
        self.cuota = cuota 
        self.menores_18 = menores_18 #aca se hace propio el parametro al objeto

    def obtener_socio_x_Id(self): #esta funcion no se toca porque no se va a mostrar en la vista la string de menores_18
        socio_encontrado = socios_model.buscar_socio_x_Id(self.id_socio)
        if socio_encontrado:
            
            socio_devuelto = Socio(socio_encontrado[0], socio_encontrado[1], 
                                    socio_encontrado[2], socio_encontrado[3], 
                                    socio_encontrado[4], socio_encontrado[5], socio_encontrado[6]) 
            return socio_devuelto 
        else:
            return socio_encontrado
    
    def guardar_socio(self): 
        self.cuota = self.calcular_cuota() 
        self.menores_18 = self.crear_menores_18()   #asignamos el valor nuevo llamando a la funcion que creamos para crear el string pedido
        socio_nuevo = socios_model.alta_socio((self.id_socio, self.nombre_socio, 
                                        self.apellido_socio, self.DNI_socio,  
                                        self.cant_grupo_familiar, self.cant_menores18, self.cuota, self.menores_18)) #agregamos el self.menores_18 para insertarlo en la BD
        socio_guardado = Socio(socio_nuevo[0], socio_nuevo[1], socio_nuevo[2], 
                                socio_nuevo[3], socio_nuevo[4], socio_nuevo[5], socio_nuevo[6], socio_nuevo[7]) 
        return socio_guardado 

    def eliminar_socio(self): #esta funcion tampoco se toca porque elimina toda la tupla(sql) de la base de datos sin importar la cantidad de columnas
        return socios_model.baja_socio(self.id_socio)

    def modificar_socio(self):
        self.cuota = self.calcular_cuota()
        self.menores_18 = self.crear_menores_18()   #asignamos el valor nuevo llamando a la funcion que creamos para crear el string pedido
        socio_modificado = (self.id_socio, self.nombre_socio, self.apellido_socio,
                    self.DNI_socio, self.cant_grupo_familiar, self.cant_menores18, self.cuota, self.menores_18) #creamos una variable con una tupla con los datos a modificar
        return socios_model.modificacion_socio(socio_modificado) 

    def calcular_cuota(self):
        cuota_grupo_familiar = (self.CUOTA_SOCIO * 
                            (self.cant_grupo_familiar-self.cant_menores18) +
            self.CUOTA_SOCIO * (1-self.DESCUENTO_MENORES) * self.cant_menores18)
        if self.cant_grupo_familiar>=10:
            return cuota_grupo_familiar * (1 - self.DESCUENTO_FAMILIA_NUMEROSA10)
        elif self.cant_grupo_familiar>=6:
            return cuota_grupo_familiar * (1 - self.DESCUENTO_FAMILIA_NUMEROSA6)
        else:
            return cuota_grupo_familiar

    def crear_menores_18(self): #creamos una funcion para generar el campo menores_18
        cadena_modificable = 'La familia {} dispone de {} '.format(self.apellido_socio, self.cant_menores18) #creamos una cadena inicial que luego modificaremos
        if self.cant_menores18 >= 3:    #si es mayor o igual a 3 se le pone la palabra mayores
            cadena_modificable+='mayores de 18 años.'   
            return cadena_modificable
        else:                           #de lo contrario pone la palabra menores
            cadena_modificable += 'menores de 18 años.'
            return cadena_modificable
             