from collections import deque
import pygame
import math
import sys
import time
from random import randint, seed

sys.setrecursionlimit(1000)

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.padre = None
        self.izq = None
        self.der = None
        self.nivel = 0
        self.color = None

    def __repr__(self):
        return f"{self.valor}"

class BST:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if not self.raiz:
            nuevo = Nodo(valor)
            self.raiz = nuevo
            nuevo.color = "negro"
            self.insertarRN(nuevo)
            return nuevo
        actual = self.raiz
        nivel = 1
        while True:
            if valor < actual.valor:  # izquierda
                if not actual.izq:
                    nuevo = Nodo(valor)
                    actual.izq = nuevo
                    nuevo.padre = actual
                    nuevo.nivel = nivel
                    nuevo.color = "rojo"
                    self.insertarRN(nuevo)
                    return nuevo
                actual = actual.izq
                nivel += 1
            if valor > actual.valor:  # derecha
                if not actual.der:
                    nuevo = Nodo(valor)
                    actual.der = nuevo
                    nuevo.padre = actual
                    nuevo.nivel = nivel
                    nuevo.color = "rojo"
                    self.insertarRN(nuevo)
                    return nuevo
                actual = actual.der
                nivel += 1
            if valor == actual.valor:
                return actual
                
    def ancestros(self, nodo):
        actual = nodo
        l = [actual]
        while actual.padre:
            actual = actual.padre
            l.append(actual)
        return l

    def inorden(self, nodo):
        l = []
        if nodo.izq:
            l.extend(self.inorden(nodo.izq))
        l.append(nodo)
        if nodo.der:
            l.extend(self.inorden(nodo.der))
        return l

    def BFS(self, nodo):
        cola = deque()
        cola.appendleft(nodo)
        l = []
        while cola:
            actual = cola.pop()
            if actual.izq: 
                cola.appendleft(actual.izq)
            if actual.der: 
                cola.appendleft(actual.der)
            l.append(actual)
        return l

    def maximo(self, nodo):
        actual = nodo
        while True:
            if actual.der:
                actual = actual.der
            else:
                return actual

    def minimo(self, nodo):
        actual = nodo
        while True:
            if actual.izq:
                actual = actual.izq
            else:
                return actual

    def buscar(self, valor):
        actual = self.raiz
        while True:
            if actual.valor == valor:
                return actual
            if valor < actual.valor:
                if not actual.izq:
                    return None
                actual = actual.izq
            if valor > actual.valor:
                if not actual.der:
                    return None
                actual = actual.der

    def pivote(self, rango):
        inferior, superior = rango
        actual = self.raiz
        while True:
            if actual.valor >= inferior and actual.valor <= superior:
                return actual
            if actual.valor < inferior:
                if actual.der:
                    actual = actual.der
                else:
                    return actual
            if actual.valor > superior:
                if actual.izq:
                    actual = actual.izq
                else:
                    return actual

    def rango(self, rango):
        inferior, superior = rango
        pivote = self.pivote(rango)
        l = []
        l.extend(self.inordenRango(pivote, rango))
        return l

    def inordenRango(self, nodo, rango):
        inferior, superior = rango
        l = []
        if not nodo:
            return l
        if nodo.valor > inferior:
            l.extend(self.inordenRango(nodo.izq, rango))
        if inferior <= nodo.valor <= superior:
            l.append(nodo)
        if nodo.valor < superior:
            l.extend(self.inordenRango(nodo.der, rango))
        return l

    def tam(self, nodo):
        tamaño = 1
        if nodo.izq:
            tamaño += self.tam(nodo.izq)
        if nodo.der:
            tamaño += self.tam(nodo.der)
        return tamaño

    def altura(self, nodo, nivel=0):
        nodo.nivel = nivel
        if not nodo:
            return 0
        if nodo.izq and nodo.der:
            if self.altura(nodo.izq, nivel+1) > self.altura(nodo.der, nivel+1):
                return 1 + self.altura(nodo.izq,nivel+1 )
            else:
                return 1 + self.altura(nodo.der,nivel+1)
        elif nodo.izq:
            return 1 + self.altura(nodo.izq,nivel+1)
        elif nodo.der:
            return 1 + self.altura(nodo.der,nivel+1)
        else:
            return 0

    def eliminar(self, nodo):
        if nodo is None:
            return

        self.borrarRN(nodo)
        if nodo.izq is None and nodo.der is None:  #Si es hoja
            if nodo.padre:  #Si tiene padre
                if nodo.padre.izq == nodo:
                    nodo.padre.izq = None
                    
                else:
                    nodo.padre.der = None
            else:  #Si no, entonces es raiz
                self.raiz = None

        elif nodo.izq is not None and nodo.der is None:  #Con solo hijo izquierdo
            if nodo.padre:
                if nodo.padre.izq == nodo:
                    nodo.padre.izq = nodo.izq
                else:
                    nodo.padre.der = nodo.izq
            else:
                self.raiz = nodo.izq
            nodo.izq.padre = nodo.padre

        elif nodo.der is not None and nodo.izq is None:  #Con solo hijo derecho
            if nodo.padre:
                if nodo.padre.izq == nodo:
                    nodo.padre.izq = nodo.der
                else:
                    nodo.padre.der = nodo.der
            else:
                self.raiz = nodo.der
            nodo.der.padre = nodo.padre

        else:  #Lo divertido, si tiene dos hijos
            reemplazo = self.maximo(nodo.izq)  #Se consigue el mayor del hijo izquierdo
            nodo.valor = reemplazo.valor  #Cambiar los valores
            self.eliminar(reemplazo)  #Se elimina el reemplazo
            self.borrarRN(nodo)

        #Ya eliminado se sube toda la descendencia del nodo
        self.actualizar_niveles(self.raiz)

    def actualizar_niveles(self, nodo, nivel=0):
        if nodo is not None:
            nodo.nivel = nivel  
            self.actualizar_niveles(nodo.izq, nivel + 1)
            self.actualizar_niveles(nodo.der, nivel + 1)

    def balancear(self, nodo):
        if nodo.padre:
            padre = nodo.padre
            
            if padre.der == nodo:
                if nodo.izq:
                    nodo.izq.padre = padre
                padre.der = nodo.izq
                if padre.padre:
                    nodo.padre = padre.padre
                    if padre.padre.izq and padre.padre.izq == padre:
                        nodo.padre.izq = nodo
                    else:
                        nodo.padre.der = nodo
                else:
                    nodo.padre = None
                    self.raiz = nodo
                padre.padre = nodo
                nodo.izq = padre
            if padre.izq == nodo:
                if nodo.der:
                    nodo.der.padre = padre
                padre.izq = nodo.der
                if padre.der:
                    padre.der.color = "negro"
                if padre.izq:
                    padre.izq.color = "negro"
                if padre.padre:
                    nodo.padre = padre.padre
                    if padre.padre.izq and padre.padre.izq == padre:
                        nodo.padre.izq = nodo
                    else:
                        nodo.padre.der = nodo
                else:
                    nodo.padre = None
                    self.raiz = nodo
                padre.padre = nodo
                nodo.der = padre

    def blackDepth(self, nodo):
        if not nodo:
            return 0
        izq = self.blackDepth(nodo.izq)
        der = self.blackDepth(nodo.der)
        if nodo.color == "negro":
            return 1 + max(izq, der)
        else:
            return 0 + max(izq, der)


    def insertarRN(self, nodo):
        if not nodo.padre:
            nodo.color = "negro"

        elif nodo.padre.color == "rojo":
            padre = nodo.padre
            if padre.padre.der and padre == padre.padre.der:
                #Bien
                if not padre.padre.izq or padre.padre.izq.color == "negro":
                    #Bien
                    if padre.valor > nodo.valor:
                        nodo.color = "negro"
                        padre.color = "rojo"
                        padre.padre.color = "rojo"
                        self.balancear(nodo)
                        self.balancear(nodo)
                    #Bien
                    else:
                        padre.color = "negro"
                        padre.padre.color = "rojo"
                        self.balancear(padre)
                #Bien
                else:
                    padre.color = "negro"
                    padre.padre.izq.color = "negro"
                    padre.padre.color = "rojo"
                    self.insertarRN(padre.padre)
            elif padre.padre.izq and padre == padre.padre.izq:
                if not padre.padre.der or padre.padre.der.color == "negro":
                    if padre.valor < nodo.valor:
                        nodo.color = "negro"
                        padre.color = "rojo"
                        padre.padre.color = "rojo"
                        self.balancear(nodo)
                        self.balancear(nodo)
                    else:
                        padre.color = "negro"
                        padre.padre.color = "rojo"
                        self.balancear(padre)
                else:
                    padre.color = "negro"
                    padre.padre.der.color = "negro"
                    padre.padre.color = "rojo"
                    self.insertarRN(padre.padre)
    
    def borrarRN(self, nodo):
        if nodo.color == "rojo":
            return
        if not nodo.padre:
            return
            
        # if nodo.der and not nodo.izq:
        #     nodo.der.color == "negro"
        # if not nodo.der and nodo.izq:
        #     nodo.izq.color == "negro"

        if nodo == nodo.padre.der:
            der = self.blackDepth(nodo)
            izq = self.blackDepth(nodo.padre.izq)
            if der > izq:
                tHeavy, tLight = nodo, nodo.padre.izq
            else:
                tLight, tHeavy = nodo, nodo.padre.izq
        else:
            der = self.blackDepth(nodo.padre.der)
            izq = self.blackDepth(nodo)
            if der > izq:
                tHeavy, tLight = nodo.padre.der, nodo
            else:
                tLight, tHeavy = nodo.padre.der, nodo
        
        if tHeavy.color == "negro":
            if tHeavy.der and tHeavy.der.color == "rojo":
                der = tHeavy.der
                tHeavy.der.color = tHeavy.padre.color
                tHeavy.padre.color = "negro"
                self.balancear(der)
                self.balancear(der)
            elif tHeavy.izq and tHeavy.izq.color == "rojo":  
                izq = tHeavy.izq
                tHeavy.izq.color = tHeavy.padre.color
                tHeavy.padre.color = "negro"
                self.balancear(izq)
                self.balancear(izq)

            elif not tHeavy.der and not tHeavy.izq:
                tHeavy.padre.color = "negro"
                tHeavy.color = "rojo"
            else:
                if tHeavy.der and tHeavy.der.color == "negro":
                    tHeavy.padre.color = "negro"
                    tHeavy.color = "rojo"
                elif tHeavy.izq and tHeavy.izq.color == "negro":
                    tHeavy.padre.color = "negro"
                    tHeavy.color = "rojo"
        else:
            padre = tHeavy.padre
            tHeavy.padre.color = "rojo"
            tHeavy.color = "negro"
            self.balancear(tHeavy)
            self.borrarRN(padre)

