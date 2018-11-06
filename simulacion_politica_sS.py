from numpy import random
from math import inf, sqrt


class Item:
    def __init__(self, tiempo):
        self.tiempo_llegada = tiempo
        self.vendido = False

    def vender(self, tiempo):
        self.tiempo_salida = tiempo
        self.vendido = True

    def tiempo(self):
        return self.tiempo_salida - self.tiempo_llegada


class Demanda_pendiente:
    def __init__(self, tiempo):
        self.tiempo_inicio = tiempo
        self.satisfecha = False

    def satisfacer(self, tiempo):
        self.tiempo_fin = tiempo
        self.satisfecha = True

    def tiempo(self):
        return self.tiempo_fin - self.tiempo_inicio


class Simulacion:
    def __init__(self):
        self.t = 0
        self.costo_total_ac = 0
        self.demanda_pendiente = []
        self.pendientes = []
        self.tam_orden = 0
        self.t_lleg_dem = random.exponential(3)
        self.inventario = []
        self.stock_actual = [Item(self.t) for i in range(60)]
        self.mes_actual = 1
        self.t_lleg_prox_orden = inf

    def simular_120_meses(self, s, S):
        self.s = s
        self.S = S
        self.t = 0
        self.costo_total_ac = 0
        self.demanda_pendiente = []
        self.pendientes = []
        self.tam_orden = 0
        self.t_lleg_dem = random.exponential(3)
        self.inventario = []
        self.stock_actual = [Item(self.t) for i in range(60)]
        self.mes_actual = 1
        self.t_lleg_prox_orden = inf
        return self.correr()

    def demanda(self):
        ran = random.random()
        if 0 <= ran < 0.16666666:
            return 1
        elif 0.16666666 <= ran < 0.5:
            return 2
        elif 0.5 <= ran < 0.8333333:
            return 3
        else:
            return 4

    def correr(self):
        while self.t < 3600:
            #print("T: {}, Stock: {}".format(self.t, self.stock_actual))
            if self.mes_actual*30 < self.t:
                #print("Revision a fin de mes")
                #######    ARREGLAR     #######self.costo_total_ac += 1*self.stock_actual + 5*self.demanda_pendiente
                #print("Costo sumado inventario y pendiente al ac: {}".format(1*self.stock_actual + 5*self.demanda_pendiente))
                if len(self.stock_actual) < self.s:
                    self.t_lleg_prox_orden = self.mes_actual*30 + random.uniform(15, 30)
                    self.tam_orden = self.S - len(self.stock_actual)
                    self.costo_total_ac += 32 + 3*self.tam_orden
                    #print("Ordenando: {} que llegan en T: {} y cuesta: {}".format(self.tam_orden, self.t_lleg_prox_orden, 32 + 3 * self.tam_orden))
                self.mes_actual += 1
            if self.t_lleg_dem < self.t_lleg_prox_orden:
                self.t = self.t_lleg_dem
                self.t_lleg_dem = self.t + random.exponential(3)
                #print("Proxima llegada demanda T: {}".format(self.t_lleg_dem))
                D = self.demanda()
                #print("Llega demanda de {}".format(D))
                if D <= len(self.stock_actual):
                    #print("Se vende")
                    for i in range(D):
                        item = self.stock_actual.pop(0)
                        item.vender(self.t)
                        self.inventario.append(item)
                    #self.stock_actual -= D
                else:
                    alcanza = len(self.stock_actual)
                    if alcanza > 0:
                        for i in range(alcanza):
                            item = self.stock_actual.pop(0)
                            item.vender(self.t)
                            self.inventario.append(item)
                    if D-alcanza > 0:
                        for i in range(D-alcanza):
                            self.demanda_pendiente.append(Demanda_pendiente(self.t))
                    #######self.demanda_pendiente += D - self.stock_actual
                    #print(Hay demanda pendiente de {}".format(self.demanda_pendiente))
                    #######self.stock_actual = 0
            else:
                self.t = self.t_lleg_prox_orden
                for i in range(self.tam_orden):
                    self.stock_actual.append(Item(self.t))
                #####self.stock_actual += self.tam_orden
                #print("Llega pedido de tamaño {} en T:{}".format(self.tam_orden, self.t))
                self.tam_orden = 0
                self.t_lleg_prox_orden = inf
                if len(self.demanda_pendiente) > 0:
                    #print("Satisfaciendo dem pendiente....")
                    if len(self.demanda_pendiente) <= len(self.stock_actual):
                        for i in range(len(self.demanda_pendiente)):
                            item = self.stock_actual.pop(0)
                            item.vender(self.t)
                            self.inventario.append(item)
                            dem_pen = self.demanda_pendiente.pop(0)
                            dem_pen.satisfacer(self.t)
                            self.pendientes.append(dem_pen)
                        #print("Se satisface toda: d_pen: {}, sto: {}".format(self.demanda_pendiente, self.stock_actual))
                        #####self.stock_actual -= self.demanda_pendiente
                        #####self.demanda_pendiente = 0
                    else:
                        for i in range(len(self.stock_actual)):
                            item = self.stock_actual.pop(0)
                            item.vender(self.t)
                            self.inventario.append(item)
                            dem_pen = self.demanda_pendiente.pop(0)
                            dem_pen.satisfacer(self.t)
                            self.pendientes.append(dem_pen)
                        #print("No se satisface toda: {}, sto: {}".format(self.demanda_pendiente, self.stock_actual))
                        ####self.demanda_pendiente -= self.stock_actual
                        ####self.stock_actual = 0
                else:
                    pass
                    #print("No hay demanda pendiente")
        #print("Ultima revision a fin de mes: stock: {}, d_p: {}".format(self.stock_actual, self.demanda_pendiente))
        ############self.costo_total_ac += 1 * self.stock_actual + 5 * self.demanda_pendiente
        #print("Termina con costo: {}".format(self.costo_total_ac))
        for inv in self.inventario:
            self.costo_total_ac += inv.tiempo()/30
        for dp in self.pendientes:
            self.costo_total_ac += (dp.tiempo()/30)*5
        for s in self.stock_actual:
            s.vender(self.t)
            self.costo_total_ac += (s.tiempo()/30)
        for p in self.demanda_pendiente:
            p.satisfacer(self.t)
            self.costo_total_ac += (p.tiempo()/30)*5
        return self.costo_total_ac/120

