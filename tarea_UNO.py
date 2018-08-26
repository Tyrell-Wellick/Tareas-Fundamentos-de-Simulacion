from numpy import random
from math import inf
from datetime import datetime


class Cliente:
    ide = 0
    def __init__(self, tiempo_llegada):
        Cliente.ide += 1
        self.id = Cliente.ide
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_compra = random.exponential(15)
        self.tiempo_llegada_cola = self.tiempo_llegada + self.tiempo_compra
        self.tiempo_salida_cola = None
        self.tiempo_atencion = None
        self.tiempo_cola = None
        self.atendido = False
        self.atendiendo = False
        self.tiempo_salida_super = None
        self.en_cola = False

    def __repr__(self):
        info = "Cliente {}:\n    tiempo llegada: {}\n    tiempo compra: {}\n    tiempo llegada cola: {}\n" \
               "    tiempo salida cola: {}\n    tiempo atencion: {}\n    tiempo en cola : {}\n    atendiendo: {}" \
               "    atendido: {}    en cola: {}\n    salida super: {}".format(self.id,
                                                                 self.tiempo_llegada,
                                                                 self.tiempo_compra,
                                                                 self.tiempo_llegada_cola,
                                                                 self.tiempo_salida_cola,
                                                                 self.tiempo_atencion,
                                                                 self.tiempo_cola,
                                                                 self.atendiendo,
                                                                 self.atendido,
                                                                 self.en_cola,
                                                                 self.tiempo_salida_super)
        return info

    def entrada_caja(self, tiempo):
        self.tiempo_salida_cola = tiempo
        self.tiempo_cola = self.tiempo_salida_cola - self.tiempo_llegada_cola

    def determinar_tiempo_atencion_caja(self, tiempo_en_caja):
        self.tiempo_atencion = tiempo_en_caja
        self.tiempo_salida_super = self.tiempo_llegada + self.tiempo_compra + self.tiempo_cola + self.tiempo_atencion


class Caja:
    ide = 0
    def __init__(self, tasa_atencion):
        Caja.ide += 1
        self.id = Caja.ide
        self.tasa_atencion = tasa_atencion
        self.cola = []
        self.status = 0
        self.cliente_atendiendo = None
        self.clientes_atendidos = []
        self.proxima_salida = inf

    def __repr__(self):
        if self.cliente_atendiendo != None:
            info = "Caja {}:\n    Status: {}\n    Cliente atendiendo: Cliente {}\n".format(self.id,
                                                                                 self.status,
                                                                                 self.cliente_atendiendo.id)
        else:
            info = "Caja {}:\n    Status: {}\n    Cliente atendiendo: None\n".format(self.id,
                                                                                 self.status)
        info += "    Clientes en cola: {}\n".format(len(self.cola))
        for c in self.cola:
            info += "        Cliente {}\n".format(c.id)
        info += "    Clientes atendidos: {}\n".format(len(self.clientes_atendidos))
        if self.proxima_salida == inf:
            info += "    Proxima salida: infinito\n"
        else:
            info += "    Proxima salida: {}\n".format(self.proxima_salida)
        return info

    def setear_tiempo_atencion(self, cliente):
        tiempo = random.exponential(self.tasa_atencion)
        cliente.determinar_tiempo_atencion_caja(tiempo)

    def ocupar(self, cliente, tiempo):
        self.status = 1
        self.cliente_atendiendo = cliente
        self.cliente_atendiendo.atendiendo = True
        self.cliente_atendiendo.entrada_caja(tiempo)
        self.setear_tiempo_atencion(cliente)
        self.proxima_salida = self.cliente_atendiendo.tiempo_salida_super

    def desocupar(self):
        self.status = 0
        self.cliente_atendiendo.atendido = True
        self.cliente_atendiendo.atendiendo = False
        self.clientes_atendidos.append(self.cliente_atendiendo)
        self.cliente_atendiendo = None
        self.proxima_salida = inf

    def agregar_cliente_cola(self, cliente):
        self.cola.append(cliente)
        cliente.en_cola = True

    def proximo_cliente_cola(self):
        #print("Avanzando la cola")
        if len(self.cola) > 0:
            prox_cliente = self.cola.pop(0)
            prox_cliente.en_cola = False
            return prox_cliente
        else:
            return None