# seed(50771708)
# valores = [500,250,750,150,350,600,800,550,400,380]
# valores = [4,7,12,15,3,5,14,18,16,17]
valores = [randint(1,400) for _ in range(22)]
abb = BST()
for v in valores:
    abb.insertar(v)

busqueda = input("1 if you want to make a search of ranges, 0 to decline") == '1'
if busqueda:
    inferior = int(input("Lower limit?"))
    superior = int(input("Upper limit?"))
    rango = abb.rango((inferior,superior))

ancho, alto = 720,720
window = (ancho, alto)
pygame.init()

pantalla = pygame.display.set_mode(window, 0, 32)
pantalla.fill("white")

numnodos=int(abb.tam(abb.raiz))
niveles=int(abb.altura(abb.raiz))+1

cuad_ancho = math.floor(720/(numnodos+1))
cuad_alto = math.floor(720/niveles+1)

if cuad_alto<cuad_ancho:
    radio=int(cuad_alto/2)
else:
    radio=int(cuad_ancho/2)

gordura=math.floor(720/(numnodos*numnodos))
if gordura==0:
    gordura=1

listain = abb.inorden(abb.raiz)

pos = dict()
cont = 0
for element in listain:
    pos[element] =  (cuad_ancho*cont+cuad_ancho,cuad_alto*(element.nivel)+cuad_alto/2)
    cont += 1