if __name__ == '__main__':
    configuraciones = {1: {"s": 20, "S": 40},
                       2: {"s": 20, "S": 50},
                       3: {"s": 20, "S": 60},
                       4: {"s": 20, "S": 70},
                       5: {"s": 20, "S": 80},
                       6: {"s": 25, "S": 60},
                       7: {"s": 25, "S": 70}}
    simulacion = Simulacion()
    ####################PARTE A#############################
    # config1 = 6
    # config2 = 7
    # N = 11
    # z1 = []  # x2-x1
    # x2 = []
    # x3 = []
    # t_st = {11: 2.764, 21: 2.528, 31: 2.457, 41: 2.423, 51: 2.403, 61: 2.390, 121: 2.358, 999: 2.326}
    # for i in range(N):
    #     x2.append(simulacion.simular_120_meses(configuraciones[config1]["s"], configuraciones[config1]["S"]))
    #     x3.append(simulacion.simular_120_meses(configuraciones[config2]["s"], configuraciones[config2]["S"]))
    # print("X1: {}".format(x2))
    # print("X2: {}".format(x3))
    # s2 = 0
    # for i in range(N):
    #     z1.append(x2[i]-x3[i])
    # zprom = sum(z1)/len(z1)
    # for i in range(N):
    #     s2 += (z1[i]-zprom)**2
    # s2 = s2 / (len(z1) - 1)
    # print("Z1: {}".format(z1))
    # print("Z1 prom: {}".format(zprom))
    # print("S2/n : {}".format(s2/N))
    # min_val = zprom - t_st[N]*sqrt(s2/N)
    # max_val = zprom + t_st[N]*sqrt(s2/N)
    # print("Intervalo de confianza: [{}, {}]".format(min_val, max_val))

    ########################PARTE B-1############################
    # x = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
    # for i in range(83):
    #     for j in range(1, 8):
    #         costo = simulacion.simular_120_meses(configuraciones[j]["s"], configuraciones[j]["S"])
    #         x[j].append(costo)
    # proms = {i: sum(x[i])/len(x[i]) for i in x}
    # eses_cuadrados = []
    # for j in range(1, 8):
    #     s2 = 0
    #     for el in x[j]:
    #         s2 += (el-proms[j])**2
    #     eses_cuadrados.append(s2/82)
    # print(proms)
    # print(eses_cuadrados)

    ########################PARTE B-2############################
    # x = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
    # for i in range(72):
    #     x[1].append(simulacion.simular_120_meses(configuraciones[1]["s"], configuraciones[1]["S"]))
    # for i in range(52):
    #     x[2].append(simulacion.simular_120_meses(configuraciones[2]["s"], configuraciones[2]["S"]))
    # for i in range(41):
    #     x[3].append(simulacion.simular_120_meses(configuraciones[3]["s"], configuraciones[3]["S"]))
    # for i in range(37):
    #     x[4].append(simulacion.simular_120_meses(configuraciones[4]["s"], configuraciones[4]["S"]))
    # for i in range(31):
    #     x[5].append(simulacion.simular_120_meses(configuraciones[5]["s"], configuraciones[5]["S"]))
    # for i in range(32):
    #     x[6].append(simulacion.simular_120_meses(configuraciones[6]["s"], configuraciones[6]["S"]))
    # for i in range(24):
    #     x[7].append(simulacion.simular_120_meses(configuraciones[7]["s"], configuraciones[7]["S"]))
    # proms = {i: sum(x[i])/len(x[i]) for i in x}
    # eses_cuadrados = []
    # for j in range(1, 8):
    #     s2 = 0
    #     for el in x[j]:
    #         s2 += (el - proms[j]) ** 2
    #     eses_cuadrados.append(s2/len(x[j])-1)
    # print(proms)
    # print(eses_cuadrados)

    #FINAL
    # x1 = {1: 125.33, 2: 120.02, 3: 118.48, 4: 118.85, 5: 121.42, 6: 117.78, 7: 120.06}
    # x2 = {1: 124.67, 2: 120.72, 3: 118.21, 4: 119.53, 5: 119.21, 6: 121.71, 7: 117.3}
    # pesos = {1: [0.1, 0.9], 2: [0.5, 0.5], 3: [0.9, 0.1]}
    # xp1 = []
    # xp2 = []
    # xp3 = []
    # for i in range (1,8):
    #     xp1.append(x1[i]*pesos[1][0] + x2[i]*pesos[1][1])
    #     xp2.append(x1[i] * pesos[2][0] + x2[i] * pesos[2][1])
    #     xp3.append(x1[i] * pesos[3][0] + x2[i] * pesos[3][1])
    # print(xp1)
    # print(xp2)
    # print(xp3)
    # print(min(xp1))
    # print(min(xp2))
    # print(min(xp3))