class Simulacion:
    def __init__(self, cantidad_cajas, tiempo_simulacion, tasa_cajas):
        self.cajas = [Caja(tasa_cajas) for i in range(cantidad_cajas)]
        self.t = 0
        self.t_simula = tiempo_simulacion
        self.nclientes = 0
        self.clientes = []
        self.estot = 0
        self.te1 = random.exponential(1/3)
        self.clientes_llegan = 1
        self.tiempos_llegan_super = [self.te1]
        self.tiempos_llegan_super_indice = 0
        self.tiempos_llegan_colas = []
        self.tiempos_salen_colas = []
        self.tiempos_salen_super = []

    def __repr__(self):
        info = ""
        je = "------------------"
        info += "{} Tiempo: {} {}\n".format(je, self.t, je)
        info += "{} Info Cajas {}\n".format(je, je)
        for caja in self.cajas:
            info += caja.__repr__()
            info += "\n"
        #info += "{} Info Clientes {}\n".format(je, je)
        #for cliente in self.clientes:
        #    info += cliente.__repr__()
        #    info += "\n"
        info += "{}{}{}".format(je, je, je)
        return info

    def det_min_te2(self):
        if len(self.clientes) == 0:
            return inf
        else:
            min = inf
            for cliente in self.clientes:
                if cliente.tiempo_llegada_cola != None and cliente.atendido == False and cliente.atendiendo == False\
                        and cliente.tiempo_llegada_cola < min and cliente.en_cola == False:
                    min = cliente.tiempo_llegada_cola
            return min

    def det_cliente_min_te2(self):
        if len(self.clientes) == 0:
            return None
        else:
            min = inf
            cliente_min_te2 = None
            for cliente in self.clientes:
                if cliente.tiempo_llegada_cola != None and cliente.atendido == False and cliente.atendiendo == False\
                        and cliente.tiempo_llegada_cola < min and cliente.en_cola == False:
                    min = cliente.tiempo_llegada_cola
                    cliente_min_te2 = cliente
            return cliente_min_te2

    def det_min_te3(self):
        if len(self.clientes) == 0:
            return inf
        else:
            min = inf
            for cliente in self.clientes:
                if cliente.tiempo_salida_super != None and cliente.atendiendo == True and cliente.en_cola == False\
                        and cliente.tiempo_salida_super < min and cliente.atendido == False:
                    min = cliente.tiempo_salida_super
            return min

    def det_cliente_min_te3(self):
        if len(self.clientes) == 0:
            return inf
        else:
            min = inf
            cliente_min_te3 = None
            for cliente in self.clientes:
                if cliente.tiempo_salida_super != None and cliente.atendiendo == True and cliente.en_cola == False\
                        and cliente.tiempo_salida_super < min and cliente.atendido == False:
                    min = cliente.tiempo_salida_super
                    cliente_min_te3 = cliente
            return cliente_min_te3

    def det_caja_desocupada(self):
        for caja in self.cajas:
            if len(caja.cola) == 0 and caja.cliente_atendiendo == None:
                return caja
        return False

    def det_caja_menor_cola(self):
        menor = inf
        caja_menor_cola = None
        for caja in self.cajas:
            if len(caja.cola) < menor:
                menor = len(caja.cola)
                caja_menor_cola = caja
        if caja_menor_cola:
            return caja_menor_cola
        else:
            return self.cajas[0]

    def correr(self):
        je = "-----------------"
        #print("{} APERTURA DE SUPERMERCADO {}".format(je, je))
        while self.t < self.t_simula:
            #print("T={}".format(self.t))
            min_te2 = self.det_min_te2()
            min_te3 = self.det_min_te3()
            if self.te1 < min_te2 and self.te1 < min_te3:
                self.t = self.te1
                if self.t > self.t_simula:
                    self.te1 = inf
                else:
                    self.te1 = self.t + random.exponential(1/3)
                    self.clientes_llegan += 1
                cliente_llega = Cliente(self.t)# Determina al crearse el tiempo de compra
                self.clientes.append(cliente_llega)
                #print("E1: Llega Cliente {} a supermercado".format(cliente_llega.id))
            else:
                if min_te2 < min_te3:
                    #print("E2.1: Entra un cliente a alguna caja o alguna cola")
                    self.t = min_te2
                    cliente_entra = self.det_cliente_min_te2()
                    if self.det_caja_desocupada():
                        caja_desocupada = self.det_caja_desocupada()
                        #print("Cliente {} entra a caja {}".format(cliente_entra.id, caja_desocupada.id))
                        self.nclientes += 1
                        caja_desocupada.ocupar(cliente_entra, self.t)
                    else:
                        caja_menor_cola = self.det_caja_menor_cola()
                        #print("E2.2: Cliente {} entra a cola de caja {}".format(cliente_entra.id, caja_menor_cola.id))
                        caja_menor_cola.agregar_cliente_cola(cliente_entra)
                else:
                    self.t = min_te3
                    cliente_sale = self.det_cliente_min_te3()
                    #print("E3: Sale cliente {} de alguna caja".format(cliente_sale.id))
                    for caja in self.cajas:
                        if caja.cliente_atendiendo != None:
                            if caja.cliente_atendiendo.id == cliente_sale.id:
                                caja.desocupar()
                                #print("De caja {}".format(caja.id))
                                proximo_cliente = caja.proximo_cliente_cola()
                                if proximo_cliente:
                                    caja.ocupar(proximo_cliente, self.t)
                                break
        #print("{} CIERRE DE SUPERMERCADO {}".format(je, je))
        estot = 0
        nclientes = 0
        sin_atender = 0
        tiempo_atencion = 0
        tiempo_compra = 0
        tiempos_cola = []
        for cl in self.clientes:
            if cl.tiempo_cola != None:
                estot += cl.tiempo_cola
                tiempos_cola.append(cl.tiempo_cola)
                nclientes += 1
                tiempo_atencion += cl.tiempo_atencion
                tiempo_compra += cl.tiempo_compra
                #print(cl)
            else:
                sin_atender += 1
        tiempos_cola_ordenada = sorted(tiempos_cola)
        indice_percentil_noventa = round((len(tiempos_cola_ordenada)*0.9))
        tiempo_percentil_noventa = tiempos_cola[indice_percentil_noventa]
        # print("{}ESTADISTICAS{}".format(je, je))
        # print("Cliente sin atender: {}".format(sin_atender))
        # print("Tiempo medio en cola: {}".format(estot/nclientes))
        # print("Tiempo medio atencion: {}".format(tiempo_atencion/nclientes))
        # print("Tiempo medio compra: {}".format(tiempo_compra/nclientes))
        # print("TIEMPO PERCENTIL 90%: {}".format(tiempo_percentil_noventa))
        return estot/nclientes, tiempo_percentil_noventa