cont = 0
circles = True
lines = True
velocidad = 1/(numnodos**(1/2))
cont2 = 0

tamaño = int(radio*1.5)


while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1: #Hice esta salvajada para detectar los clicks en un nodo
            mouse_x, mouse_y = evento.pos
            for element in listain:
                centro = pos[element]

                distance = math.sqrt((mouse_x - centro[0]) ** 2 + (mouse_y - centro[1]) ** 2)
                if distance <= radio:
                    abb.eliminar(element)
                    listain = abb.inorden(abb.raiz)
                    if busqueda:
                        rango = abb.rango((inferior, superior))
                    break

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 3:
            mouse_x, mouse_y = evento.pos
            for element in listain:
                centro = pos[element]

                distance = math.sqrt((mouse_x - centro[0]) ** 2 + (mouse_y - centro[1]) ** 2)
                if distance <= radio:
                    abb.balancear(element)
                    listain = abb.inorden(abb.raiz)
                    if busqueda:
                        rango = abb.rango((inferior, superior))
                    break

    #Después de cada elimiación se tienen que actualizar y reiniciar los valores para imprimir
    numnodos = int(abb.tam(abb.raiz))
    listain = abb.inorden(abb.raiz) 

    pos = dict()
    cont = 0

    niveles=int(abb.altura(abb.raiz))+1

    cuad_ancho = math.floor(720/(numnodos+1))
    cuad_alto = math.floor(720/niveles+1)

    if cuad_alto<cuad_ancho:
        radio=int(cuad_alto/2)
    else:
        radio=int(cuad_ancho/2)

    gordura=math.floor(720/(numnodos*numnodos))
    if gordura==0:
        gordura=1
    
    tamaño = int(radio*1.5)

    for element in listain:
        pos[element] = (cuad_ancho * cont + cuad_ancho, cuad_alto * (element.nivel) + cuad_alto / 2)
        cont += 1

    pantalla.fill("white")
    cont = 0

    while cont < numnodos:
        centro = pos[listain[cont]]
        if listain[cont].color == "negro":
            color = (0,0,0)
        else:
            color = (255,0,0)
        pygame.draw.circle(pantalla, color, centro, radio, gordura)
        cont += 1
    cont = 0
    
    while cont < numnodos:
        centro = pos[listain[cont]]
        if listain[cont].padre:
            pygame.draw.line(pantalla, (0, 0, 255), centro, pos[listain[cont].padre], gordura)
        cont += 1
    cont = 0

    if busqueda:
        while cont < len(rango):
            centro = pos[rango[cont]]
            pygame.draw.circle(pantalla, (0, 255, 0), centro, radio, gordura)
            cont += 1
    cont = 0
    
    while cont < numnodos:
        pygame.font.init()
        font = pygame.font.SysFont("Sans Serif", tamaño)
        text = str(listain[cont].valor)
        text_surface = font.render(text, True, (0, 0, 0), (255, 255, 255))
        pantalla.blit(text_surface, pos[listain[cont]])
        cont += 1
    
    pygame.display.update()