import socios_model


class Socio:
    
    CUOTA_SOCIO = 100.0
    DESCUENTO_MENORES = 0.5
    DESCUENTO_FAMILIA_NUMEROSA6 = 0.2
    DESCUENTO_FAMILIA_NUMEROSA10 = 0.3

    def __init__(self, id_socio, nombre_socio, apellido_socio, DNI_socio, 
                    cant_grupo_familiar, cant_menores18, cuota=0.0): 
        self.id_socio = int(id_socio)
        self.apellido_socio = apellido_socio
        self.nombre_socio = nombre_socio
        self.DNI_socio = DNI_socio
        self.cant_grupo_familiar = int(cant_grupo_familiar)
        self.cant_menores18 = int(cant_menores18)
        self.cuota = cuota 

    def obtener_socio_x_Id(self):
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
        socio_nuevo = socios_model.alta_socio((self.id_socio, self.nombre_socio, 
                                        self.apellido_socio, self.DNI_socio, 
                                        self.cant_grupo_familiar, self.cant_menores18, self.cuota)) 
        socio_guardado = Socio(socio_nuevo[0], socio_nuevo[1], socio_nuevo[2], 
                                socio_nuevo[3], socio_nuevo[4], socio_nuevo[5], socio_nuevo[6]) 
        return socio_guardado 
    def eliminar_socio(self):
        return socios_model.baja_socio(self.id_socio)

    def modificar_socio(self):
        self.cuota = self.calcular_cuota()
        socio_modificado = (self.id_socio, self.nombre_socio, self.apellido_socio,
                    self.DNI_socio, self.cant_grupo_familiar, self.cant_menores18, self.cuota) 
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