if __name__ == '__main__':
    tasa_cajas = 5
    simulacion = Simulacion(16, 840, tasa_cajas)
    tiempos_medio_espera = []
    tiempos_percentil_noventa = []
    tiempos_ejecucion = []
    for i in range(10):
        t = datetime.now()
        simulacion = Simulacion(16, 840, tasa_cajas)
        tiempo_medio_espera, tiempo_percentil_noventa = simulacion.correr()
        tiempo_ejecucion = datetime.now() - t
        tiempos_medio_espera.append(tiempo_medio_espera)
        tiempos_percentil_noventa.append(tiempo_percentil_noventa)
        tiempos_ejecucion.append(tiempo_ejecucion)
    for i in range(10):
        print("----------------Simulación : {}--------------------".format(i+1))
        print("Tiempo medio en cola: {}".format(tiempos_medio_espera[i]))
        print("Tiempo percentil 90%: {}".format(tiempos_percentil_noventa[i]))
        print("Tiempo ejecución: {}".format(tiempos_ejecucion[i]))
    print("--------------RESUMEN 10 REPLICAS---------------")
    print("Tiempo en cola: {}".format(sum(tiempos_medio_espera)/10))
    print("Tiempo percentil 90%: {}".format(sum(tiempos_percentil_noventa)/10))
    #print("Tiempo ejecución: {}".format(sum(tiempos_ejecucion)/10))
