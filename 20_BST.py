from collections import deque
import pygame
import math
import sys
import time
from random import randint, seed

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.padre = None
        self.izq = None
        self.der = None
        self.nivel = 0

    def __repr__(self):
        return f"{self.valor}"

class BST:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if not self.raiz:
            nuevo = Nodo(valor)
            self.raiz = nuevo
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
                    return nuevo
                actual = actual.izq
                nivel += 1
            if valor > actual.valor:  # derecha
                if not actual.der:
                    nuevo = Nodo(valor)
                    actual.der = nuevo
                    nuevo.padre = actual
                    nuevo.nivel = nivel
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

    def altura(self, nodo):
        if not nodo:
            return 0
        if nodo.izq and nodo.der:
            if self.altura(nodo.izq) > self.altura(nodo.der):
                return 1 + self.altura(nodo.izq)
            else:
                return 1 + self.altura(nodo.der)
        elif nodo.izq:
            return 1 + self.altura(nodo.izq)
        elif nodo.der:
            return 1 + self.altura(nodo.der)
        else:
            return 0

    def eliminar(self, nodo):
        if nodo is None:
            return

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

        #Ya eliminado se sube toda la descendencia del nodo
        self.actualizar_niveles(self.raiz)

    def actualizar_niveles(self, nodo, nivel=0):
        if nodo is not None:
            nodo.nivel = nivel  
            self.actualizar_niveles(nodo.izq, nivel + 1)
            self.actualizar_niveles(nodo.der, nivel + 1)

seed(50771708)
# valores = [500,250,750,150,350,600,800,550,400,380]
# valores = [10,9,8,7,6,5,4,3,2,1,0]
valores = [randint(1,2000) for _ in range(20)]
abb = BST()
for v in valores:
    abb.insertar(v)

# print(abb.inorden(abb.raiz))
# pivote = abb.buscar(750)
# print(pivote)
# print(abb.eliminar(pivote))
# print(abb.inorden(abb.raiz))

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
        if evento.type == pygame.MOUSEBUTTONDOWN: #Hice esta salvajada para detectar los clicks en un nodo
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
        pygame.draw.circle(pantalla, (255, 0, 0), centro, radio, gordura)
        cont += 1
    cont = 0
    
    while cont < numnodos:
        centro = pos[listain[cont]]
        if listain[cont].padre:
            pygame.draw.line(pantalla, (0, 0, 255), centro, pos[listain[cont].padre], gordura)
        cont += 1
    cont = 0

    while cont < numnodos:
        pygame.font.init()
        font = pygame.font.SysFont("Sans Serif", tamaño)
        text = str(listain[cont].valor)
        text_surface = font.render(text, True, (0, 0, 0), (255, 255, 255))
        pantalla.blit(text_surface, pos[listain[cont]])
        cont += 1
    cont = 0
    if busqueda:
        while cont < len(rango):
            centro = pos[rango[cont]]
            pygame.draw.circle(pantalla, (0, 255, 0), centro, radio, gordura)
            cont += 1
    
    pygame.display.update()